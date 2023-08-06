import sys

from setuptools import setup
from pathlib import Path


assert sys.version_info >= (3, 8, 0), "selenide requires Python 3.8+"

CURRENT_DIR = Path(__file__).parent
sys.path.insert(0, str(CURRENT_DIR))


def readme() -> str:
    return (CURRENT_DIR / "README.md").read_text(encoding="utf8")


def requirements() -> list:
    return (CURRENT_DIR / "requirements.txt").read_text(encoding="utf8").splitlines()


setup(
    name="selenide",
    packages=['selenide'],
    version="0.0.5",
    author="aquichita",
    author_email="chaochao.wu@outlook.com",
    description="Realization of UI automated testing wheels by selenium.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    install_requires=requirements(),
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
