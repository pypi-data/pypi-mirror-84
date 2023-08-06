from setuptools import setup, find_packages
import pathlib
import sys
import os.path
from os.path import dirname

# To add source folder to the path, otherwise below import would fail.
src_path = os.path.join(dirname(__file__), 'src')
sys.path.append(src_path)

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

import pypigeonhole_config.app_setup as app_setup

# If this is needed during dev by others, cd this folder and run pip install -e .
# This is reusable in normal cases.
setup(name=app_setup.app_name(),
      version=app_setup.app_version(),
      description='Python YAML based Configuration',
      url='https://github.com/psilons/pypigeonhole-config',

      author='psilons',
      author_email='psilons.quanta@gmail.com',

      long_description=README,
      long_description_content_type="text/markdown",
      license="MIT",

      package_dir={'': 'src'},
      packages=find_packages("src", exclude=["test"]),

      python_requires=app_setup.python_required,

      install_requires=app_setup.install_required,

      tests_require=app_setup.test_required,

      extras_require={},
      )
