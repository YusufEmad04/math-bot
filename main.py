from prompts import get_steps
import streamlit as st


def insert_spaces_and_newlines(latex):
    print(latex)
    # add spaces and newline characters to latex
    latex = latex.replace(" ", r"\ ")
    latex = latex.replace("\n", r"\\")
    print(latex)
    return latex

class QuestionLetter:
    def __init__(self, letter, letter_i):
        self.letter = letter
        self.letter_i = letter_i

    def __str__(self):
        return f"{self.letter}) {self.letter_i})"


def button_callback(q_l, q_li, text):
    print("button clicked")
    if text:
        #     latex = r'''$
        # a + ar + a r^2 + a r^3 + \cdots + a r^{n-1} =
        # \sum_{k=0}^{n-1} ar^k =
        # a \left(\frac{1-r^{n}}{1-r}\right)$
        # '''
        st.session_state.messages.append({"role": "user", "latex": False, "text": text})
        st.spinner("Thinking...")
        answer = get_steps(q_l, q_li, text)
        st.success("Done!")
        st.session_state.messages.append({"role": "bot", "latex": True, "text": answer})


if "messages" not in st.session_state:
    st.session_state.messages = []

q_objects = [
    QuestionLetter("a", "i"),
    QuestionLetter("a", "ii"),
    QuestionLetter("b", "i"),
    QuestionLetter("b", "ii"),
    QuestionLetter("b", "iii"),
    QuestionLetter("b", "iv"),
    QuestionLetter("c", "i"),
    QuestionLetter("c", "ii"),
]

q_options = {str(q): q for q in q_objects}
questions_choice = st.selectbox("Choose a question", [str(q) for q in q_objects])
q_l = q_options[questions_choice].letter
q_li = q_options[questions_choice].letter_i
# st.write(f"You selected {q_options[questions_choice].letter} and {q_options[questions_choice].letter_i}")
input_field = st.text_input("Enter a message")
button = st.button("Send", on_click=button_callback, args=(q_l, q_li, input_field,))

for message in st.session_state.messages:
    if message["role"] == "user":
        st.subheader("You: ")
        if message["latex"]:
            st.markdown(message["text"])
        else:
            st.markdown(message["text"])

    elif message["role"] == "bot":
        st.subheader("Bot: ")
        if message["latex"]:
            # st.markdown(message["text"])
            st.latex(insert_spaces_and_newlines(message["text"]))
        else:
            st.markdown(message["text"])

    st.divider()
    st.markdown(r'<p style="font-size: 25px;">This is a paragraph with smaller text size.</p>', unsafe_allow_html=True)
