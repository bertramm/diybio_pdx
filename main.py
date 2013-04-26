'''
Created on Apr 25, 2013

@author: matt@alamedalabs.com
'''


import json, datetime, time, serial
from ftplib import FTP



#-------------------------------------------------------------------------------
# FTP site credentials, for uploading data to a server 

FTP_HOST = 'alamedalabs.com'
FTP_USER = 'bot@alamedalabs.com'
FTP_PASS = '<enter password>'


#-------------------------------------------------------------------------------


MEASUREMENT_STORAGE_FILE = 'mfc_raw_data.json' 

MEASUREMENT_STORAGE_DESCRIPTOR = 'MFC-battery data' #General data holder


CHANNEL_NAME_SHEET = {'CO':'Aaron & Josh',
                      'C1':'Mitch',
                      'C2':'Marshal & Gabbi',
                      'C3':'Matt B.',
                      'C4':'Little Brownie',
                      'C5':'Avishan',
                      'C6':'Nathan',
                      'C7':'Justin'
                      }

#-------------------------------------------------------------------------------
#Microcontroller parameters. This library was developed with Teensy 2+

VIRTUAl_COMM_PORT = 29 # windows specific port, linux is slitely different.
LOAD_RESIST = 100.0 # Resistive load on each cell. Ohms
MAX_VOLTAGE = 5.0 # What is the max voltage for each analog input
CHANNEL_BITS = 2**10 #How many bits are the analog to digital inputs

#-------------------------------------------------------------------------------
#Logging specific globals

LOG_FREQUENCY = 60 # seconds
SAVE_LOCALLY_FREQUENCY = 10 #minutes
SAVE_REMOTELY_FREQUENCY = 11 #minutes


#-------------------------------------------------------------------------------
#Run in simulation mode if the microcontroller is not hooked up

SIMULATION_MODE = True


#-------------------------------------------------------------------------------
#json parsing library, and other odds and ends

dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime.datetime) else None
buffer = ""

def init(sFileName, sDescription):
    """init the dictionary object """
    
    try:
        with open(sFileName) as f:
            my_dict = json.load(f)
        
    
    except:
    
        #assume there was an error, possibly the file does not exist
        my_dict = {'descriptor':sDescription ,'measurements':[]}
        with open (sFileName, 'w') as f:
            json.dump(my_dict,f)
        
    return my_dict


def save(my_dict,sFileName, ftp_object, remote=False ):
    """save the dictionary object as JSON 
    
    save remotely or locally?
    """
    try:
        with open (sFileName, 'w') as f:
            json.dump(my_dict,f)
            
    except:
        pass
    
    try:
        if remote is True:
            
            ftp_object.storbinary('STOR '+sFileName, open(sFileName,'rb'))
    except:
        
        print "shit the FTP upload this failed"


def parse_message(message):
    
    """make shift serial parser"""

    if len(message)<8:
    
        return None, message
    
    else:
        
        try:
            
            splt_String = message.split('\r\n', 1)
            return splt_String[0], splt_String[1]
        
        except:
            return None, message



#---------------------------------------------------------------------
#Setup serial object
if SIMULATION_MODE == False:
    
    #Setup serial port
    ser = serial.Serial(
                        port=VIRTUAl_COMM_PORT, 
                        baudrate=9600, 
                        timeout=1,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        bytesize=serial.EIGHTBITS,
                        xonxoff = True,
                        rtscts = True
                        )




#--------------------------------------------------------------------------
#Initialize the data dictionary
my_dict = init(MEASUREMENT_STORAGE_FILE,MEASUREMENT_STORAGE_DESCRIPTOR)
   
#manually reset the dictionary, un comment this if you want to wipe previous data   
#my_dict = {'descriptor': MEASUREMENT_STORAGE_DESCRIPTOR ,'measurements':[]}


#-------------------------------------------------------------------------------
#Setup the ftp object

try:
    ftp = FTP(FTP_HOST, FTP_USER, FTP_PASS)
    
except:
    
    print "Could not connect to the FTP server"




#---------------------------------------------------------------------------------
#Set three timers for logging, saving locally, and saving remotely
start_time_one =datetime.datetime.now()
start_time_two =datetime.datetime.now()
start_time_three =datetime.datetime.now()


#---------------------------------------------------------------------------------
#instantiate simulation varaibles
if SIMULATION_MODE == True:
    volts = 0


#---------------------------------------------------------------------------------
#main logic loop
while(True):
    """" Start main loop"""
    
    
    #calculate timers one to log, one to save locally, and one to save remotely
    diff_time_one = datetime.datetime.now()-start_time_one
    diff_time_two = datetime.datetime.now()-start_time_two
    diff_time_three = datetime.datetime.now()-start_time_three

    #---------------------------------------------------------------------------------
    #SAVE LOCALLY
    
    if   diff_time_one.seconds > SAVE_LOCALLY_FREQUENCY*60.0:
        
        
        start_time_one = datetime.datetime.now()
        print "Logging locally: " , start_time_one
        
        save(my_dict,MEASUREMENT_STORAGE_FILE,ftp)
    
    
    #---------------------------------------------------------------------------------
    #SAVE Remotely
    elif diff_time_two.seconds > SAVE_REMOTELY_FREQUENCY*60.0:
        

        start_time_two = datetime.datetime.now()
        print "Logging remotely: " , start_time_two
        
        save(my_dict,MEASUREMENT_STORAGE_FILE,ftp,True)

                                
 
 
 
    #---------------------------------------------------------------------------------
    #In simulation mode make up voltages, then sleep

    if SIMULATION_MODE == True:
            
            volts = volts + 0.000005
            channel = 'C1'
            
            time.sleep(1)
    
    
    #---------------------------------------------------------------------------------
    #Or not read the serial port and parse. The parser is a makeshift buffer.

    else:
        
        #Hack to parse serial
        
        buffer = buffer + ser.read()
        #print buffer
        message_one, buffer = parse_message(buffer)
        
        if message_one is not None:
            
            volts = int(message_one.split(':')[1])*MAX_VOLTAGE/CHANNEL_BITS/100.0
            channel = message_one.split(':')[0]
            
    
    
    #---------------------------------------------------------------------------------
    #Only only if it's time to record
        
    if   diff_time_three.seconds > LOG_FREQUENCY:
        
        print "logging data: ", start_time_three
        
        print round(volts*1000,1)
        start_time_three = datetime.datetime.now()
        my_dict['measurements'].append({"power(mW)": round(volts/LOAD_RESIST,3), 
                                        "voltage(mV)": round(volts*1000,1), 
                                        "name": "test name", 
                                        "Channel": CHANNEL_NAME_SHEET[channel],
                                        "time": json.dumps(datetime.datetime.now(), default=dthandler).replace('\"','')
                                        })

