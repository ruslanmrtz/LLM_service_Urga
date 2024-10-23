import pandas as pd
import streamlit as st
import requests


BACKEND_PATH = 'https://llm-service-urga.onrender.com'



# Инициализация состояния Streamlit и загрузка данных из базы при первом запуске
if 'df' not in st.session_state:
    result = requests.get(f'{BACKEND_PATH}/prompts').json()
    st.session_state.df = result # Сохраняем состояние 'df'

df = pd.DataFrame(st.session_state.df)

if 'prompt_data' not in st.session_state:
    st.session_state.prompt_data = {}

st.title("Просмотр версий prompt'ов")
st.divider()

with st.sidebar:
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

# Обновление состояния при изменении выбора и загрузка данных
if all([project_name, func_name, prompt, llm_name]) and (project_name, func_name, prompt, llm_name) != st.session_state.prompt_data:
    st.session_state.prompt_data = (project_name, func_name, prompt, llm_name)

    result = requests.get(f'{BACKEND_PATH}/get_prompt/{project_name}/{func_name}/{prompt}/{llm_name}').json()
    st.session_state.prompt_data = result

# Отображение данных
if st.session_state.prompt_data:  # Проверка наличия данных в prompt_data

    st.subheader("Текст Prompt'a")

    result = requests.get(f'{BACKEND_PATH}/get_prompt/{project_name}/{func_name}/{prompt}/{llm_name}').json()
    new_prompt = st.text_input(label=' ', value=result['prompt'])

    st.divider()

    st.subheader('Справочная информация')

    st.markdown(f'Выбранный Prompt: **{result["prompt"]}**')
    st.markdown(f'Выбранный LLM: **{result["llm_name"]}**')

    new_score = st.number_input("Оценка", value=result['score'], step=1, min_value=0, max_value=100)

    new_com = st.text_input(label='Комментарий', value=result['comment'])

    if st.button('Сохранить'):
        try:
            body = {
                "id": result['id'],
                "prompt": new_prompt,
                "score": new_score,
                "comment": new_com
            }
            requests.put(f'{BACKEND_PATH}/update_prompt', params=body)
        except:
            st.error('Ошибка базы данных, свяжитесь с поставщиком услуг')
        else:
            st.success('Изменения успешно сохранены!')

else:
    st.error('Ожидание выбора модели', icon="🚨")
