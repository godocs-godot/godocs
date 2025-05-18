from argparse import ArgumentParser
import sys
import json

from parser import parse as xml_parser, create_context

def main():
  parser = ArgumentParser(
    description="The Godocs CLI can parse the XML files generated from Godot's documentation into other types of files.",
    argument_default="-h",
  )

  parser.add_argument(
    "src",
    help="The path from where Godot XML documentation files should be read.",
    type=str,
  )
  parser.add_argument(
    "build",
    help="The path where the generated documentation should be saved.",
    type=str,
  )
  parser.add_argument(
    "-c", "--constructor",
    help="The type of constructor that should be used to generate the documentation. (default: %(default)s)",
    type=str,
    default="rst",
    choices=[ "rst" ],
  )
  parser.add_argument(
    "-p", "--ref-prefix",
    help="The prefix to use on :ref: roles generated on output RST (used when --constructor is 'rst'). (default: %(default)s)",
    type=str,
    default="godocs",
  )

  # Show help if no arguments were provided
  if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(0)

  args = parser.parse_args()

  parsed_docs = xml_parser(args.src)

  context = create_context(parsed_docs, { "ref_prefix": args.ref_prefix })

  print(json.dumps(context, indent="  "))

if __name__ == "__main__":
  main()
