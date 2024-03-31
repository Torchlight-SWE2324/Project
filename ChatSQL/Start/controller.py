import time
from model import *
from widgets import *

class ControllerAuthentication:
    def __init__(self, model, view1, view2):
        self._model = model
        self._view1 = view1
        self._view2 = view2

    def updateLoginData(self, username, password):
        if username == "" and password == "":
            self._view1.esitoMancante()
        else:
            esito = self._model.check_login(username, password)
            if esito:
                self._view1.esitoPositivo()
                time.sleep(.5)
                st.session_state.logged_in = True
                st.rerun()
            else:
                self._view1.esitoNegativo()

    def getLoggedState(self):
        return self._model.getUtenteLoggato()
        

class ControllerSelezione:
    def __init__(self, model, view1, view2):
        self._model = model
        self._view1 = view1 #selezione
        self._view2 = view2 #chat
        #return self._model.filesInDB()

    def getFiles(self):
        return self._model.filesInDB()  
    
    def setDizionario(self, dizionario):
        self._model.setDizionarioAttuale(dizionario)
#eliminare
    def getDizionario(self):
        return (self._model.getDizionarioAttuale())


class ControllerUpload:
    def __init__(self, model, view):
        self._model = model
        self._view = view

    def __dictionary_check(self, uploaded_file) -> str:
        if uploaded_file is None:
            return f'File was not loaded, repeat attempt.'

        uploaded_file_name = uploaded_file.name
        if self._model.get_loaded_dictionaries_number() > 3:
            return "App cannot contain more than 4 dictionaries."

        for dictionary in self._model.get_all_dictionaries_names():
            if uploaded_file_name == dictionary:
                return f'File with name "{uploaded_file_name}" already present.'

        return "successful_check"

    def updateFileData(self):
        uploaded_file = self._view.getFileUploaded()
        dictionary_check_result = self.__dictionary_check(uploaded_file)

        if dictionary_check_result == "successful_check":

            dictionary_content = uploaded_file.read()
            uploaded_file_content = dictionary_content.decode('utf-8')
            uploaded_file_name = uploaded_file.name

            dictionary_upload_result = self._model.upload_dictionary(uploaded_file_name, uploaded_file_content)
            print("dictionary_upload_result",dictionary_upload_result)
            if dictionary_upload_result == "upload_success":
                self._view.esitoPositivo(uploaded_file_name)
            else:
                self._view.esitoNegativo(dictionary_upload_result)

        else:
            self._view.esitoNegativo(dictionary_check_result)


class ControllerDelete:
    def __init__(self, model, view):
        self._model = model
        self._view = view  

    def operazioneDelete(self, file):
        self._model.deleteFile(file)
        esito = self._model.getEsitoFileEliminato()
        if esito:
            self._view.esitoPositivoEliminazione()
            time.sleep(.5)
            st.rerun()
        else:
            self._view.esitoNegativoEliminazione()


class ControllerLogout:
    def __init__(self, model, view):
        self._model = model
        self._view = view  
    
    def logout(self):
        st.session_state.logged_in = self._model.logout()
        self._view.logoutEsito()
        time.sleep(.5)
        st.rerun()


class ControllerChat:
    def __init__(self, model, view):
        self._model = model
        self._view = view

    def operazionePrompt(self, user_input, dizionario):
        self._model.generatePrompt(user_input, dizionario)
        messaggio = self._model.getResponse()
        self._view.showResponse(messaggio)

    def operazioneDebug(self, user_input, dizionario):
        self._model.generateDebug(user_input, dizionario)
        messaggio = self._model.getResponse()
        self._view.showResponse(messaggio)
    

    