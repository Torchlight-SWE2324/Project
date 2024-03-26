from model import *
from view import *
from controller import *

# Usage
if __name__ == "__main__":
    # Create model, view, and controller
    model = Model()
    controller = Controller(model, None)  # Pass None temporarily
    view = View(controller)
    controller._view = view  # Set view in the controller

    #UPLOAD
    modelUpload = ModelUpload()
    controllerTecnico = ControllerTecnico(modelUpload, None)  # Pass None temporarily
    viewTecnico = ViewTecnico(controllerTecnico)
    controllerTecnico._view = viewTecnico

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    print("MAIN")
    if st.session_state.logged_in == False:
        view.display_data()
    else:
        viewTecnico.display_data()

    #DELETE
    modelDelete = ModelDelete()
    controllerTecnico = ControllerTecnico(modelDelete, None)  # Pass None temporarily
    viewTecnico = ViewTecnico(controllerTecnico)
    controllerTecnico._view = viewTecnico

#CHAT
    modelChat = Model() #da rifare
    controllerChat = ControllerTecnico(modelChat, None)  # Pass None temporarily
    viewChat = ViewChat(controllerChat)
    controllerChat._view = view  # Set view in the controller
    viewChat.chatUtente()