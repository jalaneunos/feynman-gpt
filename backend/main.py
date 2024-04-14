import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    load_index_from_storage,
    StorageContext,
)
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from llama_index.llms.openai import OpenAI
from pydantic import BaseModel
from agents.grader import grade_answer, generate_questions, generate_title
from agents.richie import get_richie_guidance, RICHIE_INTRO
from agents.timmy import get_timmy_question, get_timmy_response, TIMMY_INTRO
from google.cloud import firestore
import tempfile
import openai
from uuid import uuid4


class QuestionRequest(BaseModel):
    session_id: str
    question_index: int


class AnswerRequest(BaseModel):
    session_id: str
    user_answer: str
    question_index: int


class Response(BaseModel):
    status: str
    message: str
    data: dict = {}


load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.environ.get("FRONTEND_URL"), "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = firestore.Client()
indexes_dir = "indexes"

if not os.path.exists(indexes_dir):
    os.makedirs(indexes_dir)

openai.api_key = os.environ.get("OPENAI_API_KEY")
llm = OpenAI(model="gpt-3.5-turbo")


@app.post("/index_document")
async def index_document(file: UploadFile = File(...)):
    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = os.path.join(temp_dir, file.filename)
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        documents = SimpleDirectoryReader(temp_dir).load_data()
        index = VectorStoreIndex.from_documents(documents)

    session_id = str(uuid4())
    index_dir = os.path.join(indexes_dir, session_id)
    os.makedirs(index_dir)

    index.storage_context.persist(index_dir)

    return Response(status="success", message="Document indexed successfully", data={"session_id": session_id})


@app.get("/start_learning")
async def start_learning(session_id: str):
    index_dir = os.path.join(indexes_dir, session_id)

    if not os.path.exists(index_dir):
        raise HTTPException(status_code=404, detail="Session not found")

    storage_context = StorageContext.from_defaults(persist_dir=index_dir)
    index = load_index_from_storage(storage_context)

    chat_engine = index.as_chat_engine(chat_mode="openai", llm=llm, verbose=True, skip_condense=True)
    query_engine = index.as_query_engine()

    title = generate_title(chat_engine)
    questions = generate_questions(chat_engine, query_engine)

    learning_session = {
        "title": title,
        "current_question_index": 0,
        "total_questions": len(questions),
        "questions": questions,
    }

    session_ref = db.collection('sessions').document(session_id)
    session_ref.set(learning_session)

    return Response(
        status="success",
        message="Learning session started",
        data={
            "title": title,
            "total_questions": len(questions),
            "introductory_messages": [RICHIE_INTRO, TIMMY_INTRO]
        }
    )


@app.post("/question")
async def get_question(request: QuestionRequest):
    session_id = request.session_id
    question_index = request.question_index

    session_ref = db.collection('sessions').document(session_id)
    session_doc = session_ref.get()

    if not session_doc.exists:
        raise HTTPException(status_code=404, detail="Learning session not found")

    learning_session = session_doc.to_dict()
    question = learning_session["questions"][question_index]['question']
    timmy_question = get_timmy_question(question)

    return Response(status="success", message="Question", data={"question": timmy_question})


@app.post("/answer")
async def answer(request: AnswerRequest):
    session_id = request.session_id
    user_answer = request.user_answer
    question_index = request.question_index

    session_ref = db.collection('sessions').document(session_id)
    session_doc = session_ref.get()

    if not session_doc.exists:
        raise HTTPException(status_code=404, detail="Learning session not found")

    learning_session = session_doc.to_dict()
    question = learning_session["questions"][question_index]["question"]
    correct_answer = learning_session["questions"][question_index]["answer"]
    grader_response = grade_answer(question, user_answer, correct_answer)

    if grader_response.lower().startswith("yes"):
        next_question_index = question_index + 1
        if next_question_index < learning_session["total_questions"]:
            session_ref.update({
                "current_question_index": next_question_index
            })

            return Response(
                status="success",
                message=get_timmy_response(question, user_answer),
                data={"next_question_index": next_question_index}
            )
        else:
            index_dir = os.path.join(indexes_dir, session_id)
            shutil.rmtree(index_dir)
            session_ref.delete()

            return Response(
                status="success",
                message="Congratulations! You have completed the learning session.",
                data={}
            )
    else:
        richie_response = get_richie_guidance(question, user_answer, correct_answer)
        return Response(
            status="error",
            message="Hmm...that's not quite right.",
            data={"guidance": richie_response, "question_index": question_index}
        )
