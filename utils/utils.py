import streamlit as st
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import PyPDF2

from dotenv import load_dotenv
load_dotenv()

# def resend_verification(email):
    # st.success("Verification email resent successfully!")
    # verification_url = os.getenv("VERIFICATION_URL")
    # data = {'email': email}
    # response = requests.post(verification_url, json=data)
    # if response.status_code != 200:
    #     st.error(f"Failed to resend verification email: {response.text}")
    # else:
    #     st.success("Verification email resent successfully!")

def reset_password():
    if st.session_state['authentication_status']:
        try:
            if st.session_state['authenticator'].reset_password(st.session_state['username'], 'Reset password'):
                st.success('Password modified successfully')
        except Exception as e:
            st.error(e)

def send_email(subject, message, to_address):
    from_address = os.getenv("YOUR_EMAIL")
    password = os.getenv("YOUR_EMAIL_PASS")
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))
    server = smtplib.SMTP_SSL('mail.privateemail.com', 465)
    server.login(from_address, password)
    text = msg.as_string()
    server.sendmail(from_address, to_address, text)
    server.quit()

def forgot_password():
    try:
        username_forgot_pw, email_forgot_password, random_password = st.session_state['authenticator'].forgot_password('Forgot password')
        if username_forgot_pw:
            subject = 'Your Micro SaaS App New Password'
            message = f'Your new Micro SaaS App password is: {random_password}. Please login and reset your password.'
            send_email(subject, message, email_forgot_password)
            st.success('New password sent securely')
        else:
            st.error('Username not found. Register below.')
    except Exception as e:
        st.error(e)


def register_new_user():
    try:
        if st.session_state['authenticator'].register_user('Register user', preauthorization=False):
            st.success('Great! Now please complete registration by confirming your email address. Then login above!')
    except Exception as e:
        st.error(e)

def read_pdf(file):
    """
    Reads a PDF file and extracts the text content.

    Parameters:
    file (UploadedFile): The uploaded PDF file.

    Returns:
    str: Extracted text from the PDF file.
    """
    try:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        st.error(f"Failed to read PDF file: {e}")
        return None