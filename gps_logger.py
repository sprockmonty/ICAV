#!/usr/bin/env python
import rospy
import math
import time
from geometry_msgs.msg import PoseStamped
from sensor_msgs.msg import NavSatFixi
import subprocess

class gpsLogger:
    def __init__(self):
        self._globalLatLong = [0.0,0.0] #global location [lat,long]
        self._globalAlt = 0.0 #global altitude
        self._log = []
        self._jobID = 0
        subprocess.Popen(["redis-server"])
        self._red = redis.Redis(host='localhost', port=6379, db=0)
        self._pRed = pubsub()
        self._pRed.subscribe('gps')

    def locationCallback(self,msg):
        self._globalLatLong[0] = msg.latitude
        self._globalLatLong[1] = msg.longitude
        self._globalAlt = msg.altitude
        #Use dictionary to log position, time and file location
        self._red.publish(self._globalLatLong)
    
    def getLocation():
        return self._globalLatLong
   
def main():
    rospy.init_node('gps_logger')   # make ros node
    gpsLoggerInstance = gpsLogger()
    rospy.Subscriber("/mavros/global_position/global",NavSatFix ,gpsLoggerInstance.locationCallback)    #using global position rather than local (point to note, might need changing)
    rospy.spin()    #keeps python from exiting until this node is stopped


if __name__ == '__main__':
    main()
