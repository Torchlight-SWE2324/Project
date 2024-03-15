from controller import *

def main():
    model = Model()
    view = View(model)
    controller = Controller(model, view)
    #per stabilire una relazione di osservazione tra il Model e la View,
    #e tra la View e il Controller. 
    model.attach(view) 
    view.attach(controller)

    #comandi per inizializzare la MAP
    controller.initialize_commands()
    view.initialize_commands()

    #da qui inizia il programma
    view.sezioneUtente()
   

if __name__ == "__main__":
    main()
