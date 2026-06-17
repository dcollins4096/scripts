#!/usr/bin/env python

import pdb
import os
import glob
import shutil
import bibtexparser
import numpy as np
from optparse import OptionParser

def munch_n_deep(string, n):
    out = ''
    count = 0
    for c in string:
        if c == '}':
            count -= 1
        if count > n:
            out += c
        if c == '{':
            count += 1
        if count == n and len(out) > 0:
            return out

def munch_special(string):
    special = ''
    count = 0
    full = ''
    n = 1
    for c in string:
        if c == '}':
            count -= 1
            full += special[-1] if special else ''
            special = ''
            continue
        elif c == '{':
            count += 1
            continue
        elif c in (' ', "'"):
            continue
        if count >= n:
            special += c
        else:
            full += c
    return full

def parse_and(author):
    some = author.split(' and ')
    if some == author:
        return None
    tokens = some[0].split(',')
    last_name = tokens[0].strip().lstrip('{').rstrip('}')
    return last_name

def sanitize_author(author):
    ok = parse_and(author)
    ok = munch_special(ok)
    if ok is not None:
        return ok
    S1 = munch_n_deep(author, 1)
    if S1 is None:
        S2 = author.lstrip('{').strip()
        if ',' in S2:
            index = S2.index(',')
        elif '}' in S2:
            index = S2.index('}')
        else:
            index = len(S2)
        S1 = S2[:index].strip().rstrip('}')
    FirstAuthor = munch_special(S1)
    return FirstAuthor

def parse_file(fname):
    with open(fname, 'r') as fptr:
        lines = fptr.readlines()

    entries = []
    taking = False
    for line in lines:
        if line.startswith('@'):
            taking = True
            this_entry = ''
        if taking:
            this_entry += line
        if line.startswith('}'):
            taking = False
            entries.append(this_entry)
    return entries

def read(fname):
    entries = parse_file(fname)
    library = {}
    for nentry, entry in enumerate(entries):
        try:
            e = bibtexparser.loads(entry)
        except Exception as ex:
            print(f"Error parsing entry {nentry}: {ex}")
            continue
        if not e.entries:
            continue

        ee = e.entries[0]
        author_all = ee.get('author', '')
        year = ee.get('year', '0000')
        title = ee.get('title', 'untitled')

        first_author = sanitize_author(author_all)
        library.setdefault(first_author, {}).setdefault(year, {})[title] = e
    return library

def write(library, fname):
    authors = sorted(list(library.keys()))
    output = ""
    for author in authors:
        years = sorted(list(library[author].keys()))
        for year in years:
            keys = [entry.entries[0].get('ID', '') for entry in library[author][year].values()]
            titles = np.array([entry.entries[0].get('title', 'untitled') for entry in library[author][year].values()])
            order = np.argsort(keys)
            for title in titles[order]:
                e = library[author][year][title]
                output += bibtexparser.dumps(e)
    with open(fname, 'w') as fptr:
        fptr.write(output)

if __name__ == '__main__':
    default_input_file = f"{os.environ['HOME']}/Downloads/export-bibtex.bib"
    parser = OptionParser("addbib.py -o <output=ms.bib> -i <input=~/Downloads/export-bibtex.bib>; url given precedence.")
    parser.add_option("-o", "--outfile", dest="outfile", action="store", default="m2.bib")
    parser.add_option("-i", "--infile", dest="infile", action="store", default=default_input_file)
    parser.add_option("-t", "--test", dest="test", action="store_true", default=False)
    parser.add_option("-l", "--lookup", dest="lookup", action="store", default=None)
    parser.add_option("-c", "--clean", dest="clean", action="store_true", default=True)

    (options, args) = parser.parse_args()

    if not os.path.exists(options.infile):
        print(f"ERROR: no extant input file {options.infile}")
        exit(1)

    input_library = read(options.infile)

    if options.lookup:
        pass
    else:
        if os.path.exists(options.outfile):
            output_library = read(options.outfile)
        else:
            print(f"No extant output file {options.outfile}, creating new one")
            output_library = {}

        for author in input_library:
            output_library.setdefault(author, {})
            for year in input_library[author]:
                output_library[author].setdefault(year, {})
                key_offset = len(output_library[author][year])
                new_title = 0
                for ntitle, title in enumerate(input_library[author][year]):
                    if title not in output_library[author][year]:
                        ee = input_library[author][year][title]
                        year_val = ee.entries[0].get('year', '0000')
                        ntotal = key_offset + new_title
                        new_title += 1
                        this_key = (author + year_val[-2:] + ' bcdefghijklmnopqrstuvwxyz'[ntotal]).strip()
                        print("NEW", this_key)
                        ee.entries[0]['ID'] = this_key
                        output_library[author][year][title] = ee
        write(output_library, options.outfile)

    clean = ((options.clean is True) + (options.clean == 'True')) * (options.lookup is None)
    if clean:
        if not os.path.exists("old_bibs"):
            os.mkdir("old_bibs")
        n_bibs = len(glob.glob("old_bibs/*"))
        to_this = f"old_bibs/old.bib.{n_bibs}"
        shutil.move(options.infile, to_this)

