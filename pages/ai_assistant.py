# Importing required libraries
import os
from openai import OpenAI
import streamlit as st
import replicate
from navigation import make_sidebar

os.environ["REPLICATE_API_TOKEN"] = os.environ.get("REPLICATE_API_TOKEN")

# Set Streamlit page configuration
st.set_page_config(page_title="AI Assistant - MicroSaaS", page_icon="📨", layout="centered", initial_sidebar_state="auto", menu_items=None)

print('Loading Assistant Page...')

make_sidebar()

# Ensuring that the OpenAI model is set in the session state; defaulting to 'gpt-3.5-turbo'
if "meta-llama" not in st.session_state:
    st.session_state["meta-llama"] = "meta/meta-llama-3.1-405b-instruct"


st.title("Get help from the most powerful AI Assistant 📨")

html_text = f"""
    <p>Get help from the most powerful AI Assistant! Our AI Assistant uses the most powerful Meta / meta-llama-3.1-405b-instruct model to generate human-like responses to your messages. Ask questions, seek advice, or just have a casual conversation with our AI Assistant.</p>
"""

st.html(html_text)

# Ensuring that there is a message list in the session state for storing conversation history
if "assistant_messages" not in st.session_state:
    st.session_state["assistant_messages"] = []

# Displaying each message in the session state using Streamlit's chat message display
for message in st.session_state["assistant_messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handling user input through Streamlit's chat input box
if prompt := st.chat_input("How can I help you today?"):
    # Appending the user's message to the session state
    st.session_state["assistant_messages"].append({"role": "user", "content": prompt})

    # Displaying the user's message in the chat interface
    with st.chat_message("user"):
        st.markdown(prompt)

    # Preparing to display the assistant's response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()  # Placeholder for assistant's response
        full_response = ""  # Initializing a variable to store the full response

        # Generating a response from the OpenAI model
        for event in replicate.stream(
            st.session_state["meta-llama"],  # Using the model specified in the session state
            input={
                "prompt": prompt,
                "max_tokens": 1024
                },  # Passing the user's message as input
        ):
            # Updating the response as it is received
            full_response += (event.data or "")
            message_placeholder.markdown(full_response + "▌")  # Displaying the response as it's being 'typed'

        # Updating the placeholder with the final response once fully received
        message_placeholder.markdown(full_response)
    
    # Appending the assistant's response to the session's message list
    st.session_state["assistant_messages"].append({"role": "assistant", "content": full_response})                