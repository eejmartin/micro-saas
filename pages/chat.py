# Importing required libraries
import os
from openai import OpenAI
import streamlit as st
from navigation import make_sidebar

# Set Streamlit page configuration
st.set_page_config(page_title="Chat - MicroSaaS", page_icon="💬", layout="centered", initial_sidebar_state="auto", menu_items=None)
print('Loading Chat Page...')

make_sidebar()

api_key = os.getenv("OPENAI_API_KEY")
# Initializing the OpenAI client with API key from Streamlit's secret storage
client = OpenAI(api_key=api_key)

# Ensuring that the OpenAI model is set in the session state; defaulting to 'gpt-3.5-turbo'
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Displaying the title of the chat interface
st.title("Chat with the AI Assistant 💬")

# Ensuring that there is a message list in the session state for storing conversation history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Displaying each message in the session state using Streamlit's chat message display
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handling user input through Streamlit's chat input box
if prompt := st.chat_input("What is up?"):
    # Appending the user's message to the session state
    st.session_state["messages"].append({"role": "user", "content": prompt})
    
    # Displaying the user's message in the chat interface
    with st.chat_message("user"):
        st.markdown(prompt)

    # Preparing to display the assistant's response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()  # Placeholder for assistant's response
        full_response = ""  # Initializing a variable to store the full response

        # Generating a response from the OpenAI model
        for response in client.chat.completions.create(
            model=st.session_state["openai_model"],  # Using the model specified in the session state
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state["messages"]],  # Passing the conversation history
            stream=True,  # Enabling real-time streaming of the response
        ):
            # Updating the response as it is received
            full_response += (response.choices[0].delta.content or "")
            message_placeholder.markdown(full_response + "▌")  # Displaying the response as it's being 'typed'

        # Updating the placeholder with the final response once fully received
        message_placeholder.markdown(full_response)
    
    # Appending the assistant's response to the session's message list
    st.session_state["messages"].append({"role": "assistant", "content": full_response})