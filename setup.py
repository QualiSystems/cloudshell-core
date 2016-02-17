from setuptools import setup, find_packages
import os

with open(os.path.join('version.txt')) as version_file:
    version_from_file = version_file.read().strip()

with open('requirements.txt') as f_required:
    required = f_required.read().splitlines()

with open('test_requirements.txt') as f_tests:
    required_for_tests = f_tests.read().splitlines()

setup(
    name='cloudshell-core',
    url='https://github.com/QualiSystems/cloudshell-core',
    author='QualiSystems',
    author_email='info@qualisystems.com',
    packages=['cloudshell-core'],
    install_requires=required,
    test_suite='tests',
    tests_require=required_for_tests,
    version=version_from_file,
    description='CloudShell Core Python package',
    include_package_data = True
)