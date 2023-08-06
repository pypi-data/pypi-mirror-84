import setuptools
from setuptools import setup

TEST_DEPS = [
    'mock==3.0.5',
    'pytest==5.0.1',
    'pytest-runner==5.1',
    'pytest-pylint==0.14',
    'pytest-cov==2.7.1',
    'pylint==2.3.1'
]

setup(
    name='kouyierr',
    author='vmdude',
    author_email='frederic@martin.lc',
    url='https://github.com/vmdude/kouyierr',
    description='Document Generator, aka Doc As Code',
    long_description='file: README.md',
    license='MIT',
    keywords='aws',
    classifiers=[
        'Programming Language :: Python :: 3.8'
    ],
    entry_points={
        'console_scripts': ['kouyierr=kouyierr.main:main']
    },
    zip_safe=True,
    include_package_data=True,
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'boto3',
        'click',
        'rich',
        'yamllint',
        'Jinja2',
    ],
    tests_require=TEST_DEPS,
    extras_require={
        'test': TEST_DEPS
    }
)
