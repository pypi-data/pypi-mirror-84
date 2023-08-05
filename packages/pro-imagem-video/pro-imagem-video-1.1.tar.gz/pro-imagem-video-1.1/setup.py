from setuptools import setup, find_packages
from pathlib import Path

setup(
    name='pro-imagem-video',
    version=1.1,
    descrição='Este pacote possui ferramentas de processamento de imagens e vídeo',
    long_description=Path('README.md').read_text(),
    author='Jhonatan',
    author_email='jhonatan@hotmail.com',
    keywords=['camera', 'video'],
    packages=find_packages()
)
