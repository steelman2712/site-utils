import setuptools

setuptools.setup(
    name="steelforge-site-utils",
    version="0.0.1",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",

)