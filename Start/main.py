from model import *
from view import *
from controller import *

# Usage
if __name__ == "__main__":

    #modelli
    modelAut = ModelAuthentication()
    modelSel = ModelSelezione() 
    modelUp = ModelUpload() 
    modelDel = ModelDelete()

    #controller
    controllerAut = ControllerAuthentication(modelAut, None)
    controllerSel = ControllerSelezione(modelSel, None, None) #questo widget viene usato in 2 viste diverse
    controllerUp = ControllerUpload(modelUp, None)
    controllerDel = ControllerDelete(modelDel, None)
    controllerLog = controllerLogout(modelAut, None)

    #view
    viewUtente = ViewUtente(controllerAut, controllerSel)
    viewTecnico = ViewTecnico(controllerSel, controllerUp, controllerDel, controllerLog)
    #viewChat = View(controller)

    #creazione view dei controller
    controllerAut._view = viewUtente
    controllerSel._view1 = viewUtente
    controllerSel._view2 = viewTecnico
    controllerUp._view = viewTecnico
    controllerDel._view = viewTecnico
    controllerLog._view = viewTecnico

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in == False:
        viewUtente.display_data()
    else:
        viewTecnico.display_data()


#CHAT
    #modelChat = ModelAuthentication() #da rifare
    #controllerChat = ControllerTecnico(modelChat, None)  # Pass None temporarily
    #viewChat = ViewChat(controllerChat)
    #controllerChat._view = view  # Set view in the controller
    #viewChat.chatUtente()
