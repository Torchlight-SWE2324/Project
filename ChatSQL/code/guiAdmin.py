import streamlit as st

from guiUtils import checkData

def logout():
    st.session_state.logged_in = False

def init():
    # Variabile di stato per tenere traccia dello stato di autenticazione
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False 

def main():
    init()
    st.header("Admin menu")

    # se l'utente non è loggato mostra il form di login
    if not st.session_state.logged_in:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        # Controllo del login
        if st.button("Login"):
            if checkData(username, password):
                st.success("Login successful!")
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Invalid username or password!")
    
    #se l'utente è loggato mostra il menu dell'admin
    else:
        uploaded_file = st.file_uploader("Upload new data dictionary file", accept_multiple_files=False, type="json")
        if uploaded_file is not None:
             #ora che ho il file cosa ne faccio?
            pass

        col1, col2 = st.columns(2)
        with col1:
            st.selectbox('Data dictionary file:', ["file1", "file2", "file3"]) #sostituire la lista con st.session_state.files
        with col2:
            st.button("Delete selected file", type="primary")
        
        #bottone per fare il logout
        st.write("***")
        st.button("Log out", type="secondary", on_click=logout)
                   

if __name__ == "__main__":
    main()