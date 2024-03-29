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

    def updateFileData(self):
        file = self._view.getFileUploaded()
        esito = self._model.uploadFileModel(file)
        if esito:
            self._view.esitoPositivo()
        else:
            self._view.esitoNegativo()


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
    

    