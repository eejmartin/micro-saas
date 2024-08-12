import streamlit as st
import time
from streamlit_js_eval import streamlit_js_eval
from utils.utils import send_email
from navigation import make_sidebar

# Set Streamlit page configuration
st.set_page_config(page_title="Contact Us - MicroSaaS", page_icon="✉️", layout="centered", initial_sidebar_state="auto", menu_items=None)

## Contact Form
st.header("✉️ Contact Form")

print('Loading Contact Us Page...')
make_sidebar()

col1, col2, col3, col4 =  st.columns([4, 0.25, 1, 0.25]) # column widths for a balanced distribution of elements in the page

## Contact form
with col1: # left side of the layout
    name = st.text_input("**Your name***", value=st.session_state.get('name', ''), key='name') # input widget for contact name
    email = st.text_input("**Your email***", value=st.session_state.get('email', ''), key='email') # input widget for contact email
    message = st.text_area("**Your message***", value=st.session_state.get('message', ''), key='message') # input widget for message

    st.markdown('<p style="font-size: 13px;">*Required fields</p>', unsafe_allow_html=True) # indication to user that both fields must be filled

    if st.button("Send", type="primary"):
        if not email or not message:
            st.error("Please fill out all required fields.") # error for any blank field
        else:
            try:
                # Robust email validation
                valid = validate_email(email, check_deliverability=True)
                    
                data = {'email': email, 'message': message, 'name': name}, 
                send_email("Contact Form Submission", data, recipient) # send email to recipient
                st.success("Sent successfully!") # Success message to the user. 
                
                time.sleep(3)
                streamlit_js_eval(js_expressions="parent.window.location.reload()")

            except EmailNotValidError as e:
                st.error(f"Invalid email address. {e}") # error in case any of the email validation checks have not passed

#st.markdown(f'<div style="position: fixed; bottom: 0; width: 100%; "><p style="text-align: left; color: #a3a0a3; margin-bottom: 28px; font-size: 11px;"><a href="https://github.com/jlnetosci/streamlit-contact-form" target="_blank" style="color: inherit;">Base template</a> by: <a href="https://github.com/jlnetosci" target="_blank" style="color: inherit;">João L. Neto</a></p></div>', unsafe_allow_html=True)