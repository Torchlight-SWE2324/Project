import streamlit as st
import time
from guiFileOperations import getFiles
from guiUtils import getPath, generateEmbeddingUpsert
from guiEmbedder import generatePrompt


#genera gli upsert solo quando il dizionario dati viene cambiato
def generateUpsert():
    if st.session_state.option != None:
        st.session_state.chat.append({"role": "assistant", "content": "Effettua gli upsert relativi al dizionario dati selezionato: "+st.session_state.option})
        #effettua gli upsert relativi al dizionario appena selezionato
        jsonFilePath=getPath(st.session_state.option)
        if jsonFilePath == "Error":
            st.session_state.chat.append({"role": "assistant", "content": "Error: file path not valid"})
        else:
            st.session_state.upsert_commands=generateEmbeddingUpsert(jsonFilePath)


def answer(assistant_response):
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        # Simulate stream of response with milliseconds delay
        for character in assistant_response:
            full_response += character
            time.sleep(0.014)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
        st.session_state.chat.append({"role": "assistant", "content": full_response})

def admin():
    st.session_state.chat.append({"role": "assistant", "content": "Access the admin section"})

def exit():
    st.session_state.chat.append({"role": "assistant", "content": "Exit the program"})

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

def guiUser():
    init()

    st.title("ChatSQL")
    st.subheader("Type your natural language query in the chat box below and press enter to get the corresponding SQL query.")
    st.subheader("To access the admin section or exit the program, use the buttons on the sidebar.")

    with st.sidebar:
        st.button("Admin section", help="Access the admin section to upload or delete a data dictionary file",
                   on_click=admin, type="primary", use_container_width=False, disabled=False, key=None)
        files=getFiles()
        st.session_state.option_prev = st.session_state.option
        st.session_state.option = st.selectbox('Data dictionary file:', files)
        #effettua gli upsert solo se il dizionario dati selezionato è cambiato rispetto a prima
        if st.session_state.option != st.session_state.option_prev:
            generateUpsert()
        st.write("***")
        st.button("Exit", help="Exit the program :(", on_click=exit, type="secondary", use_container_width=False, disabled=False, key=None)

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
        if st.session_state.option != None:
            #answer("Messaggio di prova. Dizionario dati selezionato: " + st.session_state.option)
            answer(generatePrompt(st.session_state.upsert_commands, prompt))
        else:
            answer("Cannot answer without a data dictionary file. Please upload one using the admin section.")

if __name__ == "__main__":
    guiUser()