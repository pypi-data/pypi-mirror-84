import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="twitch_plays_hackru", 
    version="1.1.0",
    author="Jeffrey Fung",
    author_email="rnd@hackru.org",
    description="A TwitchPlays API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HackRU/twitch-plays",
    packages=setuptools.find_packages(),
    install_requires=[
        "requests==2.24.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
