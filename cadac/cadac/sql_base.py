from pysqlite2 import dbapi2 as sqlite

dbpath = '/Users/rpwagner/Projects/lcagrid/cadac/code/cadac/test.db'

class SQLBase:

    def __init__(self):
        self.con = sqlite.connect(dbpath)
        self.cur = self.con.cursor()

    def delete(self, uuid):
        sql = 'DELETE FROM %s WHERE uuid="%s";' % (self.table_name, uuid)
        res = self.cur.execute(sql)
        self.con.commit()

