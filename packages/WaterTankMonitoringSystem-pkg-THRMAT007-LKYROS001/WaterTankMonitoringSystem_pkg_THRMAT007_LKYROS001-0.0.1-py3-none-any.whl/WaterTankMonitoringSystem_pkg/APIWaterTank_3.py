#attempt 2, have less opp and rather just straight access the sensors
#Matts imports
import io 
import os
import time
import VL53L1X
import keyboard
import datetime
from datetime import timedelta
import time
import sqlite3
from sqlite3 import Error
#Ross imports
import re
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn



conn =None
tank_depth = None
minTemp = None
maxTemp = None
flag = True
tof = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=0x29)
spi = None
cs = None
mcp = None

def setup():
    global tof    
    global tank_depth
    global minTemp
    global maxTemp
    global spi
    global cs
    global mcp

    # starting tof sensor in Long range which is up to 4m
    print("Sensors Used: ")
    print("LM335z")
    print("MCP3008")
    tof.open()
    tof.start_ranging(3)
    
    #Ross please put your setup here
    # create the spi bus
    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
    # create the cs (chip select)
    cs = digitalio.DigitalInOut(board.D5)
    # create the mcp object
    mcp = MCP.MCP3008(spi, cs)
    #bla bla

    # database setup
    create_connection()
    #insert_dummy_data()

    #config values, taken from a config file
    a_file = open("./Data/config.txt","r")
    list_of_lines = a_file.readlines()
    list_of_lines = list_of_lines
    tank_depth = float(list_of_lines[0].rstrip())
    minTemp = float(list_of_lines[1].rstrip())
    maxTemp = float(list_of_lines[2])
    a_file.close()
    pass

def get_config():
    a_file = open("./Data/config.txt","r")
    list_of_lines = a_file.readlines()
    a_file.close()
    return list_of_lines

def get_WaterLevel():
    global tank_depth
    global tof
    #take 5 results and get the average to improve accuracy
    distance_in_mm = 0

    for i in range(0,7):
        if i>2:
            distance_in_mm += int(tof.get_distance())
    distance_in_mm = distance_in_mm/5

    wl = float( 1 - (distance_in_mm/1000.0)/float(tank_depth))*100.0
    wl = round(wl,0)
    return wl


def set_tank_depth(data):
    global tank_depth
    tank_depth = float(data)
    a_file = open("./Data/config.txt","r")
    list_of_lines = a_file.readlines()
    list_of_lines[0] = str(tank_depth)+"\n"

    #print (list_of_lines)
    a_file = open("./Data/config.txt","w")
    a_file.writelines(list_of_lines)
    a_file.close()
    pass

def set_min_Temp(data):
    global minTemp
    minTemp = float(data)
    a_file = open("./Data/config.txt","r")
    list_of_lines = a_file.readlines()
    list_of_lines[1] = str(minTemp)+"\n"

    a_file = open("./Data/config.txt","w")
    a_file.writelines(list_of_lines)
    a_file.close()
    pass

def set_max_Temp(data):
    global maxTemp
    maxTemp = float(data)
    a_file = open("./Data/config.txt","r")
    list_of_lines = a_file.readlines()
    list_of_lines[2] = str(maxTemp)

    a_file = open("./Data/config.txt","w")
    a_file.writelines(list_of_lines)
    a_file.close()
    pass

#NB NOTE FOR MATTHEW: programmed so that channel 0 of ADC is for water sensro and channel 1 of ADC is for air
def get_air_temp():
    global spi
    global cs
    global mcp
    airtemp=0
    for i in range(0,5):
        airsensor = AnalogIn(mcp, MCP.P1)
        airtemp += (airsensor.voltage * 100)-273 # insert code to get air temperature//DONE
    airtemp = airtemp/5 +295.6
    return round(airtemp,1)

def get_water_temp():
    global spi
    global cs
    global mcp
    watertemp=0
    for i in range(0,5):
        watersensor = AnalogIn(mcp, MCP.P0)
        watertemp += (watersensor.voltage * 100)-273 # insert code to get air temperature//DONE
    watertemp = watertemp/5  +293# insert code to get water temperature
    return round(watertemp,1)


