import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pytraits",
    version="0.0.1",
    author="TaylorHere",
    author_email="taylorherelee@gmail.com",
    description="apply traits to your YAML template",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TaylorHere/traits",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=["Click"],
    entry_points='''
        [console_scripts]
        traits=traits:main
    ''',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
