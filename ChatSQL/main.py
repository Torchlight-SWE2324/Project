from model import AuthenticationService, SelectionService, UploadService, DeleteService, ChatService, JsonSchemaVerifierService, UserResponse, TechnicianResponse
from controller import AuthenticationController, SelectionController, UploadController, DeleteController, LogoutController, ChatController
from widgets import LoginWidget, LogoutWidget, SelectWidget, UploadWidget, DeleteWidget, ChatWidget, st
from embedder import Embedder

if __name__ == "__main__":

    st.set_page_config(
    page_title="ChatSQL - torchlight",
    page_icon= ":flashlight",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={
        'Get Help': 'https://github.com/Torchlight-SWE2324/Documentazione',
        'Report a bug': 'mailto:torchlight.swe2324@outlook.com',
        'About': "# Generate a prompt that once given to any LLM, will translate your natural language query into the equivalent SQL one!"
    }
)

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
    aut_controller = AuthenticationController(aut_model, None)
    sel_controller = SelectionController(sel_model, None)
    up_controller = UploadController(up_model, None)
    del_controller = DeleteController(del_model, None)
    log_controller = LogoutController(aut_model, None)
    cha_controller = ChatController(cha_model, sel_model, aut_model, None)

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

    if st.session_state.logged_in is False:
        aut_model.set_logged_status(False)
        select_widget.create()
        chat_widget.create()
        login_widget.create()

    else:
        aut_model.set_logged_status(True)
        delete_widget.create()
        chat_widget.create()
        upload_widget.create()
        logout_widget.create()
