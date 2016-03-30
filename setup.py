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
    url='http://www.quali.com/',
    author='Quali',
    author_email='info@quali.com',
    packages=find_packages(),
    install_requires=required,
    tests_require=required_for_tests,
    license='Apache 2.0',
    version=version_from_file,
    description='Core package for CloudShell Python orchestration and automation. This package can be referenced by '
                'code running under CloudShell to get access to logging, basic interfaces and other utilities',
    include_package_data=True,
    keywords="sandbox cloud cmp cloudshell",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: Apache Software License",
    ]
)