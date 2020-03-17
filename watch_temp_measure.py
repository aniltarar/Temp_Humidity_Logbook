import sqlite3
from csv import writer
import datetime
from time import sleep
import math
import grovepi
from grove_rgb_lcd import *

# Connect the Grove Rotary Angle Sensor to analog port A0
# SIG,NC,VCC,GND
potentiometer = 0
sensor = 6
blue = 0
button = 3

grovepi.pinMode(potentiometer,"INPUT")
grovepi.pinMode(button,"INPUT")

# Reference voltage of ADC is 5v
adc_ref = 5

# Vcc of the grove interface is normally 5v
grove_vcc = 5

# Full value of the rotary angle is *300 (now set to 255) degrees, as per it's specs (0 to 300)
full_angle = 255

#print("sensor_value = %d voltage = %.2f degrees = %.1f" %(sensor_value, voltage, degrees))
def append_list_as_row(write_obj, list_of_elem):
    # Open file in append mode
    with open('/home/pi/Desktop/python_scripts/Watch/temp_logbook.csv', 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)

def append_csv():
    [temp,humidity] = grovepi.dht(sensor,blue)
    temp_measure = "%.02f"%(temp)
    humidity_measure = "%.02f"%(humidity)
    new_mesurement = ['{}-{}-{}'.format(now.day,now.month,now.year),'{}'.format(now.strftime("%X")),'{}'.format(temp_measure),'{}'.format(humidity_measure)]
    append_list_as_row('write_obj',new_mesurement)

def append_sql():
    [temp,humidity] = grovepi.dht(sensor,blue)
    temp_measure = "%.02f"%(temp)
    humidity_measure = "%.02f"%(humidity)
    conn = sqlite3.connect('temp_log.db')
    cur = conn.cursor()
    Date = str('{}-{}-{}'.format(now.day,now.month,now.year))
    Time = str('{}'.format(now.strftime("%X")))
    Temperature = temp_measure
    Humidity = humidity_measure
    cur.execute('''INSERT INTO Logbook(Date, Time, 'Temperature C', Humidity)
        VALUES (?,?,?,?)''',(Date, Time, Temperature, Humidity))
    conn.commit()
    

# while degrees <= 100:
#     print("yes")
#     setRGB(degrees,255-degrees,0)
a = 0
while True:
    try:
        now = datetime.datetime.now()
        full_hour = int(now.strftime("%M"))
        if (grovepi.digitalRead(button)==0):
            #print(full_hour)
            #print(full_hour)
            setText_norefresh('{} {}\n{} {}'.format(now.strftime("%x"),now.strftime("%A"), now.strftime("%X"),now.strftime("%B")))
            # Read sensor value from potentiometer
            sensor_value = grovepi.analogRead(potentiometer)
            # Calculate voltage
            voltage = round((float)(sensor_value) * adc_ref / 1023, 2)
            # Calculate rotation in degrees (0 to 255)
            degrees = int(round((voltage * full_angle) / grove_vcc, 2))
            setRGB(degrees,degrees,degrees)
            if(full_hour == 0):
                if a == 0:
                    sleep(1)
                    append_sql()
                    sleep(1)
                    append_csv()
                    a = a + 1

            elif(full_hour == 1):
                a = 0

        elif (grovepi.digitalRead(button)==1):
            [temp,humidity] = grovepi.dht(sensor,blue)
            sleep(0.4)
            if math.isnan(temp) == False and math.isnan(humidity) == False:
                setText("temp = %.02f C \nhumidity =%.02f%%"%(temp, humidity))
                sleep(2.5)
                setText("")
        
    except KeyboardInterrupt:
        setRGB(0,0,0)
        setText("")
    except IOError:
        print ("Error")
        
#         if (grovepi.digitalRead(button)==1):
#             setText(time_string)
#             setRGB(100,100,0)
#         if (degrees <= 50):
#             setText(time_string)
#             setRGB(0,128,0)
#             time.sleep(2)
#         elif(degrees > 50 and degrees <100):
#             setText(time_string)
#             setRGB(255,0,255)
#             time.sleep(2)
#         else:
#             if math.isnan(temp) == False and math.isnan(humidity) == False:
#                 setText("temp = %.02f C humidity =%.02f%%"%(temp, humidity))
#                 setRGB(0,0,255)
#                 time.sleep(2)
#     except KeyboardInterrupt:
#         setRGB(0,0,0)
#         setText("")
#         break
#     except IOError:
#         print ("Error")
