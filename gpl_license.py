#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import argparse

PY_TAG = "#"
PY_BEGIN_TAG = PY_END_TAG = "###############################################################################"
C_BEGIN_TAG = "/*"
C_END_TAG = "*/"
C_TAG = "*"
LICENSE_TXT = requests.get("https://www.gnu.org/licenses/gpl.txt").text

vals = {"author": "Onur Özüduru",
    "year": "2015",
    "prog_name": "PROGRAM NAME",
    "lang": "C"}

template_license = """    Copyright (C) {year}  {author}

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

template_file_header = """    Copyright (C) {year}  {author}

    This file is part of {prog_name}.

    {prog_name} is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Foobar is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
"""

def save(txt, f_name):
    with open(f_name, "w") as f:
        f.write(txt)

def format_header_for(lang="C"):
    added_tags = ""
    if lang == "C":
        added_tags += C_BEGIN_TAG + "\n"
        for line in template_file_header.splitlines(True):
            added_tags += C_TAG + line
        added_tags += C_END_TAG
        return added_tags
    if lang == "PY":
        added_tags += PY_BEGIN_TAG + "\n"
        for line in template_file_header.splitlines(True):
            added_tags += PY_TAG + line
        added_tags += PY_END_TAG
        return added_tags

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--author", help="Author of the program.")
    parser.add_argument("-y", "--year", help="Year of the program.")
    parser.add_argument("-n", "--name", help="Name of the program.")
    parser.add_argument("-P", "--python", action="store_true", help="Output, LICENSE_FILE_HEADING.txt, will be formatted as Python comment format (Default is in C format.)")
    args = parser.parse_args()
    if args.author:
        vals["author"] = args.author
    if args.year:
        vals["year"] = args.year
    if args.name:
        vals["prog_name"] = args.name
    if args.python:
        vals["lang"] = "PY"
    save(LICENSE_TXT, "LICENSE")
    save(template_license.format(year=vals["year"], author=vals["author"]), "LICENSE_SHORT.txt")
    save(format_header_for(vals["lang"]).format(year=vals["year"], author=vals["author"], prog_name=vals["prog_name"]), "LICENSE_FILE_HEADING.txt")
        
if __name__ == "__main__":
    main()

