import keyboard
import os
import psutil
import random
import streamlit as st
import time
from guiAdmin import guiAdmin
from guiFileOperations import getFiles
from guiEmbedder import generatePromptUser, loadIndex


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
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
        st.session_state.chat.append({"role": "assistant", "content": full_response})


def exit():
    st.session_state.chat.append({"role": "assistant", "content": "Exiting the program..."})
    # Delay for user experience
    time.sleep(1)
    # Close streamlit browser tab
    keyboard.press_and_release('ctrl+w')
    # Terminate streamlit python process
    pid = os.getpid()
    p = psutil.Process(pid)
    p.terminate()

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



def guiUser():
    init()
    st.title("ChatSQL")
    st.subheader("Type your natural language query in the chat box below and press enter to get the corresponding SQL query.")
    st.divider()
    st.text("To access the admin section or exit the program, use the buttons on the sidebar.")

    with st.sidebar:
        st.session_state.files=getFiles()
        st.session_state.option_prev = st.session_state.option
        st.session_state.option = st.selectbox('Data dictionary file:', st.session_state.files)
        st.write("***")
        st.button("Exit", help="Exit the program :(", on_click=exit, type="secondary", use_container_width=False, disabled=False, key=None)

    # Display chat messages from history on app rerun
    for message in st.session_state.chat:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # effettua gli upsert solo se il dizionario dati selezionato è cambiato rispetto a prima
    if (st.session_state.option != st.session_state.option_prev) and (st.session_state.option != None):
        answer(f"Switching data dictionary to \"{st.session_state.option}\"...")
        with st.spinner('Loading...'):
            loadIndex(st.session_state.option)
        answer(f"Data dictionary switched to \"{st.session_state.option}\" correctly 👍")
    
    # React to user input
    if prompt := st.chat_input("Insert natural language query here"):
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Add user message to chat history
        st.session_state.chat.append({"role": "user", "content": prompt})

        # Display assistant response in chat message container
        if st.session_state.option != None:
            answer("Generating SQL query...")

            with st.spinner('Loading whimsical wonders and dazzling delights into the digital playground of possibilities!'):
                t_start = 1.25
                t_end = 2.75
                sleep_duration = random.uniform(t_start, t_end)
                time.sleep(sleep_duration)
                st.code(generatePromptUser(st.session_state.emb, prompt), language='markdown')
        else:
            answer("Cannot answer without a data dictionary file. Please upload one using the admin section.")


if __name__ == "__main__":
    guiUser()