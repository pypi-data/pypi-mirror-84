import setuptools
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


install_requires = [
    'torch==1.6.0',
    'scikit-learn==0.23.2',
    'numpy==1.19',
    'pandas==1.1.3',
]

dev = [
    "pytest",

]

setuptools.setup(
    name="synthetig",
    version="0.0.1a1",
    author="Jonathan Hind and Nick Lee-McMaster",
    author_email="info@synthetig.ai",
    description="Synthetig: An open-source synthetic data generation platform.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/synthetig/synthetig",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    install_requires=install_requires,


)
