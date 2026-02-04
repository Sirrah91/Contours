from glob import glob
from os import path
import argparse
import socket

from scr.devtools.parser import CustomArgumentParser, CustomFormatter, inplace_process_nargs1_args, print_args, farewell

from scr.pipelines.processing.postprocessing import compute_phase_split


if __name__ == "__main__":
    hostname = socket.gethostname()
    print(f"Running on: {hostname}\n")

    parser = CustomArgumentParser(
        allow_abbrev=False,
        add_help=False,
        description="Split track contours to evolutionary phases.\n\n"
                    "Example:\n"
                    "  python run_split_to_phases.py --contour_dirname /path/to/contours --mode sunspots",
        formatter_class=CustomFormatter
    )

    # Positional arguments
    positional = parser.add_argument_group("positional arguments")

    # Required arguments
    required = parser.add_argument_group("required arguments")
    required.add_argument(
        "--contour_dirname",
        type=str,
        required=True,
        nargs=1,
        help="Directory containing input contour files."
    )
    required.add_argument(
        "--mode",
        type=str,
        required=True,
        nargs=1,
        choices=["sunspots", "pores"],
        help="What type of measurements is processed."
    )

    slope_opts = parser.add_argument_group("slope arguments")
    slope_opts.add_argument(
        "--collect_new_slopes",
        action="store_true",
        help="Flag to trigger new slope computation."
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

    print_args(args)

    # This function saves outputs to disk as a side effect and also returns them.
    _, _ = compute_phase_split(
        contour_files=sorted(glob(path.join(args.contour_dirname, "*.npz"))),
        mode=args.mode,
        collect_new_slopes=args.collect_new_slopes
    )

    farewell()
