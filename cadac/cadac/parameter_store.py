from parameter import Parameter, ParameterList
from sql_base import SQLBase

class ParameterStore(SQLBase):

    def __init__(self):
        self.table_name = 'parameters'
        SQLBase.__init__(self)

    def update(self, new_data, id):

        if isinstance(new_data, Parameter):
            self.update_parameter(new_data, id)
        else:
            self.update_parameters(new_data, id)


    def update_parameter(self, parameter, run_id, commit=True):

        if self.has_parameter(parameter, run_id):
            sql = 'update parameters set '
            sql += 'value="%s", url="%s" '% (parameter.val, parameter.attr['url'])
            sql += 'where uuid="%s" and name="%s";' % (run_id,
                                                       parameter.attr['name'])
        else:
            sql = 'insert into parameters (uuid, name, value, url) values '
            sql += '("%s", "%s", "%s", "%s");' % (run_id, 
                                              parameter.attr['name'],
                                              parameter.val,
                                              parameter.attr['url'])
        self.cur.execute(sql)
        if commit:
            self.con.commit()

    def update_parameters(self, param_list, run_id):
        for param in param_list.params:
            self.update_parameter(param, run_id, commit=False)
        self.con.commit()

    def get(self, uuid):
        return self.get_parameters(uuid)

    def get_parameters(self, run_id):
        
        sql = 'SELECT DISTINCT name, value, url FROM parameters WHERE '
        sql += 'uuid= "%s";' % run_id
        res = self.cur.execute(sql)

        rl = []
        for row in res:
            rl.append(Parameter(row[0],row[1],row[2]))

        return ParameterList(rl)

    def has_parameter(self, parameter, uuid):

        sql = 'SELECT uuid FROM parameters WHERE '
        sql += 'uuid="%s" and name="%s";' % (uuid, 
                                             parameter.attr['name'])

        res = self.cur.execute(sql)
        row = res.fetchone()
        if row:
            return True

        return False