def create_connection():
    #creats a database coonnection to a sqlite database
    global conn
    try:
        conn = sqlite3.connect('./Data/pythonsqlite.db')
        #print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def insert_dummy_data():

    try:
        connect = sqlite3.connect('./Data/pythonsqlite.db')
        cur = connect.cursor()
        cur.execute('CREATE TABLE waterlevel (stdate DATE, midnight REAL DEFAULT 0 , morning REAL DEFAULT 0, noon REAL DEFAULT 0, evening REAL DEFAULT 0, change REAL DEFAULT 50);')
        connect.commit()
        dummydate = datetime.datetime(2020, 10, 12)
        fakedata = (dummydate, 88, 83, 78, 69, 19)

        sqlite_insert = '''INSERT INTO waterlevel (stdate, midnight, morning, noon, evening, change) values (?, ?, ?, ?, ?, ?);'''
        cur.execute(sqlite_insert,fakedata)
        connect.commit()

        dummydate = datetime.datetime(2020, 10, 13)
        fakedata = (dummydate, 65, 58, 70, 66, -1)

        sqlite_insert = '''INSERT INTO waterlevel (stdate, midnight, morning, noon, evening, change) values (?, ?, ?, ?, ?, ?);'''
        cur.execute(sqlite_insert,fakedata)
        connect.commit()
    
    except Error as e:
        print(("failed to insert into the sqlite table",e))
    finally:
        if connect:
            connect.close()
            print(read_table)


def insert_table(data,pos):
    #create a new project into the project table

    try:
        connect = sqlite3.connect('./Data/pythonsqlite.db')
        cur = connect.cursor()
        data = float(data)
        mydate = datetime.datetime.now().date()
        print(mydate)
        cur.execute("SELECT * FROM waterlevel WHERE stdate = date('now');")
        print((cur.fetchall()))
        if cur.fetchall() == []:
            print(("no data entries for date: ",mydate))
            sqlite_insert = '''INSERT INTO waterlevel (stdate) values (?);'''
            cur.execute(sqlite_insert,(mydate,))
            connect.commit()
            print("date added")
        if(pos==0):
            sqlite_insert = '''UPDATE waterlevel SET midnight = ? WHERE stdate = date('now');'''
            cur.execute(sqlite_insert,(data,))
            connect.commit()
        elif(pos==1):
            sqlite_insert = '''UPDATE waterlevel SET morning = ? WHERE stdate = date('now');'''
            cur.execute(sqlite_insert,(data,))
            connect.commit()
        elif(pos==2):
            sqlite_insert = '''UPDATE waterlevel SET noon = ? WHERE stdate = date('now');'''
            cur.execute(sqlite_insert,(data,))
            connect.commit()
        elif(pos==3):
            sqlite_insert = '''UPDATE waterlevel SET evening = ? WHERE stdate = date('now');'''
            cur.execute(sqlite_insert,(data,))
            connect.commit()

            sqlite_insert = '''UPDATE waterlevel SET change = (SELECT (midnight - evening) FROM waterlevel WHERE stdate = date('now')) WHERE stdate = date('now'); '''
            cur.execute(sqlite_insert)
            connect.commit()

        print("wah")
    
    except Error as e:
        print(("failed to insert into the sqlite table",e))
    finally:
        if connect:
            connect.close()
    
def cal_daysleft():
    connect = sqlite3.connect('./Data/pythonsqlite.db')
    cur = connect.cursor()
    cur.execute('SELECT AVG(change) FROM waterlevel')
    data_avg = cur.fetchall()
    connect.close()
    return data_avg


def read_table():
    #reads the data out of the database
    connect = sqlite3.connect('./Data/pythonsqlite.db')
    cur = connect.cursor()
    cur.execute('SELECT * FROM waterlevel ORDER BY stdate ASC')
    data_1 = cur.fetchall()

    connect.close()
    return data_1



