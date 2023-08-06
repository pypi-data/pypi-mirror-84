#!/usr/bin/python3

from .__init__ import __doc__ as description, __version__ as version
from os.path import abspath, expanduser, exists, isfile
from sys import argv, exit
from argparse import ArgumentParser as Parser, RawDescriptionHelpFormatter as Formatter
from pdfrw import PdfReader, PdfWriter
from libfunx import shell_ask, get_source, get_target

# classes

class args:
    "container for arguments"
    pass

# functions

def choice2first_last(choice):
    """>>> choice2first_last("23,23-34,23-n,n-34,n,n-n")
[(23, 23), (23, 34), (23, 0), (0, 34), (0, 0), (0, 0)]"""
    status = 0; first_last = []
    for char in choice + ",":
        if status == 0:
            if "1" <= char <= "9":
                first = ord(char) - 48; status = 1
            elif char == "n":
                first = 0; status = 2
            else:
                exit(f"ERROR: syntax error in {choice!r} near {char!r}")
        elif status == 1:
            if "0" <= char <= "9":
                first = first * 10 + ord(char) - 48
            elif char == "-":
                status = 3
            elif char == ",":
                first_last.append((first, first)); status = 0
            else:
                exit(f"ERROR: syntax error in {choice!r} near {char!r}")
        elif status == 2:
            if char == "-":
                status = 3
            elif char == ",":
                first_last.append((first, first)); status = 0
            else:
                exit(f"ERROR: syntax error in {choice!r} near {char!r}")
        elif status == 3:
            if "1" <= char <= "9":
                last = ord(char) - 48; status = 4
            elif char == "n":
                last = 0; status = 5
            else:
                exit(f"ERROR: syntax error in {choice!r} near {char!r}")
        elif status == 4:
            if "0" <= char <= "9":
                last = last * 10 + ord(char) - 48
            elif char == ",":
                first_last.append((first, last)); status = 0
            else:
                exit(f"ERROR: syntax error in {choice!r} near {char!r}")
        elif status == 5:
            if char == ",":
                first_last.append((first, last)); status = 0
            else:
                exit(f"ERROR: syntax error in {choice!r} near {char!r}")
    if status != 0:
        exit(f"ERROR: syntax error in {choice!r} near end")
    return first_last

# main functions
    
def catpdf(argv):
    "conCATenate one or more source PDF files (or pieces of) into first target PDF file"

    # get arguments
    parser = Parser(prog="catpdf", formatter_class=Formatter, description=description)
    parser.add_argument("-V", "--version", action="version", version=version)
    parser.add_argument("-v", "--verbose", action="store_true", help="show what happens")
    parser.add_argument("-y", "--yes",  action="store_true", help="overwrite existing target file (default: ask)")
    parser.add_argument("-n", "--no",  action="store_true", help="don't overwrite existing target file (default: ask)")
    parser.add_argument("source", nargs="+", help="one or more source files (each with choice or not), followed by...")
    parser.add_argument("target", help="...one target file")
    parser.parse_args(argv[1:], args)
    
    # check arguments
    sources, first_lasts = [], []
    for source_choice in args.source:
        nsemicolons = source_choice.count(":")
        if nsemicolons == 0:
            source, choice = source_choice, "1-n"
        elif nsemicolons == 1:
            source, choice = source_choice.split(":")
        else:
            exit(f"ERROR: syntax error in {source_choice!r} near ':'")
        sources.append(get_source(source, ext=".pdf"))
        first_lasts.append(choice2first_last(choice))
    target = get_target(args.target, ext=".pdf", yes=args.yes, no=args.no)
    for source in sources:
        if source == target:
            exit(f"ERROR: source = {source!r} = target, but they can't be the same")

    # open target, scan sources
    writer = PdfWriter()
    target_pages = 0
    for source, first_last in zip(sources, first_lasts):
    
        # check source content
        try:
            pages = PdfReader(source).pages
            assert pages
        except:
            exit(f"ERROR: source file {source!r} is corrupted or does not contain any pages")
        source_pages = len(pages)
        if args.verbose:
            print(f"source {source!r} contains {source_pages} pages\ncopied:", end=" ")
        
        # source --> target
        copied_pages = 0
        for first, last in first_last:
            first = first or source_pages
            last = last or source_pages
            if min(first, last) <= source_pages:
                start, stop, step = (first, min(source_pages, last) + 1, 1) if first <= last else (min(source_pages, first), last - 1, -1) 
                for jpage in range(start, stop, step):
                    writer.addpage(pages[jpage - 1])
                    copied_pages += 1
                    target_pages += 1
                    if args.verbose:
                        print(jpage, end=" ")
        if args.verbose:
            print(f"\ncopied {copied_pages} pages from source {source!r} ...\n... into target {target!r}")

    # close target
    try:
        writer.write(target)
    except:
        exit(f"ERROR: error writing target file {target!r}")
    if args.verbose:
        print(f"target {target!r} contains {target_pages} pages")
    
def main():
    try:
        catpdf(argv)
    except KeyboardInterrupt:
        print()

if __name__ == "__main__":
    main()
