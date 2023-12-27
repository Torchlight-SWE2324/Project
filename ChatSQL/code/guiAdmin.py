import streamlit as st

from guiUtils import checkData
# Variabile di stato per tenere traccia dello stato di autenticazione
if "logged_in" not in st.session_state:
        st.session_state.logged_in = False 

def main():
    st.title("Admin Section")

    if not st.session_state.logged_in:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        # Controllo del login
        if st.button("Login"):
            if checkData(username, password):
                st.success("Login successful!")
                st.session_state.logged_in = True
                st.experimental_rerun()
            else:
                st.error("Invalid username or password!")

    else: 
        col1, col2, col3, col4 = st.columns(4)

        # Pulsanti per le opzioni
        if col1.button("Add a file"):
            st.session_state.option_selected = "Add a file"

        if col2.button("Delete a file"):
            st.session_state.option_selected = "Delete a file"

        if col3.button("Get all the files in the database"):
            st.session_state.option_selected = "Get all the files in the database"

        if col4.button("Leave the admin section"):
            st.session_state.option_selected = "Leave the admin section"
            st.warning("Leaving the admin section...")

        # Controlla quale opzione è stata selezionata
        if "option_selected" in st.session_state:
            option = st.session_state.option_selected

            if option == "Add a file":
                # Logica per "Add a file"
                pass
            elif option == "Delete a file":
                # Logica per "Delete a file"
                pass
            elif option == "Get all the files in the database":
                # Logica per "Get all the files in the database"
                pass
            elif option == "Leave the admin section":
                # Logica per "Leave the admin section"
                pass
                   

if __name__ == "__main__":
    main()