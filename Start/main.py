#from model import *
from authentication import *
from view import *
from controller import *

modelU = AuthenticationCSV()
controllerU = ControllerUtente()
viewU = ViewUtente()
controllerU.initialize(modelU, viewU)
viewU.initialize(controllerU)

""""
if __name__ == "__main__":



    


    # Aggiornamento della vista
    #controllerU.login()
"""
