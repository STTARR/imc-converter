"""
Conversion script for IMC .txt -> single page .tif files & .afi file for HALO.
Outputs 16-bit images with normalized channels & a scale_factors.csv file containing
normalization.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from lxml import etree as et
from PIL import Image

IGNORE_COLUMNS = ["Start_push", "End_push", "Pushes_duration"]
IMC_MPP = 1e-6
HIGH_QUANTILE = 0.98

# IMC text data
data = Path(r"K:\000300-000399\000360_Siddiqui\Fluidigm\160301_OCIP23-28_aSMA-Coll-GH2AX-etc\OCIP28 cis-4-1 A1; He=1090, Ar=0_9, Z=3600, atten=39, 1000umX1000um, 200Hz 1000pulses 200um-sec 1 um stepsize area1.txt")
outdir = Path(data.name.split(";")[0])
outdir.mkdir(exist_ok=True)
print(outdir.name)
df = pd.read_csv(data, sep="\t", usecols=lambda c: c not in IGNORE_COLUMNS)

assert tuple(df.columns[0:3]) == ("X", "Y", "Z"), "First three columns not X/Y/Z."

xsz = df.X.max() + 1
ysz = df.Y.max() + 1

xyz = df.iloc[:,:3].values.reshape((xsz, ysz, -1))

# Check that reshape assumed the correct structure
assert (xyz[:,:,0][0,:] == np.array(range(xsz))).all()
assert (xyz[:,:,1][:,0] == np.array(range(ysz))).all()

imc_data = df.iloc[:,3:]

scale_factors = {}
# TODO: Scale consistently over a set of data?

for channel in imc_data:
    print(f"\t{channel}")
    arr = imc_data[channel].values.reshape((xsz, ysz))

    # Rescale channel to 16-bit
    low = arr.min()
    high = np.quantile(arr, q=HIGH_QUANTILE)  # 98% is recommended in Fluidigm guide
    scale_factor = 255**2 / (high - low)
    arr = (arr * scale_factor).astype(np.uint16)
    
    im = Image.fromarray(arr)
    im.save(outdir / (channel + ".tif"), compression="tiff_deflate")

    # Keep record of scaling factor used from raw data
    scale_factors[channel] = scale_factor

# Save scaling factors
pd.DataFrame(scale_factors, index=[0]).to_csv(outdir / "scale_factors.csv", index=None)

# Create afi file
root = et.Element("ImageList")
for channel in imc_data:
    image = et.SubElement(root, "Image")
    et.SubElement(image, "Path").text = str((outdir / (channel + ".tif")).resolve(strict=True))  # Will raise error if file doesn't exist
    et.SubElement(image, "ChannelName").text = channel
out_tree = et.ElementTree(root)
out_tree.write(str(outdir / (outdir.name + ".afi")), pretty_print=True)