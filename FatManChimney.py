#!/usr/bin/env python
import random
import pdb
import sys

people=['Anne','David','Marguerite','Patrick','Maggie','Mike','Steve']
hat=people+people
debug = 0
#The list.  Set it up. ['got'] is who you got.
WhoGotWho={}    # this is a 'dictionary'.  It's like a rolodex.
for P in people:
    WhoGotWho[P] = {}    # excpet you can't have a rolodex on your rolodex card.  Yo dawg.
    WhoGotWho[P]['got']=[]

#No Spouses.
Spouse={}
for P in people:
    Spouse[P] = None
Spouse['Marguerite'] = 'David'
Spouse['David'] = 'Marguerite'
Spouse['Maggie'] = 'Mike'
Spouse['Mike'] = 'Maggie'
#Spouse['Daniel'] = 'Anne'
No={}
for P in people:
    No[P] = [P]
    if Spouse[P]:
        No[P] += [Spouse[P]]

for P in people:
    print P
    while len(WhoGotWho[P]['got']) < 2:  #Two and only two.
        NUM = random.choice(range(len(hat)))
        other_person = hat.pop(NUM)      #Pull from the hat.
        if debug > 0:
            print "   ", other_person,
        if other_person in No[P]:
            if len(hat) == 0:
                print "Hat failure"
                raise
            hat.append(other_person)     #Back in the hat!
            #continue
            print "nope",
            if len(hat):
                continue
            else:
                print "Failure!"
                sys.exit(1)


        if debug > 0:
            print "yay",
        WhoGotWho[P]['got'].append(other_person)
        No[P].append(other_person)
        if Spouse[P]:
            No[Spouse[P]].append(other_person)
        if debug > 0:
            print P, WhoGotWho[P]['got'], hat
for P in people:
    print "%s has  %s and %s"%(P, WhoGotWho[P]['got'][0], WhoGotWho[P]['got'][1])
#end
