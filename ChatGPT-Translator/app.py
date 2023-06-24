import openai
import streamlit as st

openai.api_key = st.secrets["api_key"]

parallel_example = {
            "Korean": ["오늘 날씨 어때", "딥러닝 기반의 AI기술이 인기를끌고 있다."],
            "English": ["How is the weather today", "Deep learning-based AI technology is gaining popularity."],
            "Japanese": ["今日の天気はどうですか", "ディープラーニングベースのAIテクノロジーが人気を集めています。"],
            "Spanish" : ["¿Qué tiempo hace hoy?", "Las técnicas de IA basadas en el aprendizaje profundo están ganando popularidad."]
                    }

def translator_davinci(text, src_language, target_language):
    response = openai.Completion.create(engine="text-davinci-003",
                             prompt = f"Translate the following {src_language} text to {target_language} : {text} ",
                             max_tokens = 200,
                             n =1,
                            temperature =1)
    
    translated_text = response.choices[0].text.strip()
    
    return translated_text


def translator_chatgpt(text, src_language, target_language):
    def build_fewshot(src_language, target_language):
        src_examples = parallel_example[src_language]
        target_examples = parallel_example[target_language]
        
        fewshot_messages = []
        
        for src_text, target_text in zip(src_examples, target_examples):
            fewshot_messages.append({"role":"user","content":src_text})
            fewshot_messages.append({"role":"assistant","content":target_text})
        
        return fewshot_messages
        
    system_instruction = f"assistant는 번역앱으로서 동작한다. {src_language} 는 {target_language}로 번역하고 번역된 text만 출력한다. "
    
    fewshot_messages = build_fewshot(src_language=src_language, target_language=target_language)
    
    messages = [{"role":"system","content":system_instruction},
                *fewshot_messages,
               {"role":"user","content": text}]
    
    response =openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                           messages = messages)
    translated_text = response['choices'][0]['message']['content']
    return translated_text

st.title("ChatGPT를 활용한 번역 서비스")
text = st.text_area("번역할 내용을 입력하세요.")

src_language = st.selectbox("입력 언어", ['English', 'Korean', 'Japanese', 'Spanish'], index=1)
target_language = st.selectbox("번역할 언어", ['English', 'Korean', 'Japanese', 'Spanish'])

if st.button("translate"):
    translated_text = translator_chatgpt(text, src_language, target_language)
    st.success(translated_text)