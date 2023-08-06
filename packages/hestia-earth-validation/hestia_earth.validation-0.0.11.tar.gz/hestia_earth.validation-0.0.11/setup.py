from setuptools import find_packages, setup


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name='hestia_earth.validation',
    version='0.0.11',
    description='Hestia Data Validation library',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Guillaume Royer',
    author_email='guillaumeroyer.mail@gmail.com',
    license='GPL-3.0-or-later',
    url='https://gitlab.com/hestia-earth/hestia-data-validation',
    keywords=['hestia', 'data', 'validation'],
    packages=find_packages(exclude=("tests", "scripts")),
    python_requires='>=3',
    classifiers=[],
    install_requires=[
        'hestia_earth.schema>=0.1.8',
        'requests',
        'python-dateutil',
        'area',
    ]
)
