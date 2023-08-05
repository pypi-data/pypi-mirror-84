#!/usr/bin/python3
import setuptools

def reader(filename:str, lister:bool):
    text = ''
    with open(filename) as f:
        text = f.read()
        if lister:
            text = [ i.split('=')[0] for i in text.splitlines()]
        return text

setuptools.setup(name="pydirbuster",
                 version="0.5",
                 author="Zachary Farquharson",
                 author_email="PercyJackson235@gmail.com",
                 description="Python Web Directory and File Brute Forcer",
                 long_description=reader('README.md', False),
                 long_description_content_type="text/markdown",
                 url="https://github.com/PercyJackson235/pydirbuster",
                 packages=setuptools.find_packages(),
                 classifiers=["Development Status :: 4 - Beta",
                              "Intended Audience :: Developers",
                              "Intended Audience :: Education",
                              "Intended Audience :: End Users/Desktop",
                              "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
                              "Operating System :: OS Independent",
                              "Programming Language :: Python :: 3"],
                 python_requires=">=3",
                 install_requires=reader('requirements.txt', True),
                 scripts=['pydirbuster/pydirbuster'])
