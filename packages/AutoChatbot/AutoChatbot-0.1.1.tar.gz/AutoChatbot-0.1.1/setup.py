import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="AutoChatbot", # Replace with your own username
    version="0.1.1",
    author="Kritik Seth",
    author_email="sethkritik@gmail.com",
    description="Package that makes chatbots automatically",
    py_modules=['chat', 'clean'],
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
          'tensorflow', 'keras', 'gensim', 're', 'numpy', 'tqdm', 'pandas',
          'contractions', 'pycontractions', 'unicodedata', ''
      ],
    python_requires='>=3.6',
    project_urls={
    'Documentation': 'https://kritikseth.github.io/autochatbot_docs'
},
)
