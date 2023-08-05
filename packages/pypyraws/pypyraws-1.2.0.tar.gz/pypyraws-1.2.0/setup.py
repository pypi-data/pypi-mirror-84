"""A setuptools based setup module for continuous deployment devops.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

import pypyraws.version

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pypyraws',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=pypyraws.version.__version__,

    description=(
        "pypyr task runner AWS plugin. Automate services like ECS, S3, "
        "Beanstalk & EC2 with automation pipelines without writing having to "
        "write code."),
    long_description=long_description,
    long_description_content_type='text/markdown',

    # The project's main homepage.
    url='https://pypyr.io/',

    project_urls={
        'Documentation': 'https://pypyr.io/docs/plugins/aws/',
        'Source': 'https://github.com/pypyr/pypyr-aws',
        'Release notes': 'https://pypyr.io/updates/releases/',
        'Tracker': 'https://github.com/pypyr/pypyr-aws/issues/',
    },

    # Author details
    author='Thomas Gaigher',
    author_email='info@pypyr.io',

    # Choose your license
    license='Apache License 2.0',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Libraries :: Python Modules',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: Apache Software License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],

    # What does your project relate to?
    keywords='pypyr,aws,plugin,devops,task-runner,pipeline,automation',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    # packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    packages=find_packages(exclude=['tests']),

    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    #   py_modules=["my_module"],

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['pypyr', 'boto3', 'ruamel.yaml'],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
        'dev': [
            'bumpversion',
            'codecov',
            'flake8',
            'flake8-docstrings',
            'pypyr',
            'pytest',
            'pytest-cov',
            'setuptools',
            'twine',
            'wheel'
        ]
    },

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    # package_data={
    #     'sample': ['package_data.dat'],
    # },

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    # data_files=[('my_data', ['data/data_file'])],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    # entry_points={
    # 'pypyr': ['aws=pypyraws']
    # 'pypyr': [
    #    'pypyr.aws=pypyraws'
    # ]
    # },
)
