import setuptools
name = "steelforge_site_utils"
print(name)
setuptools.setup(
    name=name,
    version="0.0.1",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",

)