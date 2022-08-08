#!/usr/bin/env python
import random
import pdb
import sys

people=['Marguerite','David','Anne','Amanda','Patrick','Maggie','Mike','Steve']
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
Spouse['Amanda'] = 'Steve'
Spouse['Steve'] = 'Amanda'
#Spouse['Daniel'] = 'Anne'
No={}
for P in people:
    No[P] = [P]
    if Spouse[P]:
        No[P] += [Spouse[P]]

if 0:
    #debug
    for P in No:
        print("%s:"%P,)
        for O in No[P]:
            print(O,)
    sys.exit(0)

#hat.append(hat.pop(0))
#hat.append(hat.pop(0))
put_back=[]
for P in people:
    print("===",P)
    while len(WhoGotWho[P]['got']) < 2:  #Two and only two.
        if len(hat) == 0:
            print("ERROR Hat failure")
            raise
        
        NUM = random.choice(list(range(len(hat))))
        other_person = hat.pop(NUM)      #Pull from the hat.
        if debug > 0:
            print("   ", other_person, end=' ')

        if other_person in No[P]:
            #hat.append(other_person)     #Back in the hat!
            put_back.append(other_person)
            #random.shuffle(hat)
            continue
            print("nope (%s) "%other_person, end=' ')
        print(" y (%s)"%other_person)
        WhoGotWho[P]['got'].append(other_person)
        #Can't get the person again, 
        #neither can the spouse
        No[P].append(other_person)
        if Spouse[P]:
            No[Spouse[P]].append(other_person)
        if debug > 0:
            print(P, WhoGotWho[P]['got'], hat)
    hat+= put_back
    put_back=[]
for P in people:
    print("%s has  %s and %s"%(P, WhoGotWho[P]['got'][0], WhoGotWho[P]['got'][1]))
#end
