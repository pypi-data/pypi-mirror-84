import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dbutils-gonzalo123", # Replace with your own username
    version="0.0.1",
    author="Gonzalo Ayuso",
    author_email="gonzalo123@gmail.com",
    description="psycopg2 db utils",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gonzalo123/dbutils",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
