from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup(
    name='time-series-models',
    version='0.0.2',
    description='Neural netork models for time-series-predictor.',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY,
    license='The Unlicense',
    packages=find_packages(exclude=("tests",)),
    author='Daniel Kaminski de Souza',
    author_email='daniel@kryptonunite.com',
    keywords=['Time series models'],
    url='https://github.com/krypton-unite/time_series_models.git',
    download_url='https://pypi.org/project/time-series-models/',
    install_requires = [
        'torch'
    ],
    extras_require={
        'test': [
            'pytest',
            'pytest-cov'
        ],
        'dev': [
            'bumpversion',
            'twine',
            'wheel',
            'autopep8'
        ]
    }
)