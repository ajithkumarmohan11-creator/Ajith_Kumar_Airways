
from datetime import datetime,timedelta

class flight_details:
    def __init__(self,database_manager):
        self.dbm=database_manager

    def seat_allocation(self,total_available_seats,class_order,seat_allocation_in_percentage):
        self.seat_allocat={"total_seats":total_available_seats,
                     "seats_by_class":{}
                     }
        total_assigned_seats=0
        premium_class_order=[c for c in class_order if c!="economy"]
        for clas in premium_class_order:
            percentage=seat_allocation_in_percentage.get(clas,0)
            no_of_seats_allocated=int( total_available_seats * percentage)
            self.seat_allocat["seats_by_class"][clas]=no_of_seats_allocated
            total_assigned_seats+=no_of_seats_allocated
            #print(f"{clas} :{no_of_seats_allocated}")
        economy_seats=total_available_seats-total_assigned_seats
        self.seat_allocat["seats_by_class"]["economy"]=economy_seats
        #print(f"economy : {economy_seats}")    
        self.seat_allocated=[self.seat_allocat["seats_by_class"][clas] for clas in class_order]
        seat_allocated=self.seat_allocated  
        return self.seat_allocated  
    
    def price_calculation_for_classes(self,base_price,class_order,base_price_for_classes):
        self.classes_pricing=[base_price*base_price_for_classes.get(clas,1.0) for clas in class_order]
        for i,clas in enumerate(class_order):
            #print(f"{clas} price : {self.classes_pricing[i]}")
            classes_pricing=self.classes_pricing
        return self.classes_pricing   

    def automate_flight_shedule(self,flight_cols,flight_vals,days_to_schedule=30,time_interval=4):
        # from datetime import datetime,timedelta
        start_date_time=f"{flight_vals[3]} {flight_vals[4]}"
        base_date_time=datetime.strptime(start_date_time,"%Y-%m-%d %H:%M:%S")
        trip_per_day=24//time_interval
        print(f"schedule :{trip_per_day} trip per day with {time_interval} hours of gap")
        seat_alloated_with_price=[]
        for i in range(len(self.seat_allocated)):
            seat_allocat=self.seat_allocated[i]
            pricing=self.classes_pricing[i]
            seat_alloated_with_price.extend([seat_allocat,pricing])
        print(f"seats : {self.seat_allocated} price :{self.classes_pricing}")
        seat_alloated_with_price=tuple(seat_alloated_with_price)
        for day in range(days_to_schedule):
            for f in range(trip_per_day):
                total_hours=(day *24)+(f*time_interval)
                current_date_time=base_date_time+timedelta(hours=total_hours)
                current_date=current_date_time.date()
                current_time=current_date_time.strftime("%H:%M:%S")
                columns=flight_cols
                values=flight_vals[:3]+(current_date,current_time)+(flight_vals[5],)+seat_alloated_with_price+(flight_vals[6],)
                #print(f" debug value :{values}")
                self.dbm.insert_data("flight_details",columns,values)
