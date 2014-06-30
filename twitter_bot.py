'''
Created on Apr 25, 2013

@author: matt@alamedalabs.com
'''


import time, datetime
import serial, measuremouse, twitter, json


def tweet(tweet_status):
    
    
    
    # OAuth authentication
    api = twitter.Api(
    consumer_key = '##',
    consumer_secret = '##',
    access_token_key = '##',
    access_token_secret = '##'
    )
    
    status = api.PostUpdate(tweet_status)
    print "Posted successfully"
    print status.text
    
    
    
#-------------------------------------------------------------------------------
# FTP site credentials, for uploading data to a server 

FTP_HOST = '##'
FTP_USER = '##'
FTP_PASS = '##'



MEASUREMENT_STORAGE_FILE = 'mfc_raw_data.json' 


MEASUREMENT_STORAGE_DESCRIPTOR = 'MFC-battery data' #General data holder

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


my_dict = init(MEASUREMENT_STORAGE_FILE,MEASUREMENT_STORAGE_DESCRIPTOR)


working = True

while(working):
    


