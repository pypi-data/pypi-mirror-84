import pathlib
import os


SUPPORT_TEMPLATE = [
    'pybind11'
]


TEMPLATES_DIR = pathlib.Path(__file__).parent.joinpath('../../templates')


def copy(src: pathlib.Path, dst: pathlib.Path):
    with src.open('r') as f:
        file_content = f.read()
    with dst.open('w') as f:
        f.write(file_content)


def copy_and_transform(src: pathlib.Path, dst: pathlib.Path, transformer):
    with src.open('r') as f:
        file_content = f.read()
    file_content = transformer(file_content)
    with dst.open('w') as f:
        f.write(file_content)


class Deployer:
    def __init__(self, base_dir):
        self.base_dir = pathlib.Path(base_dir)

    def deploy(self, options=None):
        # TODO: Exception handling
        try:
            os.mkdir(self.base_dir)
        except:
            print('Unsupport init directory:', self.base_dir)