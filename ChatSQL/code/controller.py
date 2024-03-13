# controller.py

import random
import time
import model
import view
from guiEmbedder import generatePrompt, loadIndex
from guiFileOperations import getFiles
from guiAdmin import guiAdmin

def answer(assistant_response):
    message_placeholder = view.display_chat_message("assistant", "")
    full_response = ""
    for character in assistant_response:
        full_response += character
        time.sleep(0.01)
        message_placeholder.markdown(full_response + " ")
    message_placeholder.markdown(full_response)

def switch_data_dictionary(option):
    model.switch_data_dictionary(option)
    answer(f"Switching data dictionary to \"{option}\"...")
    view.display_spinner('Loading...')
    loadIndex(option)
    answer(f"Data dictionary switched to \"{option}\" correctly.")

def handle_user_input(prompt):
    view.display_chat_message("user", prompt)
    model.chat_history.append({"role": "user", "content": prompt})
    answer("Generating SQL query...")
    view.display_spinner('Loading whimsical wonders and dazzling delights into the digital playground of possibilities!')
    sleep_duration = random.uniform(1.25, 2.75)
    time.sleep(sleep_duration)
    view.display_code(generatePrompt(model.emb, prompt, model.option))

def initialize():
    model.init()  # Initialize the model
    view.st.title("ChatSQL")
    view.st.subheader("Type your natural language query in the chat box below and press enter to get the corresponding SQL query.")

if __name__ == "__main__":
    initialize()
    if not model.logged_in:
        view.st.divider()
        view.st.text("To access the technician menu, log in through the sidebar.")

    with view.st.sidebar:
        model.files = getFiles()
        model.option_prev = model.option
        model.option = view.st.selectbox('Data dictionary file:', model.files)
        guiAdmin()

    for message in model.chat_history:
        view.display_chat_message(message["role"], message["content"])

    if model.option != model.option_prev and model.option is not None:
        switch_data_dictionary(model.option)

    if model.option is None:
        view.display_chat_input("A data dictionary has not been uploaded. Please log in as a technician to upload one.", disabled=True)
    else:
        view.display_chat_input("Insert natural language query here", disabled=False)
        if prompt := view.display_chat_input("Insert natural language query here"):
            handle_user_input(prompt)
