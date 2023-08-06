from setuptools import setup, find_packages

setup(
    name='zzhprobm',
    version='0.4',
    description=('Gaussian distributions'),
    author='maxoyed',
    author_email='maxoyed@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=['matplotlib==3.3.2']
)
