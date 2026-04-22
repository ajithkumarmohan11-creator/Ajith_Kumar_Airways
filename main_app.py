from db_engine import database_manager as dbm
import common_tools as common
import json
import os
import admin_ops as admin
import customer_ops as customer

if os.path.exists("db_connect_details.json"):
    with open("db_connect_details.json", "r") as f:
        details = json.load(f)
    db = dbm(**details) 
else:
    db = None

width = 50
print("welcome to Ajith Airways ".center(width))
print("' Wings for your Dreams, Wheels for your Journey! '" .center(width)) 

while True:
    print("enter  as \n1.passanger\n2.admin\n3.exit ")
    choice=int(input("your choice :"))

    if choice==3:
        break

    elif choice==1:
        mobile_number=input("mobile number :").strip()
        mobile_number=common.validate_mobile_number(mobile_number)

        if mobile_number:
            otp=common.authorize_user()
            if otp:
                already_exist=customer.authentication_customer(db,mobile_number)
                if already_exist:
                    full_name=already_exist["full_name"]
                    print(f"welcome {full_name} ")
                else:
                    user_gender=int(input("gender\n1.male\n2.female\n3.shemale(others) :"))
                    gender=common.gender(user_gender)
                    if gender:
                        user_gender=gender
                    full_name=input(" full Name :").strip()
                    dob=input("date of birth(YYYY-MM-DD) :")
                    age=common.calculate_age(dob)
                    details={"mobile_number":mobile_number,"full_name":full_name,"gender":user_gender,"date_of_birth":dob}
                    customer.customer_details(db,details)
                          
                while True:
                    print("1.check availablity\n2.Book ticket\n3.status checking\n4.cancel ticket\n5.exit")
                    passenger_choice=int(input("choice :"))

                    if passenger_choice==5:
                        print("thank you for your visit")
                        break 

                    elif passenger_choice==1:
                        search_values={
                        "origine":input("origine :").strip(),
                        "destination":input("destination :").strip(),
                        "departure_date":input("departure_date YYYY-MM_DD :").strip()
                            }
                        customer.check_flight_availablity(db,**search_values)

                    elif passenger_choice==2:
                        booking_values={
                        "flight_id":int(input("flight id :")),
                        "class_type":input("class (economy/premium economy,business/first class) :").strip().lower().replace(" ","_"),
                        "no_of_seats":int(input("no of seat(s) :"))
                                    }
                        booking_initiat=customer.ticket_booking_manager(db)
                        result=booking_initiat.initiate_booking(db,mobile_number,**booking_values)

                    elif passenger_choice==3:
                        user_pnr_no=input("enter your Pnr NO to proceed status check :").strip()
                        customer.status_checking(db,user_pnr_no) 

                    elif passenger_choice==4:
                        user_pnr_no=input("enter your Pnr NO to proceed to cancel :").strip()
                        refund=customer.cancel_ticket(db,user_pnr_no) 
                        if refund:
                            refund_amount=common.Ajith_Kumar_National_Bank.deposit_amount(refund)
                            if refund_amount:
                                print("refund done")
                            else:
                                print(f"your refund amount credited to your account within 7 to 15 working days")    

                    else:
                        print("invalide choice")
                        continue 
            else:
                print("user validation faild")             

    elif choice==2:
        user_id=input("enter your user id :")
        user_password=input("enter your password :")
        if admin.authentication_admin(user_id,user_password):
            print(f"welcome {user_id} ")
            while True:
                print("enter your choice of operations")
                choice_for_operations=int(input("1.connect to database\n2.create database\n3.create table\n4.flight automation\n5.exit:"))
                if choice_for_operations==5:
                    break
                elif choice_for_operations==1:
                    host=input("enter host (eg=>local host) :")
                    user=input("enter user(eg=>root) :")
                    password=input("enter password :")

                    db_connect_details={"user":user,"host":host,"password":password}
                    db=admin.admin_operations(db,choice_for_operations,db_connect_details)

                elif choice_for_operations==2:
                    database_name=input("database name :")

                    database_name={"database_name":database_name}
                    db=admin.admin_operations(db,choice_for_operations,**database_name) 

                elif choice_for_operations==3:
                    current_database=admin.admin_operations(db,choice_for_operations,database_name=True)
                    print(f"current database :{current_database}  ")

                    table_name=input(f"enter table name you want to create :")

                    all_columns={}
                    while True:
                        print("enter 'done' for finish column insert")
                        column_name=input("column name :").lower().strip()
                        if column_name=="done":
                            if not all_columns: 
                                print(" You must add at least one column!")
                                continue
                            break

                        data_type=input(f"data type for {column_name} :")

                        all_columns[column_name]=data_type

                    table_name_columns_datatype={"table_name":table_name,
                                              "columns":all_columns,
                                              }
                    db=admin.admin_operations(db,choice_for_operations,**table_name_columns_datatype) 

                elif choice_for_operations==4:
                    flight_no = input("Flight No: ")
                    origine = input("Origine: ")
                    destination = input("Destination: ")
                    departure_date = input("Start Date (YYYY-MM-DD): ")
                    departure_time = input("Start Time (HH:MM:SS): ")
                    total_available_seats = int(input("Total Seats: "))
                    base_price = int(input("Base Price: "))
                
                    details={"flight_no":flight_no, "origine":origine, 
                                "destination":destination, "departure_date":departure_date, 
                                "departure_time":departure_time, "total_available_seats":total_available_seats, 
                                "base_price":base_price, 
                                }
                    db = admin.admin_operations(db, choice_for_operations, **details)

        else:
            print("invalid user_id/admin")



     
