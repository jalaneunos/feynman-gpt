from fastapi import FastAPI, UploadFile, File, HTTPException
from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    StorageContext,
    load_index_from_storage
)
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from llama_index.llms.openai import OpenAI
from pydantic import BaseModel
from agents.grader import grade_answer, generate_questions, generate_title
from agents.richie import get_richie_guidance
from agents.timmy import get_timmy_question, get_timmy_response
import tempfile
import os
import openai


class AnswerRequest(BaseModel):
    user_answer: str
    question_index: int
    learning_session: dict


class QuestionRequest(BaseModel):
    question_index: int
    learning_session: dict


class Response(BaseModel):
    status: str
    message: str
    data: dict = {}


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
chat_engine = None
query_engine = None
learning_session = None
message_history = None

openai.api_key = os.environ["OPENAI_API_KEY"]
llm = OpenAI(model="gpt-3.5-turbo")


@app.post("/index_document")
async def index_document(file: UploadFile = File(...)):
    global index
    storage_context = StorageContext.from_defaults()
    if os.path.exists(index_dir):
        storage_context = StorageContext.from_defaults(persist_dir="index_storage")
        index = load_index_from_storage(storage_context)
    else:
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = os.path.join(temp_dir, file.filename)
            with open(file_path, "wb") as buffer:
                buffer.write(await file.read())
            documents = SimpleDirectoryReader(temp_dir).load_data()
            index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)
            storage_context.persist(index_dir)
    return Response(status="success", message="Document indexed successfully")


@app.get("/start_learning")
async def start_learning():
    if index is None:
        raise HTTPException(status_code=500, detail="Index not initialized")
    global learning_session
    chat_engine = index.as_chat_engine(chat_mode="openai", llm=llm, verbose=True)
    query_engine = index.as_query_engine()
    title = generate_title(chat_engine)
    questions = generate_questions(chat_engine, query_engine)
    learning_session = {
        "title": title,
        "current_question_index": 0,
        "total_questions": len(questions),
        "questions": questions
    }
    return Response(status="success", message="Learning session started", data={"learning_session": learning_session})


@app.post("/question")
async def get_question(request: QuestionRequest):
    question_index = request.question_index
    learning_session = request.learning_session
    question = learning_session["questions"][question_index]['question']
    timmy_question = get_timmy_question(question)
    return Response(status="success", message="Question", data={"question": timmy_question})


@app.post("/answer")
async def answer(request: AnswerRequest):
    user_answer = request.user_answer
    question_index = request.question_index
    learning_session = request.learning_session

    question = learning_session["questions"][question_index]["question"]
    correct_answer = learning_session["questions"][question_index]["answer"]
    grader_response = grade_answer(question, user_answer, correct_answer)

    if grader_response.lower().startswith("yes"):
        next_question_index = question_index + 1
        if next_question_index < learning_session["total_questions"]:
            return Response(
                status="success",
                message=get_timmy_response(question, user_answer),
                data={"next_question_index": next_question_index}
            )
        else:
            return Response(
                status="success",
                message="Congratulations! You have completed the learning session.",
                data={"learning_session": learning_session}
            )
    else:
        richie_response = get_richie_guidance(question, user_answer, correct_answer)
        return Response(
            status="error",
            message="Unsatisfactory answer. Here's some guidance from Richie:",
            data={"guidance": richie_response, "question_index": question_index}
        )
