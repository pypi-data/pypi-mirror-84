import setuptools


import atomion


with open("README.md", "r", encoding='utf-8') as fichier:
    long_description = fichier.read()


setuptools.setup(
    name = "atomion",
    version = atomion.__version__,
    author = "Asurix",
    author_email = "asurix@outlook.fr",
    description = "Manipuler des atomes, ions et molécules facilement.",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/4surix/atomion",
    packages = setuptools.find_packages(),
    keywords = 'quark atome ion molecule equation reaction',
    classifiers = [
        'Intended Audience :: Education',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Programming Language :: Python :: 3 :: Only',
        'Typing :: Typed',
        'Natural Language :: French',
        'Programming Language :: Python :: Implementation :: MicroPython'
    ],
    python_requires = '>=3.6, <4',
)