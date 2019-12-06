import xarray as xr
import tifffile

from pathlib import Path
from typing import Union, List, Sequence, Generator


def write_ometiff(imarr: xr.DataArray, outpath: Union[Path, str], summary: bool=False, **kwargs) -> None:
    """Write DataArray to a multi-page OME-TIFF file.
    Args:
        imarr: image DataArray object
        outpath: file to output to
        summary: whether to output MCDViewer summary file with export
        **kwargs: Additional arguments to tifffile.imwrite
    """
    outpath = Path(outpath)
    imarr = imarr.transpose("c", "y", "x")
    Nc, Ny, Nx = imarr.shape
    # Generate standard OME-XML
    channels_xml = '\n'.join(
        [f"""<Channel ID="Channel:0:{i}" Name="{channel}" SamplesPerPixel="1" />"""
            for i, channel in enumerate(imarr.c.values)]
    )
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
    <OME xmlns="http://www.openmicroscopy.org/Schemas/OME/2016-06"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xsi:schemaLocation="http://www.openmicroscopy.org/Schemas/OME/2016-06 http://www.openmicroscopy.org/Schemas/OME/2016-06/ome.xsd">
        <Image ID="Image:0" Name="{outpath.stem}">
            <Pixels BigEndian="false"
                    DimensionOrder="XYZCT"
                    ID="Pixels:0"
                    Interleaved="false"
                    SizeC="{Nc}"
                    SizeT="1"
                    SizeX="{Nx}"
                    SizeY="{Ny}"
                    SizeZ="1"
                    PhysicalSizeX="1.0"
                    PhysicalSizeY="1.0"
                    Type="float">
                <TiffData />
                {channels_xml}
            </Pixels>
        </Image>
    </OME>
    """
    outpath.parent.mkdir(parents=True, exist_ok=True)
    tifffile.imwrite(outpath, data=imarr.values, description=xml, contiguous=True, **kwargs)
    if summary:
        # Write MCDViewer summary, might be needed for compatibility with Visiopharm (?)
        summaryfname = outpath.name.rstrip(''.join(outpath.suffixes)) + "_summary.txt"
        rows = []
        for page, imchannel in enumerate(imarr):
            channel, label = str(imchannel.c.values).split("_")
            rows.append([page, channel, label, imchannel.values.min(), imchannel.values.max()])
        pd.DataFrame(rows, columns=["Page", "Channel", "Label", "MinValue", "MaxValue"]) \
          .to_csv(outpath.with_name(summaryfname), index=False, sep="\t")


def write_individual_tiffs(imarr: xr.DataArray, outdir: Union[Path, str], **kwargs) -> None:
    """Write DataArray to individual TIFF files in a folder.
    Args:
        imarr: image DataArray object
        outdir: folder to output to
        **kwargs: Additional arguments to tifffile.imwrite
    """
    imarr = imarr.transpose("c", "y", "x")
    outdir.mkdir(parents=True, exist_ok=True)
    for imchannel in imarr:
        tifffile.imwrite(Path(outdir) / f"{str(imchannel.c.values)}.tiff", data=imchannel.values, **kwargs)
