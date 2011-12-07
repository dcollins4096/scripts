#!/usr/bin/env python

import cadac
from cadac import run_store

rs = run_store.RunStore()
users = ['rpwagner','dcollins','padoan']
comps = ['Cobalt', 'Abe']

for user in users:


     ts = []
     for i in range(0,4):
          ts.append(cadac.Tag(i,user))

 
     tl = cadac.TagList(ts)
     ps = []
     for i in range(0,3):
          ps.append(cadac.Parameter('param'+str(i),i,'http://lca.ucsd.edu/enzo/param'+str(i)))
      
     pl = cadac.ParameterList(ps)

     p = cadac.Program('Enzo',1052,'svn://mngrid.ucds.edu/Enzo/trunk/devel/Enzo')
     us = []

     for i in range(0,5):
          us.append(cadac.UserField('mydat'+str(i),10.4*i))


     ul = cadac.UserFieldList(us)

     u = cadac.User(user,'http://lca.ucsd.edu/projects/'+user)

     for comp in comps:
          c = cadac.Computer(comp,'http://lca.ucsd.edu/computers/'+comp)
          r1 = cadac.Run('r1',c,p,u,ul,tl,pl,ToDo='Way too much!',Comments='Disabled')
          r2 = cadac.Run('r2',c,p,u,ul,tl,ToDo='Way too much!',Comments='Disabled',Nodes=2,TasksPerNode=8,Account='MUT')

          r1_id = rs.add_run(r1)
          r2_id = rs.add_run(r2)
