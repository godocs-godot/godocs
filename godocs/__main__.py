from argparse import ArgumentParser
import sys

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

  # Show help if no arguments were provided
  if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(0)

  args = parser.parse_args()

  print(args)

if __name__ == "__main__":
  main()
