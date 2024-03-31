from model import *
#from view import *
from controller import *
from widgets import *

# Usage
if __name__ == "__main__":

    #modelli
    modelAut = ModelAuthentication()
    modelSel = ModelSelezione() 
    modelUp = ModelUpload() 
    modelDel = ModelDelete()
    modelCha = ModelChat()

    #controller
    controllerAut = ControllerAuthentication(modelAut, None, None) #aut e chat
    controllerSel = ControllerSelezione(modelSel, None, None) #selezione & chat 
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
    controllerAut._view1 = loginWidget
    controllerAut._view2 = chatWidget
    controllerSel._view1 = selectWidget
    controllerSel._view2 = chatWidget
    controllerUp._view = uploadWidget
    controllerDel._view = deleteWidget
    controllerLog._view = logoutWidget
    controllerCha._view = chatWidget


    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    st.session_state.logged_in = True #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


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