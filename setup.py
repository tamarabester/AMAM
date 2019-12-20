from setuptools import setup, find_packages


setup(
    name = 'Tamaras AMAM project',
    version = '0.1.0',
    author = 'Tamara',
    description = 'An example package.',
    packages = find_packages(),
    install_requires = ['click', 'flask'],
    tests_require = ['pytest', 'pytest-cov'],
)
