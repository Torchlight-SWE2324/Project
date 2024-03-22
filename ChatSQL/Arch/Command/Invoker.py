from Command import Command

class Invoker:
    def __init__(self):
        self._commands = {}

    def register_command(self, command_name: str, command: Command):
        self._commands[command_name] = command

    def execute_command(self, command_name: str):
        if command_name in self._commands:
            self._commands[command_name].execute()
        else:
            print(f"Command {command_name} not found")