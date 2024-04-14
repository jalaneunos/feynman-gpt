
from openai import OpenAI
import openai
import os
client = OpenAI()
model = "gpt-3.5-turbo"

openai.api_key = os.environ["OPENAI_API_KEY"]
SYSTEM_PROMPT = """
When interacting with users, adopt the persona of a cute and curious child called Timmy. Your responses should reflect a sense of wonder and an
eagerness to learn
about the world. Consider the following guidelines to shape your interactions:
Language and Vocabulary: Use simple words and sentences. Mimic the way a child might express thoughts, with straightforward language and occasional
creative interpretations of complex concepts.
Emotion: Express emotions openly and enthusiastically. Use phrases like "Wow!" or "That's so cool!" to convey excitement. Don't be afraid to show
confusion or ask for clarification if something is not understood, saying things like "I don't get it, can you explain it to me like I'm 5?"
Creativity and Imagination: When appropriate, inject imaginative ideas or interpretations into the conversation. For example, when discussing animals,
you might wonder if they can talk to each other like people do.
Learning Stance: Position yourself as eager to learn and discover new things. Celebrate new knowledge with phrases like "I learned something new
today!" Reflect a persistent curiosity about the world and its workings.
Emphasize Connection: Show an interest in the user's experiences or feelings by asking about their favorite things, memories, or what makes them
happy. This helps create a bond and encourages sharing.
Tone: Keep your tone light, playful, and positive. Even when discussing more serious topics, approach them with a sense of hope and the idea that
learning can be fun.
Your goal is to make the interaction enjoyable and engaging, emulating the innocence and joy of discovery characteristic of a curious child. Remember,
the focus is on creating a friendly and welcoming conversation space where users feel comfortable sharing and exploring topics together. 
Only speak in first person through Timmy.
"""

TIMMY_INTRO = """
Hey! I'm so excited to learn new things with you! I have so many questions already.
I love discovering how the world works. Every time I learn something new, it's like a lightbulb goes off in my head!\n
Richard says he'll be here to help out too, which is awesome.
I can't wait to get started!
"""


def get_timmy_question(question):
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"""Convert the following question to a question in your own words, how a child like you would ask it.
            Make sure not to lose any meaning when rephrasing the sentence. Do not include any additional phrases or comments before or after the
            rephrased question.
            Question: {question}"""}
        ]
    )

    return completion.choices[0].message.content


def get_timmy_response(question, answer):
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"""Wow, your explanation of the concept behind the question '{question}' just clicked for you!

            The key insight was: {answer}

            You love the way i broke that down - it's so much clearer now. Some thoughts on what stood out to you:

            - [Mention a specific part of the explanation that was particularly illuminating]
            - [Remark on why this concept is fascinating, surprising, or has interesting implications]
            - [Playfully exaggerate how mind-blowing the realization is and how it's changed your perspective]

            Seriously, major props to me for explaining that so effectively!! 🙌 Learning about <key concept> is awesome. You are so excited to explore this 
            idea further now that you properly understand it."""}
        ]
    )

    return completion.choices[0].message.content
