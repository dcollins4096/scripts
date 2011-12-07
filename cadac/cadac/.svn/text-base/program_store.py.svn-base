from program import Program
from sql_base import SQLBase

class ProgramStore(SQLBase):

    def __init__(self):
        self.table_name = 'programs'
        SQLBase.__init__(self)

    def update(self, program, run_id):

        if self.has_program(program, run_id):
            sql = 'update programs set version="%s", url="%s" '% (program.attr['version'],
                                                                  program.attr['url'])
            sql += 'where uuid="%s" and name="%s";' % (run_id,
                                                       program.val)

        else:
            sql = 'insert into programs (uuid, name, version, url) values '
            sql += '("%s", "%s", "%s", "%s");' % (run_id, 
                                        program.val,
                                        program.attr['version'],
                                        program.attr['url'])

        self.cur.execute(sql)
        self.con.commit()

    def get(self, run_id):
        return self.get_program(run_id)

    def get_program(self, run_id):
        
        sql = 'SELECT DISTINCT name, version, url FROM programs WHERE '
        sql += 'uuid= "%s";' % run_id
        res = self.cur.execute(sql)

        row = res.fetchone()

        return Program(row[0], row[1], row[2])

    def has_program(self, program, uuid):

        sql = 'SELECT uuid FROM programs WHERE '
        sql += 'uuid="%s" and name="%s" ;' % (uuid, 
                                              program.val)

        res = self.cur.execute(sql)
        row = res.fetchone()
        if row:
            return True

        return False
