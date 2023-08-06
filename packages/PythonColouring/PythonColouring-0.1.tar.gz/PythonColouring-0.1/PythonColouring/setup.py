import setuptools

with open("PythonColouring/readme.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PythonColouring", # Replace with your own username
    version="0.1",
    author="CoolJames1610",
    author_email="jadokofie@gmail.com",
    description="A module used to get colours to use in the Python terminal",
    long_description=long_description,
    long_description_content_type="text/markdown",
    #url="https://github.com/CoolJames1610/Flighter",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    keywords = ['PYTHON', 'COLOURING', 'TERMINAL', 'COLORED', 'PRINT', 'STYLE', 'COLORS', 'COLOURS'],   
)