from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

version = '0.0.1.4';
setup(
    name='tidy3dclient',
    version=version,
    description='A Python API for TIDY3d FDTD Solver',
    author='FlexCompute, Inc.',
    author_email='lei@flexcompute.com',
    packages=['tidy3d'],
    install_requires=['aws-requests-auth', 'bcrypt'] + requirements,
    dependency_links=['http://github.com/flexcompute/warrant/tarball/master#egg=warrant-0.6.4'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5'
)
