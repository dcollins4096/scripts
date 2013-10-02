#!/usr/bin/env python
import random
people=['Anne','David','Marguerite','Patrick','Steve','Maggie','Mike']
hat=['Anne','David','Marguerite','Patrick','Steve','Maggie','Mike','Anne','David','Marguerite','Patrick','Steve','Maggie','Mike']
debug = 0
#The list.  Set it up. ['got'] is who you got, ['count'] is how many you get
WhoGotWho={}    # this is a 'dictionary'.  It's like a rolodex.
for P in people:
    WhoGotWho[P] = {}    # excpet you can't have a rolodex on your rolodex card.  Yo dawg.
    WhoGotWho[P]['count']=0
    WhoGotWho[P]['got']=[]

#No Spouses.
No={}
No['Marguerite'] = ['David']
No['David'] = ['Marguerite']
No['Maggie'] = ['Mike']
No['Mike'] = ['Maggie']

for P in people:
    while len(WhoGotWho[P]['got']) < 2:  #Two and only two.
        NUM = random.choice(range(len(hat)))
        other_person = hat.pop(NUM)      #Pull from the hat.
        if other_person == P:            #Can't have your self
            hat.append(other_person)     #Back in the hat!
            continue
        if other_person in WhoGotWho[P]['got']:  #Can't have someone twice
            hat.append(other_person)
            continue
        if No.has_key(P):                #No spouses.  (Yay Maggie and Mike!)
            if other_person in No[P]:
                hat.append(other_person)
                continue

        WhoGotWho[P]['got'].append(other_person)
        WhoGotWho[other_person]['count'] += 1
        if debug > 0:
            print P, WhoGotWho[P]['got'], hat
for P in people:
    print P, WhoGotWho[P]['got']
#end
