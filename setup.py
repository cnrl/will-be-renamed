from setuptools import setup
from cerebro.globals import PACKAGE_NAME

# TODO: change package name (name and packages)
# TODO: change url when package name changed
# TODO: consider versions in dependencies
setup(
    name=PACKAGE_NAME,
    version='0.1.0dev',
    description='A Simulator for Spiking Neural Networks',
    url='https://github.com/cnrl/cerebro',
    author='CNRL Team',
    packages=['cerebro'],
    license='MIT',
    install_requires=['numpy', 'scikit-image', 'opencv-python', 'sympy', 'Jinja2']
)
