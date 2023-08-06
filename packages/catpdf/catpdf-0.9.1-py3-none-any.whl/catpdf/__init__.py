"""conCATenate one or more source PDF files (or pieces of) into a target PDF file

syntax of positional arguments:

    <source>   ::= [<path>/]<file>.pdf[:<choice>]
    <choice>   ::= <interval>[,<interval>]*
    <interval> ::= <index>[-<index>]
    <index>    ::= <integer>|n
    <integer>  ::= 1..9[0..9]*
    
    <target>   ::= [<path>/]<file>.pdf

explanation:

    each source is made by:

        an optional path followed by '/'
        a file name followed by '.pdf' extension
        an optional choice preceded by ':' (default: ':1-n')

    the choice is a comma-separated list of one or more intervals

    each interval is made by:

        an index of a single page
        or two indexes separated by '-' (meaning first and last page)
       
    each index is:

        a positive integer constant (leading zeros not allowed)
        or a single lowercase 'n' letter (meaning the number of pages in source file)

examples:

    $ catpdf a.pdf b.pdf c.pdf

concatenate a.pdf and b.pdf into c.pdf

    $ catpdf a.pdf:1-10,95-n b.pdf:50-40 c.pdf

concatenate a.pdf (first 10 pages and from page 95 until the end of file)
and b.pdf (from page 50 backwards until page 40) into c.pdf"""

__version__ = "0.9.1"
