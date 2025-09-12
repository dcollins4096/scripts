#!/usr/bin/env python3

import re
import sys
import os
import pdb
from optparse import OptionParser
import difflib
import csv

parser = OptionParser(usage="usage: %prog [options] quiz_name.csv")
parser.add_option("-g","--gradebook",action="store",default="gradebook.csv", help="Main grade book for student list")
parser.add_option("-v","--verbose",action="store_true",default=False, help="Verbose.  Say which names are altered by the script")
parser.add_option("-q","--quiz",action="store",default="Quiz 1", help="Column header in gradebook to update.")
parser.add_option("-m","--missing",action="store",default="", help="Value for missing students")
(options,args)=parser.parse_args()


if len(args) == 0:
    parser.print_help()
    sys.exit(1)

this_quiz_fname = args[0]
if 0: #not used
    name_parts = this_quiz_fname.split(".")
    output_name = name_parts[0] + "_parsed." + name_parts[1]

verbose = options.verbose
gradebook = options.gradebook
quiz = options.quiz
missing = options.missing

if not os.path.exists(gradebook):
    print("Gradebook does not exist: %s"%options.gradebook)
    sys.exit(1)

#read gradebook
gradebook_lines=[]
with open(gradebook,newline="", encoding="utf-8-sig") as f:
    reader = csv.reader(f)
    for row in reader:
        gradebook_lines.append(row)

#read all names from gradebook
main_names = []
gradebook_key={}
for nline,line in enumerate(gradebook_lines):
    if not len(line):
        continue
    if nline > 2:
        name = line[0].split(',')
        last = name[0].upper().strip()
        first = name[1].upper().strip()
        parsed_name="%s %s"%(last,first)
        main_names.append(parsed_name)
        gradebook_key[parsed_name] = nline


#find column
ncolumn = -1
for icolumn, column in enumerate(gradebook_lines[0]):
    if column.startswith(quiz):
        ncolumn = icolumn
        break
if ncolumn < 0:
    print(" Cannot find column that starts with %s"%quiz)
    sys.exit(0)

fptr = open(this_quiz_fname)
quiz_lines = fptr.readlines()
fptr.close()
        
#get the answers. Not actually used in the rest of the script, but maybe you need it elsewhere.
quiz_answers = []
quiz_key = quiz_lines[2].split(',')
for token in quiz_key[2:]:
    if len(token.strip())>0:
        quiz_answers.append(token)
nquestions = len(quiz_answers)

#parse the student answers.
student_work={}
student_names=[]
student_number={}
for nl, line in enumerate(quiz_lines[3:]):
    lll = line.split(',')
    name_element = len(quiz_answers)+2
    qname=lll[name_element].strip()
    student_names.append(qname)
    grade = 0
    for q,token in enumerate(lll[2:2+nquestions]):
        if token == quiz_answers[q]:
            grade += 1
    student_work[qname]=grade
    student_number[qname] = lll[0]

#Match students that spelled their names right
final_grades = {}
import copy
remaining_main = set(main_names)
for name in main_names:
    if name in student_work:
        #grade = student_work[name]
        final_grades[name] = student_work[name]
        student_work.pop(name)
        remaining_main.remove(name)

remaining_main = list(remaining_main)

#spell check the students that can't spell their names
cutoff = 0.6
altered={}
remaining_names = sorted(list(student_work.keys()))
for name in remaining_names:
    if len(name) == 0:
        print("There is at least one quiz without a name, see the error pdf to find out if they just forgot to bubble it in.")
        continue
    close_match = difflib.get_close_matches(name, remaining_main, n=1, cutoff=cutoff)
    if len(close_match) == 1:
        match_name = close_match[0]
        altered[name] = match_name
        final_grades[match_name]=student_work[name]
        student_work.pop(name)
        if verbose:
            print("%20s -> %20s"%(name, match_name))
    elif len(close_match) == 0:
        #try swapping first and last names.

        if " " in name:
            ind = name.index(" ")
            swapped = name[ind:] + " " + name[:ind]
            next_match = difflib.get_close_matches(swapped, remaining_main, n=1, cutoff=cutoff)
            if verbose:
                print("%20s -> %20s"%(name, swapped))
        else: 
            next_match=[]
        if len(next_match) == 1:
            final_grades[next_match[0]] = student_work[name]
            altered[name] = next_match[0]
        else:
            print("Really can't find", name, "quiz number", student_number[name])
    elif len(close_match) > 1:
        print("Multiple match, please address manually", name, close_match)


#write one csv with just this quiz
if 0:
    fptr = open(output_name,'w')
    for name in main_names:
        grade = final_grades.get(name,missing)
        fptr.write("%s,%s\n"%(name,str(grade)))
    fptr.close()

#write the whole grade book
for name in main_names:
    extant_grade = gradebook_lines[ gradebook_key[ name] ][ncolumn] 
    new_grade = final_grades.get(name, missing)
    if len(extant_grade) > 0:
        if float(extant_grade) != float(new_grade):
            print("%20s %s %s"%(name, extant_grade, new_grade))
    gradebook_lines[ gradebook_key[ name] ][ncolumn] = new_grade

with open("output.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(gradebook_lines)



if 0:
    print("Names that dont make sense")
    print('-------------------')
    for name in student_work:
        print(name)
    print('-------------------')
    print("Missing Students")
    print('-------------------')
    all_set = set(main_names)
    took_set = set(student_names)
    skipped=all_set-took_set
    skipped = sorted(list(skipped))
    for kid in skipped:
        print(kid)
    print('-------------------')


