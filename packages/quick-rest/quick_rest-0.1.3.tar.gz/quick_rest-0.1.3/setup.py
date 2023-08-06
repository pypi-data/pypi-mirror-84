import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="quick_rest",
    version="0.1.3",
    author="lamerlink",
    author_email="lamerlink@live.com",
    description="A simple utility for any REST API, regardless of authentication type.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LamerLink/quick_rest",
    packages=setuptools.find_packages(),
    install_requires=[
          'requests',
      ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
        "Typing :: Typed",
    ],
    python_requires='>=3.4',
)
