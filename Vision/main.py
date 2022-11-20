from RoboSub import challenge
import rospy
from std_msgs.msg import String


Step1 = challenge()
# Publisher Function
def talker():
    pub = rospy.Publisher('vision_py', String, queue_size = 25)
    rospy.init_node('vision_py', anonymous=True)
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        #Vision Code
        Step1.GetCentroidLocation(pub)  
        





