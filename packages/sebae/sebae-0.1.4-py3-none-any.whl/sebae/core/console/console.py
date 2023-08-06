from cleo import Command
from ..deployer import SUPPORT_TEMPLATE
from ..deployer import DeployerPybind11
import pathlib

class GreetCommand(Command):
    """
    Greets someone

    greet
        {name? : Who do you want to greet?}
        {--y|yell : If set, the task will yell in uppercase letters}
    """

    def handle(self):
        name = self.argument('name')

        if name:
            text = 'Hello {}'.format(name)
        else:
            text = 'Hello'

        if self.option('yell'):
            text = text.upper()

        self.line(text)



class InitCommand(Command):
    """
    Deploy template

    init
        {dir? : initialization directory, default './sebea_project'}
    """

    def select_template(self):
        promt_info = 'Select init schema:'
        mapping = {}
        for i, s in enumerate(SUPPORT_TEMPLATE):
            j = i + 1
            promt_info += f"\n{j}.{s}"
            mapping[str(j)] = s
        print(promt_info)
        name = None
        while not name in SUPPORT_TEMPLATE:
            in_str = input('selection ([q]uit):')
            if in_str == 'q':
                exit()
            try:
                name = mapping[in_str]
            except KeyError:
                if name in SUPPORT_TEMPLATE:
                    break
                print('Invalid input!')
        return name

    def handle(self):
        directory = self.argument('dir')


        if directory:
            p = pathlib.Path(directory).absolute()
            # print('info', p.stem, p.cwd().stem)
            if p.stem == p.cwd().stem:
                print('Initializing in current directory is not supported')
                exit()

        name = self.select_template()
        if not directory:
            directory = f'./{name}_project'

        pkg_name = input('Package name: ')
        author = input('Author: ')
        author_email = input('Author email: ')
        msg = f"Initializing {name} schema project {pkg_name}"
        self.line(msg)
        options = {
            'pkg_name': pkg_name,
            'author': author,
            'author_email': author_email
        }
        deployer = DeployerPybind11(directory)
        deployer.deploy(options)
        self.line('Finish!')
