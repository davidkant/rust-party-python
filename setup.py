from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE.md') as f:
    license = f.read()

requirements = [
    'numpy',
    'librosa',
    'matplotlib',
    'librosa',
]

setup(
    name='rust-party-python',
    version='0.0.1',
    description='python side of the rust-party',
    long_description=readme,
    author='David Kant',
    author_email='david.kant@gmail.com',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=requirements
)
