from setuptools import setup

from os import path

DIR = path.dirname(path.abspath(__file__))
DEPEND_PACKAGES = open(path.join(DIR, 'requirements.txt')).read().splitlines()
with open(path.join(DIR, "README.md"), "r", encoding="UTF-8") as fh:
    README = fh.read()

setup(
    name="selenide",
    packages=['selenide'],
    version="0.0.4",
    author="aquichita",
    author_email="chaochao.wu@outlook.com",
    description="Realization of UI automated testing wheels by selenium.",
    long_description=README,
    long_description_content_type="text/markdown",
    install_requires=DEPEND_PACKAGES,
    url="https://github.com/aquichita/selenide",
    package_data={
        '': ['*.json', 'models/*.pkl', 'models/*.json'],
    },
    include_package_data=True,
    tests_require=[
        'pytest',
        'pytest-cov',
        'pytest-sugar'
    ],
    python_requires='>=3.8'
)
