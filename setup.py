from setuptools import setup, find_packages

with open('README.rst', encoding='UTF-8') as f:
    readme = f.read()

setup(
    name='ec2yaml',
    version='1.0.0',
    description='Create an EC2 instance from a simple YAML configuration file.',
    long_description=readme,
    author='Alex Cook',
    author_email='alexpcook@protonmail.com',
    license='MIT',
    install_requires=['boto3', 'pyyaml', 'requests'],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': [
            'ec2yaml=ec2yaml.main:main'
        ]
    }
)
