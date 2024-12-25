from agent.configuration.configuration import configuration
from agent.logger.logger import setup_logging
from agent.agent import app
import streamlit as st

# Настройка логгера
logger_config_path = configuration.project_root / "logger_config.json"

setup_logging(config_path=logger_config_path)

if __name__ == "__main__":
    # Настройка фронта для агента
    st.title("AI city agent")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Отображаем сообщения на странице
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Логика получения вопроса от пользователя
    if prompt := st.chat_input("Type your question?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

    # Логика отаета агента на вопрос пользователя
    if st.session_state.messages:    
        with st.chat_message("agent"):
            stream = app.stream(input={"question": st.session_state.messages[-1]["content"]}, stream_mode="values", output_keys="generation")
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})