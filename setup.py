import setuptools

setuptools.setup(
    name="imc-converter",
    version="0.0.1",
    author="Fred Fu",
    author_email="Fred.Fu@rmp.uhn.ca, STTARR.Image.Analysis@rmp.uhn.ca",
    description="Read and write Fluidigm IMC (imaging mass cytometry) files.",
    url="https://github.com/STTARR/imc-converter",
    packages=["imcconv"],
    python_requires=">=3.6",
    install_requires=[
        "numpy",
        "pandas",
        "tifffile",
        "xarray",
        "xmltodict"
    ]
)