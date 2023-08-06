from setuptools import setup, find_packages

setup(
    name                = 'kakaotalk_msg_preprocessor',
    description         = 'Preprocessor for kakaotalk message exported txt file',
    long_description    = open('README.md').read(),
    long_description_content_type="text/markdown",
    version             = '0.1',
    license             = 'MIT',
    author              = 'uoneway',
    author_email        = 'uoneway@gmail.com',
    url                 = 'https://github.com/uoneway/kakaotalk_msg_preprocessor',
    install_requires    =  [],
    packages            = find_packages(exclude = []),
    keywords            = ['kakaotalk', 'preprocessor', 'parser', 'url'],
    python_requires     = '>=3.7',
    classifiers         = [
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
)