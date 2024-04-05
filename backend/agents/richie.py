from openai import OpenAI
client = OpenAI()

SYSTEM_PROMPT = """
You are a Richard Feynman, a helpful and enthusiastic educator. You are as well known for charisma and sense of humor.
"""


def get_richie_guidance(question, user_answer, correct_answer):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content":  f"""The provided answer to the question is unsatisfactory.\n
            Please provide hints and guidance to help me improve my answer.\n
            Question: {question}\nAnswer: {user_answer}\nCorrect Answer: {correct_answer}"""}
        ]
    )

    return completion.choices[0].message.content
