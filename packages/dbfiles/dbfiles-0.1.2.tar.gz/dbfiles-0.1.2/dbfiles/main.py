import os
import argparse
import yaml

from dbfiles.schema import Schema
from dbfiles.compiler import Compiler



def parseArgs():
    parser = argparse.ArgumentParser(prog="dbfiles")

    parser.add_argument("--src-root", dest="srcRoot", default=os.path.abspath(os.getcwd()))
    parser.add_argument("--dst-root", dest="dstRoot", default=os.path.abspath(os.getcwd()))
    parser.add_argument("--schemas", nargs="*", dest="schemas", required=True)
    parser.add_argument("--force", dest="force", action="store_true", default=False)
    parser.add_argument("--debug", dest="debug", action="store_true", default=False)

    return parser.parse_args()


def main():
    args = parseArgs()

    Schema.setRoot(args.srcRoot)
    compiler = Compiler(args.dstRoot, args.force, args.debug)

    for schemaPath in args.schemas:
        schema = Schema(schemaPath)
        compiler.add(schema)

    compiler.createEntry()

if __name__ == "__main__":
    main()
