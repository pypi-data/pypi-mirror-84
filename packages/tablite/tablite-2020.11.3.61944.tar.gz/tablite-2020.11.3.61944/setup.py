"""
tablite
"""
build_tag = "394c283c27405456540f6fe39563e0f1023114cdf144e68c76252dc7997fae74"
from setuptools import setup
from pathlib import Path


folder = Path(__file__).parent
file = "README.md"
readme = folder / file
assert isinstance(readme, Path)
assert readme.exists(), readme
with open(str(readme), encoding='utf-8') as f:
    long_description = f.read()

keywords = list({
    'table', 'tables', 'csv', 'txt', 'excel', 'xlsx', 'ods', 'zip', 'log',
    'any', 'all', 'filter', 'column', 'columns', 'rows', 'from', 'json', 'to',
    'inner join', 'outer join', 'left join', 'groupby', 'pivot', 'pivot table',
    'sort', 'is sorted', 'show', 'use disk', 'out-of-memory', 'list on disk',
    'stored list', 'min', 'max', 'sum', 'first', 'last', 'count', 'unique',
    'average', 'standard deviation', 'median', 'mode', 'in-memory', 'index'
})

keywords.sort(key=lambda x: x.lower())


setup(
    name="tablite",
    version="2020.11.3.61944",
    url="https://github.com/root-11/tablite",
    license="MIT",
    author="Bjorn Madsen",
    author_email="bjorn.madsen@operationsresearchgroup.com",
    description="A table crunching library",
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=keywords,
    packages=["table"],
    include_package_data=True,
    data_files=[(".", ["LICENSE", "README.md"])],
    platforms="any",
    install_requires=[
        'xlrd>=1.2.0',
        'pyexcel-ods>=0.5.6',
        'openpyxl>=3.0.5',
        'pyperclip>=1.8.1',
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)


