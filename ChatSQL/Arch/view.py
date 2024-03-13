import streamlit as st
import time
import random

class Model:
    def __init__(self):
        self.observers = []

    def generate_sql_query(self, prompt, data_dictionary):
        # Your SQL query generation logic here
        return generatePrompt(self.emb, prompt, data_dictionary)

    def add_observer(self, observer):
        self.observers.append(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer.update()

class View:
    def __init__(self, model):
        self.model = model
        self.model.add_observer(self)

    def update(self):
        # Update view when notified by the model
        st.code(self.model.generated_sql_query, language='markdown')

    def render(self):
        st.title("ChatSQL")
        st.subheader("Type your natural language query in the chat box below and press enter to get the corresponding SQL query.")
        if not st.session_state.logged_in:
            st.divider()
            st.text("To access the technician menu, log in through the sidebar.")

        with st.sidebar:
            st.session_state.files = getFiles()
            st.session_state.option_prev = st.session_state.option
            st.session_state.option = st.selectbox('Data dictionary file:', st.session_state.files)
            guiAdmin()

        # Display chat messages from history on app rerun
        for message in st.session_state.chat:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Effettua gli upsert solo se il dizionario dati selezionato è cambiato rispetto a prima
        if (st.session_state.option != st.session_state.option_prev) and (st.session_state.option is not None):
            answer(f"Switching data dictionary to \"{st.session_state.option}\"...")
            with st.spinner('Loading...'):
                loadIndex(st.session_state.option)
            answer(f"Data dictionary switched to \"{st.session_state.option}\" correctly.")

        if st.session_state.option is None:
            st.chat_input("A data dictionary has not been uploaded. Please log in as a technician to upload one.", disabled=True)
        else:
            st.chat_input(disabled=False)
            # React to user input
            if prompt := st.chat_input("Insert natural language query here"):
                # Display user message in chat message container
                with st.chat_message("user"):
                    st.markdown(prompt)
                # Add user message to chat history
                st.session_state.chat.append({"role": "user", "content": prompt})

                # Display assistant response in chat message container
                answer("Generating SQL query...")

                with st.spinner('Loading whimsical wonders and dazzling delights into the digital playground of possibilities!'):
                    t_start = 1.25
                    t_end = 2.75
                    sleep_duration = random.uniform(t_start, t_end)
                    time.sleep(sleep_duration)
                    generated_sql_query = self.model.generate_sql_query(prompt, st.session_state.option)
                    self.model.generated_sql_query = generated_sql_query  # Update model's generated SQL query
                    self.update()  # Notify view to update with the generated SQL query

class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def run(self):
        self.view.render()

def main():
    model = Model()
    view = View(model)
    controller = Controller(model, view)
    controller.run()

if __name__ == "__main__":
    main()
