import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="after_class", # Replace with your own username
    version="0.0.21",
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
        "pandas==1.1.3",
        "scikit-learn==0.23.2",
        "pickle5==0.0.11",
        "matplotlib==3.3.2"
    ],
    include_package_data=True,
    python_requires='>=3.6',
)