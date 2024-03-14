from controller import *

def main():
    model = Model()
    view = View(model)
    controller = Controller(model, view)

    model.attach(view)
    view.attach(controller)

    view.technician_login()


if __name__ == "__main__":
    main()
