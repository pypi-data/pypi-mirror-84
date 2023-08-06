import setuptools

with open("README.md",'r') as fh:
    long_description = fh.read()


setuptools.setup(
    name='RBytes',
    version='2.1',
    #scripts=['RBytes.py'],
    author='DrEenot',
    author_email='dreenot@gmail.com',
    description='Library that allows you to work with arrays of bytes',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/DoctorEenot/RBytes',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
        ],
    )
