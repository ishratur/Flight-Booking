#! python2
# -*- coding: utf-8 -*-
##add passenger

def main():

    import pymssql
    import datetime





    #connecting to the cypress server
    conn = pymssql.connect(host='cypress.csil.sfu.ca', user='s_mirahman',
    password='Rq2F7Erm47jhP3fy', database='mirahman354')

    cur = conn.cursor()
    print ""
    print "WELCOME TO BANGLADESH AIRLINES"
    print ""

    print "CHOOSE OPTION 1 TO ADD NEW PASSENGER."
    print "CHOOSE OPTION 2 TO VIEW A BOOKING LIST OF A FLIGHT INSTANCE."
    print "CHOOSE OPTION 3 TO ADD A BOOKING."
    print "CHOOSE OPTION 4 TO EXIT."
    print ""
    choose_option=input("YOUR OPTION: ")
    print ""

    if choose_option==1:
        f_name = raw_input("YOUR FIRST NAME:  ")
        l_name=raw_input("YOUR LAST NAME: ")
        p_miles=0
        submit=raw_input("CHOOSE YES/NO TO ADD THE PASSENGER: ")

        if submit=="yes" or submit== "YES":
          cur.execute("SELECT MAX(passenger_id) AS p_id FROM Passenger")
          result = cur.fetchall()
          for i in result:
            p_id= int(i[0])+1


          cur.execute("""
            INSERT INTO Passenger
            (passenger_id,first_name, last_name,miles) VALUES
            (%d,%s, %s,%d)""" , (p_id,f_name, l_name,p_miles))
          print ""
          print "THE PROFILE FOR PASSENGER ID: ",p_id," ",f_name," ", l_name," ","WAS CREATED"

        elif submit=="no" or submit== "NO":
          print "NO PASSENGER INSERTED"




    ##################################




    ##implement a user interface to query all the passengers who have booked a certain
    ##flight instance with a user-provided “flight_code” and “depart_date

    elif choose_option==2:
        cur = conn.cursor()
        f_code=raw_input("PLEASE ENTER THE FLIGHT CODE:  ")
        d_date=raw_input("ENTER THE DEPART DATE AS YYYY-MM-DD: ")

        cur.execute("""SELECT flight_code, depart_date FROM Flight_Instance
        WHERE Flight_Instance.flight_code=%s AND Flight_Instance.depart_date=%s""",(f_code,d_date))
        row=cur.rowcount

        if row!=0:
            cur.execute(""" SELECT  Passenger.passenger_id,Passenger.first_name,Passenger.last_name,Passenger.miles
            FROM Booking
            INNER JOIN Passenger ON Booking.passenger_id = Passenger.passenger_id
            WHERE Booking.flight_code=%s AND Booking.depart_date=%s""",(f_code,d_date))
            result= cur.fetchall()
            a=0
            
            for i in result:
                        a=a+1
                        print a,". ","PASSENGER ID:", i[0],"FIRST NAME:",i[1],"LAST NAME:",i[2],"MILES:",i[3]
                        
                    
                     
            print "TOTAL NUMBER OF PASSENGER: ",a
            cur.execute("""SELECT available_seats 
            FROM Flight_Instance
            WHERE Flight_Instance.flight_code=%s AND Flight_Instance.depart_date=%s""",(f_code,d_date))
            result = cur.fetchone()
            print "TOTAL NUMBER OF SEATS AVAILABLE IN ",f_code,"ON DEPART DATE: ",d_date ," is ",result[0]
        else:
            print""
            print "ERROR!!GIVEN FLIGHT INSTANCE IS INVALID"



    ####################


    ##Add booking
    elif choose_option==3:
        cur = conn.cursor()
        p_id=raw_input("Please enter your passenger id: ")
        ##check p_id if exist in the passenger table

        cur.execute("""SELECT passenger_id FROM Passenger
        WHERE passenger_id=%d """,(p_id))
        row=cur.rowcount
        if row==0:
            print "ERROR!!PASSENGER ID NOT FOUND"
        elif row!=0:
            submit=raw_input("Select 'single' or 'multi' city trip: ")
            
            if submit=="single" or submit=="SINGLE":
                print "Booking for a single trip "
                f_code=raw_input("PLEASE ENTER THE FLIGHT CODE:  ")
                d_date=raw_input("ENTER THE DEPART DATE AS YYYY-MM-DD: ")
                
        ##    check the f_code and d_date and available seats in the flight instance
                
                cur.execute("""SELECT flight_code, depart_date FROM Flight_Instance
                WHERE Flight_Instance.flight_code=%s AND Flight_Instance.depart_date=%s""",(f_code,d_date))
                row=cur.rowcount
                cur.execute("""SELECT available_seats FROM Flight_Instance
                WHERE Flight_Instance.flight_code=%s AND Flight_Instance.depart_date=%s""",(f_code,d_date))
                row_1=cur.fetchone()
                
                if row==0:
                    print "ERROR!!FLIGHT INSTANCE NOT FOUND "
                elif row_1[0]==0:
                    print("SORRY!! NO MORE SEAT AVAILABLE IN THIS FLIGHT")
                elif row!=0 and row_1[0]>0:
                    cur.execute("""INSERT INTO
                    Booking (flight_code,depart_date,passenger_id) VALUES
                    (%s,%s,%d)""",(f_code,d_date,p_id))
                    print "The booking for passenger ID ",p_id," flight code ",f_code," depart date ",d_date,"has been added."

                    
            elif submit=="multi" or submit=="MULTI":
                print "Booking for a multicity trip. NOTE:The maximum legs are 2."
                print ""
                print "Flight Instance for leg:1 "
                print ""
                f_code=raw_input("ENTER THE FLIGHT CODE FOR LEG-1:  ")
                d_date=raw_input("ENTER THE DEPART DATE AS YYYY-MM-DD for leg1: ")
            
        ##    check the f_code and d_date and available seats in the flight instance
            
                cur.execute("""SELECT flight_code, depart_date,available_seats FROM Flight_Instance
                WHERE Flight_Instance.flight_code=%s AND Flight_Instance.depart_date=%s""",(f_code,d_date))
                row=cur.rowcount
                cur.execute("""SELECT available_seats FROM Flight_Instance
                WHERE Flight_Instance.flight_code=%s AND Flight_Instance.depart_date=%s""",(f_code,d_date))
                row_1=cur.fetchone()
                
                if row==0:
                    print "ERROR!!FLIGHT INSTANCE NOT FOUND FOR LEG 1"
                elif row_1[0]==0:
                    print("ERROR!! NO MORE SEAT AVAILABLE")
                elif row!=0 and row_1[0]>0:
                
                    print "Flight Instance for leg:2 "
                    f1_code=raw_input("ENTER THE FLIGHT CODE FOR LEG-2:  ")
                    d1_date=raw_input("ENTER THE DEPART DATE AS YYYY-MM-DD for leg2: ")
        ##    check the f1_code and d1_date and available seats in the flight instance
                    cur.execute("""SELECT flight_code, depart_date,available_seats FROM Flight_Instance
                    WHERE Flight_Instance.flight_code=%s AND Flight_Instance.depart_date=%s""",(f1_code,d1_date))
                    row=cur.rowcount

                    cur.execute("""SELECT available_seats FROM Flight_Instance
                    WHERE Flight_Instance.flight_code=%s AND Flight_Instance.depart_date=%s""",(f1_code,d1_date))
                    row_1=cur.fetchone()

                    if row==0:
                        print "ERROR!!FLIGHT INSTANCE NOT FOUND FOR LEG 2"
                    elif row_1[0]==0:
                        print("ERROR!! NO MORE SEAT AVAILABLE IN LEG 2")
                    elif row!=0 and row_1[0]>0:
                        d_cast= datetime.datetime.strptime(d_date, "%Y-%m-%d")
                        d1_cast=datetime.datetime.strptime(d1_date, "%Y-%m-%d")
        ##    checking depart dates for both legs
                        result=d_cast<d1_cast
                        if result==False:
                            print("BOOKING ERROR!! DEPART DATE OF SECOND LEG IS EARLIER THAN FIRST LEG")
                        elif result==True:
                            print "SUCCESSFUL"
                            print ""
        ##        insert both legs in one query
                            cur.executemany("""INSERT INTO
                            Booking (flight_code,depart_date,passenger_id) VALUES
                            (%s,%s,%d)""",[(f_code,d_date,p_id),(f1_code,d1_date,p_id)])
                            print "THE BOOKING FOR PASSENGER: ",p_id," FLIGHT CODE: ",f_code," DEPART DATE: ",d_date,"AND FLIGHT CODE:",f1_code," DEPART DATE: ",d1_date,"HAS BEEN SUCCESSFUL"





    elif choose_option==4:
        print ""
        print "BYE BYE"
        exit()
                            
    conn.commit()
    conn.close()

    

    
    print " "
    print " "
    
    print "WOULD YOU LIKE TO SEE THE OPTIONS AGAIN? "
    print ""
    restart=raw_input("PRESS YES/NO: ")
    if restart=="YES" or restart=="yes":
        main()
    elif restart=="NO" or restart=="no":
        print "THANKS FOR BEING WITH BANGLADESH AIRLINES"
        exit()
        
#starts the code again
main()
    


