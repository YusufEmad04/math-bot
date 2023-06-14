from questions import *

from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

from langchain.prompts import (
    ChatPromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI

from langchain import LLMChain, LLMMathChain


abbreviation = "Abbreviation: \n" \
               "\tM: Method marks - for a correct method applied to appropriate numbers\n" \
               "\tA: Accuracy marks - depend on M marks. Hence M0 A1 is not possible\n" \
               "\tB: Independent of method marks - for a correct final answer or intermediate stage\n" \
               "\tSC: Marks given in special cases only when indicated in mark scheme\n" \
               "\tFT: Work can be followed through after an error\n" \
               "\tisw: Ignore subsequent working (after correct answer obtained)\n" \
               "\tcao: Correct answer only\n" \
               "\toe:  Or equivalent\n" \
               "\tnfww: Not from wrong working\n" \
               "\tsoi: Seen or implied\n" \
               "\teeo: Each error or omission\n" \
               "\tdep: Dependent on mark(s)\n\n" \

human_text_helper_template_text = "Question in the past paper exam: \n" \
                                  "{question} \n\n" \
                                  "Answer in the marking scheme:\n" \
                                  "{answer} \n\n" \
                                  "Student question:\n" \
                                  "{student_question}\n\n" \
                                  "Can the student's question be answered directly without mathematical steps? " \
                                  "If the question can be answered directly, answer with Yes. " \
                                  "If the question requires " \
                                  "some mathematical steps to solve, answer with No. Only answer with Yes or No, nothing else."


human_text_helper_template_text = abbreviation + human_text_helper_template_text

helper_system_message_text = "You are a smart experienced math teacher who knows how different questions can be " \
                             "solved. You will take questions from past paper exams, their marking scheme and " \
                             "the student's question. You will answer " \
                             "with Yes if the question can be answered directly, and answer with No if the " \
                             "question requires some steps in order to solve it. " \
                             "You only answer with " \
                             "Yes or No. You may receive questions in English or Latex. "

assistant_system_message_text = "You are a helpful and smart math assistant for high school students. You will " \
                                "take " \
                                "questions from past paper exams and their marking scheme from students and give " \
                                "them general and numbered step-by-step guide for how to solve the " \
                                "question without giving them any details. You will not give the answer directly " \
                                "to the student. You will give the general " \
                                "steps ordered in numerical order. You may receive questions in English or Latex. " \
                                "You always give simple, easy and numbered steps without complicating the steps. "

human_text_assistant = "Question in the past paper exam: \n" \
                       "{question} \n\n" \
                       "Answer in the marking scheme:\n" \
                       "{answer} \n" \
                       "\n" \
                       "Student question:\n" \
                       "{student_question}\n" \
                       "\n" \
                       "You should give me numbered general step by step guide for how to solve this question " \
                       "without giving me " \
                       "the actual answers. Give me only the numbered general steps without any other text."


human_text_assistant = abbreviation + human_text_assistant

# while True:
#     try:
#         letter = input("Enter letter: ")
#         i_letter = input("Enter i_letter: ")
#         student_question = "\t" + input("Enter question: ")
#         steps = input("steps? y/n: ")
#         # prompt = PromptTemplate.from_template(human_text_helper_template_text)
#
#         if steps.lower() != "y":
#             sys_message = SystemMessage(content=helper_system_message_text)
#             human_message_template = HumanMessagePromptTemplate.from_template(human_text_helper_template_text)
#         else:
#             sys_message = SystemMessage(content=assistant_system_message_text)
#             human_message_template = HumanMessagePromptTemplate.from_template(human_text_assistant)
#
#         chat_prompt_template = ChatPromptTemplate.from_messages(
#             [
#                 sys_message,
#                 human_message_template
#             ]
#         )
#
#         model = ChatOpenAI(temperature=0)
#
#         chain = LLMChain(llm=model, prompt=chat_prompt_template)
#
#         question = get_question_text(letter, i_letter)
#         answer = get_marking_scheme_text(letter, i_letter)
#
#         text = chain.predict(question=question, answer=answer, student_question=student_question)
#
#         print(chain.prompt.format(question=question, answer=answer, student_question=student_question))
#
#         print(text)
#
#     except:
#         print("Error")


def get_steps(letter, i_letter, student_question):
    sys_message = SystemMessage(content=assistant_system_message_text)
    human_message_template = HumanMessagePromptTemplate.from_template(human_text_assistant)

    chat_prompt_template = ChatPromptTemplate.from_messages([sys_message, human_message_template])

    model = ChatOpenAI(temperature=0)

    chain = LLMChain(llm=model, prompt=chat_prompt_template)

    question = get_question_text(letter, i_letter)
    answer = get_marking_scheme_text(letter, i_letter)

    text = chain.predict(question=question, answer=answer, student_question=student_question)

    return text