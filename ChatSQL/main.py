from model import *
from controller import *
from widgets import *
from embedder import Embedder

if __name__ == "__main__":
    embedder = Embedder()
    dictionary_schema_verifier = JsonSchemaVerifierService()
    user_response = UserResponse(embedder)
    technician_response = TechnicianResponse(embedder)
    
    #modelli
    aut_model = AuthenticationService()
    sel_model = SelectionService() 
    up_model = UploadService(embedder, dictionary_schema_verifier)
    del_model = DeleteService()
    cha_model = ChatService(user_response, technician_response)

    #controller
    aut_controller = AuthenticationController(aut_model, None) #aut
    sel_controller = SelectionController(sel_model, None) #selezione 
    up_controller = UploadController(up_model, None)
    del_controller = DeleteController(del_model, None)
    log_controller = LogoutController(aut_model, None)
    cha_controller = ChatController(cha_model, sel_model, aut_model, None) # chatModel, selModel, authModel

    #view
    login_widget = LoginWidget(aut_controller)
    logout_widget = LogoutWidget(log_controller)    
    select_widget = SelectWidget(sel_controller)
    upload_widget = UploadWidget(up_controller)
    delete_widget = DeleteWidget(select_widget, del_controller)
    chat_widget = ChatWidget(cha_controller)

    #controller imposto view
    aut_controller.set_view(login_widget) 
    sel_controller.set_view(select_widget)
    up_controller.set_view(upload_widget)
    del_controller.set_view(delete_widget)
    log_controller.set_view(logout_widget)
    cha_controller.set_view(chat_widget)
    

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if "chat" not in st.session_state:
        st.session_state.chat = []

    if st.session_state.logged_in == False:
        aut_model.setLoggedStatus(False)
        select_widget.create()   #creazione widget selezione dizionario
        chat_widget.create()     #deve essere messa come ultimo widget (non primo)
        login_widget.create()    #creazione widget login
        
    else:
        aut_model.setLoggedStatus(True)
        delete_widget.create()   #creazione widget delete (crea in automatico anche la selezione diz)
        chat_widget.create()     #deve essere messa come ultimo widget (non primo)
        upload_widget.create()   #creazione widget selezione dizionario
        logout_widget.create()   #creazione widget selezione dizionario