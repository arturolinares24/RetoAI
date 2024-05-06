# Document Retrieval System (FastAPI)

This FastAPI application is designed to provide an advanced document retrieval system that leverages the power of Faiss (Facebook AI Similarity Search) for efficient and scalable vector search capabilities. The system facilitates the processing and querying of documents to retrieve relevant information quickly and accurately. It utilizes NLP techniques, supported by LangChain and OpenAI's embeddings, to handle complex queries and provide precise answers.

**Please note that the application is designed to handle PDF documents only, and the PDF document used for testing can be found in the repository.**
## Key Features:

- **Document Processing:** Upload and process documents to extract and index content, making it searchable.
- **Question Answering:** Allow users to submit questions and retrieve contextually relevant answers from the processed documents.
- **Cache Management:** Efficient management of user-specific and global caches to optimize retrieval speeds and resource usage.
- **FAISS Integration:** Utilizes Facebook's AI Similarity Search technology for fast retrieval of documents based on vectorized content, enhancing the performance of search operations.

## Project Structure
    
    Proyecto/
    │
    ├── app/                        # Main application directory
    │   ├── __init__.py             # Initializes your FastAPI app
    │   ├── routes/                 # Contains all the routing of the application
    │   │   ├── __init__.py         # Makes routes a Python package
    │   │   └── routes.py           # Defines all route endpoints
    │   ├── schemas/                # Pydantic models for request and response validation
    │   │   ├── __init__.py         # Makes schemas a Python package
    │   │   └── schemas.py          # Defines all schemas used in the app
    │   ├── config.py               # Contains configuration settings
    │   ├── utils.py                # Utility functions used throughout the app
    │   └── __init__.py             # App-level init for managing imports
    │
    ├── Dockerfile                  # Dockerfile for building container images
    ├── docker-compose.yml          # Docker Compose file for orchestrating containers
    ├── main.py                     # Entry point for the FastAPI application
    ├── README.md                   # Project documentation
    ├── requirements.txt            # Python dependencies
    └── .env                        # Environment variables 

## Prerequisites

To run this project, you will need:
- Python 3.9+
- pip (Python package installer)

## Setup and Running Locally

1. **Clone the Repository**
   ```bash
   git clone https://yourrepositoryurl.com/Proyecto
   cd Proyecto

2. **Create and Activate Virtual Environment**
   ```bash
    # Create a virtual environment
    python3 -m venv venv
    
    # Activate the virtual environment
    source venv/bin/activate (Linux/MacOS)
    venv\Scripts\activate.bat (Windows)
   
2. **Install Dependencies**
      ```bash
   pip install -r requirements.txt

3. **Set Environment Variables**

    Create a .env file in the project root directory and populate it with the necessary environment variables:
      ```bash
    OPENAI_API_KEY=API-KEY

4. **Run the Application**
     ```bash
    python3 main.py

## Running with Docker

1. **Build and Run the Docker Container**
   ```bash
   docker-compose up --build
   
2. **Access the Application**
      ```bash
   http://localhost:8000


## API Documentation

Once the application is running, access the Swagger UI to interact with the API at:

    http://localhost:8000/docs

# API Functionalities

## Upload File
- **Endpoint:** POST /api/upload
- **Description:** Uploads a PDF file and processes it to store document-related data.
- **Parameters:**
  - `user_name`: Identifier for the user.
  - `file`: The PDF file to be uploaded.

## Ask a Question
- **Endpoint:** POST /api/askqa/{user_name}
- **Description:** Processes a user's question against stored documents and returns an answer.
- **Parameters:**
  - `user_name`: Identifier for the user whose documents to query against.
  - `question`: The question to be processed.

## Clear User Cache
- **Endpoint:** GET /api/clearall-user/{user_name}
- **Description:** Clears all cached data related to a specific user.
- **Parameters:**
  - `user_name`: Identifier for the user whose cache should be cleared.

## Clear All Caches
- **Endpoint:** GET /api/clearall
- **Description:** Clears all caches and temporary storage across all users.


## Postman Collection for Testing

You can use the following Postman collection to perform tests on the API:

[Document Retrieval System Postman Collection](https://www.postman.com/arturolinares26/workspace/pi-reto-ai/collection/34720329-35fac8f7-becb-4a89-8b92-01253a86574f?action=share&creator=34720329&active-environment=34720329-6cecd0b4-9213-47a2-a348-3ebdf8e13f6b)
