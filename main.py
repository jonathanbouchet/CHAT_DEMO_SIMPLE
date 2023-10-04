import openai
import streamlit as st
from utils import template_questionaire

st.title("Chat bot")

MODEL = st.sidebar.selectbox(
    label=":blue[MODEL]",
    options=["gpt-3.5-turbo",
             "ft:gpt-3.5-turbo-0613:osc:finetuned-v6:80vd3iOe",
             "gpt-4"])

# Set API key if not yet
openai_api_key = st.sidebar.text_input(
    ":blue[API-KEY]",
    placeholder="Paste your OpenAI API key here",
    type="password")

if openai_api_key:

    openai.api_key = openai_api_key

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = MODEL
        template = template_questionaire()

    # initialization of the session_state
    if "messages" not in st.session_state:
        # st.session_state["messages"] = []
        # adding the system prompt once at the initialization
        template = template_questionaire()
        st.session_state['messages'] = [
            {"role": "system", "content": template}
        ]
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = MODEL

    # display chat messages from history on app rerun
    for message in st.session_state.messages:
        # don't print the system content
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # react to user input
    if prompt := st.chat_input("Hello"):
        # display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # add user message to chat history
        st.session_state["messages"].append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            for response in openai.ChatCompletion.create(
                    model=st.session_state["openai_model"],
                    temperature=0,
                    stream=True,
                    messages=[
                        {"role": m["role"], "content": m["content"]} for m in st.session_state["messages"]]
            ):
                full_response += response.choices[0].delta.get("content", "")
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        # add assistant response to chat history
        st.session_state["messages"].append({"role": "assistant", "content": full_response})
