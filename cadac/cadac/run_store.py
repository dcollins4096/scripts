import uuid

from sql_base import SQLBase

from node import Node
from tag import TagList
from parameter import ParameterList
from program import Program
from userfield import UserFieldList
from run import User, Computer, Run, RunList, id

from tag_store import TagStore
from link_store import LinkTypeStore
from parameter_store import ParameterStore
from node_store import NodeStore
from userfield_store import UserFieldStore
from program_store import ProgramStore

server_base = 'http://lca.ucsd.edu'

store_map = { Node: NodeStore,
              TagList: TagStore,
              ParameterList: ParameterStore,
              Program: ProgramStore,
              UserFieldList: UserFieldStore,
              User: LinkTypeStore,
              Computer: LinkTypeStore }

class RunStore(SQLBase):

    def __init__(self):
        self.table_name = 'runs'
        self.stores = [NodeStore, TagStore, ParameterStore,
                       ProgramStore, UserFieldStore, LinkTypeStore]

        SQLBase.__init__(self)

    def add_run(self, run):

        run_id = str(uuid.uuid4())

        for childnode in run.childnodes:
            for nodetype in store_map:
                if isinstance(childnode, nodetype):
                    store = store_map[nodetype]()
                    store.update(childnode, run_id)

        sql = 'insert into runs (uuid) values '
        sql += '("%s");' % run_id

        self.cur.execute(sql)
        self.con.commit()
        
        url = server_base + '/xml/runs/%s' % (run_id)

        return id(run_id, url)

    def update_run(self, run, run_id):

        for childnode in run.childnodes:
            for nodetype in store_map:
                if isinstance(childnode, nodetype):
                    store = store_map[nodetype]()
                    store.update(childnode, run_id)

    def get_run(self, run_id):

        res = self.cur.execute('select * from runs where uuid = "%s"' % run_id)
        r = res.fetchone()
        if not r:
            return None
        

        new_run = Run()

        for store in self.stores:
            s = store()
            nodes = s.get(run_id)
            if nodes:
                if isinstance(nodes, list):
                    new_run.childnodes += nodes
                    for node in nodes:
                        if node.name == 'User':
                            username = node.val
                else:
                    new_run.childnodes.append(nodes)

        url = server_base + '/xml/runs/%s' % (run_id)
        new_run.childnodes.append(id(run_id, url))

        return new_run

    def get_run_list(self, run_ids):

        runs = []
        for run_id in run_ids:
            runs.append(self.get_run(run_id))

        return RunList(runs)


    def get_user_run_list(self, username):
        
        sql = 'select uuid from linktypes where name = "%s" and value ="%s"' % ('User', username)
        res = self.cur.execute(sql)
        rows = res.fetchall()

        run_ids = []

        for row in rows:
            run_ids.append(row[0])

        return self.get_run_list(run_ids)

    def get_user_tagged_run_list(self, tag, username):
        
        ts = TagStore()

        run_ids = ts.get_tagged_objects_by_user(tag, username)
        
        return self.get_run_list(run_ids)

    def delete(self, run_id):
        
        for store in self.stores:
            s = store()
            s.delete(run_id)

        SQLBase.delete(self, run_id)
