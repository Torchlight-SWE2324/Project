import streamlit as st
from observer import *
from Subject import *
class View(Observer, Subject):
    def __init__(self, model):
        Subject.__init__(self)
        Observer.__init__(self)
        self._model = model
        #self._model.attach(self)
        #self.attach(self)
        st.title("ChatSQL")
        st.subheader("Type your natural language query in the chat box below and press enter to get the corresponding SQL query.")
        st.sidebar.title("Login sidebar")
        self.username = None
        self.password = None
        self.isLogged = False
    

        
    def successLogin(self):
        self.isLogged = True
        st.success("Login successful!")

    def erroreLogin(self):
        st.error("Login NO")

    def successLogout(self):
        self.isLogged = False
        st.success("Logout successful!")

    def update(self):
        print("View: Updating view")
        if self._model.getIsLogedd():   # valore dentro al model                                    
            self.successLogin()
            print("View: Login successful")
        else:
            if self.isLogged == False: # valore dentro alla view
                self.erroreLogin()
                print("View: No1")
            else: 
                self.successLogout()
                print("View: No2")


    def technician_login(self):
    
        self.username = st.sidebar.text_input("Username")
        self.password = st.sidebar.text_input("Password", type="password")
    
        if st.sidebar.button("LoginButton"):
            #st.success("Login successful!")
            #if not empty
            if self.username or self.password:
                self.notify_observers()

            #st.error("Login failed. Invalid username or password.")

    def getUser(self):
        return [self.username, self.password]