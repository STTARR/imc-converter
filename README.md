## background

This package was written to interact with Fluidigm imaging mass cytometry files in .txt or .mcd format and write them out as TIFF or OME-TIFF images, which have the advantages of being smaller in file size because of image compression (neither TXT or MCD files use any sort of compression) and usable in other software (e.g. digital pathology platforms for downstream analysis). In comparison, for Fluidigm's official MCD Viewer:

- The exports to OME-TIFF do not actually follow the OME-TIFF standard:
    - Exported 16-bit OME-TIFFs do not contain the necessary OME-XML
    - Exported 32-bit OME-TIFFs fail to specify required OME-XML attributes for the image dimensions, resulting in image channels being interpreted as time-series images by Fiji/Bio-Formats (and software dependent on it, like [https://qupath.github.io/](QuPath)) instead of multichannel images
- MCD Viewer silently ignores missing data values in TXT files by removing the row entirely

This package exists as both a module for interacting with IMC data in Python (as xarray DataArrays), but also includes a script for batch IMC conversion with an optional graphical interface built using [https://github.com/chriskiehl/Gooey](Gooey). 

DataArray objects were chosen since they maintain the channel name information, which makes any downstream analysis easier to read compared to a standard numpy array, while still allowing a numpy representation to be accessed (using the `.values` property), thus being compatible with the standard scientific Python ecosystem.

## usage

WIP