from .__init__ import *

import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dir", help="select directory")
ap.add_argument("-e", "--ext", nargs='+', help="search certain file types")
ap.add_argument("-v", "--verbose", action="store_true", help="show detailed log")

args = ap.parse_args()

run(args.dir, args.ext and [(ext, CodeGenCtx) for ext in args.ext], args.verbose)