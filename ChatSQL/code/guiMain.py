import streamlit as st
import time

#test admin button
def admin():
    st.session_state.option = "admin"
    content="Access the admin section"
    st.session_state.chat.append({"role": "user", "content": content})

#test user button
def user():
    st.session_state.option = "user"
    content="Interact with the database"
    st.session_state.chat.append({"role": "user", "content": content})

#test exit button
def exit():
    st.session_state.option = "exit"
    content="Exit the program"
    st.session_state.chat.append({"role": "user", "content": content})

def answer(assistant_response):
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        # Simulate stream of response with milliseconds delay
        for chunk in assistant_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
        st.session_state.chat.append({"role": "assistant", "content": full_response})


def mainGUI():
    st.title("Welcome to ChatSQL")

    # Initialize chat history
    if "chat" not in st.session_state:
        st.session_state.chat = []

    # Display chat messages from history on app rerun
    for message in st.session_state.chat:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    st.chat_input("Insert natural language query here", disabled=True)

    # Display assistant response in chat message container
    if "option" not in st.session_state:
        answer("What do you want to do?")
        #buttons for the menu
        st.button("Access the admin section", help="Access the admin section to upload or delete a data dictionary file",
                on_click=admin, type="secondary", use_container_width=False, disabled=False, key=None)
        st.button("Interact with the database", help="Query the database using natural language to get the corresponding SQL query",
                on_click=user, type="secondary", use_container_width=False, disabled=False, key=None)
        st.button("Exit the program", help="Exit the program :(",
                on_click=exit, type="secondary", use_container_width=False, disabled=False, key=None)
    elif st.session_state.option == "admin":
        answer("Admin section")
    elif st.session_state.option == "user":
        answer("User section")
    elif st.session_state.option == "exit":
        answer("Exit")

if __name__ == "__main__":
    mainGUI()