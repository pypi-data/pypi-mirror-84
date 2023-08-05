import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="after_class", # Replace with your own username
    version="0.0.1",
    author="Moiseev Arseniy",
    author_email="arseniy.moiseyev@phystech.edu",
    description="Tool to analyze multiclassification ML models.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/streetbee/dv_after_class",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "bs4",
        "pandas",
        "scikit-learn",
        "pickle"
    ],
    include_package_data=True,
    python_requires='>=3.6',
)