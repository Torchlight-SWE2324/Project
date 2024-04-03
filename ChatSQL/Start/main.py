from model import *
#from view import *
from controller import *
from widgets import *
from embedder import Embedder

# Usage
if __name__ == "__main__":

    embedder = Embedder()
    dictionary_schema_verifier = JsonSchemaVerifierService()

    #modelli
    modelAut = ModelAuthentication()
    modelSel = ModelSelezione() 
    modelUp = ModelUpload(embedder, dictionary_schema_verifier)
    modelDel = ModelDelete()
    modelCha = ModelChat()

    #controller
    controllerAut = ControllerAuthentication(modelAut, None) #aut
    controllerSel = ControllerSelezione(modelSel, None) #selezione 
    controllerUp = ControllerUpload(modelUp, None)
    controllerDel = ControllerDelete(modelDel, None)
    controllerLog = ControllerLogout(modelAut, None)
    controllerCha = ControllerChat(modelCha, None)

    #view
    loginWidget = LoginWidget(controllerAut)
    logoutWidget = LogoutWidget(controllerLog)    
    selectWidget = SelectWidget(controllerSel)
    uploadWidget = UploadWidget(controllerUp)
    deleteWidget = DeleteWidget(selectWidget, controllerDel)
    chatWidget = ChatWidget(controllerCha, controllerSel, controllerAut)

    #controller imposto view
    controllerAut._view = loginWidget
    controllerSel._view = selectWidget
    controllerUp._view = uploadWidget
    controllerDel._view = deleteWidget
    controllerLog._view = logoutWidget
    controllerCha._view = chatWidget


    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False


    if st.session_state.logged_in == False:
        modelAut.setUtenteLoggato(False)
        selectWidget.create() #creazione widget selezione dizionario
        chatWidget.create() #deve essere messa come ultimo widget (non primo)
        loginWidget.create()  #creazione widget login
        
    else:
        modelAut.setUtenteLoggato(True)
        deleteWidget.create()   #creazione widget delete (crea in automatico anche la selezione diz)
        chatWidget.create() #deve essere messa come ultimo widget (non primo)
        uploadWidget.create()   #creazione widget selezione dizionario
        logoutWidget.create()   #creazione widget selezione dizionario