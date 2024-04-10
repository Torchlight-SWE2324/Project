import sys
from streamlit.testing.v1 import AppTest
sys.path.append('ChatSQL')  # Assicurati di aggiungere il percorso che contiene la directory 'embedder'

#-------------------------------------------------------------------------------------------------------------------------------------
# test d'integrazione Login
#-------------------------------------------------------------------------------------------------------------------------------------

def login_func():
    """
    The function builds an application which has in its GUI only the graphical components of "LoginWidget" 
    and "AuthenticationController" and "AuthenticationService" classes in the back-end
    """
    import streamlit as st
    from model import AuthenticationService
    from controller import AuthenticationController
    from widgets import LoginWidget

    aut_model = AuthenticationService()
    aut_controller = AuthenticationController(aut_model, None)
    login_widget = LoginWidget(aut_controller)
    aut_controller.set_view(login_widget)
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "doing_test" not in st.session_state:
        st.session_state.doing_test = True
    aut_model.set_logged_status(False)
    login_widget.create()

def test_login_missing_credentials():
    """
    tests the case of trying logging in without inserting both username and password
    """
    at = AppTest.from_function(login_func)
    at.run()

    at.sidebar.text_input[0].set_value("a").run()
    at.sidebar.text_input[1].set_value("").run()
    at.sidebar.button[0].click().run()

    # assert at.sidebar.text_input[0].value == "a"
    # assert at.sidebar.text_input[1].value == "a"
    assert at.session_state.logged_in == False
    assert at.toast[0].value == ":orange[Please write both username and password]" and at.toast[0].icon == "⚠️"

    # assert at.sidebar.button[0].value == False
    # at.sidebar.button[0].click().run()
    # assert at.sidebar.button[0].value == True

def test_login_wrong_credentials():
    """
    tests the case of trying logging in with wrong credentials
    """
    at = AppTest.from_function(login_func)
    at.run()

    at.sidebar.text_input[0].set_value("wrong username").run()
    at.sidebar.text_input[1].set_value("wrong password").run()
    at.sidebar.button[0].click().run()

    assert at.session_state.logged_in == False
    assert at.toast[0].value == ":red[Wrong credentials. Please try again.]" and at.toast[0].icon == "🚨"

def test_login_correct_credentials():
    """
    tests the case of trying logging in with correct credentials
    """
    at = AppTest.from_function(login_func)
    at.run()

    at.sidebar.text_input[0].set_value("admin").run()
    at.sidebar.text_input[1].set_value("admin").run()
    at.sidebar.button[0].click().run()

    assert at.session_state.logged_in == True
    assert at.toast[0].value == ":green[Login successful!]" and at.toast[0].icon == "✅"

#-------------------------------------------------------------------------------------------------------------------------------------
# test d'integrazione Logout
#-------------------------------------------------------------------------------------------------------------------------------------

def logout_func():
    import streamlit as st
    from model import AuthenticationService
    from controller import LogoutController
    from widgets import LogoutWidget

    aut_model = AuthenticationService()
    log_controller = LogoutController(aut_model, None)
    logout_widget = LogoutWidget(log_controller)
    log_controller.set_view(logout_widget)
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = True
    if "doing_test" not in st.session_state:
        st.session_state.doing_test = True
    aut_model.set_logged_status(True)
    logout_widget.create()

def test_logout_correct():
    """
    tests the case of logging out
    """
    at = AppTest.from_function(logout_func)
    at.run()

    at.sidebar.button[0].click().run()
    assert at.session_state.logged_in == False
    assert at.toast[0].value == ":green[Logged out.]" and at.toast[0].icon == "✅"