import re
import ast
from setuptools import setup, find_packages


version_re=re.compile(r'(?<=__version__\s=\s).*')
with open("fxtest/__init__.py","rb") as f:
    base=str(f.read().decode('utf-8'))
version=str(ast.literal_eval(version_re.search(base).group()))

setup(
    name="fxtest",
    url="https://github.com/shuaiwangNB/fxtest",
    author="shuaiwang",
    version=version,
    install_requires=[
        "py",
        "ansi2html",
        'pytest',
        "allure-pytest",
        "pytest-fxtest",
        "openpyxl",
        "pyyaml",
        "selenium",
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts' :[
            'fxtest=fxtest.cli:main'
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ]
)