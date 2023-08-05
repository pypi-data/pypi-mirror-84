#!/usr/bin/python3

from .__init__ import __doc__ as description, __version__ as version
from os.path import abspath, expanduser, exists, isfile
from sys import argv, exit
from argparse import ArgumentParser as Parser, RawDescriptionHelpFormatter as Formatter
from pdfrw import PdfReader, PdfWriter

# classes

class args:
    "container for arguments"
    pass

# constants

infinite = 999999999

# generic functions

def ask(question, allowed_answers):
    "return answer to a question at terminal"
    while True:
        answer = input(question).strip()
        if answer in allowed_answers:
            return answer

def checksource(source, ext=""):
    "check source file and return it as absolute path"
    source = abspath(expanduser(source))
    if not source.endswith(ext):
        exit(f"ERROR: source {source!r} doesn't end with {ext!r}")
    elif not exists(source):
        exit(f"ERROR: source {source!r} doesn't exist")
    elif not isfile(source):
        exit(f"ERROR: source {source!r} exists but is not a file")
    else:
        return source
        
def checktarget(target, ext="", yes=False, no=False):
    "check target file and return it as absolute path"
    if yes and no:
        exit("ERROR: you can't give both -y and -n arguments")
    target = abspath(expanduser(target))
    if not target.endswith(ext):
        exit(f"ERROR: target {target!r} doesn't end with {ext!r}")
    elif exists(target):
        if not isfile(target):
            exit(f"ERROR: target {target!r} exists and is not a file")
        elif no or not yes and ask(f"target file {target!r} exists, overwrite? [y/n] --> ", ["y","n"]) == "n":
            exit(f"ERROR: target file {target!r} exists, not overwritten")
    return target

def show(lines):
    "for line in lines: print(line.rstrip())"
    for line in lines:
        print(line.rstrip())

# specific functions

def choice2azaz(choice):
    """>>> choice2azaz("23,23-34,23-n,n-34,n,n-n")
[(23, 23), (23, 34), (23, 0), (0, 34), (0, 0), (0, 0)]"""
    status = 0; azaz = []
    for char in choice + ",":
        if status == 0:
            if "1" <= char <= "9":
                a = ord(char) - 48; status = 1
            elif char == "n":
                a = 0; status = 2
            else:
                exit(f"ERROR: syntax error in {choice!r} near {char!r}")
        elif status == 1:
            if "0" <= char <= "9":
                a = a * 10 + ord(char) - 48
            elif char == "-":
                status = 3
            elif char == ",":
                azaz.append((a, a)); status = 0
            else:
                exit(f"ERROR: syntax error in {choice!r} near {char!r}")
        elif status == 2:
            if char == "-":
                status = 3
            elif char == ",":
                azaz.append((a, a)); status = 0
            else:
                exit(f"ERROR: syntax error in {choice!r} near {char!r}")
        elif status == 3:
            if "1" <= char <= "9":
                z = ord(char) - 48; status = 4
            elif char == "n":
                z = 0; status = 5
            else:
                exit(f"ERROR: syntax error in {choice!r} near {char!r}")
        elif status == 4:
            if "0" <= char <= "9":
                z = z * 10 + ord(char) - 48
            elif char == ",":
                azaz.append((a, z)); status = 0
            else:
                exit(f"ERROR: syntax error in {choice!r} near {char!r}")
        elif status == 5:
            if char == ",":
                azaz.append((a, z)); status = 0
            else:
                exit(f"ERROR: syntax error in {choice!r} near {char!r}")
    if status != 0:
        exit(f"ERROR: syntax error in {choice!r} near end")
    return azaz

# main functions
    
def catpdf(argv):
    "CAT function for PDF files"

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
    sources, azazs = [], []
    for source_choice in args.source:
        nsemicolons = source_choice.count(":")
        if nsemicolons == 0:
            source, choice = source_choice, "1-n"
        elif nsemicolons == 1:
            source, choice = source_choice.split(":")
        else:
            exit(f"ERROR: syntax error in {source_choice!r} near ':'")
        sources.append(checksource(source, ext=".pdf"))
        azazs.append(choice2azaz(choice))
    target = checktarget(args.target, ext=".pdf", yes=args.yes, no=args.no)
    for source in sources:
        if source == target:
            exit(f"ERROR: source = {source!r} = target, but they can't be the same")

    # open target, scan sources
    writer = PdfWriter()
    target_pages = 0
    for source, azaz in zip(sources, azazs):
    
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
        for a, z in azaz:
            a = a or source_pages
            z = z or source_pages
            if min(a, z) <= source_pages:
                start, stop, step = (a, min(source_pages, z) + 1, 1) if a <= z else (min(source_pages, a), z - 1, -1) 
                for jpage in range(start, stop, step):
                    writer.addpage(pages[jpage-1])
                    copied_pages += 1
                    target_pages += 1
                    if args.verbose:
                        print(jpage, end=" ")
        if args.verbose:
            print(f"\ncopied {copied_pages} pages from source {source!r} into target {target!r}")

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
