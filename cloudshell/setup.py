from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='CloudShell-Core',
      version='1.1',
      description='CloudShell Core functionality',
      long_description=readme(),
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: Apache License',
          'Programming Language :: Python :: 2.7',
          'Topic :: System :: Distributed Computing',
          'Operating System :: Microsoft :: Windows',
          'Intended Audience :: Information Technology',
          'Operating System :: MacOS',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX',
          'Operating System :: Unix'
      ],
      keywords='cloud QualiSystems',
      url='https://github.com/QualiSystems/CloudShell-Core',
      author='Boris Modylevsky',
      author_email='borismod@gmail.com',
      license='Apache 2.0',
      packages=['CloudShell-Core'],
      install_requires=[],
      test_suite='',
      tests_require=[],
      entry_points={},
      include_package_data=True,
      zip_safe=False)
