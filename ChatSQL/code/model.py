# model.py

class ChatSession:
    def __init__(self):
        self.chat_history = []
        self.option = None
        self.option_prev = None
        self.upsert_commands = []
        self.emb = None
        self.files = []
        self.logged_in = False

    def switch_data_dictionary(self, new_option):
        self.option_prev = self.option
        self.option = new_option

    # You can add more methods related to managing chat session data here
