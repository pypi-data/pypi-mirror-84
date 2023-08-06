import os
import sys

from pypigeonhole_build.dependency import Dependency, INSTALL, DEV, PIP
from pypigeonhole_build.conda_translator import CONDA
import pypigeonhole_build.pip_translator as pip_translator
import pypigeonhole_build.app_version_control as vc
import pypigeonhole_build.dep_manager as dep_manager

curr_dir = os.path.dirname(os.path.realpath(__file__))
__app_name = os.path.basename(curr_dir).replace('_', '-')

# ##############################################################################
# These are the settings for the app.
# ##############################################################################
# 3 digits, major, minor, patch. Keep this line unique.
__app_version = "0.0.3"
vc.bump_version = vc.bump_version_upto10

top_pkg = __app_name.replace('-', '_')
CONDA.env = top_pkg  # _ is easier to copy the word
CONDA.channels = ['defaults', 'psilons', 'psilons-local']  # update channels, if needed.

dependent_libs = [
    # your dependencies here
    # your dependencies here
    Dependency(name='pycryptodome', version='==3.9.8', scope=INSTALL, installer=CONDA),
    Dependency(name='pyyaml', version='==5.3.1', scope=INSTALL, installer=CONDA),
    Dependency(name='pypigeonhole-simple-utils', scope=INSTALL, installer=CONDA),

    Dependency(name='pypigeonhole-build', installer=CONDA),  # default scope DEV, latest version

    Dependency(name='python', version='>=3.6', scope=INSTALL, installer=CONDA),
    Dependency(name='pip', installer=CONDA),  # Without this Conda complains
    Dependency(name='coverage', version='==5.3', installer=CONDA, desc='test coverage'),  # DEV
    Dependency(name='pipdeptree', scope=DEV, installer=PIP),
    Dependency(name='coverage-badge'),  # default to DEV and PIP automatically.
    Dependency(name='twine'),  # uploading to pypi
    Dependency(name='conda-build', installer=CONDA),
    Dependency(name='conda-verify', installer=CONDA),
    Dependency(name='anaconda-client', installer=CONDA),
]

# ##############################################################################
# No need change below, unless you want to customize
# ##############################################################################

# used by setup.py, hide details - how we compute these values.
install_required = pip_translator.get_install_required(dependent_libs)

test_required = pip_translator.get_test_required(dependent_libs)

python_required = pip_translator.get_python_requires(dependent_libs)


def app_name():
    return __app_name


def app_version():
    return __app_version


if __name__ == "__main__":
    dep_manager.main(sys.argv, dependent_libs)
