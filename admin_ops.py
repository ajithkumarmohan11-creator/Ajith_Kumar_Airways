print("admin login")

import json
import os
from db_engine import database_manager as dbm
import flight_automation

def authentication_admin(user_id,user_password):
    admin_id="ajithkumar11"
    password="1101AjithM"
    if user_id==admin_id and password==user_password:
        return True
    return False

def admin_operations(db,choice_for_operations,db_connect_details=None,**kwargs):
    if choice_for_operations!=1:
        with open("db_connect_details.json","r") as f:
            db_connect_details=json.load(f)

    if choice_for_operations==3 and kwargs.get("database_name")==True:
        result=db.read_data_from_database(optional_column="database() as current_db",mode="one")
        return result["current_db"] if result else "Not selected"

    if choice_for_operations==1:
        db=dbm(**db_connect_details) 
        with open("db_connect_details.json","w") as f:
            json.dump(db_connect_details,f,indent=4)
            print(f"{db_connect_details} saved")
            return db
        
    elif choice_for_operations==2:
        database_name=kwargs.get("database_name")
        if database_name:
            db.create_database(database_name)

            with open("db_connect_details.json","w") as f:
                json.dump(db_connect_details,f,indent=4)
            print(f"database created : {database_name}") 
        else:
            print("database name missing")
        return db
      
    elif choice_for_operations==3:
        table_name=kwargs.get("table_name")
        columns_datatype=kwargs.get("columns")

        if table_name and columns_datatype:
            db.create_table(table_name,columns_datatype)
            print(f"{table_name} created")
        
        else:
            print("table name or column details missing")  
        return db 
       
    elif choice_for_operations==4:
        flight=flight_automation.flight_details(db)
        class_order = ["economy", "premium_economy", "business", "first_class"]
        seat_ratio = {"economy": 0.4, "premium_economy": 0.3, "business": 0.2, "first_class": 0.1}
        price_ratio = {"economy": 1.0, "premium_economy": 1.5, "business": 3.0, "first_class": 5.0}
        
        flight.seat_allocation(kwargs["total_available_seats"],class_order,seat_ratio)
        flight.price_calculation_for_classes(kwargs["base_price"],class_order,price_ratio)
        
        flight_cols = ("flight_no","origine", "destination", "departure_date", "departure_time", "total_available_seats","economy_seats","economy_seat_price","premium_economy_seats","premium_economy_seat_price","business_seats","business_seat_price","first_class_seats","first_class_seat_price","base_price")
        flight_vals = (kwargs["flight_no"],kwargs["origine"],kwargs["destination"],kwargs["departure_date"], kwargs["departure_time"],kwargs["total_available_seats"] ,kwargs["base_price"])
       
        flight.automate_flight_shedule(flight_cols,flight_vals,)

        return db
    

            


    

   



