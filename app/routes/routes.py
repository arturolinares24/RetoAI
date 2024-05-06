from fastapi import UploadFile, File, HTTPException, APIRouter
from ..config import DBS, PROMPTS, LLM, PROMPT, MEMORY
from ..schemas.schemas import (
    AskQARequest,
    SimpleResponse,
    UploadFileResponse,
    ClearCacheResponse,
)
from ..utils import format_docs, detect_language_langid
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import (
    RunnableParallel,
    RunnablePassthrough,
    RunnableLambda,
)
import requests
import os
import shutil
from langchain_community.vectorstores import FAISS

router = APIRouter(prefix="/api")


@router.post("/upload", response_model=UploadFileResponse)
async def upload_file(user_name: str, file: UploadFile = File(...)):
    """
    Endpoint to upload a file, process it, and store relevant data.

    Args:
        user_name (str): The name of the user.
        file (UploadFile): The file to be uploaded.

    Returns:
        dict: A response indicating the status of the file upload.
    """
    try:
        # Read the contents of the file
        contents = await file.read()
        # Write the file contents to disk
        with open(f"files/file_{user_name}.pdf", "wb") as gf:
            gf.write(contents)
    except requests.exceptions.RequestException as err:
        raise HTTPException(
            status_code=500, detail=f"Error occurred during file upload: {str(err)}"
        )

    try:
        # Load the PDF file and process it
        loader = PyPDFLoader(f"files/file_{user_name}.pdf")
        documents = loader.load()
        splitter = RecursiveCharacterTextSplitter(
            separators=["\n\n", "\n", " "], chunk_size=200, chunk_overlap=20
        )
        data = splitter.split_documents(documents)

        # Construct the database name
        db_name = f"faiss_db_{user_name}"
        # Create a FAISS vector store and save it
        DBS[db_name] = FAISS.from_documents(data, OpenAIEmbeddings())
        DBS[db_name].save_local(f"faiss_db/{db_name}")
        # Remove the uploaded file
        os.remove(f"files/file_{user_name}.pdf")
        return {"filename": f"file uploaded successfully for user {user_name}"}
    except requests.exceptions.RequestException as err:
        raise HTTPException(
            status_code=400, detail=f"Error occurred during file upload: {str(err)}"
        )


@router.post("/askqa/{user_name}", response_model=SimpleResponse)
async def askqa(request: AskQARequest):
    """
    Endpoint to process a question and provide an answer.

    Args:
        request (AskQARequest): The request object containing user name and question.

    Returns:
        dict: A response containing the answer to the question.
    """
    user_name = request.user_name
    question = request.question

    # Detect language of the question
    languagedetector = RunnableLambda(detect_language_langid)
    try:
        # Initialize the FAISS database
        if user_name not in MEMORY:
            MEMORY[user_name] = user_name

        db_name = f"faiss_db_{user_name}"
        new_db = FAISS.load_local(
            f"faiss_db/{db_name}",
            OpenAIEmbeddings(),
            allow_dangerous_deserialization=True,
        )
        retriever = new_db.as_retriever()
    except FileNotFoundError as file_err:
        raise HTTPException(
            status_code=404,
            detail=f"File not found for user {user_name}. First upload the docs: {str(file_err)}",
        )

    # Define the chain of runnables for QA
    rag_chain = (
        RunnableParallel(
            {
                "language": languagedetector,
                "context": retriever | format_docs,
                "question": RunnablePassthrough(),
            }
        )
        | PROMPT
        | LLM
        | StrOutputParser()
    )

    try:
        # Save the question
        PROMPTS[user_name] = question
        # Invoke the QA chain to get the answer
        answer = rag_chain.invoke(PROMPTS[user_name])
        return {"answer": answer}
    except requests.exceptions.HTTPError as err:
        raise HTTPException(status_code=404, detail=str(err))


@router.get("/clearall-user/{user_name}", response_model=SimpleResponse)
async def clearall_user(user_name: str):
    """
    Endpoint to clear cache for a specific user.

    Args:
        user_name (str): The username of the user whose cache is to be cleared.

    Returns:
        SimpleResponse: A response indicating the status of the cache clearance.
    """
    try:
        # Database name
        db_name = f"faiss_db_{user_name}"
        # Remove the directory corresponding to the user's cache
        shutil.rmtree(f"faiss_db/{db_name}")
        # Clear user data from memory
        if user_name in MEMORY:
            del MEMORY[user_name]
            del DBS[db_name]
            del PROMPTS[user_name]
        # Return success response
        return SimpleResponse(answer=f"Cache cleared for user {user_name}")
    except FileNotFoundError as file_err:
        # Raise exception if cache directory doesn't exist
        raise HTTPException(
            status_code=404,
            detail=f"Cache does not exist for user {user_name}: {str(file_err)}",
        )


@router.get("/clearall", response_model=ClearCacheResponse)
async def clear_all():
    """
    Endpoint to clear all caches.

    Returns:
        dict: A response indicating the status of all caches clearance.
    """
    try:
        shutil.rmtree("faiss_db")
        MEMORY.clear()
        DBS.clear()
        return {"message": "All caches cleared"}
    except FileNotFoundError as file_err:
        raise HTTPException(
            status_code=404,
            detail=f"All caches have already been cleared: {str(file_err)}",
        )
