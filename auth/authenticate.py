import jwt
import bcrypt
import streamlit as st
from datetime import datetime, timedelta
import extra_streamlit_components as stx
from .utils import *
from .exceptions import CredentialsError, ForgotError, RegisterError, ResetError, UpdateError
from mongo_db.models.users import Users

class Authenticate:
    """
    This class will create login, logout, register user, reset password, forgot password, 
    forgot email, and modify user details widgets.
    """
    def __init__(self, cookie_name: str, key: str, cookie_expiry_days: int=30):
        """
        Create a new instance of "Authenticate".
        Parameters
        ----------
        cookie_name: str
            The name of the JWT cookie stored on the client's browser for passwordless reauthentication.
        key: str
            The key to be used for hashing the signature of the JWT cookie.
        cookie_expiry_days: int
            The number of days before the cookie expires on the client's browser.
        """
        self.cookie_name = cookie_name
        self.key = key
        self.cookie_expiry_days = cookie_expiry_days
        self.cookie_manager = stx.CookieManager()

        if 'name' not in st.session_state:
            st.session_state['name'] = None
        if 'authentication_status' not in st.session_state:
            st.session_state['authentication_status'] = None
        if 'email' not in st.session_state:
            st.session_state['email'] = None
        if 'logout' not in st.session_state:
            st.session_state['logout'] = None
        self.preauthorized = {'emails': []}

    def _token_encode(self) -> str:
        """
        Encodes the contents of the reauthentication cookie.
        Returns
        -------
        str
            The JWT cookie for passwordless reauthentication.
        """
        return jwt.encode({'name':st.session_state['name'],
            'email':st.session_state['email'],
            'exp_date':self.exp_date}, self.key, algorithm='HS256')

    def _token_decode(self) -> str:
        """
        Decodes the contents of the reauthentication cookie.
        Returns
        -------
        str
            The decoded JWT cookie for passwordless reauthentication.
        """
        try:
            return jwt.decode(self.token, self.key, algorithms=['HS256'])
        except:
            return False

    def _set_exp_date(self) -> str:
        """
        Creates the reauthentication cookie's expiry date.
        Returns
        -------
        str
            The JWT cookie's expiry timestamp in Unix epoch

        """
        return (datetime.utcnow() + timedelta(days=self.cookie_expiry_days)).timestamp()

    def _check_pw(self, user) -> bool:
        """
        Checks the validity of the entered password.
        Returns
        -------
        bool
            The validity of the entered password by comparing it to the hashed password in the Airtable.
        """
        if user is not None:
            hashed_pw = user['password']
            return bcrypt.checkpw(self.password.encode(), hashed_pw.encode())
        return False

    def _check_cookie(self):
        """
        Checks the validity of the reauthentication cookie.
        """
        print('Checks the validity of the reauthentication cookie')
        self.token = self.cookie_manager.get(self.cookie_name)
        if self.token is not None:
            self.token = self._token_decode()            
            if self.token is not False:
                if st.session_state['logout'] in [None, False]:
                    if self.token['exp_date'] > datetime.utcnow().timestamp():
                        if 'name' and 'email' in self.token:
                            st.session_state['name'] = self.token['name']
                            st.session_state['email'] = self.token['email']
                            st.session_state['authentication_status'] = True

    def _check_email_verified(self) -> bool:
        """
        Checks the validity of the entered email.

        Parameters
        ----------
        email: str
            The email to check the validity of.
        Returns
        -------
        bool
            Validity of entered email.
        """
        print('checking email verified')
        if not self.email:
            return False
        users = Users()
        user = users.get_user_by_email(self.email)
        if user is not None:
            if 'verified' in user and user['verified']:
                st.session_state['verified'] = True
                print('user verified!!!')
                return True
            else:
                st.session_state['verified'] = False
                print('user not verified')
                return False
        st.session_state['verified'] = False
        return False
    
    def _check_credentials(self, inplace: bool=True) -> bool:

        """
        Checks the validity of the entered credentials.

        Parameters
        ----------
        inplace: bool
            Inplace setting, True: authentication status will be stored in session state, 
            False: authentication status will be returned as bool.
        Returns
        -------
        bool
            Validity of entered credentials.
        """
        print('checking credentials....')
        st.session_state['verified'] = False
        users = Users()
        user = users.get_user_by_email(self.email)
        if user is not None:
            try:
                if 'verified' in user and user['verified']:
                    print("VERIFIED")
                    st.session_state['verified'] = True                    
                if self._check_pw(user):
                    if inplace:
                        st.session_state['name'] = user['name']
                        self.exp_date = self._set_exp_date()
                        self.token = self._token_encode()
                        self.cookie_manager.set(self.cookie_name, self.token,
                                                expires_at=datetime.now() + timedelta(days=self.cookie_expiry_days))
                        st.session_state['authentication_status'] = True
                    else:
                        return True
                else:
                    if inplace:
                        st.session_state['authentication_status'] = False
                    else:
                        return False
            except Exception as e:
                print(e)
        else:
            if inplace:
                st.session_state['authentication_status'] = False
            else:
                return False


    def login(self, form_name: str, location: str='main') -> tuple:       
        """
        Creates a login widget.

        Parameters
        ----------
        form_name: str
            The rendered name of the login form.
        location: str
            The location of the login form i.e. main or sidebar.
        Returns
        -------
        str
            Name of the authenticated user.
        bool
            The status of authentication, None: no credentials entered, 
            False: incorrect credentials, True: correct credentials.
        str
            email of the authenticated user.
        """                 
        if st.session_state.get('authentication_status') in [None, False] or st.session_state.get('verified') in [None, False]:                
            if location in ['main', 'contact_us', 'home', 'chat', 'ai_photo_editing', 'ai_document_summarize']:
                login_form = st.form('Login')
            elif location == 'sidebar':
                login_form = st.sidebar.form('Login')
            
            login_form.subheader(form_name)
            self.email = login_form.text_input('Email').lower()
            st.session_state['email'] = self.email
            self.password = login_form.text_input('Password', type='password')
            
            if login_form.form_submit_button('Login'):
                self._check_credentials()
            columns = st.columns((1,1,1))
            if columns[0].button('Forgot password', key="1", use_container_width=True):
                self.forgot_password('Forgot Password', location)
            if columns[2].button('Register', key="2", use_container_width=True):
                st.warning('New to Micro - SaaS app? Register below.')
                self.register_user('Register user', location)

        return st.session_state['name'], st.session_state['authentication_status'], st.session_state['email']

    def check_authentication(self, location: str='main') -> tuple:
        if location not in ['main', 'sidebar', 'contact_us', 'home', 'chat', 'ai_photo_editing', 'ai_document_summarize']:
            raise ValueError("Location must be one of 'main' or 'sidebar'")
        if not st.session_state['authentication_status'] or st.session_state.get('verified') in [None, False]:             
            self._check_cookie()
            self.email = st.session_state.get('email')

            if st.session_state.get('verified') in [None, False]:
                email_verified = self._check_email_verified()                
                return email_verified
            
            return False
        
    def login_modal(self, email, password):
        self.email = email
        self.password = password
        self._check_credentials()

    def logout(self, button_name: str, location: str='main', key='123'):
        """
        Creates a logout button.

        Parameters
        ----------
        button_name: str
            The rendered name of the logout button.
        location: str
            The location of the logout button i.e. main or sidebar.
        """
        print('------------------logout------------------')
        
        if location not in ['main', 'sidebar']:
            raise ValueError("Location must be one of 'main' or 'sidebar'")
        if location == 'main':
            if st.button(button_name, key=key):
                self.cookie_manager.delete(self.cookie_name)
                st.session_state['logout'] = True
                st.session_state['name'] = None
                st.session_state['email'] = None
                st.session_state['authentication_status'] = None
                st.session_state['verified'] = None
        elif location == 'sidebar':
            self.cookie_manager.delete(self.cookie_name)
            st.session_state['logout'] = True
            st.session_state['name'] = None
            st.session_state['email'] = None
            st.session_state['authentication_status'] = None
            st.session_state['verified'] = None
  

    def _update_password(self, email: str, password: str):
        """
        Updates user's password in the database.

        Parameters
        ----------
        email: str
            The email of the user to update the password for.
        password: str
            The updated plain text password.
        """
        users = Users(True)
        user = users.get_user_by_email(self.email)
        if user:
            users.update_password(email, password)

    def reset_password(self, email: str, form_name: str, location: str='main') -> bool:
        """
        Creates a password reset widget.

        Parameters
        ----------
        email: str
            The email of the user to reset the password for.
        form_name: str
            The rendered name of the password reset form.
        location: str
            The location of the password reset form i.e. main or sidebar.
        Returns
        -------
        bool
            The status of resetting the password.
        """
        if location not in ['main', 'sidebar']:
            raise ValueError("Location must be one of 'main' or 'sidebar'")

        reset_password_form = None
        if location == 'main':
            reset_password_form = st.form('Reset password')
        elif location == 'sidebar':
            reset_password_form = st.sidebar.form('Reset password')

        reset_password_form.subheader(form_name)
        self.email = email.lower()
        self.password = reset_password_form.text_input('Current password', type='password')
        new_password = reset_password_form.text_input('New password', type='password')
        new_password_repeat = reset_password_form.text_input('Repeat password', type='password')
        if reset_password_form.form_submit_button('Reset'):
            users = Users()
            user_info = users.get_user_by_email(self.email)
            if user_info is not None:
                if self._check_credentials(inplace=False):
                    if len(new_password) > 0:
                        if new_password == new_password_repeat:
                            if self.password != new_password:
                                self._update_password(self.email, new_password)
                                return self.email
                            else:
                                raise ResetError('New and current passwords are the same')
                        else:
                            raise ResetError('Passwords do not match')
                    else:
                        raise ResetError('No new password provided')
                else:
                    raise ResetError('Wrong password')
            else:
                raise CredentialsError
        else:
            return False

    def register_user(self, form_name: str, location: str='main', preauthorization=True) -> bool:
        """
        Creates a password reset widget.

        Parameters
        ----------
        form_name: str
            The rendered name of the password reset form.
        location: str
            The location of the password reset form i.e. main or sidebar.
        preauthorization: bool
            The preauthorization requirement, True: user must be preauthorized to register, 
            False: any user can register.
        Returns
        -------
        bool
            The status of registering the new user, True: user registered successfully.
        """
        if preauthorization:
            if not self.preauthorized:
                raise ValueError("preauthorization argument must not be None")
        if location not in ['main', 'sidebar']:
            raise ValueError("Location must be one of 'main' or 'sidebar'")
        if location == 'main':
            register_user_form = st.form('Register user')
        elif location == 'sidebar':
            register_user_form = st.sidebar.form('Register user')

        register_user_form.subheader(form_name)
        new_email = register_user_form.text_input('Email')
        new_name = register_user_form.text_input('Name')
        new_password = register_user_form.text_input('Password', type='password')
        new_password_repeat = register_user_form.text_input('Repeat password', type='password')
        postal_code = register_user_form.text_input('Your postal code')

        users = Users(True)
        if register_user_form.form_submit_button('Register'):
            if validate_email(new_email):
                if len(new_email) and len(new_email) and len(new_name) and len(new_password) > 0:
                    if users.find_one({'email': new_email}) is None:
                        if new_password == new_password_repeat:
                            if preauthorization:
                                if self.preauthorized.find_one({'email': new_email}) is not None:
                                    users.create_user(new_email, new_name, new_password, postal_code)                                    
                                    return True
                                else:
                                    users.disconnect()
                                    raise RegisterError('User not preauthorized to register')
                            else:
                                users.create_user(new_email, new_name, new_password, postal_code)
                                return True
                        else:
                            users.disconnect()
                            raise RegisterError('Passwords do not match')
                    else:
                        users.disconnect()
                        raise RegisterError('email already taken')
                else:
                    users.disconnect()
                    raise RegisterError('Please enter an email, name, and password')
            else:
                users.disconnect()
                raise RegisterError('Please enter a valid email address')

    def forgot_password(self, form_name: str, location: str='main') -> tuple:
        """
        Creates a forgot password widget.

        Parameters
        ----------
        form_name: str
            The rendered name of the forgot password form.
        location: str
            The location of the forgot password form i.e. main or sidebar.
        Returns
        -------
        str
            email associated with forgotten password.
        str
            Email associated with forgotten password.
        str
            New plain text password that should be transferred to user securely.
        """
        if location not in ['main', 'sidebar']:
            raise ValueError("Location must be one of 'main' or 'sidebar'")
        if location == 'main':
            forgot_password_form = st.form('Forgot password')
        elif location == 'sidebar':
            forgot_password_form = st.sidebar.form('Forgot password')

        forgot_password_form.subheader(form_name)
        email = forgot_password_form.text_input('email').lower()

        if forgot_password_form.form_submit_button('Submit'):
            if len(email) > 0:                
                users = Users()
                user = users.get_user_by_email(email)
                if user is not None:
                    return email, user['email'], self._set_random_password(email)
                else:
                    return False, None, None
            else:
                raise ForgotError('email not provided')
        return None, None, None
    
    def _set_random_password(self, email: str) -> str:
        """
        Updates the database with user's hashed random password.

        Parameters
        ----------
        email: str
            email of user to set random password for.
        Returns
        -------
        str
            New plain text password that should be transferred to user securely.
        """
        self.random_password = generate_random_pw()        
        users = Users()
        users.update_password(email, self.random_password)
        return self.random_password

    def update_user_details(self, email: str, form_name: str, location: str='main') -> bool:
        """
        Creates a update user details widget.

        Parameters
        ----------
        email: str
            The email of the user to update user details for.
        form_name: str
            The rendered name of the update user details form.
        location: str
            The location of the update user details form i.e. main or sidebar.
        Returns
        -------
        str
            The status of updating user details.
        """
        if location not in ['main', 'sidebar']:
            raise ValueError("Location must be one of 'main' or 'sidebar'")
        if location == 'main':
            update_user_details_form = st.form('Update user details')
        elif location == 'sidebar':
            update_user_details_form = st.sidebar.form('Update user details')
        
        update_user_details_form.subheader(form_name)
        self.email = email.lower()
        field = update_user_details_form.selectbox('Field', ['name']).lower()
        new_value = update_user_details_form.text_input('New value')
        users = Users(True)
        user = users.get_user_by_email(email)
        if update_user_details_form.form_submit_button('Update'):
            if len(new_value) > 0:                
                if new_value != user[field]:
                    user.update_by_key(field, new_value, email)                    
                    if field == 'name':
                            st.session_state['name'] = new_value
                            self.exp_date = self._set_exp_date()
                            self.token = self._token_encode()
                            self.cookie_manager.set(self.cookie_name, self.token,
                            expires_at=datetime.now() + timedelta(days=self.cookie_expiry_days))                    
                    return True
                else:
                    users.disconnect()
                    raise UpdateError('New and current values are the same')
            if len(new_value) == 0:
                users.disconnect()
                raise UpdateError('New value not provided')
