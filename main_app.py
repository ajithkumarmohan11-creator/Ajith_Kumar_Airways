import json
import os

from db_engine import database_manager as dbm
import admin_ops as admin
import customer_ops as customer
import common_tools as common




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
    choice=input("your choice :").strip()

    if choice=="3":
        break

    elif choice=="1":
        mobile_number=common.authorize_mobile_number()
        if not mobile_number: continue
        otp=common.authorize_user()
        if not otp: continue
        already_exist=customer.authentication_customer(db,mobile_number)
        if already_exist:
            full_name=already_exist["full_name"]
            dob=already_exist["date_of_birth"]
            age=common.calculate_age(dob)
            print(f"welcome {full_name} Age :{age} ")
        else:
            user_profile=customer.user_personal_details(db,mobile_number)
            if not user_profile: continue
            print("sing up success")
        while True:
                print("1.check availablity\n2.Book ticket\n3.status checking\n4.cancel ticket\n5.exit")
                passenger_choice=(input("choice :"))

                if passenger_choice=="5":
                    print("thank you for your visit")
                    break 

                elif passenger_choice=="1":
                    origine_list = customer.get_serviceable_locations(db, "origine")
                                
                    if not origine_list:
                        print("\n[!] No flights scheduled at the moment.")
                        input("Press Enter to return...")
                        continue

                    origine = common.universal_live_search(origine_list, "Search Origin (Flying From)")
                    if not origine: continue

                    destination_list = customer.get_serviceable_locations(db, "destination", {"origine": origine})
                                
                    if not destination_list:
                        print(f"\n[!] No destinations available from {origine.title()}.")
                        input("Press Enter to return...")
                        continue

                    destination = common.universal_live_search(destination_list, f"Search Destination from {origine.title()}")
                    if not destination: continue

                    os.system('cls') 
                    print(f"ROUTE: {origine.title()} >>> {destination.title()}")
                    
                    date= common.universal_input_handler(
                        "Enter Departure Date (DD-MM-YYYY)", 
                        common.date_is_future, 
                        "Invalid! Please enter a future date."
                        )
                                
                    if date:
                        date=common.date_db_format(date)
                        search_values={
                            "origine":origine,
                            "destination":destination,
                            "departure_date":date
                            }
                        customer.check_flight_availablity(db,**search_values)
                    else:
                        print("Search cancelled.")
                                


                elif passenger_choice=="2":
                    booking_values={
                    "flight_id":int(input("flight id :")),
                    "class_type":input("class (economy/premium economy,business/first class) :").strip().lower().replace(" ","_"),
                    "no_of_seats":int(input("no of seat(s) :"))
                    }
                    booking_initiat=customer.ticket_booking_manager(db)
                    result=booking_initiat.initiate_booking(db,mobile_number,**booking_values)

                elif passenger_choice=="3":
                    user_pnr_no=input("enter your Pnr NO to proceed status check :").strip()
                    customer.status_checking(db,user_pnr_no) 

                elif passenger_choice=="4":
                    user_pnr_no=input("enter your Pnr NO to proceed to cancel :").strip()
                    refund=customer.cancel_ticket(db,user_pnr_no) 
                    if refund:
                        refund_amount=common.Ajith_Kumar_National_Bank.deposit_amount(refund)
                        if refund_amount:
                            print("refund done")
                        else:
                            print(f"your refund amount credited to your account within 7 to 15 working days")    
                else:
                    print("enter valid choice ")
                    break
                                       

    elif choice=="2":
        user_id=input("enter your user id :").strip()
        user_password=input("enter your password :").strip()
        if admin.authentication_admin(user_id,user_password):
            print(f"welcome {user_id} ")
            while True:
                print("enter your choice of operations")
                choice_for_operations=(input("1.connect to database\n2.create database\n3.create table\n4.flight automation\n5.exit:"))
                if choice_for_operations=="5":
                    break
                elif choice_for_operations=="1":
                    host=input("enter host (eg=>local host) :")
                    user=input("enter user(eg=>root) :")
                    password=input("enter password :")

                    db_connect_details={"user":user,"host":host,"password":password}
                    db=admin.admin_operations(db,choice_for_operations,db_connect_details)

                elif choice_for_operations=="2":
                    database_name=input("database name :")

                    database_name={"database_name":database_name}
                    db=admin.admin_operations(db,choice_for_operations,**database_name) 

                elif choice_for_operations=="3":
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

                elif choice_for_operations=="4":
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
    else:
        print(" Invalid choice ")        



     
