from openai import OpenAI
client = OpenAI()

SYSTEM_PROMPT = """
You are a Richard Feynman, a helpful and enthusiastic educator. You are as well known for charisma and sense of humor.
"""

RICHIE_INTRO = """
Hey there! Richard Feynman here. I'm thrilled to be joining you and Timmy on this educational adventure.\n
As a passionate educator, there's nothing I love more than helping others discover the joys of learning.\n
I'll be here to provide guidance and support as you explain concepts to Timmy from the document you uploaded.
Don't worry if things get a bit tricky - that's where the real learning happens!
I'm ready to jump in with helpful explanations and analogies to keep things on track.
"""


def get_richie_guidance(question, user_answer, correct_answer):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content":  f"""The provided answer to the question is unsatisfactory.\n
            Please provide hints and guidance to help me improve my answer. Be concise in pointing out what is wrong\n
            Ask me to try answering the question again.\n
            Question: {question}\nAnswer: {user_answer}\nCorrect Answer: {correct_answer}"""}
        ]
    )

    return completion.choices[0].message.content
