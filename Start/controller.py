import time
from model import *
from view import *

class Controller:
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


class ControllerTecnico:
    def __init__(self, model, view):
        self._model = model
        self._view = view
        self._modelDelete = ModelDelete()

    def updateFileData(self):
        file = self._view.getFileUploaded()
        esito = self._model.uploadFileModel(file)
        if esito:
            self._view.esitoPositivo()
            #self._view.
        else:
            self._view.esitoNegativo()

    def getFiles(self):
        return self._modelDelete.getFiles()
    
    def operazioneDelete(self, file):
        self._modelDelete.deleteFile(file)
        esito = self._modelDelete.getEsitoFileEliminato()
        if esito:
            self._view.esitoPositivoEliminazione()
            time.sleep(.5)
            st.rerun()
        else:
            self._view.esitoNegativoEliminazione()


