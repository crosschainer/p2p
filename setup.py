from setuptools import setup, find_packages

setup(
    name='p2p', 
    version='0.1',
    packages=['p2p'],
    install_requires=[
        'flask',
        'requests'
    ],
    entry_points={
        'console_scripts': [
            'p2p = p2p.main:boot'
        ]
    }

)

