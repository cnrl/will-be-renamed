from setuptools import setup
from cnrl.globals import package_name

# TODO: change package name (name and packages)
# TODO: change url when package name changed
# TODO: consider versions in dependencies
setup(
    name=package_name,
    version='0.1.0dev',
    description='A Simulator for Spiking Neural Networks',
    url='https://github.com/cnrl/will-be-renamed',
    author='CNRL Team',
    packages=['cnrl'],
    license='MIT',
    install_requires=['numpy', 'scikit-image', 'opencv-python', 'sympy', 'Jinja2']
)
