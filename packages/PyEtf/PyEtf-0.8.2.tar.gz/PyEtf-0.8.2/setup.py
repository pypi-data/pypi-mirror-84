from setuptools import setup

setup(
    name='PyEtf',
    version='0.8.2',
    description='Look for files and text inside files',
    long_description=open('README.md').read(),
    py_modules = ['etf', 'portfolio', 'functions'],
    packages = ['pyetf','pyetf/frames', 'pyetf/finance'],
    install_requires=[
        'certifi==2020.6.20',
        'chardet==3.0.4',
        'cycler==0.10.0',
        'idna==2.10',
        'kiwisolver==1.2.0',
        'lxml==4.6.0',
        'matplotlib==3.3.2',
        'multitasking==0.0.9',
        'numpy==1.19.2',
        'pandas==1.1.3',
        'Pillow==8.0.0',
        'pyparsing==2.4.7',
        'python-dateutil==2.8.1',
        'pytz==2020.1',
        'requests==2.24.0',
        'six==1.15.0',
        'urllib3==1.25.10',
        'yfinance==0.1.55'
    ],
    author='Alfredo Mauri',
    author_email='alfredo.mauri.2000@gmail.com',
    license='BSD',
    keywords='python etfs portfoliomanager',
    scripts=['scripts/Update.py', 'scripts/GUI.py'],
    include_package_data=True,
    platforms='all',
    classifiers = [
        'Intended Audience :: Education',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Topic :: Documentation',
        'Topic :: Education :: Testing',
    ]
)
