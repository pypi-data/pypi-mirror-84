from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='costra',
    version='1.0',
    author='Petra Barancikova',
    author_email='barancikova@ufal.mff.cuni.cz',
    url='https://github.com/barancik/costra',
    packages=['costra'],
    package_dir={'costra': 'costra'},
    package_data={'costra':['data/data.tsv']},
    include_package_data=True,
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='embeddings evaluation',
    python_requires='>=3.5, <4',
    install_requires=['numpy'],

)
