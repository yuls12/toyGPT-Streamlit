import streamlit as st
from streamlit_chat import message
import requests

if 'messages' not in st.session_state:
    st.session_state['messages'] = []

chat_url = "http://localhost:8000/chat"


def chat(text):
    user_turn = {"role": "user", "content": text}
    messages = st.session_state['messages']
    resp = requests.post(chat_url, json={"messages": messages + [user_turn]})
    assistant_turn = resp.json()
    
    st.session_state['messages'].append(user_turn)
    st.session_state['messages'].append(assistant_turn)


st.title("Chatbot App")

row1 = st.container()
row2 = st.container()

with row2:
    input_text = st.text_input("You")
    if input_text:
        chat(input_text)


with row1:
    for i, msg_obj in enumerate(st.session_state['messages']):
        msg = msg_obj['content']
        is_user = False
        if i % 2 == 0:
            is_user = True

        message(msg, is_user=is_user, key=f"chat_{i}")

