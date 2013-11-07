import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))


requires = [
    ]

test_requires = [
    'pytest',
    ]

setup(
    name='webradiocast',
    version='0.1.0',
    description='webradio->->podcast packages',
    long_description='',
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP",
    ],
    author='attakei',
    author_email='attakei@gmail.com',
    url='',
    keywords='',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    tests_require=requires + test_requires,
    test_suite="tests",
    entry_points={
        'console_scripts': [
            'webradiocast-build-xml = webradiocast.scripts.build_xml:main',
        ]
    },
)
