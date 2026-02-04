import argparse
import socket

from scr.config.naming import SEP_OUT, SEP_IN

from scr.devtools.parser import CustomArgumentParser, CustomFormatter, inplace_process_nargs1_args, print_args, farewell

from scr.io.tracks import save_tracks_and_stats

from scr.pipelines.processing.stats_computation import compute_stats_from_contours


if __name__ == "__main__":
    hostname = socket.gethostname()
    print(f"Running on: {hostname}\n")

    parser = CustomArgumentParser(
        allow_abbrev=False,
        add_help=False,
        description="Recompute statistics.\n\n"
                    "Example:\n"
                    "  python run_calc_stats.py --contour_file /path/to/contours/contour_file.npz "
                    "--quantities Ic --stat_types sunspots",
        formatter_class=CustomFormatter
    )

    # Positional arguments
    positional = parser.add_argument_group("positional arguments")

    # Required arguments
    required = parser.add_argument_group("required arguments")
    required.add_argument(
        "--contour_file",
        type=str,
        required=True,
        nargs=1,
        help="Directory containing input contour files."
    )
    required.add_argument(
        "--quantities",
        type=str,
        choices=["Ic", "B", "Bp", "Bt", "Br", "Bhor"],
        required=True,
        nargs="+"
    )
    required.add_argument(
        "--stat_types",
        type=str,
        choices=["sunspots", "pores"],
        required=True,
        nargs="+"
    )

    # Contour settings
    contour = parser.add_argument_group("contour sampling")
    contour.add_argument(
        "--header_index",
        type=int,
        default=0,
        nargs=1,
        help="Header index to use for the foreshortening correction."
    )
    contour.add_argument(
        "--min_step",
        type=float,
        default=0.5,
        nargs=1,
        help="Minimum step between two contour vertices before sampling a map."
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

    tracks, stats, metadata = compute_stats_from_contours(
        contour_file=args.contour_file,
        quantities=args.quantities,
        stat_types=args.stat_types,
        header_index=args.header_index,
        min_step=args.min_step,
    )

    save_tracks_and_stats(
        filename=args.contour_file.replace(
            ".npz",
            (
                f"{SEP_OUT}{f'{SEP_IN}'.join(args.quantities)}"
                f"{SEP_OUT}{f'{SEP_IN}'.join(args.stat_types)}"
                f".npz"
            )
        ),
        tracks=tracks,
        stats=stats,
        metadata=metadata
    )

    farewell()
