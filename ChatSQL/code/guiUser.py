import random
import streamlit as st
import time

from guiAdmin import guiAdmin
from guiFileOperations import getFiles
from guiEmbedder import generatePrompt, loadIndex

# risposta del chatbot
def answer(assistant_response):
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        # Simulate stream of response with milliseconds delay
        for character in assistant_response:
            full_response += character
            time.sleep(0.01)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + " ")
        message_placeholder.markdown(full_response)
        st.session_state.chat.append({"role": "assistant", "content": full_response})

def init():
    # Initialize chat history
    if "chat" not in st.session_state:
        st.session_state.chat = []
    # Initialize option parameter
    if "option" not in st.session_state:
        st.session_state.option = None
    if "option_prev" not in st.session_state:
        st.session_state.option_prev = None
    # Initialize upsert commands
    if "upsert_commands" not in st.session_state:
        st.session_state.upsert_commands = []
    if "emb" not in st.session_state:
        st.session_state.emb = None
    if "files" not in st.session_state:
        st.session_state.files = []
    if "logged_in" not in st.session_state: # Variabile di stato per tenere traccia dello stato di autenticazione
        st.session_state.logged_in = False

def guiUser():
    init()
    st.title("ChatSQL")
    st.subheader("Type your natural language query in the chat box below and press enter to get the corresponding SQL query.")
    if st.session_state.logged_in == False:
        st.divider()
        st.text("To access the technician menu, log in through the sidebar.")

    with st.sidebar:
        st.session_state.files=getFiles()
        st.session_state.option_prev = st.session_state.option
        st.session_state.option = st.selectbox('Data dictionary file:', st.session_state.files)
        guiAdmin()

    # Display chat messages from history on app rerun
    for message in st.session_state.chat:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # effettua gli upsert solo se il dizionario dati selezionato è cambiato rispetto a prima
    if (st.session_state.option != st.session_state.option_prev) and (st.session_state.option != None):
        answer(f"Switching data dictionary to \"{st.session_state.option}\"...")
        with st.spinner('Loading...'):
            loadIndex(st.session_state.option)
        answer(f"Data dictionary switched to \"{st.session_state.option}\" correctly.")

    if st.session_state.option is None:
        st.chat_input("A data dictionary has not been uploaded. Please log in as a technician to upload one.", disabled=True)
    else:
        st.chat_input(disabled=False)
        # React to user input
        if prompt := st.chat_input("Insert natural language query here"):
            # Display user message in chat message container
            with st.chat_message("user"):
                st.markdown(prompt)
            # Add user message to chat history
            st.session_state.chat.append({"role": "user", "content": prompt})

            # Display assistant response in chat message container
            answer("Generating SQL query...")

            with st.spinner('Loading whimsical wonders and dazzling delights into the digital playground of possibilities!'):
                t_start = 1.25
                t_end = 2.75
                sleep_duration = random.uniform(t_start, t_end)
                time.sleep(sleep_duration)
                #st.session_state.option
                st.code(generatePrompt(st.session_state.emb, prompt, st.session_state.option), language='markdown')
      
if __name__ == "__main__":
    guiUser()

#MVC
"""import random
import streamlit as st
import time

from guiAdmin import guiAdmin
from guiFileOperations import getFiles
from guiEmbedder import generatePrompt, loadIndex

class Model:
    def __init__(self):
        if "chat" not in st.session_state:
            self.chat = []
        if "option" not in st.session_state:
            self.option = None
        if "option_prev" not in st.session_state:
            self.option_prev = None
        if "upsert_commands" not in st.session_state:
            self.upsert_commands = []
        if "emb" not in st.session_state:
            self.emb = None
        if "files" not in st.session_state:
            self.files = []
        if "logged_in" not in st.session_state:
            self.logged_in = False
    
    def add_chat_message(self, role, content):
        self.chat.append({"role": role, "content": content})

class View:
    def __init__(self, model):
        self.model = model

    def render(self):
        st.title("ChatSQL")
        st.subheader("Type your natural language query in the chat box below and press enter to get the corresponding SQL query.")
        if not self.model.logged_in:
            st.divider()
            st.text("To access the technician menu, log in through the sidebar.")

        with st.sidebar:
            self.model.files = getFiles()
            self.model.option_prev = self.model.option
            self.model.option = st.selectbox('Data dictionary file:', self.model.files)
            #guiAdmin()

        # Display chat messages from history on app rerun
        for message in self.model.chat:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        '''     
        # effettua gli upsert solo se il dizionario dati selezionato è cambiato rispetto a prima
        if (self.model.option != self.model.option_prev) and (self.model.option is not None):
            self.answer(f"Switching data dictionary to \"{self.model.option}\"...")
            with st.spinner('Loading...'):
                loadIndex(self.model.option)
            self.answer(f"Data dictionary switched to \"{self.model.option}\" correctly.")

        if self.model.option is None:
            st.chat_input("A data dictionary has not been uploaded. Please log in as a technician to upload one.", disabled=True)
        else:
            st.chat_input(disabled=False)
            # React to user input
            if prompt := st.chat_input("Insert natural language query here"):
                # Display user message in chat message container
                with st.chat_message("user"):
                    st.markdown(prompt)
                # Add user message to chat history
                self.model.add_chat_message("user", prompt)

                # Display assistant response in chat message container
                self.answer("Generating SQL query...")

                with st.spinner('Loading whimsical wonders and dazzling delights into the digital playground of possibilities!'):
                    t_start = 1.25
                    t_end = 2.75
                    sleep_duration = random.uniform(t_start, t_end)
                    time.sleep(sleep_duration)
                    st.code(generatePrompt(self.model.emb, prompt, self.model.option), language='markdown')'''

    def answer(self, assistant_response):
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            # Simulate stream of response with milliseconds delay
            for character in assistant_response:
                full_response += character
                time.sleep(0.01)
                # Add a blinking cursor to simulate typing
                message_placeholder.markdown(full_response + " ")
            message_placeholder.markdown(full_response)
            self.model.add_chat_message("assistant", full_response)

class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def run(self):
        self.view.render()

def main():
    model = Model()
    view = View(model)
    controller = Controller(model, view)
    controller.run()

if __name__ == "__main__":
    main()"""

