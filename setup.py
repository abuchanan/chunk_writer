from distutils.core import setup

import chunk_writer


setup(
    name='chunk_writer',
    description='TODO',
    long_description=open('README.md').read(),
    version=chunk_writer.__version__,
    author='Alex Buchanan',
    author_email='buchanae@gmail.com',
    license='BSD',
    py_modules=['chunk_writer']
)
