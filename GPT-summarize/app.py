import streamlit as st
import requests
import pandas as pd
import os
import io

if 'prev_upload_file' not in st.session_state:
    st.session_state['prev_upload_file'] = None
    st.session_state['prev_df'] = None


summarize_url = "http://localhost:8000/summarize"

def call_summarize(text):
    response = requests.post(summarize_url, json = {"text":text})
    summary = response.json()["summary"]
    return summary

def summarize_df(df):
    global progress_bar
    total = len(df)
    news_summary = []
    for i, content in enumerate(df['content'], start=1):
        summary = call_summarize(content)
        news_summary.append(summary)
        progress_bar.progress(i/total, text='progress')
        i += 1
    df['summary'] = news_summary
    return df


def to_excel(df):
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name="Sheet1", index=False)
    writer.close()
    progressed_data =  output.getvalue()
    return progressed_data

st.title('Summarie Application')

tab1, tab2 = st.tabs(["실시간", "파일 업로드"])

with tab1:
    input_text = st.text_area('텍스트를 입력하세요', height=300)
    if st.button('start'):
        if input_text:
            try:
                summary = call_summarize(input_text)
                st.success(summary)
            except:
                st.error("요청 오류가 발생했습니다.")
        else:
            st.warning('텍스트를 입력하세요.')
    st.write()

with tab2:
    upload_file = st.file_uploader('Chosse a file')
    if upload_file:
        st.success("Upload 완료!")
        if upload_file == st.session_state['prev_upload_file']:
            df = st.session_state['prev_df']
        else:
            progress_bar = st.progress(0, text="progress")
            
            df = pd.read_excel(upload_file)
            df = summarize_df(df)
            st.dataframe(df)
            
            st.session_state['prev_upload_file'] = upload_file
            st.session_state['prev_df'] = df
            
        file_base_name = os.path.splitext(os.path.basename(upload_file.name))[0]
        st.download_button(
            label="Download",
            data=to_excel(df),
            file_name=f"{file_base_name}_summaryzed.xlsx"
    )