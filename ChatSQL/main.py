from model import *
from controller import *
from widgets import *
from embedder import Embedder

if __name__ == "__main__":
    embedder = Embedder()
    dictionary_schema_verifier = JsonSchemaVerifierService()
    responseUser = ResponseUser(embedder)
    responseTechnician = ResponseTechnician(embedder)
    
    #modelli
    modelAut = AuthenticationService()
    modelSel = SelectionService() 
    modelUp = UploadService(embedder, dictionary_schema_verifier)
    modelDel = DeleteService()
    modelCha = ChatService(responseUser, responseTechnician)

    #controller
    controllerAut = AuthenticationController(modelAut, None) #aut
    controllerSel = SelectionController(modelSel, None) #selezione 
    controllerUp = UploadController(modelUp, None)
    controllerDel = DeleteController(modelDel, None)
    controllerLog = LogoutController(modelAut, None)
    controllerCha = ChatController(modelCha, modelSel, modelAut, None) # chatModel, selModel, authModel

    #view
    loginWidget = LoginWidget(controllerAut)
    logoutWidget = LogoutWidget(controllerLog)    
    selectWidget = SelectWidget(controllerSel)
    uploadWidget = UploadWidget(controllerUp)
    deleteWidget = DeleteWidget(selectWidget, controllerDel)
    chatWidget = ChatWidget(controllerCha)

    #controller imposto view
    controllerAut.setView(loginWidget) 
    controllerSel.setView(selectWidget)
    controllerUp.setView(uploadWidget)
    controllerDel.setView(deleteWidget)
    controllerLog.setView(logoutWidget)
    controllerCha.setView(chatWidget)
    

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if "chat" not in st.session_state:
        st.session_state.chat = []

    if st.session_state.logged_in == False:
        modelAut.setLoggedStatus(False)
        selectWidget.create()   #creazione widget selezione dizionario
        chatWidget.create()     #deve essere messa come ultimo widget (non primo)
        loginWidget.create()    #creazione widget login
        
    else:
        modelAut.setLoggedStatus(True)
        deleteWidget.create()   #creazione widget delete (crea in automatico anche la selezione diz)
        chatWidget.create()     #deve essere messa come ultimo widget (non primo)
        uploadWidget.create()   #creazione widget selezione dizionario
        logoutWidget.create()   #creazione widget selezione dizionario