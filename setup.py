from setuptools import setup

from gitcount import __version__

setup(
    name    = 'git-count',
    description = 'It counts commits in each day, week, month or year.',
    long_description = open('README.rst').read(),
    version = __version__,
    author  = 'Mosky',
    author_email = 'mosky.tw@gmail.com',
    #url = 'http://git-count.mosky.tw/',
    py_modules = ['gitcount'],
    license = 'MIT',
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities',
        'Topic :: Software Development',
    ],
    entry_points = {
         'console_scripts': [
             'git-count = gitcount:main',
        ]
    },
    install_requires = ['clime>=0.1.5'],
)

