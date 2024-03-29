from model import *
from view import *
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
    controllerAut = ControllerAuthentication(modelAut, None)
    controllerSel = ControllerSelezione(modelSel, None) 
    controllerUp = ControllerUpload(modelUp, None)
    controllerDel = ControllerDelete(modelDel, None)
    controllerLog = ControllerLogout(modelAut, None)
    controllerCha = ControllerChat(modelCha, None)

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False 


    if st.session_state.logged_in == False:
        # set model UtenteLoggato
        modelAut.setUtenteLoggato(False)
        #widget utente
        loginWidget = LoginWidget(controllerAut)
        selectWidget = SelectWidget(controllerSel)
        chatWidget = ChatWidget(controllerCha, controllerAut, controllerSel)
        
        #creazione widget utente nei controller
        controllerAut._view = loginWidget
        controllerSel._view1 = selectWidget
    else:
        # set model UtenteLoggato
        modelAut.setUtenteLoggato(True)
        #widget tecnico
        logoutWidget = LogoutWidget(controllerLog)
        selectWidget = SelectWidget(controllerSel)
        uploadWidget = UploadWidget(controllerUp)
        deleteWidget = DeleteWidget(selectWidget, controllerDel)
        chatWidget = ChatWidget(controllerCha, controllerAut, controllerSel)
        #creazione widget tecnico nei controller
        controllerUp._view = uploadWidget
        controllerDel._view = deleteWidget
        controllerLog._view = logoutWidget
    
    controllerCha._view = chatWidget



    #view
    #viewUtente = ViewUtente(controllerAut, controllerSel)
    #viewTecnico = ViewTecnico(controllerSel, controllerUp, controllerDel, controllerLog)

    #creazione widget nei controller
    # controllerAut._view = loginWidget
    # controllerSel._view1 = selectWidget
    # controllerSel._view2 = viewTecnico

    #if st.session_state.logged_in == False:
    #    modelAut.setUtenteLoggato(False)
    #    chatWidget.selectChatUtente()
    #else:
    #    modelAut.setUtenteLoggato(True)
    #    chatWidget.selectChatTecnico()

    #viewChat.display_data()


