import numpy as np
import pandas as pd


class sqlparser2:
    def __init__(self, *args):

        select_lower = args[0].lower().replace(' ', '')

        # select

        self.select = self.str_between(select_lower,'select','from').split(',')
        self.select = [int(i)-1 if i.isdigit() else i for i in self.select]
        # struct


        data_structure_string= self.str_between(select_lower,'from','where')
        if data_structure_string == None:

            data_structure_string = self.str_between(select_lower,'from').split(',')

        self.data_structure_list=([subs.strip() for subs in data_structure_string.split(',')])

        structure_type=[]
        for structure in args[1:]:
            if isinstance(structure, list):
                structure_type.append('list')
            elif isinstance(structure, dict):
                structure_type.append('dict')
            elif isinstance(structure, pd.DataFrame):
                structure_type.append('DataFrame')
        print(structure_type)
        self.data_structure_dict=dict(zip(self.data_structure_list,structure_type))

        # where

        if select_lower.find('group by')>0:

            self.where_statement = self.str_between(select_lower,'where','group by')
        elif select_lower.find('order by')>0:

            self.where_statement = self.str_between(select_lower,'where','order by')
        elif select_lower.find('limit')>0:

            self.where_statement = self.str_between(select_lower,'where','limit')
        else:

            self.where_statement = self.str_between(select_lower,'from')

        where_statement2 = [i.split('=') for i in self.where_statement.replace('"', '').split('and')]
        where_statement3 = {}
        where_statement4 = []
        self.where_list_formatted = []
        for line in where_statement2:
            key, value = line[0], line[1]
            where_statement3[key]=('=',value)
            where_statement4.append([key,'=',value])
        self.where_dict=where_statement3
        self.where_list=where_statement4
        print('test')
        for i in self.where_list:
            #i=str(i).replace('=','==')
            #print('this is i: '+i)
            value=list(map(lambda x, y, z: '[\'' + x + '\']' + y.replace('=','==') + '\'' + z + '\'', i[0], i[1], i[2:]))
            print('value')
            print(value)
            self.where_list_formatted.append(value)

        # limit
        limit_statement = select_lower[select_lower.find('limit') + len('limit'):]
        self.limit=limit_statement.strip()


    def str_between(self,string,start_string,end_string=None):
        if end_string == None:
            return string[string.find(start_string) + len(start_string):]
        else:
            return string[string.find(start_string) + len(start_string):string.rfind(end_string)]


class sqldata:
    def __init__(self, data):



        if isinstance(data, list):
            self.data_structure_type='list'
            self.dataframe=pd.DataFrame(data)

        elif isinstance(data, dict):
            self.data_structure_type='dict'
            self.dataframe=pd.DataFrame.to_dict(data,orient=index)
        elif isinstance(data, pd.DataFrame):
            self.data_structure_type='DataFrame'
            self.dataframe=data
        self.shape=self.dataframe.shape

    #def list_to_dataframe(self):


    #def dict_to_dataframe(self):

    def select(self,fields):
        if fields[0]=='*':
            return self.dataframe
        else:
            #return self.dataframe.loc[fields].values
            #return self.dataframe.loc[fields]
            return self.dataframe[fields]

    def limit(self,limit):
        if limit:
            self.dataframe=self.dataframe.head(limit)
            return self


    #def where(self,fields):
table = [1,2,3,4,5]
table2 = [[1,2,3],[5,6,7]]
table3 = [1,2,3]

test = sqlparser2('select 1,2 from table2  where 1 = "test" and 2="123" limit 5 ',table2)

#table_df.loc[[0,1]]

print(test.select)
print(test.data_structure_list)
print(test.data_structure_dict)
print(test.where_statement)
print("where dict")
print(test.where_dict['1'][0])
print(test.where_dict['1'][1])
print(test.limit)

sqldatatest = sqldata(table2)
print("test")
print(sqldatatest.data_structure_type)
print(sqldatatest.shape)
print("test2")
print(sqldatatest.limit(2).select(test.select))

print(test.data_structure_list)
print(test.where_statement)
print(test.where_statement.replace('=','=='))
#print(test.where_statement.replace())
print(test.where_dict)
where_statement2=test.where_statement
for key in test.where_dict:
    where_statement2=test.where_statement.replace(key,'['+key+']')
print(where_statement2)
print("where_list")
print(test.where_list)

# do this
for i in test.where_list:
    print('i')
    print(i)
    value = list(map(lambda x,y,z: '[\''+x+'\']'+y+'\''+z+'\'',i[0],i[1],i[2:]))
    print(value)

print('where list formatted')
print(test.where_list_formatted)
# replace equality symbols

