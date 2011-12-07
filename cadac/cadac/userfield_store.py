from userfield import UserField, UserFieldList
from sql_base import SQLBase

class UserFieldStore(SQLBase):

    def __init__(self):
        self.table_name = 'userfields'
        SQLBase.__init__(self)

    def update(self, new_data, id):

        if isinstance(new_data, UserField):
            self.update_userfield(new_data, id)
        else:
            self.update_userfields(new_data, id)

    def update_userfield(self, userfield, run_id, commit=True):

        if self.has_userfield(userfield, run_id):
            sql = 'update userfields set name="%s", value="%s" ' % (userfield.attr['name'],
                                                       userfield.val)
            sql += 'where uuid="%s" and name="%s";' % (run_id,
                                                       userfield.attr['name'])
        else:
            sql = 'insert into userfields (uuid, name, value) values '
            sql += '("%s", "%s", "%s");' % (run_id, 
                                        userfield.attr['name'],
                                        userfield.val)

        self.cur.execute(sql)
        if commit:
            self.con.commit()

    def update_userfields(self, userfield_list, run_id):
        for userfield in userfield_list.userfields:
            self.update_userfield(userfield, run_id, commit=False)
        self.con.commit()

    def get(self, uuid):
        return self.get_userfields(uuid)

    def get_userfields(self, run_id):
        
        sql = 'SELECT name, value FROM userfields WHERE '
        sql += 'uuid= "%s";' % run_id
        res = self.cur.execute(sql)

        ul = []
        for row in res:
            ul.append(UserField(row[0],row[1]))

        return UserFieldList(ul)

    def has_userfield(self, userfield, uuid ):

        sql = 'select uuid from userfields where '
        sql += 'uuid="%s" and name="%s";' % (uuid, 
                                              userfield.attr['name'])

        row = self.cur.execute(sql).fetchone()
        if row:
            return True

        return False
