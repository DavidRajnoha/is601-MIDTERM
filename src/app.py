"""
This module contains the App class which is responsible for running the application.
"""
import os

from src.command.command import ExitException
from src.command.command_handler import CommandHandler
import src.command.commands as commands_package
from dotenv import load_dotenv
import logging
import logging.config


class App:
    """
    App class is responsible for running the application.
    """
    def __init__(self):
        load_dotenv()
        self.configure_logging()
        self.command_handler = CommandHandler()


    def load_commands(self):
        """
        Loads the commands from the commands package.
        """
        self.command_handler.load_commands(commands_package)

    def configure_logging(self):
        """
        Configures the logging level.
        """
        os.makedirs("logs", exist_ok=True)
        if os.path.exists("logging.conf"):
            logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
            logging_configuration = "configured from logging.conf"
        else:
            logging.basicConfig(level=logging.DEBUG)
            logging_configuration = "configured with basicConfig"
        logging.info(f"Logging {logging_configuration}")

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
            except (ExitException, EOFError):
                logging.info("Exiting the application.")
                print("Exiting the application...")
                break


def main():
    app = App()
    app.run()

if __name__ == "__main__":
    main()