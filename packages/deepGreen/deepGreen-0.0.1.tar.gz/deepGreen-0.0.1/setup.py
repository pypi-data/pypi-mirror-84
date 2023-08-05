from setuptools import setup, find_packages

__version__ = '0.0.1'

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='deepGreen',
    version=__version__,
    description='A tree-ring width model based on deep learning algorithms',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Feng Zhu, Andong Hu',
    author_email='fengzhu@usc.edu, andong.hu@cwi.nl',
    url='https://github.com/fzhu2e/deepGreen',
    packages=find_packages(),
    license="MIT license",
    keywords='Paleoclimate Data Assimilation',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
    ],
    install_requires=[
    ],
)