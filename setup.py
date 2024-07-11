from setuptools import setup, find_packages

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setup(
    name="Projeto Teste/Estudo Flask",
    version="0.1.0",
    descricao="Projeto Teste/Estudo Flask",
    author="Victor Costa Prieto",
    author_email="vitao.prieto@gmail.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=requirements,
)