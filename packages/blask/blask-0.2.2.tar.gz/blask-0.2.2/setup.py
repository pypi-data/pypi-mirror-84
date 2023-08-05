"""
blask

Copyright (C) 2018  https://github.com/zerasul/blask

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

from setuptools import setup, find_packages
from pathlib import Path

info_file = Path(__file__).resolve().parents[0] / "README.md"
with info_file.open() as f:
    long_desc = f.read()
# adding nonpython files to package
mdownfile = Path(__file__).resolve().parents[0] / "blask" / "markdown_template.md"
indextempfile = Path(__file__).resolve().parents[0] / "blask" / "index_template.html"
Dockerfile_template = Path(__file__).resolve().parents[0] / "blask" / "Dockerfile_template"
default404 = Path(__file__).resolve().parents[0] / "blask" / "default_404.md"
default_env = Path(__file__).resolve().parents[0] / "blask" / "default_env.env"

setup(
    name="blask",
    version="0.2.2",
    packages=find_packages(exclude=["tests"]),
    url="https://getblask.com",
    license="GPL 3.0",
    author="zerasul",
    author_email="zerasul@gmail.com",
    description="A simple Blog engine using Flask and Markdown.",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: News/Diary",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    package_data={
        "blask": [
            str(mdownfile),
            str(Dockerfile_template),
            str(indextempfile),
            str(default404),
            str(default_env),
        ]
    },
    entry_points="""
        [console_scripts]
        blaskcli=blask.blaskcli:blaskcli
    """,
    long_description=long_desc,
    long_description_content_type="text/markdown",
    python_requires=">=3",
    install_requires=["flask", "markdown", "Pygments", "click"],
    test_requires=["pytest", "pytest-cov", "pylint", "pytest-mock"],
)
