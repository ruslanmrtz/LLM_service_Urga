import pandas as pd
import streamlit as st
import requests


BACKEND_PATH = 'https://llm-service-urga.onrender.com'

result = requests.get(f'{BACKEND_PATH}/prompts').json()
df = pd.DataFrame(result)

st.title("Просмотр версий prompt'ов")
st.divider()

project_name = st.selectbox(
    "Проект",
    [''] + list(df['project_name'].unique())
)

labels_func = df[df['project_name'] == project_name] if project_name else df
func_name = st.selectbox(
    "Функция",
    [''] + list(labels_func['func_name'].unique()),
)

labels_prompt = df[(df['project_name'] == project_name) & (df['func_name'] == func_name)]\
    if (project_name and func_name) else df
prompt = st.selectbox(
    "Prompt",
    [''] + list(labels_prompt['prompt'].unique()),
)

label_llm = df[(df['project_name'] == project_name) & (df['func_name'] == func_name) & (df['prompt'] == prompt)]\
    if (project_name and func_name and prompt) else df
llm_name = st.selectbox(
    "LLM",
    [''] + list(label_llm['llm_name'].unique()),
)

st.divider()

if project_name and func_name and prompt and llm_name:
    st.header("Текст Prompt'a")

    result = requests.get(f'{BACKEND_PATH}/get_prompt/{project_name}/{func_name}/{prompt}/{llm_name}').json()
    st.text_input(label='', value=result['prompt'])


    def copy_to_clipboard(text):
        """
        Функция для копирования текста в буфер обмена
        """
        js = f"navigator.clipboard.writeText('{text}')"
        html = f"<script>{js}</script>"
        st.markdown(html, unsafe_allow_html=True)

    text = st.session_state.input_text

    if st.button("Скопировать"):
        copy_to_clipboard(text)
        st.success("Текст скопирован!")