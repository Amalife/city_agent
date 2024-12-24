from agent.configuration.configuration import configuration
from agent.logger.logger import setup_logging
from agent.agent import app
import streamlit as st

logger_config_path = configuration.project_root / "logger_config.json"

setup_logging(config_path=logger_config_path)

if __name__ == "__main__":
    st.title("AI city agent")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Type your question?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

    if st.session_state.messages:    
        with st.chat_message("agent"):
            stream = app.stream(input={"question": st.session_state.messages[-1]["content"]}, stream_mode="values", output_keys="generation")
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})