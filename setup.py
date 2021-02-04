from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
# with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
#     long_description = f.read()

setup(
    name='posture_detector',
    version='0.0.1',
    packages=['posture_detector'],
    package_dir={'': 'posture_detector'},
    url='',
    license='',
    author='gabriel',
    author_email='',
    description='helo',
    # long_description=long_description,
    # long_description_content_type='text/markdown'
)
