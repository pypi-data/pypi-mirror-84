import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pjeuler-chicotobi",
    version="0.0.1",
    author="Chicotobi",
    author_email="tobias310788@googlemail.com",
    description="Tools in Python for Project Euler",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chicotobi/pjeuler_python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
