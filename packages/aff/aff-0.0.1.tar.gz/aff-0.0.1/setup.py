import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aff", # Replace with your own username
    version="0.0.1",
    author="Dmitriy Kravchuk",
    author_email="jogerwarlock@yandex.ru",
    description="Anti Fragile Forecasting",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://https://github.com/dishkakrauch/aff",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)