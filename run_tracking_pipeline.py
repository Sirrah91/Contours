from glob import glob
from os import path
import argparse
import socket

from scr.config.naming import SEP_OUT, SEP_IN
from scr.config.paths import PATH_CONTOURS

from scr.devtools.parser import CustomArgumentParser, CustomFormatter, inplace_process_nargs1_args, print_args, farewell

from scr.utils.filesystem import check_dir

from scr.io.fits.stack import load_fits_stack
from scr.io.tracks import save_tracks_and_stats

from scr.pipelines.processing.tracking import track_and_merge_sunspots


if __name__ == "__main__":
    hostname = socket.gethostname()
    print(f"Running on: {hostname}\n")

    parser = CustomArgumentParser(
        allow_abbrev=False,
        add_help=False,
        description="Extract and track contours from AR data based on user-defined "
                    "thresholds and conditions.\n\n"
                    "Example:\n"
                    "  python run_contour_tracking.py --data_dir /path/to/fits --contour_quantity Ic "
                    "--penumbra_threshold 0.9 --umbra_threshold 0.5 --pore_threshold 0.65",
        formatter_class=CustomFormatter)

    # Positional arguments
    positional = parser.add_argument_group("positional arguments")

    # Required arguments
    required = parser.add_argument_group("required arguments")

    # Core options
    core = parser.add_argument_group("core settings")
    core.add_argument(
        "--data_dir",
        type=str,
        required=True,
        nargs=1,
        help="Directory containing input FITS files."
    )

    # Contour extraction settings
    contour = parser.add_argument_group("contour extraction")
    contour.add_argument(
        "--contour_quantity",
        type=str,
        required=True,
        nargs=1,
        choices=["Ic", "B", "Bp", "Bt", "Br", "Bhor", "1", "2", "3", "4", "33"],
        help="Quantity used to compute the contour."
    )
    contour.add_argument(
        "--penumbra_threshold",
        type=float,
        required=True,
        nargs=1,
        help="Threshold value to define the penumbra contour."
    )
    contour.add_argument(
        "--umbra_threshold",
        type=float,
        required=True,
        nargs=1,
        help="Threshold value to define the umbra contour."
    )
    contour.add_argument(
        "--pore_threshold",
        type=float,
        required=True,
        nargs=1,
        help="Threshold value to define the pore contour."
    )

    # Filtering based on area and persistence
    filtering = parser.add_argument_group("filtering options")
    filtering.add_argument(
        "--min_area",
        type=float,
        default=5.0,
        nargs=1,
        help="Minimum contour area in pixels² for contours to be considered."
    )
    filtering.add_argument(
        "--max_gap",
        type=int,
        default=3,
        nargs=1,
        help="Maximum number of consecutive frames a tracked contour can be absent and "
             "still be considered part of a valid track."
    )
    filtering.add_argument(
        "--min_frames",
        type=int,
        default=0,
        nargs=1,
        help="Minimum number of image frames in which the contour must appear."
    )

    # Morphology and contour merging
    morph = parser.add_argument_group("morphology and merging")
    morph.add_argument(
        "--iou_threshold",
        type=float,
        default=0.3,
        nargs=1,
        help="Minimum IoU (Intersection over Union) required to merge two contours into one region."
    )
    morph.add_argument(
        "--min_containment",
        type=float,
        default=0.8,
        nargs=1,
        help="Minimum containment ratio required to consider one region inside another."
    )
    morph.add_argument(
        "--registration",
        action="store_true",
        help="Enable image alignment (registration) before contour tracking."
    )

    # Output options
    output = parser.add_argument_group("output options")
    output.add_argument(
        "--outdir",
        type=str,
        default=PATH_CONTOURS,
        nargs=1,
        help="Output directory for saving results."
    )
    output.add_argument(
        "--save_name",
        type=str,
        default="",
        nargs=1,
        help="Base name for saved output files. If empty, it is construct from other inputs."
    )

    # Create a proper "optional arguments" group for help
    optional = parser.add_argument_group("optional arguments")
    optional.add_argument(
        "-h", "--help",
        action="help",
        default=argparse.SUPPRESS,
        help="Show this help message and exit."
    )

    args = parser.parse_args()

    # convert list[arg] to arg
    inplace_process_nargs1_args(
        parser=parser,
        args=args
    )

    check_dir(args.outdir)

    if isinstance(args.contour_quantity, str) and args.contour_quantity.isdigit():
        args.contour_quantity = int(args.contour_quantity)

    if not args.save_name:
        args.save_name = (
            f"{args.contour_quantity}{SEP_IN}"
            f"{args.penumbra_threshold}{SEP_IN}"
            f"{args.umbra_threshold}{SEP_OUT}"
            f"{path.basename(path.normpath(args.data_dir))}"
            f".npz")

    print_args(args)

    args.filename_list = sorted(glob(path.join(f"{args.data_dir}", "*.fits")))
    images = load_fits_stack(
        args.filename_list,
        args.contour_quantity,
        allow_inhomogeneous_shape=True
    )

    tracks = track_and_merge_sunspots(
        images=images,
        outer_level=args.penumbra_threshold,
        middle_level=args.pore_threshold,
        inner_level=args.umbra_threshold,
        min_area=args.min_area,
        max_gap=args.max_gap,
        min_frames=args.min_frames,
        iou_threshold=args.iou_threshold,
        min_containment=args.min_containment,
        registration=args.registration
    )

    # Save track dictionary to a compressed file
    contour_file = path.join(args.outdir, args.save_name)
    save_tracks_and_stats(
        filename=contour_file,
        tracks=tracks,
        stats={},
        metadata=vars(args)
    )

    farewell()
