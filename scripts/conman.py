#!/usr/bin/env python
import rospy
from std_msgs.msg import *
from sensor_msgs.msg import NavSatFix
import comms


class _conman():
    """Conman: connection manager. It automatically sends a heartbeat with GPS fix if available. 
    """
    def __init__(self):
        ip = rospy.get_param('/ip')
        port = rospy.get_param('/port')
        TMID = rospy.get_param('/TID')
        mode=3
        if (rospy.has_param('/mode')):
            mode=rospy.get_param('/mode')
        gpsChannel="/gps/fix"
        if (rospy.has_param('/GPSChannel')):
            gpsChannel=rospy.get_param('/GPSChannel')
        comsub = rospy.Subscriber("comms", String, self.comms_callback)
        navsub = rospy.Subscriber(gpsChannel, NavSatFix, self.nav_callback)
        comms.conman_init(ip, port, TMID)
        self.hbstate = {
            'mode': mode,
            'AUVstat': 1
        }
        self.hbready = False
        if rospy.has_param('/debug'):
            self.hbstate = {
                'latitude': 0,
                'longitude': 0,
                'longEW': 'E',
                'latNS': 'N',
                'mode': mode,
                'AUVstat': 1
            }
            self.hbready = True

    def nav_callback(self, msg):
        self.hbstate.latitude = abs(msg.latitude)
        if (msg.latitude>0):
            self.hbstate.latNS='N'
        else:
            self.hbstate.latNS='S'
        self.hbstate.longitude = abs(msg.longitude)
        if (msg.longitude>0):
            self.hbstate.longEW='E'
        else:
            self.hbstate.longEW='W'
        self.hbready=True

    def comms_callback(self, msg):
        """Processes messages from communications.

        Arguments:
            msg {[type]} -- [description]
        """
        pass

    def send_heartbeat(self):
        """Send the heartbeat message.
        """
        if self.hbready:
            comms.sendHeartbeatMessage(self.hbstate)


# this should always be run

conman = _conman()
rospy.init_node("communicator")
rate = rospy.Rate(1)
while not rospy.is_shutdown():
    # broadcast the heartbeat message
    fakeState = {}
    conman.send_heartbeat()

    rate.sleep()
