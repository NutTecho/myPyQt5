import pymssql

class GetDB():
    def __init__(self,server,user,password,database,*args, **kwargs):
        '''
        GetDB will return header at first of list
        '''
        super(GetDB, self).__init__(*args, **kwargs)
        self.conn =  pymssql.connect(server,user,password,database)
        self.cursor = self.conn.cursor()
        
        
    def selectdata(self):
        listdata = []
        with self.conn as conn:
            with conn.cursor(as_dict=False) as cursor:
                cursor.execute('SELECT * FROM dbo.xx')
                listdata.append( list(col[0] for col in cursor.description))
                print(listdata)
                for row in cursor:
                    listdata.append(row)
                    # print(row)
                # print(self.cursor.fetchall())
                # return  self.cursor.fetchall()
        return listdata
          
