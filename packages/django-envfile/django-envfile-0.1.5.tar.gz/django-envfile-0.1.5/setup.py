import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='django-envfile',
    version='0.1.5',
    description='handle the environment variables as from a file in a simpler way.',
    url='https://github.com/josuedjh3/django-environment',
    author='Josuedjh Cayola',
    include_package_data=True,
    author_email='josuedjh456@gmail.com',
    license='GNU General Public License v3.0',
    packages=['envfile'],
    keywords=['django environment'],
    long_description=read('README.rst'),
    long_description_content_type='text/x-rst',

)