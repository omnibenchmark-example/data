import argparse
import os

# Output ids this module can write, and the file name each one gets when the
# benchmark does not say (api < 0.8.0).
LEGACY_NAMES = {
    "data.counts": "{name}.txt.gz",
    "data.meta": "{name}.meta.json",
    "data.data_specific_params": "{name}_params.txt",
}


def create_file(file_name):
    os.makedirs(os.path.dirname(file_name) or ".", exist_ok=True)
    with open(file_name, 'w') as outfile:
        outfile.write(f'1. Created dataset file {file_name}.\n')


def main():
    parser = argparse.ArgumentParser(description='Materialize dataset files.')
    parser.add_argument('--output_dir', type=str, help='output directory where dataset files will be saved.')
    parser.add_argument('--name', type=str, help='name of the dataset')
    # api >= 0.8.0: one `--output id=PATH` per output the stage declares.
    parser.add_argument('--output', action='append', default=[], help='id=PATH of an output to write')
    args, _ = parser.parse_known_args()

    outputs = dict(o.split("=", 1) for o in args.output)
    if not outputs:
        outputs = {
            output_id: os.path.join(args.output_dir, pattern.format(name=args.name))
            for output_id, pattern in LEGACY_NAMES.items()
        }

    for output_id, path in outputs.items():
        if output_id not in LEGACY_NAMES:
            raise SystemExit(f"unknown output id '{output_id}'; this module writes {sorted(LEGACY_NAMES)}")
        create_file(path)


if __name__ == "__main__":
    main()
