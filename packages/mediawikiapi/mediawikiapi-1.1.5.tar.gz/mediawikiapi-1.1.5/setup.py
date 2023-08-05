# -*- coding: utf-8 -*-
import codecs
import os
import setuptools
from distutils.util import convert_path

main_ns = {}
ver_path = convert_path('mediawikiapi/version.py')
with open(ver_path) as ver_file:
    exec(ver_file.read(), main_ns)


def local_file(file):
    if os.path.exists(file):
        f = codecs.open(os.path.join(os.path.dirname(__file__), file), 'r', 'utf-8')
        return f.readlines()
    return []


install_reqs = [
    line.strip()
    for line in local_file('requirements.txt')
    if line.strip() != ''
]

install_test_reqs = [
    line.strip()
    for line in local_file('requirements-test.txt')
    if line.strip() != ''
]

try:
    import pypandoc

    long_description = pypandoc.convert_file('README.md', 'rst')
except(IOError, ImportError, OSError):
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'README.md'), encoding="utf-8") as f:
        long_description = f.read()

setuptools.setup(
    name="mediawikiapi",
    version=main_ns['__version__'],
    author="Taras Lehinevych",
    author_email="mediawikiapi@taraslehinevych.me",
    description="Wikipedia API on Python",
    license="MIT",
    keywords="python wikipedia API mediawiki",
    url="https://github.com/lehinevych/MediaWikiAPI",
    install_requires=install_reqs,
    tests_require=install_test_reqs,
    test_suite="tests",
    packages=['mediawikiapi'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ]
)
