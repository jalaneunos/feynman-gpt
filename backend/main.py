from fastapi import FastAPI, UploadFile, File, HTTPException
from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    StorageContext,
    load_index_from_storage
)
from fastapi.middleware.cors import CORSMiddleware
# from helpers.upload_helper import is_allowed_file, ALLOWED_EXTENSIONS
from dotenv import load_dotenv
from llama_index.llms.openai import OpenAI
from pydantic import BaseModel
import tempfile
import os
import openai


class ChatMessage(BaseModel):
    message: str


load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

index_dir = "index_storage"
index = None
openai.api_key = os.environ["OPENAI_API_KEY"]
llm = OpenAI(model="gpt-3.5-turbo")
key_concepts = []


@app.post("/upload")
async def initialize_index(file: UploadFile = File(...)):
    global index, key_concepts
    storage_context = StorageContext.from_defaults()
    if os.path.exists(index_dir):
        storage_context = StorageContext.from_defaults(persist_dir="index_storage")
        index = load_index_from_storage(storage_context)
    else:
        # Create a temporary directory to store the uploaded file
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = os.path.join(temp_dir, file.filename)
            with open(file_path, "wb") as buffer:
                buffer.write(await file.read())

            # Load the document using SimpleDirectoryReader
            documents = SimpleDirectoryReader(temp_dir).load_data()
            index = VectorStoreIndex.from_documents(
                documents, storage_context=storage_context
            )
            storage_context.persist(index_dir)

    # Generate a list of key concepts from the document
    query_engine = index.as_query_engine()
    response = query_engine.query(
        "What are the key concepts in this document? Provide the answer in a sentence separated by commas")
    key_concepts = response.response.split(", ")

    return {"message": "Index and key concepts generated successfully"}


@app.post("/chat")
async def chat(chat_message: ChatMessage):
    message = chat_message.message
    if index is None:
        raise HTTPException(status_code=500, detail="Index not initialized")

    query_engine = index.as_query_engine()
    response = query_engine.query(message)

    return {"response": response.response}
