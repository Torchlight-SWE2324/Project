import time
from model import *
from view import *

class ControllerAuthentication:
    def __init__(self, model, view):
        self._model = model
        self._view = view

    def updateLoginData(self, username, password):
        esito = self._model.check_login(username, password)
        if esito:
            self._view.esitoPositivo()
            st.session_state.logged_in = True
            st.rerun()
        else:
            self._view.esitoNegativo()

class ControllerSelezione:
    def __init__(self, model, view1, view2):
        self._model = model
        self._view1 = view1
        self._view2 = view2
        #return self._model.filesInDB()

    def getFiles(self):
        return self._model.filesInDB()  

class ControllerUpload:
    def __init__(self, model, view):
        self._model = model
        self._view = view

    def updateFileData(self):
        file = self._view.getFileUploaded()
        esito = self._model.uploadFileModel(file)
        if esito:
            self._view.esitoPositivo()
            #self._view.
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

class controllerLogout():
    def __init__(self, model, view):
        self._model = model
        self._view = view  
    
    def logout(self):
        st.session_state.logged_in = self._model.logout()
        self._view.logoutEsito()
        time.sleep(.5)
        st.rerun()
