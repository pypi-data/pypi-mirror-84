import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="swachhdata", # Replace with your own username
    version="0.0.1",
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
          'beautifulsoup4==4.9.1', 'contractions==0.0.25', 'pycontractions', 'regex==2020.6.8', 'emoji==0.6.0', 'html2text==2019.8.11', 'html5lib==1.0.1',
          'httplib2==0.18.1', 'lxml==4.5.1', 'nltk==3.5', 'num2words==0.5.10', 'pycrypto==2.6.1', 'textblob==0.15.3', 'Unidecode==1.1.1',
          'unicode==2.7', 'textsearch==0.0.17'
      ],
    python_requires='>=3.6'
)