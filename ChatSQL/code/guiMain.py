import streamlit as st
import time

#test admin button
def admin():
    content="Access the admin section"
    st.session_state.chat.append({"role": "user", "content": content})

#test user button
def user():
    content="Interact with the database"
    st.session_state.chat.append({"role": "user", "content": content})

#test exit button
def exit():
    content="Exit the program"
    st.session_state.chat.append({"role": "user", "content": content})

def main():
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
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        assistant_response = "What do you want to do?"
        # Simulate stream of response with milliseconds delay
        for chunk in assistant_response.split():
            full_response += chunk + " "
            time.sleep(0.04)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
        #selected = option_menu(None, ["Access the admin section", 'Interact with the database', 'Exit the program'], 
        #    icons=['gear', 'keyboard', 'x-circle'], default_index=0, on_change=callback, key='main-menu')
        st.button("Access the admin section", help="Access the admin section to upload or delete a data dictionary file",
                on_click=admin, type="secondary", use_container_width=False, disabled=False, key=None)
        st.button("Interact with the database", help="Query the database using natural language to get the corresponding SQL query",
                on_click=user, type="secondary", use_container_width=False, disabled=False, key=None)
        st.button("Exit the program", help="Exit the program :(",
                on_click=exit, type="secondary", use_container_width=False, disabled=False, key=None)
    st.session_state.chat.append({"role": "assistant", "content": full_response})

if __name__ == "__main__":
    main()