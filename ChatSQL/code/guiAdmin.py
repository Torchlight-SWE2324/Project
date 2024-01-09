import streamlit as st
from guiUtils import checkData
from guiFileOperations import deleteFile, uploadFile, getFiles

def logout():
    st.session_state.logged_in = False
    st.session_state.chat=[]
    st.success("Logout successfull!", icon="👍")
 
def delete():
    message=deleteFile(st.session_state.selected_file_admin) #filename_to_delete=st.session_state.selected_file_admin
    st.session_state.files=getFiles()
    st.success(message, icon="👍")

def upload():
    if st.session_state.uploaded_file is not None:
        message=uploadFile(st.session_state.uploaded_file.read(), st.session_state.uploaded_file.name)
        st.session_state.files=getFiles()
        st.warning(message)
    else:
        st.success("Choose a file to upload")

def init():
    if "logged_in" not in st.session_state: # Variabile di stato per tenere traccia dello stato di autenticazione
        st.session_state.logged_in = False
    if "selected_file_admin" not in st.session_state:
        st.session_state.selected_file_admin = ""
    if "files" not in st.session_state:
        st.session_state.files=getFiles()
    if "uploaded_file" not in st.session_state:
        st.session_state.uploaded_file=None

def guiAdmin():
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
                st.session_state.chat=[]
                st.rerun()
            else:
                st.error("Invalid username or password!")
    #se l'utente è loggato mostra il menu dell'admin
    else:
        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                st.session_state.uploaded_file = st.file_uploader("Upload new data dictionary file", accept_multiple_files=False, type="json")
            with col2:
                st.button("Upload file", type="primary", on_click=upload, disabled=st.session_state.uploaded_file==None)

        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                st.session_state.selected_file_admin = st.selectbox('Your data dictionary files', st.session_state.files)
            with col2:
                st.button("Delete selected file", type="primary", on_click=delete, disabled=st.session_state.selected_file_admin==None)
        st.write("***")
        st.button("Logout", type="secondary", on_click=logout)
                   

if __name__ == "__main__":
    guiAdmin()