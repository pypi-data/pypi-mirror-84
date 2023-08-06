import setuptools

# Reads README.md and sets it to long description
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="BD103", # Replace with your own username
    version="0.0.1", # Replace for every update
    author="BD103", # Your name / username
    author_email="dont@stalk.me", # YEmail
    description="Personal Package by BD103", # Small Desc
    long_description=long_description, # Keep
    long_description_content_type="text/markdown", # Keep
    url="https://repl.it/@BD103/BD103-Python-Package", # Github / Repl.it / Website URL
    packages=setuptools.find_packages(), # DO NOT EDIT
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ], # Keep
    python_requires='>=3.6', # Don't change unless you know what you're doing
)