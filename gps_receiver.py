import redis
import subprocess

class gpsMessages:
    def __init__(self):
        self._globalLatLong = [0.0,0.0]

    def messageCallback(self,message):
        message = eval(message['data'].decode("utf-8"))
        self._globalLatLong = message
    
    def getLatLong(self):   
        return self._globalLatLong    

def main():
    #redis setup
    red = redis.Redis(host='localhost', port=6379, db=0)
    pReceive = red.pubsub()
    gpsMessageInstance = gpsMessages()
    pReceive.subscribe(**{'gps': gpsMessageInstance.messageCallback})
    thread = pReceive.run_in_thread(sleep_time=0.001)
    while True:
        print(gpsMessageInstance.getLatLong())

if __name__ == "__main__":
    main()
