from .console import GreetCommand, InitCommand
from cleo import Application

application = Application()
application.add(GreetCommand())
application.add(InitCommand())


def main():
    application.run()
