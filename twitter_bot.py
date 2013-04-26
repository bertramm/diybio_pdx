'''
Created on Apr 25, 2013

@author: matt@alamedalabs.com
'''


import time, datetime
import serial, measuremouse, twitter, json


def tweet(tweet_status):
    
    
    
    # OAuth authentication
    api = twitter.Api(
    consumer_key = 'IJ69UOCvmk4slkgzJBDsWg',
    consumer_secret = '9wy4MDF2GXd1dkOrtbofXZYSoGO5btxDzyTBlLTSOc',
    access_token_key = '1366362246-GQw4OJBu9FTMKOHgn0aCql82PwuZzltk8v6trWr',
    access_token_secret = 'HPbqJZg6vNTAS9X63kA2LriQBmRxyikJLintT9ZA'
    )
    
    status = api.PostUpdate(tweet_status)
    print "Posted successfully"
    print status.text
    
    
    
#-------------------------------------------------------------------------------
# FTP site credentials, for uploading data to a server 

FTP_HOST = 'alamedalabs.com'
FTP_USER = 'bot@alamedalabs.com'
FTP_PASS = 'laser@45'



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
    


