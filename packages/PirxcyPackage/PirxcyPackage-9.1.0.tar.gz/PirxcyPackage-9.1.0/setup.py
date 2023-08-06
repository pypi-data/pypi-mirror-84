import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name="PirxcyPackage",
    version="9.1.0",
    author="Pirxcy",
    description="PirxcyBot in a PyPi package form to easily be ran on repl. Or in a simple py file",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PirxcyFinal/PirxcyBotFiles",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'crayons',
        'fortnitepy',
        'psutil',
        'pypresence',
        'BenBotAsync',
        'FortniteAPIAsync',
        'uvloop',
        'sanic',
        'aiohttp'
    ],
)
