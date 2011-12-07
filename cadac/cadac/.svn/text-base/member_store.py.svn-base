from member import Member, MemberList
from sql_base import SQLBase

class MemberStore(SQLBase):

    def __init__(self):
        self.table_name = 'members'
        SQLBase.__init__(self)

    def update(self, new_data):

        if isinstance(new_data,  Member):
            self.update_member(new_data)
        else:
            self.update_members(new_data)

    def update_member(self,member, commit=True):

        username, name, url = member.get_values()

        if self.has_member(member):
            sql = 'update members set '
            sql += 'name="%s", url="%s" WHERE ' % (name, url)
            sql += 'username="%s";' % username

        else:
            sql = 'insert into members (username, name, url) values '
            sql += '("%s", "%s", "%s");' % (username, name, url)

        self.cur.execute(sql)
        if commit:
            self.con.commit()

    def update_members(self, member_list):
        for member in member_list.members:
            self.update_member(member, commit=False)
        self.con.commit()

    def get(self, username):
        return self.get_member(username)

    def get_member(self, username):
        sql = 'SELECT username, name, url FROM members WHERE '
        sql += 'username= "%s";' % username
        res = self.cur.execute(sql)

        row = res.fetchone()
        return Member(row[0],row[1], row[2])

    def get_members(self):
        sql = 'SELECT username, name, url FROM members;'
        res = self.cur.execute(sql)

        ml = []
        for row in res.fetchall():
            ml.append(Member(row[0],row[1], row[2]))

        return MemberList(ml)

    def delete_member(self, username):
        sql = 'DELETE FROM members WHERE '
        sql += 'username= "%s" ;' % username
        res = self.cur.execute(sql)
        self.con.commit()

    def has_member(self, member ):

        sql = 'select username from members where '
        sql += ' username="%s";' % member.childnodes[0].val

        row = self.cur.execute(sql).fetchone()
        if row:
            return True

        return False