def menu():
    #menu user interacts with the API with
    global flag
    global tank_depth
    global minTemp
    global tof
    global maxTemp
    while flag:
        print("\nWelcome to Water Tank Managmnet")
        print("Please select a choice")
        print("1 to view data, 2 to set tank depth, 3 to set minimum Temperature , 4 to set maximum Temperature,5 to monitor, 6 to quit")
        choice = eval(input("Enter a command:\n"))

        if choice==1:   
            con = get_config()
            print("Config setting are")
            print(("The tank depth is set at "+str(re.sub("[^0-9.]",'',con[0]))+"m .\nThe minimum Temperature is: "+str(re.sub("[^0-9.]",'',con[1]))+", and the maximum Temperature is: "+str(re.sub("[^0-9.]",'',con[2]))))
            wlevel = get_WaterLevel()
            print("Sensor data")
            print(("The water level is: "+str(wlevel)+"%"))
            rows = cal_daysleft()
            row = float(re.sub("[^0-9.]",'',str(rows[0])))
            print(("There are: "+str(round(wlevel/row ,1))+" days left of water"))
            airT = get_air_temp()
            waterT = get_water_temp()
            print("The water temperatue is: "+str(waterT))
            print("The air temperatue is: "+str(airT))
            datatable = read_table()
            print("Date:                Midnight:   Morning:    Noon:   Evening:    Change:")
            for x in datatable:
                print((str(x[0])+"   "+str(x[1])+"        "+str(x[2])+"       "+str(x[3])+"      "+str(x[4])+"       "+str(x[5])))
            #print(row)
            
        elif (choice == 2):
		    #set Matts max water depth
            wlMax = eval(input("enter depth in m\n"))
            wlMax = float(wlMax)
            set_tank_depth(wlMax)
            print(("Tank depth has been updated to to: "+str(wlMax)+"m"))
        elif (choice == 3):
		    #set minimum temperature warning flag
            tmin= eval(input("enter minimum temperatue in celsius\n"))
            tmin = float(tmin)
            set_min_Temp(tmin)
            print(("the minimum temperature has been updated to to: "+str(tmin)))
        elif (choice == 4):
		    #set maximum temperature warning flag
            tmax= eval(input("enter maximum temperatue in celsius\n"))
            tmax = float(tmax)
            set_max_Temp(tmax)
            print(("the minimum temperature has been updated to to: "+str(tmax)))
        elif (choice == 5):
            print("press the w key to wake up")
            monitor()
            flag = False
            
        elif (choice == 6):
            flag = False
            tof.stop_ranging()
            print("goodbye")
        else:
            print("invalid input, please try again")
    pass
		


def monitor():
    #do stuff in background
    global flag
    global minTemp
    global maxTemp
    #idle animation
    Loading = ['\\____','/\___','_/\__','__/\_','___/\\','____/','_____']
    counter =0

    warningflag = False
    fl =True

    #flags used to check if data has been stored
    measuring = [True,True,True,True]

    print("press CTRL+C to exit idle")
    print("idling")
    starttime = time.time()


    while fl:      
        try:
            now = datetime.datetime.now()
            # Measuring time conditions
            if now.hour == 0 and now.minute == 0 and measuring[0]:
                insert_table(get_WaterLevel(),0)
                measuring[0] = False
                measuring[1] = True

            if now.hour == 6 and now.minute == 0 and measuring[1]:
                insert_table(get_WaterLevel(),1)
                measuring[1] = False
                measuring[2] = True
            
            if now.hour == 12 and now.minute == 0 and measuring[2]:
                insert_table(get_WaterLevel(),2)
                measuring[2] = False
                measuring[3] = True
            
            if now.hour == 18 and now.minute == 0 and measuring[3]:
                insert_table(get_WaterLevel(),3)
                measuring[3] = False
                measuring[0] = True
            
            #Warning Conditions for temperature and waterlevel
            if(get_air_temp() > maxTemp):
                print("Warning air temperature has exceeded maximum temperate allowed!!")
                warningflag = True

            elif(get_air_temp() < minTemp):    
                print("Warning air temperature has exceeded minimum temperate allowed")
                warningflag = True

            elif(get_water_temp() > maxTemp):
                print("Warning water temperature has exceeded maximum temperate allowed")
                warningflag = True

            elif( get_water_temp() < minTemp):
                print("Warning water temperature has exceeded minimum temperate allowed")
                warningflag = True

            elif(get_WaterLevel() < 5):
                print("Tank is 5% or less full, please disconnect from rainwater tank and use mains water")
                warningflag = True
                
            #stop program is there is a warning
            if(warningflag):
                print("please fix issue before continueing monitoring")
                fl = False
                quit()
            #Ideal if no warnings    
            else:
                #background recording of data
                if counter ==7:
                    counter=0              
                #print(chr(27) + "[2J") # clears terminal
                print((Loading[counter]))
                counter+=1
            #sleep program for 5 seconds, gives time for keyboard interupt, slows program down to make idle animation work, 
            time.sleep(5)
            wlevel = get_WaterLevel()
            print(now.strftime("%Y/%m/%d, %H:%M:%S"))
            print(("The water level is: "+str(wlevel)+"%"))
            wtemp = get_water_temp()
            atemp = get_air_temp()
            print(("The ambient air temperatur is: "+str(wtemp)+chr(176)+"C. The water temperaturn is: "+str(atemp)+chr(176)+"C."))

        #Idle escape condition
        except KeyboardInterrupt:
            print("exiting")
            #break the idle loop
            fl=False
                
    #escape condition has been met
    print("\nwaking up")
    endtime = time.time() - starttime
    endtime = round(endtime)
    print(("idled for: "+str(timedelta(seconds=endtime))))
    flag=True
    menu()
    pass

# Main that is executed when program starts
if __name__ == "__main__":
    try:
        # Call setup function
        setup()
        menu()
        
    except Exception as e:
        print(e)


          

    
