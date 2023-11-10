from setuptools import setup, find_packages

setup(
    name="Py-core",
    version="0.1.0",
    packages=find_packages(),
    description="A Python package to allow communication between COM, OBC and EPS systems in all communication protocols regardless of the project components used",
    author="Alpha Mamadou Diallo",
    author_email="alphamamadoud99@gmail.com",
    url="https://gitlab.obspm.fr/cceres/FlatSat/py_core.git",
    install_requires=[
        "numpy",
        "pandas"
    ],
    setup_requires=["wheel"],
    python_requires=">=2.7.16",
)
