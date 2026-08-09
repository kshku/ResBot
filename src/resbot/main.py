from dotenv import load_dotenv

load_dotenv()

def analyze(args):
    print("analyzing...")

def generate(args):
    print("generating...")

def edit(args):
    print("editing...")

def main():
    import argparse as ap
    from importlib.metadata import metadata

    resbot = metadata('resbot')

    parser = ap.ArgumentParser(prog=resbot["Name"], description=resbot["Summary"])

    parser.add_argument("--version", action="version", version="%(prog)s " + resbot["Version"])

    subparsers = parser.add_subparsers(dest="command", required=True, help="What to do")

    analyze_parser = subparsers.add_parser("analyze", help="Analyze the resume for JD and give score")
    analyze_parser.set_defaults(handler=analyze)
    analyze_parser.add_argument("resume", help="The resume")
    analyze_parser.add_argument("jd", help="The Job Description")

    generate_parser = subparsers.add_parser("generate", help="Generate a resume for given JD")
    generate_parser.set_defaults(handler=generate)
    generate_parser.add_argument("jd", help="The Job Description")

    edit_parser = subparsers.add_parser("edit", help="Edit a resume")
    edit_parser.set_defaults(handler=edit)
    edit_parser.add_argument("resume", help="The resume to edit")

    args = parser.parse_args()
    args.handler(args)

if __name__ == "__main__":
    main()
