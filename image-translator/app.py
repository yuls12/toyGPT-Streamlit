import streamlit as st
import openai
from PIL import Image
import os


# openai.api_key = st.secrets["api_key"]

st.title("Image to Text")

def save_uploaded_file(directory, file):
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    with open(os.path.join(directory, file.name), 'wb') as f:
        f.write(file.getbuffer())
    return st.success('파일 업로드 성공!')

with st.form("form"):
    img_file =  st.file_uploader('이미지를 업로드 하세요.', type=['png', 'jpg', 'jpeg'])
    language = st.selectbox("Language", ["English", "Korean", "Spanish", "Japanese"])
    submit = st.form_submit_button("Submit")
    
    if img_file is not None: # 파일이 없는 경우는 실행 하지 않음
        print(type(img_file))
        print(img_file.name)
        print(img_file.size)
        print(img_file.type)
        save_uploaded_file('image', img_file)

        st.image(f'image/{img_file.name}')

