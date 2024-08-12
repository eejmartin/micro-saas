import streamlit as st
from streamlit.logger import get_logger
import logging
import threading
from utils import utils
from dotenv import load_dotenv
from navigation import make_sidebar
load_dotenv('.env')

# Set Streamlit page configuration
st.set_page_config(page_title="Micro - SaaS", page_icon=":computer:", layout="centered", initial_sidebar_state="auto", menu_items=None)
st.markdown('# Welcome to Generative AI Micro-SaaS App')

# Set custom CSS
with open('./style/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

LOGGER = get_logger(__file__)
LOGGER.setLevel(logging.DEBUG)
LOGGER.debug(f'start of streamlit_test, {threading.get_ident()}')
LOGGER.debug(f'end of streamlit_test, {threading.get_ident()}')

make_sidebar()

LOGGER.debug(st.session_state)
# Set default session state values if not already set
if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = None
if 'verified' not in st.session_state:
    st.session_state['verified'] = None

# Handle login if not authenticated and not verified
if not st.session_state['authentication_status'] and not st.session_state['verified']:
    if st.session_state['authenticator'].check_authentication() is False:
        st.session_state['authenticator'].login('Login', 'main')

# Handle actions for users with correct password but unverified email
elif st.session_state["authentication_status"] == True and st.session_state['verified'] == False:
    st.error('Email has not been not verified. Check your email for a verification link. After you verify your email, refresh this page to login.')
    
    # Add a button to resend the email verification
    if st.session_state.get('email'):
        if st.button(f"Resend Email Verification to {st.session_state['email']}"):
            utils.resend_verification(st.session_state['email'])

# Handle actions for users with incorrect login credentials
elif st.session_state["authentication_status"] == False:
    st.error('Username/password is incorrect or does not exist. Reset login credential or register below.')


print('Loading Home Page...')
print('------------------------------------------')

if (st.session_state['authentication_status'] and st.session_state['verified']):
    st.html('<h3>Unlock the Power of Generative AI with Ease!</h3>')
    st.markdown('Welcome to your one-stop solution for leveraging the latest in AI technology to automate tasks, generate content, and supercharge your business. Our Generative AI Micro-SaaS App provides a suite of powerful tools designed to help you innovate and stay ahead of the curve.')
    st.html("<H3>Why Choose Us?</H3>")
    html_list = f"""
        <ul>
            <li><strong>Automate Repetitive Tasks</strong>: Let AI handle the mundane so you can focus on what really matters.</li>
            <li><strong>Create Custom Content</strong>: Generate unique text, images, and media for your marketing, blogging, or creative projects.</li>
            <li><strong>Enhance Productivity</strong>: Use AI to optimize workflows and improve decision-making with intelligent insights.</li>
        </ul>

        <h3>What Can You Do with Our App?</h3>
        <ul>
            <li>Automate Repetitive Tasks: Let AI handle the mundane so you can focus on what really matters.</li>
            <li>Create Custom Content: Generate unique text, images, and media for your marketing, blogging, or creative projects.</li>
            <li>Enhance Productivity: Use AI to optimize workflows and improve decision-making with intelligent insights.</li>
        </ul>        
    """
    st.html(html_list)

# Display the main title
