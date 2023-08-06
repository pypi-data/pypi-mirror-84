from distutils.core import setup
from setuptools import find_packages

setup(
    name='dwork',
    python_requires='>=3',
    version='0.0.1',
    author='KIProtect GmbH',
    author_email='dwork@kiprotect.com',
    license='BSD-3',
    url='https://github.com/kiprotect/dwork',
    packages=find_packages(),
    package_data={'': ['*.ini']},
    include_package_data=True,
    install_requires=['click'],
    zip_safe=False,
    entry_points={
        'console_scripts': [
            #'beam = beam.cli.main:beam'
        ]
    },
    description='Dwork - Differentially private data science library.',
    long_description=""""""
)
