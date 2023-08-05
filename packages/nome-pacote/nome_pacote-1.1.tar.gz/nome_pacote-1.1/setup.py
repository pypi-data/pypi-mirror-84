from setuptools import setup, find_packages
from pathlib import Path

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='nome_pacote',
    version=1.1,
    description='Descrição curta',
    long_description=Path('README.md').read_text(),
    packages=find_packages(),
    author='Jhonatan',
    author_email='jhonatan@hotmal.com',
    keywords='camera',
    install_requires=['']
)
