from controller import *

def main():
    controller = Controller()
    controller.change_state(controller._view.ask_user())
    print(controller._model.get_state())
    controller._view.technician_login()
    #print(controller._model.checkLogin("admin", "admin"))

if __name__ == "__main__":
    main()
