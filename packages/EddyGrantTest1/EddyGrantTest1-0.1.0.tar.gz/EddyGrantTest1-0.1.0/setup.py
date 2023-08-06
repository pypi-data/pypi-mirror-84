from distutils.core import setup

setup(
    name='EddyGrantTest1',
    version='0.1.0',
    author='Sachin Saini',
    author_email='eddy@example.com',
    packages=['eddygranttest1'],
    scripts=['bin/eddy.py'],
    url='http://pypi.python.org/pypi/TowelStuff/',
    license='LICENSE.txt',
    description='TEst package by sachin saini',
    long_description=open('README.txt').read(),
    install_requires=[
        "excel",
    ],
)
