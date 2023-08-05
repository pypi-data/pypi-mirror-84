import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="swachhdata", # Replace with your own username
    version="0.0.2",
    author="Kritik Seth",
    author_email="sethkritik@gmail.com",
    description="Package that cleans your data",
    py_modules=['text'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kritikseth",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
          'beautifulsoup4', 'contractions', 'pycontractions', 'regex', 'emoji', 'html2text', 'html5lib',
          'httplib2', 'lxml', 'nltk', 'num2words', 'pycrypto', 'textblob', 'Unidecode',
          'unicode', 'textsearch'
      ],
    python_requires='>=3.6'
)

