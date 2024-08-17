import streamlit as st
from time import sleep
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit.source_util import get_pages
from auth import Authenticate

def get_current_page_name():
    ctx = get_script_run_ctx()
    if ctx is None:
        raise RuntimeError("Couldn't get script context")

    pages = get_pages("")

    return pages[ctx.page_script_hash]["page_name"]


def make_sidebar():
    # Initialize the authenticator
    st.session_state['authenticator'] = Authenticate("coolcookiesd267", "keyd3214", 60)

    current_page_name = get_current_page_name()
    st.session_state['authenticator'].check_authentication(current_page_name)

    with st.sidebar:

        st.sidebar.page_link('home.py', label='Home')
        st.sidebar.page_link('pages/contact_us.py', label='Contact Us', icon="✉️")
        
        if st.session_state["authentication_status"] and st.session_state["verified"]:            
            st.sidebar.page_link('pages/ai_chat.py', label='Chat with AI bot', icon="💬")
            st.sidebar.page_link('pages/ai_assistant.py', label='AI Assistant', icon="📨")
            st.sidebar.page_link('pages/ai_photo_editing.py', label='AI Photo Editing', icon="📷")
            st.sidebar.page_link('pages/ai_document_summarize.py', label='AI Document Summarize', icon="📰")
            
            st.write("")
            st.write("")

            if st.button("Log out"):
                logout()

        elif current_page_name != "home" and current_page_name != "contact_us":
            # If anyone tries to access a secret page without being logged in,
            # redirect them to the login page            
            st.switch_page("home.py")

def logout():
    print('Logging out...')
    st.session_state['authenticator'].logout('Logout', 'sidebar', key='123')
    st.info("Logged out successfully!")
    sleep(0.5)
    st.switch_page("home.py")