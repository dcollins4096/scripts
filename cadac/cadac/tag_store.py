from tag import Tag, TagList
from sql_base import SQLBase

class TagStore(SQLBase):

    def __init__(self):
        self.table_name = 'tags'
        SQLBase.__init__(self)

    def update(self, new_data, id):

        if isinstance(new_data,  Tag):
            self.update_tag(new_data, id)
        else:
            self.update_tags(new_data, id)

    def update_tag(self,tag, id, commit=True):

        if not self.has_tag(tag, id):
            sql = 'insert into tags (uuid, tag, user) values '
            sql += '("%s", "%s", "%s");' % (id, tag.val, tag.attr['user'])
            self.cur.execute(sql)

            if commit:
                self.con.commit()

    def update_tags(self, tag_list, id):
        for tag in tag_list.tags:
            self.update_tag(tag, id, commit=False)
        self.con.commit()

    def get(self, uuid):
        return self.get_object_tags(uuid)

    def get_user_tags(self, username):
        sql = 'SELECT DISTINCT tag, user FROM tags WHERE '
        sql += 'user= "%s";' % username
        res = self.cur.execute(sql)

        tl = []
        for row in res:
            tl.append(Tag(row[0],row[1]))

        return TagList(tl)

    def get_object_tags(self, uuid):
        sql = 'SELECT DISTINCT tag, user FROM tags WHERE '
        sql += 'uuid= "%s";' % uuid
        res = self.cur.execute(sql)

        tl = []
        for row in res:
            tl.append(Tag(row[0],row[1]))

        return TagList(tl)

    def get_object_tags_by_tag(self, uuid, tagname):
        sql = 'SELECT DISTINCT tag, user FROM tags WHERE '
        sql += 'uuid= "%s" and tag="%s";' % (uuid, tagname)
        res = self.cur.execute(sql)

        tl = []
        for row in res:
            tl.append(Tag(row[0],row[1]))

        return TagList(tl)

    def get_tagged_objects(self,tag):
        sql = 'SELECT DISTINCT uuid FROM tags WHERE '
        sql += 'tag= "%s";' % tag.val
        res = self.cur.execute(sql)

        ol = []
        for row in res:
            ol.append(row[0])

        return ol

    def get_tagged_objects_by_user(self,tag, username):
        sql = 'SELECT DISTINCT uuid FROM tags WHERE '
        sql += 'tag= "%s" and user="%s";' % (tag.val, username)
        res = self.cur.execute(sql)

        ol = []
        for row in res:
            ol.append(row[0])

        return ol

    def delete_object_tag(self, tag, uuid):
        sql = 'DELETE FROM tags WHERE '
        sql += 'tag= "%s" and uuid="%s";' % (tag.val, uuid)
        res = self.cur.execute(sql)
        self.con.commit()

    def delete_object_tags(self, uuid):
        sql = 'DELETE FROM tags WHERE '
        sql += 'uuid="%s";' % uuid
        res = self.cur.execute(sql)
        self.con.commit()

    def has_tag(self, tag, uuid ):

        sql = 'select uuid from tags where '
        sql += 'uuid="%s" and tag="%s" and user="%s";' % (tag.val, uuid,  tag.attr['user'])

        row = self.cur.execute(sql).fetchone()
        if row:
            return True

        return False
