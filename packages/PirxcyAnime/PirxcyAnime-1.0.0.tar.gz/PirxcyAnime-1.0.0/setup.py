import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name="PirxcyAnime",
    version="1.0.0",
    author="Pirxcy",
    description="A Multi Action Discord Bot Based On Anime",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PirxcyFinal/AnimeBot/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'crayons',
        'dhooks',
        'os',
        'discord',
        'discord.py',
        'timeago',
        'jinja2',
        'jaconv',
        'requests',
        'psutil',
        'pypresence',
        'BenBotAsync',
        'uvloop',
        'sanic',
        'aiohttp'
    ],
)
