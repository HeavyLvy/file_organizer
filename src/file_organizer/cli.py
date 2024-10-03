import argparse
import sys


def main():
    parser = argparse.ArgumentParser(description="A CLI with subcommands")
    subparsers = parser.add_subparsers(help="sub-command help")

    load_parser = subparsers.add_parser("load", help="Load data")
    load_parser.add_argument("filename", help="Input filename")

    list_parser = subparsers.add_parser("list", help="List data")

    save_parser = subparsers.add_parser("save", help="Save data")
    save_parser.add_argument("filename", help="Output filename")

    args = parser.parse_args()

    # if args.command == 'load':
    #     # Load data using args.filename
    #     print(f"Loading data from: {args.filename}")

    # elif args.command == 'list':
    #     # List data
    #     print("Listing data...")

    # elif args.command == 'save':
    #     # Save data using args.filename
    #     print(f"Saving data to: {args.filename}")

    # else:
    #     parser.print_help()
    #     sys.exit(1)


if __name__ == "__main__":
    main()
