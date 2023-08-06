import os
import sys
from distutils.command.register import register as register_orig
from distutils.command.upload import upload as upload_orig

from setuptools import find_packages, setup

if sys.version_info < (3, 0):
    from io import open

try:
    # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError:
    # for pip <= 9.0.3
    from pip.req import parse_requirements

project_path = os.path.dirname(__file__)


class register(register_orig):
    def _get_rc_file(self):
        return os.path.join('.', '.pypirc')


class upload(upload_orig):
    def _get_rc_file(self):
        return os.path.join('.', '.pypirc')


def load_requirements():
    fname = os.path.join(project_path, 'requirements.txt')
    reqs = parse_requirements(fname, session=False)
    requirements = []
    try:
        requirements = [str(ir.req) for ir in reqs]
    except Exception as e:
        print(e)
        requirements = [str(ir.requirement) for ir in reqs]
    return requirements


def load_description():
    fname = os.path.join(project_path, 'README.md')
    with open(fname, encoding='utf-8') as f:
        return f.read()


def load_version():
    fname = os.path.join(project_path, 'pubsub/version.py')
    with open(fname, 'r', encoding='utf-8') as f:
        exec(compile(f.read(), fname, 'exec'))
    return locals()['__version__']


setup(name='aa-pubsub',
      version=load_version(),
      py_modules=['pubsub.publisher', 'pubsub.subscriber', 'pubsub.camera'],
      author='shuyuanhao',
      author_email='shuyuanhao@cetiti.com',
      keywords='redis publisher&subscriber',
      url='https://git.d.com/hik-aa-robots/robots-intelligent-systems/pubsub',
      description='a publish&subscrib toolkit',
      packages=find_packages(),
      install_requires=load_requirements(),
      entry_points={'console_scripts': ['camera_redis=app:main']},
      long_description=load_description(),
      long_description_content_type='text/markdown',
      classifiers=[
          'Development Status :: 3 - Alpha', 'Topic :: Utilities',
          'License :: OSI Approved :: GNU General Public License (GPL)'
      ],
      cmdclass={
          'register': register,
          'upload': upload,
      },
      zip_safe=False)
