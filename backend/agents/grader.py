from openai import OpenAI
client = OpenAI()


def grade_answer(question, user_answer, correct_answer):
    grader_prompt = f"""Evaluate the user's response based on the following criteria:
- Question Posed: {question}
- User's Response: {user_answer}
- Expected Correct Response: {correct_answer}

Determine whether the essence of the user's response aligns with the core concept of the correct answer. ]
It's not necessary for the user's response to mirror the correct answer precisely. However, if the response
employs analogies or similar devices, they must accurately convey the intended underlying concept.

Please answer with 'Yes' if the user's response captures the fundamental idea of the correct answer,
even if presented differently. Answer 'No' if the user's response diverges in understanding or
interpretation from the expected correct response."""

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": grader_prompt}
        ]
    )

    print(completion.choices[0].message.content)

    return completion.choices[0].message.content


def generate_title(chat_engine):
    return chat_engine.chat("Summarize this document into a title. Reply with only the title").response


def generate_questions(chat_engine, query_engine):

    response = few_shot_prompt(initial_prompt, chat_engine)
    questions = []
    for line in response.strip().split("\n"):
        parts = line.split(":")
        if len(parts) == 2:
            question = parts[1].strip()
            answer = query_engine.query(question).response
            questions.append({"question": question, "answer": answer})
    return questions


initial_prompt = (
    "Generate a series of questions about the document in increasing difficulty\n."
    "All questions must be related to the key concepts of the document's contents\n."
    "Do not ask vague and general questions, and do not ask questions about the file path or other metadata\n."
    "Make sure the questions are not about specific examples unrelated to the key ideas."
    "Start with questions about contents of simple and specific concepts,"
    "before harder questions that require critical thinking.\n"
    "Respond ONLY with the questions in the following structured format\n"
    "Question 1 (Easy): <easy_question_1>\n"
    "Question 2 (Easy): <easy_question_2>\n"
    "Question 3 (Medium): <medium_question_1>\n"
    "Question 4 (Medium): <medium_question_2>\n"
    "Question 5 (Hard): <hard_question_1>\n"
    "Question 6 (Hard): <hard_question_2>\n"
)


def few_shot_prompt(initial_prompt, chat_engine):
    initial_response = chat_engine.chat(initial_prompt).response

    second_prompt = f"""
    The prompt was {initial_prompt}\n
    The response was: {initial_response}\n
    Are the questions strongly related to the key concepts of the whole document?
    Identify the flaws in the response and give a better answer for the task.\n
    Follow the response structure of the prompt.
    """

    # response = chat_engine.chat(second_prompt).response
    return initial_response
