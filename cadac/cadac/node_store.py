from node import Node
from sql_base import SQLBase

class NodeStore(SQLBase):

    def __init__(self):
        self.table_name = 'nodes'
        SQLBase.__init__(self)

    def update(self, new_data, id):

        if isinstance(new_data, Node):
            self.update_node(new_data, id)
        else:
            self.update_nodes(new_data, id)

    def update_node(self, node, uuid, commit=True):

        if self.has_node(node, uuid):
            sql = 'update nodes set value="%s" ' % node.val
            sql += 'where uuid="%s" and name="%s";' % (uuid, node.name)
        else:
            sql = 'insert into nodes (uuid, name, value) values '
            sql += '("%s", "%s", "%s");' % (uuid, node.name, node.val)

        self.cur.execute(sql)            
        if commit:
            self.con.commit()

    def update_nodes(self, link_list, uuid):
        for node in link_list:
            self.udpate_node(node, uuid, commit=False)
        self.con.commit()

    def get(self, uuid):
        return self.get_nodes(uuid)

    def get_nodes(self, uuid):
        sql = 'SELECT DISTINCT name, value FROM nodes WHERE '
        sql += 'uuid= "%s";' % uuid
        res = self.cur.execute(sql)

        nl = []
        for row in res:
            nl.append(Node(row[0],row[1]))

        return nl

    def get_node(self, name, uuid):
        sql = 'SELECT DISTINCT name, value FROM nodes WHERE '
        sql += 'uuid= "%s" and name="%s";' % (uuid, name)
        res = self.cur.execute(sql)

        row = res.fetchone()

        return Node(row[0],row[1])

    def has_node(self, node, uuid):
        sql = 'SELECT uuid FROM nodes WHERE '
        sql += 'uuid= "%s" and name="%s";' % (uuid, 
                                              node.name)

        res = self.cur.execute(sql)
        row = res.fetchone()
        if row:
            return True

        return False

