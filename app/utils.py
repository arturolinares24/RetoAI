import os
import langid
from typing import List, Optional
from langchain_community.document_loaders.pdf import Document


def create_directory(directory: str) -> None:
    """
    Create a directory if it does not exist.

    Args:
        directory (str): The path of the directory to create.
    """
    # Check if the directory already exists
    if not os.path.exists(directory):
        try:
            # Attempt to create the directory
            os.mkdir(directory)
            print(f"Directory '{directory}' created successfully.")
        except Exception as e:
            # Print error message if directory creation fails
            print(f"Error creating directory '{directory}': {e}")
    else:
        # Print message if directory already exists
        print(f"The directory '{directory}' already exists.")


def format_docs(docs: List[Document]) -> str:
    """
    Formats a list of documents into a single string.

    Args:
        docs (List[str]): List of document contents.

    Returns:
        str: Concatenated document contents with double newlines between each document.
    """
    return "\n\n".join(doc.page_content for doc in docs)


def detect_language_langid(text: str) -> Optional[str]:
    """
    Detects the language of the given text using langid library.

    Args:
        text (str): The text to detect language for.

    Returns:
        Optional[str]: Detected language code, or None if detection fails.
    """
    try:
        detected_language = langid.classify(text)
        return detected_language[0]
    except Exception as e:
        print("An error occurred:", e)
        return None
