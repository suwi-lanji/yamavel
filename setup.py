from setuptools import setup, find_packages

setup(
    name='yamavel',
    version='0.1.0',
    packages=find_packages(),
    install_requires=['PyYAML', 'inflection'],
    entry_points={
        'console_scripts': [
            'yamavel=yamavel.generator:main',
        ],
    },
)