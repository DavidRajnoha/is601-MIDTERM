"""
This module contains the App class which is responsible for running the application.
"""
import os

from dotenv import load_dotenv
import logging
import logging.config

from src.command.command import ExitException
from src.command.command_handler import CommandHandler
import src.command.commands as commands_package
from src.core.application_context import ApplicationContext
from src.core.logging_configurator import LoggingConfigurator


class App:
    """
    App class is responsible for running the application.
    """
    def __init__(self):
        load_dotenv()
        LoggingConfigurator.configure()

        self.setup_dependencies()
        self.command_handler = CommandHandler()


    def load_commands(self):
        """
        Loads the commands from the commands package.
        """
        self.command_handler.load_commands(commands_package)

    def setup_dependencies(self):
        """
        Configures the application dependencies.
        """
        repository_type = os.getenv("REPOSITORY_TYPE", "csv")
        file_path = os.getenv("REPOSITORY_DATA_PATH", "data/calculations.csv")
        ApplicationContext.configure_repositories(repository_type, file_path)


    def run(self):
        """
        Runs the application loop.
        """
        self.load_commands()
        logging.info("Starting the application.")
        while True:
            try:
                command = input("Enter a command: ")
                self.command_handler.handle(command)
            except (ExitException, EOFError, KeyboardInterrupt):
                logging.info("Exiting the application.")
                print("\nExiting the application...")
                break


def main():
    app = App()
    app.run()

if __name__ == "__main__":
    main()