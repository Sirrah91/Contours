import numpy as np
import argparse
from glob import glob
from os import path

from scr.devtools.parser import CustomArgumentParser, CustomFormatter, inplace_process_nargs1_args


if __name__ == "__main__":
    parser = CustomArgumentParser(
        allow_abbrev=False,
        add_help=False,
        description="Calculate memory requirements to process sunspot contours.\n\n"
                    "Example:\n"
                    "  python job_sizes.py --data_dir /path/to/data",
        formatter_class=CustomFormatter
    )

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
        help="Directory containing input files."
    )

    # Create a proper "optional arguments" group for help
    optional = parser.add_argument_group("optional arguments")
    optional.add_argument(
        "-h", "--help",
        action="help",
        default=argparse.SUPPRESS,
        help="Show this help message and exit."
    )

    # To be able to pass all ${SETTINGS}
    args, _ = parser.parse_known_args()

    # convert list[arg] to arg
    inplace_process_nargs1_args(
        parser=parser,
        args=args
    )

    filename_list = glob(path.join(args.data_dir, "*"))
    mem_gb_per_quantity = 0.
    for filename in filename_list:
        if not path.isfile(filename):
            continue
        bare_filename = path.split(filename)[1]
        no_quantities = len(bare_filename.split(".")[-2])
        mem_gb_per_quantity += path.getsize(filename) / no_quantities if no_quantities > 0 else 0.
    mem_gb_per_quantity /= 1024.0 ** 3

    # print usage for qsub
    print(f"{np.clip(np.ceil(mem_gb_per_quantity * 1.5), a_min=1., a_max=None):.0f}")
