from setuptools import setup
import setuptools
from subprocess import call

# from setuptools.command.install import install as _install
#
#
# class Install(_install):
from setuptools.command.bdist_egg import bdist_egg as _bdist_egg

class bdist_egg(_bdist_egg):
    def run(self):
        # _install.do_egg_install(self)
        # call(["python -m pip install --user nltk"], shell=True)
        # self.do_egg_install()
        import nltk
        nltk.download('stopwords')
        nltk.download('averaged_perceptron_tagger')
        nltk.download('wordnet')
        # call(["python -m -user nltk.downloader stopwords"], shell=True)
        _bdist_egg.run(self)

setup(name='grooming',
version='0.5',
description='Grooming is a easiest way to clean-up the text',
author='Jayant Singh',
author_email='jayantsingh75@gmail.com',
url="https://github.com/jaysin60/grooming",
# cmdclass={'install': Install},
cmdclass={'bdist_egg': bdist_egg},
setup_requires=['nltk'],
packages=setuptools.find_packages(),
classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
python_requires='>=3.6',
install_requires = ['nltk','word2number']
)
