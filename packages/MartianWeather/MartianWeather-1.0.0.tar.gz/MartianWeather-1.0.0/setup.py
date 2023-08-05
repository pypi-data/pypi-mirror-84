import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="MartianWeather",
    version="1.0.0",
    author="William Larsson",
    description="A python wrapper for the Insight: Mars Weather Service API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/wilmlar/martianweather",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords='insight, mars, weather, api',
    install_requires=['requests'],
    python_requires='>=3.6',
    project_urls={
        'Source': 'https://gitlab.com/wilmlar/martianweather',
        'Wiki': 'https://gitlab.com/wilmlar/martianweather/-/wikis/home',
        'Bug Reports': 'https://gitlab.com/wilmlar/martianweather/-/issues',
    },
)
