#!/usr/bin/env python

import cadac
ts = []
for i in range(0,4):
     ts.append(cadac.Tag(i,'rpwagner'))
 
tl = cadac.TagList(ts)
print tl.toxml()
ps = []
for i in range(0,3):
     ps.append(cadac.Parameter('param'+str(i),i,'http://lca.ucsd.edu/enzo/param'+str(i)))
 
pl = cadac.ParameterList(ps)
print pl.toxml()

p = cadac.Program('Enzo',1052,'svn://mngrid.ucds.edu/Enzo/trunk/devel/Enzo')
us = []

for i in range(0,5):
     us.append(cadac.UserField('mydat'+str(i),10.4*i))
 
ul = cadac.UserFieldList(us)
print ul.toxml()

u = cadac.User('rpwagner','http://lca.ucsd.edu/projects/rpwagner')
c = cadac.Computer('ppcluster','http://ppcluster.ucsd.edu')
r1 = cadac.Run('r1',c,p,u,ul,tl,pl,ToDo='Way too much!',Comments='Disabled')
r2 = cadac.Run('r1',c,p,u,ul,tl,ToDo='Way too much!',Comments='Disabled',Nodes=2,TasksPerNode=8,Account='MUT')
print r1.toxml()

print r2.toxml()

print r1.totuple()
print r1.totuple(fmt='short')
rl = cadac.RunList([r1,r2])
print rl.toxml()

print rl

tl.write('tl.xml')
ul.write('ul.xml')
pl.write('pl.xml')
rl.write('rl.xml')
r1.write('r1.xml')
r2.write('r2.xml')
