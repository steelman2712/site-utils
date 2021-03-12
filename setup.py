import setuptools
name = "steelforge_site_utils"
print(name)
setuptools.setup(
    name=name,
    version="0.0.1",
    package_dir={"": "steelforge_site_utils"},
    packages=setuptools.find_packages(where="steelforge_site_utils"),
    python_requires=">=3.6",

)