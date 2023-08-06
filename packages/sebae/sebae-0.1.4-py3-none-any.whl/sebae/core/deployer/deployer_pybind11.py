import pathlib
import os
from .base import Deployer
from .base import TEMPLATES_DIR
from .base import copy
from .base import copy_and_transform
import shutil
import pybind11


def gen_cfg(base_dir, metadata, options):
    default_meta_data = {
        "name": metadata['pkg_name'],
        "author": metadata['author'],
        "author_email": metadata['author_email'],
        "version": "0.0.1",
    }
    default_options = {
        "packages": "find:",
        "python_requires": ">= 3.6"
    }
    file_content = ""
    file_content += "[metadata]\n"
    for k, v in default_meta_data.items():
        file_content += f"{k} = {v}\n"

    file_content += "\n[options]\n"
    file_content += "package_dir=\n\t=pkg\n"
    for k, v in default_options.items():
        file_content += f"{k} = {v}\n"
    file_content += "\n[options.packages.find]\n"
    file_content += "\nwhere=pkg\n"


    with base_dir.joinpath('setup.cfg').open('w') as f:
        f.write(file_content)


def gen_entrypoint(main_path):
    with main_path.joinpath('__init__.py').open('w') as f:
        f.write('from .binding import *\n')


class DeployerPybind11(Deployer):
    def __init__(self, base_dir):
        super().__init__(base_dir)

    def deploy(self, options):
        super().deploy()
        src_path = self.base_dir.joinpath('src')
        header_path = self.base_dir.joinpath('include')

        os.mkdir(src_path)
        os.mkdir(header_path)
        main_path = self.base_dir.joinpath('pkg')
        os.mkdir(main_path)
        main_path = main_path.joinpath(options["pkg_name"])
        os.mkdir(main_path)
        gen_entrypoint(main_path)

        template_dir = TEMPLATES_DIR.joinpath('pybind11')
        common_dir = TEMPLATES_DIR.joinpath('common')

        copy(template_dir.joinpath('algo.h'), header_path.joinpath('algo.h'))
        copy(template_dir.joinpath('main.cc'), src_path.joinpath('main.cc'))

        def trans_binding(file_content):
            return file_content.format(**{
                'project_name': options['pkg_name'],
                'module_name': 'binding'
            })
        copy_and_transform(
            template_dir.joinpath('binding.cc'),
            src_path.joinpath('binding.cc'),
            trans_binding
        )

        def trans_cmakelists(file_content):
            return file_content.format(**{
                'project_name': options['pkg_name'],
                'module_name': 'binding'
            })
        copy_and_transform(
            template_dir.joinpath('CMakeLists.txt'),
            self.base_dir.joinpath('CMakeLists.txt'),
            trans_cmakelists
        )

        def trans_setuppy(file_content):
            content = 'if __name__ == "__main__":\n'
            content += '    setup(\n'
            content += f'        ext_modules=[CMakeExtension("{options["pkg_name"]}.binding")],\n'
            content += f'        cmdclass=dict(build_ext=CMakeBuild),\n'
            content += '    )'
            return file_content + content
        copy_and_transform(template_dir.joinpath('setup.py'), self.base_dir.joinpath('setup.py'), trans_setuppy)

        copy(common_dir.joinpath('pyproject.toml'), self.base_dir.joinpath('pyproject.toml'))

        shutil.copytree(pybind11.get_include(), self.base_dir.joinpath('3rd/pybind11/include'))
        shutil.copy(template_dir.joinpath('pybind11/CMakeLists.txt'),
                    self.base_dir.joinpath('3rd/pybind11/CMakeLists.txt'))
        shutil.copytree(template_dir.joinpath('pybind11/tools'),
                    self.base_dir.joinpath('3rd/pybind11/tools'))
        gen_cfg(self.base_dir, options, {})






