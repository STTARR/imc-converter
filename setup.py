import setuptools

setuptools.setup(
    name="imc-converter",
    version="0.0.1",
    author="Fred Fu",
    author_email="Fred.Fu@rmp.uhn.ca, STTARR.Image.Analysis@rmp.uhn.ca",
    description="Read and write Fluidigm IMC (imaging mass cytometry) files.",
    url="https://github.com/STTARR/imc-converter",
    packages=setuptools.find_packages(),
    package_data={
        "imcconv": ["gui/images/*"]
    },
    python_requires=">=3.6",
    install_requires=[
        "numpy",
        "pandas",
        "tifffile",
        "xarray",
        "xmltodict"
    ],
    extras_require={
        "GUI": ["Gooey"]
    },
    entry_points={
        "console_scripts": [
            "imcconv-gui-console = imcconv.gui.convert:main [GUI]"
        ],
        "gui_scripts": [
            "imcconv-gui = imcconv.gui.convert:main [GUI]"
        ]
    }
)