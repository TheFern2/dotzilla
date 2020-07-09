import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dotzilla",
    version="0.0.1",
    author="Fernando B",
    author_email="fernandobe+git@protonmail.com",
    description="A sane simple management tool for syncing dot files for multiple computers.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kodaman2/dotzilla",
    packages=setuptools.find_packages(),
    license='GPLv3',
    entry_points={
        'console_scripts': [
            # command = package.module:function
            'dotzilla = dotzilla.app:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)