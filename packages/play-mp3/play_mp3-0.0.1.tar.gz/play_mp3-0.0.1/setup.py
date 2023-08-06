import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="play_mp3", # Replace with your own username
    version="0.0.1",
    author="Shreyansh Kushwaha",
    author_email="shreyansh.halk@gmail.com",
    description="This is a simple python package with which we can play .mp3 sounds.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires = ['playsound'],
    url="https://github.com/pypa/play_mp3",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)