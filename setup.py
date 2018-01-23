import re

from setuptools import find_packages, setup

with open('requirements.txt', 'rt') as f:
    requirements = f.read().splitlines()

with open('README.md', 'rt') as f:
    readme = f.read()

try:
    with open('bot/__init__.py', 'rt') as f:
        version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                            f.read(), re.MULTILINE).group(1)
except (AttributeError, FileNotFoundError):
    raise RuntimeError('version is not set')

if not version:
    raise RuntimeError('version is not set')

setup(
    name='factorio-mod-portal-bot',
    author='Sparta142',
    url='http://github.com/Sparta142/factorio-mod-portal-bot',
    version=version,
    packages=find_packages(exclude=['tests']),
    license='MIT',
    description='Reddit bot that links Factorio mods on request.',
    long_description=readme,
    include_package_data=True,
    install_requires=requirements,
    setup_requires=[
        'flake8',
        'pytest-runner'
    ],
    tests_require=[
        'pytest',
        'pytest-cov'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Topic :: Games/Entertainment',
        'Topic :: Internet',
        'Topic :: Utilities'
    ]
)
