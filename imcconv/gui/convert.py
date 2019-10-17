from pathlib import Path
from ..imcconv import *
from gooey import Gooey, GooeyParser, local_resource_path
import os
import sys

@Gooey(
    program_name="IMC Converter",
    image_dir=local_resource_path(Path(__file__).parent / "images"),
    progress_regex=r"^File (?P<current>\d+)/(?P<total>\d+): .+$",
    progress_expr="current / total * 100",
    hide_progress_msg=False,
    # Windows-only fix for calling this as a script while still working with pyinstaller
    # Need to quote target in case it contains spaces
    # related: https://github.com/chriskiehl/Gooey/issues/219
    target=f'"{Path(sys.argv[0]).name}.exe"' if os.name == "nt" and \
           Path(sys.argv[0]).suffix != ".exe" else f'"{Path(sys.argv[0]).name}"',
)
def main():
    parser = GooeyParser(
        description="Convert IMC (.txt/.mcd) files to images."
    )
    parser.add_argument(
        "filelist", action="store", type=lambda l: [Path(f) for f in l.split(";")],
        help="Paths to IMC files (.txt or .mcd).",
        widget="MultiFileChooser"
    )
    parser.add_argument(
        "outdir", action="store", type=Path,
        help="Output directory.",
        widget="DirChooser"
    )
    parser.add_argument(
        "type", choices=["OME-TIFF", "TIFF (Individual Channels)"], nargs="+",
        default=["OME-TIFF"],
        help="Image output type (can select multiple).",
        widget="Listbox"
    )
    parser.add_argument(
        "-f", "--fillmissing", type=float, default=-1,
        help="Value to use assign to any missing image data."
    )
    parser.add_argument(
        "-c", "--compress", type=int, default=6,
        help="Compression value (lossless/deflate) from 0 to 9 (0 being uncompressed).",
        gooey_options={
            "validator": {
                "test": "user_input.isnumeric() and 0 <= float(user_input) <= 9",
                "message": "Must be integer between 0 and 9 (inclusive)."
            }
        }
    )
    args = parser.parse_args()

    args.outdir.mkdir(exist_ok=True)
    for i, f in enumerate(args.filelist):

        print(f"File {i+1}/{len(args.filelist)}:", f)
        try:
            if f.suffix == ".txt":
                arrs = [read_txt(f, fill_missing=args.fillmissing)]
            elif f.suffix == ".mcd":  # Generator
                arrs = read_mcd(f, fill_missing=args.fillmissing)
            else:
                raise ValueError("File does not have a valid IMC file extension.")

            # TODO: bubble exceptions from generator
            for arr in arrs:
                outname = f"ROI{arr.ID}_{arr.Description}" if f.suffix == ".mcd" else f.stem
                if "OME-TIFF" in args.type:
                    write_ometiff(arr, args.outdir / f"{outname}.ome.tiff",
                                compress=args.compress)
                if "TIFF (Individual Channels)" in args.type:
                    (args.outdir / outname).mkdir()
                    write_individual_tiffs(arr, args.outdir / outname, compress=args.compress)
        except Exception as e:
            print(e)
            continue


if __name__ == "__main__":
    main()