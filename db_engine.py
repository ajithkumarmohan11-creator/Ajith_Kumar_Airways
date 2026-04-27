print("data base manager ")

import mysql.connector

class database_manager:
    def __init__(self,host,user,password,database=None):
            self.conn=mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
            )

            self.cursor=self.conn.cursor(dictionary=True)
            print("connect with Mysql success")  

    def write_into_database(self,query,values=None):
        self.cursor.execute(query,values or ())
        self.conn.commit()    
    
    def create_database(self,database_name):
        query=f"create database if not exists {database_name}"
        self.write_into_database(query)

        self.database_name=database_name
        #print(f"database : {self.database_name} created")

        query_use=f"use {self.database_name}"
        self.write_into_database(query_use)
        #print(f"Database : {database_name} used") 
            
    def create_table(self,table_name,columns_datatype):
        if isinstance(columns_datatype,dict):
            columns_datatype=", ".join([f"{column_name} {datatype}" for column_name,datatype in columns_datatype.items()])

        elif isinstance(columns_datatype,(list,tuple)):
            columns_datatype=", ".join(columns_datatype)
        else:
            columns_datatype=columns_datatype

        query=f"create table if not exists {table_name} ({columns_datatype})"
        self.write_into_database(query)
        self.table_name=table_name
        #print(f"Table : {self.table_name} created ")

    def column_add(self,table_name,exist_column_name,new_column_name,data_type):
        query=f"alter table {table_name} add column {new_column_name} {data_type} after {exist_column_name}"
        self.write_into_database(query)
        #print(f"Column : {new_column_name} added in {table_name}")
      
    def column_rename(self,table_name,old_name,new_name):
        query=f" alter table {table_name} rename column {old_name} to {new_name}"
        self.write_into_database(query)
        #print(f"column name {old_name} to {new_name} changed in {table_name}") 
      
    def column_data_type_modify(self,table_name,column_name,old_data_type,new_data_type):
        query = f"alter table {table_name} modify {column_name} {new_data_type}" 
        self.write_into_database(query)
        #print(f"{column_name} datatype {old_data_type} into {new_data_type} modified in {table_name}")  

    def insert_data(self,table_name,columns=None,values=None,**kwargs):
        if kwargs:
            columns=list(kwargs.keys())
            values=list(kwargs.values())

        else:
            if isinstance(columns,str):
                columns=[columns]

            if  isinstance(values,tuple):
                values=list(values)

            elif not isinstance(values,list):
                values=[values]    

        if columns is None or values is None or len(columns) != len(values):
            print(f"no of column : {len(columns)}!= no of values :{len(values)}") 
            return    
        
        no_columns=", ".join(columns)
        no_values=", ".join((["%s"])*len(columns))

        query=f"insert into {table_name} ({no_columns}) values ({no_values})"
        values=values
        self.write_into_database(query,values)
        
    def  update_large_quantity_data_list_tuple(self,table_name,columns,values,condition_columns,condition_values):
        if isinstance(columns, str):
            columns=[columns]
        if isinstance(values,tuple):
            values = list(values) 
        elif not isinstance(values, list): 
            values=[values] 
        if len(columns)!=len(values):
            print(f"no of column : {len(columns)}!= no of values :{len(values)}") 
            return   
        columns_and_values=", ".join(f"{column}=%s" for column in columns)    
        if isinstance(condition_columns, str):
            condition_columns = [condition_columns]
        if isinstance(condition_values,tuple):
            condition_values = list(condition_values)
        elif not isinstance(condition_values,list):
            condition_values=[condition_values]    
        if len(condition_columns) != len(condition_values):
            print(f"no of condition cols : {len(condition_columns)} : != no of condition values :{len(condition_values)} ")
            return  
        condition_columns_values= " and ".join(f"{col}=%s" for col in condition_columns)
        query=f"update {table_name} set {columns_and_values} where {condition_columns_values}" 
        values=values+condition_values
        self.write_into_database(query,values) 
        #print(f"{",".join(map(str,values))} updated {columns} in {table_name}")

    def update_small_quantity_data_dictionary(self, table_name,update_columns_values,conditions_column_values):

        columns= ", ".join([f"{col}=%s" for col in update_columns_values.keys()])
        condition_columns= " and ".join([f"{col}=%s" for col in conditions_column_values.keys()])
    
        query = f"update {table_name} set {columns} where {condition_columns}"
        values= list(update_columns_values.values()) + list(conditions_column_values.values())
        self.write_into_database(query, values)
    
        #print(f"{update_columns_values} updated where {conditions_column_values} in {table_name}")

    def delete_data_from_database(self, table_name, conditions_columns_values):
        #eg=> conditions_columns_values= {"flight_id": 101, "status": "Cancelled"}
        if not conditions_columns_values:
            print(f" there is no condtions for data delete {conditions_columns_values}")
            return
        condition_columns= " and ".join([f"{col}=%s" for col in conditions_columns_values.keys()])
        query = f"delete from {table_name} where {condition_columns}"
        values = list(conditions_columns_values.values())
        self.write_into_database(query, values)
        #print(f"Deleted from {table_name} where {conditions_columns_values}")

    def truncate_table_data(self, table_name):
        query = f"truncate table {table_name}"
        self.write_into_database(query)
        #print(f"All data cleared from {table_name}. Structure remains.")

    def drop_table(self, table_name):
        query = f"drop table if exists {table_name}"
        self.write_into_database(query)
        #print(f"Table {table_name} has been completely deleted.")

    def close_connection(self):
        self.cursor.close()
        self.conn.close()   

    def read_data_from_database(self,table_name=None,conditions_columns_values=None,mode="all",limit=None,**kwargs):
        optional_column=kwargs.get("optional_column","*")
        
        query=f"select {optional_column} "
        
        if table_name:
            query+=f" from {table_name} "

        values=[]
        if conditions_columns_values:
            conditions_columns=" and ".join([f"{column}=%s" for column in conditions_columns_values.keys()])
            query+=f" where {conditions_columns} "
            values=list(conditions_columns_values.values())
        self.cursor.execute(query,values)

        if mode=="one":
            return self.cursor.fetchone()
        elif mode=="many" and limit:
            return self.cursor.fetchmany(limit or 1)
        else:
            return self.cursor.fetchall()
    
    def count_data(self,table_name,conditions_columns_values):
        result=self.read_data_from_database(table_name,
                                            conditions_columns_values=conditions_columns_values,
                                            optional_column="count(*)",
                                            mode="one")
        return list(result.values())[0] if result else 0 
    
    def get_table_columns(self, table_name):
        query = f"SHOW COLUMNS FROM {table_name}"
        self.cursor.execute(query)
        return [columns['Field'] for columns in self.cursor.fetchall()]
    
