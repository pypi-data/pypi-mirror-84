import setuptools

setuptools.setup(
    name="sheetreader",
    version="0.0.1",
    author="Jason Strauss",
    author_email="jason@popcornnotify.com",
    description="Iterate through rows of a Google Spreadsheet as if it were a Python CSV DictReader or DictWriter.",
    long_description="See https://github.com/jastrauss/SheetReader/blob/master/README.md",
    long_description_content_type="text/plain",
    url="https://github.com/jastrauss/SheetReader",
    packages=setuptools.find_packages(),
    classifiers=[
    ],
    python_requires='>=3.6',
)
