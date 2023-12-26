import streamlit as st
import time
from guiFileOperations import getFiles

def answer(assistant_response):
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        # Simulate stream of response with milliseconds delay
        for character in assistant_response:
            full_response += character
            time.sleep(0.015)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
        st.session_state.chat.append({"role": "assistant", "content": full_response})

def admin():
    st.session_state.chat.append({"role": "assistant", "content": "Access the admin section"})

def exit():
    st.session_state.chat.append({"role": "assistant", "content": "Exit the program"})

def guiUser():
    st.title("ChatSQL")
    st.subheader("Type your natural language query in the chat box below and press enter to get the corresponding SQL query.")
    st.subheader("To access the admin section or exit the program, use the buttons on the sidebar.")

    with st.sidebar:
        st.button("Admin section", help="Access the admin section to upload or delete a data dictionary file",
                   on_click=admin, type="primary", use_container_width=False, disabled=False, key=None)
        files=getFiles()
        option = st.selectbox('Data dictionary file:', files)
        st.write("***")
        button_exit = st.button("Exit", help="Exit the program :(", on_click=exit, type="secondary", use_container_width=False, disabled=False, key=None)

    # Initialize chat history
    if "chat" not in st.session_state:
        st.session_state.chat = []

    # Display chat messages from history on app rerun
    for message in st.session_state.chat:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # React to user input
    if prompt := st.chat_input("Insert natural language query here"):
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Add user message to chat history
        st.session_state.chat.append({"role": "user", "content": prompt})

        # Display assistant response in chat message container
        if option != None:
            answer("Messaggio di prova. Dizionario dati selezionato: " + option)
        else:
            answer("Cannot answer without a data dictionary file. Please upload one using the admin section.")

if __name__ == "__main__":
    guiUser()