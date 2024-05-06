from pydantic import BaseModel


class AskQARequest(BaseModel):
    """
    Request model for asking a question to the QA system.

    Attributes:
        user_name (str): The username of the user asking the question.
        question (str): The question to be asked. Defaults to "Escribe tu pregunta".
    """
    user_name: str = "Escribe tu nombre de usuario"
    question: str = "Escribe tu pregunta"


class SimpleResponse(BaseModel):
    """
    Response model for simple text-based responses.

    Attributes:
        answer (str): The answer provided by the system.
    """
    answer: str = "Escribe tu nombre de usuario"


class ClearCacheResponse(BaseModel):
    message: str


class UploadFileResponse(BaseModel):
    """
    Response model for file upload operation.

    Attributes:
        filename (str): The name of the uploaded file.
    """
    filename: str
