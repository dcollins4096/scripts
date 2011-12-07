from link import LinkType
from sql_base import SQLBase

class LinkTypeStore(SQLBase):

    def __init__(self):
        self.table_name = 'linktypes'
        SQLBase.__init__(self)

    def update(self, new_data, id):

        if isinstance(new_data, LinkType):
            self.update_linktype(new_data, id)
        else:
            self.update_linktypes(new_data, id)

    def update_linktype(self, link, uuid, commit=True):

        if self.has_linktype(link, uuid):
            sql = 'update linktypes set value="%s", url="%s" ' % (link.val, link.attr['url'])
            sql += 'where uuid="%s" and name="%s";' % (uuid, link.name)
        else:
            sql = 'insert into linktypes (uuid, name, value, url) values '
            sql += '("%s", "%s", "%s", "%s");' % (uuid, link.name, link.val, link.attr['url'])

        self.cur.execute(sql)
        if commit:
            self.con.commit()

    def update_linktypes(self, link_list, uuid):
        for linktype in link_list:
            self.update(linktype, uuid, commit=False)
        self.con.commit()

    def get(self, uuid):
        return self.get_linktypes(uuid)

    def get_linktypes(self, uuid):
        sql = 'SELECT DISTINCT name, value, url FROM linktypes WHERE '
        sql += 'uuid= "%s";' % uuid
        res = self.cur.execute(sql)

        ll = []
        for row in res:
            ll.append(LinkType(row[0],row[1], row[2]))

        return ll

    def get_linktype(self, name, uuid):
        sql = 'SELECT DISTINCT name, value, url FROM linktypes WHERE '
        sql += 'uuid= "%s" and name="%s";' % (uuid, name)
        res = self.cur.execute(sql)

        row = res.fetchone()

        return LinkType(row[0],row[1], row[2])

    def has_linktype(self, link, uuid ):

        sql = 'select uuid from linktypes where '
        sql += 'uuid="%s" and name="%s";' % (uuid,  link.name)

        row = self.cur.execute(sql).fetchone()
        if row:
            return True

        return False
