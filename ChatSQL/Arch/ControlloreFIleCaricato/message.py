from abc import ABC, abstractmethod
import streamlit as st

class StreamlitMessenger(ABC):
    @abstractmethod
    def success_message(self, message):
        pass

    @abstractmethod
    def error_message(self, message):
        pass

    @abstractmethod
    def warning_message(self, message):
        pass

class StreamlitMessengerImplementation(StreamlitMessenger):
    def success_message(self, message):
        st.success(message)

    def error_message(self, message):
        st.error(message)

    def warning_message(self, message):
        st.warning(message)

if __name__ == "__main__":
    messenger = StreamlitMessengerImplementation()
    messenger.success_message("Operation successful!")
    messenger.error_message("An error occurred!")
    messenger.warning_message("This is a warning!")
