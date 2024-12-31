import DobotDllType as dType
import time
import serial.tools.list_ports
# import heartrate; heartrate.trace(browser=True)


def get_com_port(device_name):
	ports = serial.tools.list_ports.comports()
	for port, desc, hwid in sorted(ports):
		# print("{}: {}".format(port, desc))
		if device_name in desc:
			return port

CON_STR = {
    dType.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
    dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
    dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}


api = dType.load()

state = dType.ConnectDobot(api, get_com_port("Silicon"), 115200)[0]
print("Connect status:",CON_STR[state])

if (state == dType.DobotConnect.DobotConnect_NoError):

	dType.SetQueuedCmdClear(api)

	dType.SetHOMEParams(api, 200, 200, 200, 200, isQueued = 1)
	dType.SetPTPJointParams(api, 400, 400, 400, 400, 400, 400, 400, 400, isQueued = 1)
	dType.SetPTPCommonParams(api, 100, 100, isQueued = 1)
	dType.SetPTPJumpParams(api, 0, 0)
	pos = dType.GetPose(api)
	dType.SetIODO(api, 13, 1, 1)
	x = pos[0]
	y = pos[1]
	z = pos[2]
	rHead = pos[3]
	indexx = 0

def dobot(x,y,z=None,rHead=0):
	if (state == dType.DobotConnect.DobotConnect_NoError):
			pos = dType.GetPose(api)
			# x = pos[0]
			# y = pos[1]
			if z is None:
				z = pos[2]
			dType.SetQueuedCmdClear(api)

			indexx = dType.SetPTPCmd(api, 1, x,y,z, rHead, 1)[0]
			
			
			dType.SetQueuedCmdStartExec(api)
			# print(sd[x1], sd[y1], z1, z2)
			# print(indexx)
			while indexx > dType.GetQueuedCmdCurrentIndex(api)[0]:
				dType.dSleep(100)
			# print("sdf")
			dType.SetQueuedCmdStopExec(api)	
			# print("Asd")

dType.ClearAllAlarmsState(api)

def gripper_cmd(gripper_state):
	if (state == dType.DobotConnect.DobotConnect_NoError):
			dType.SetQueuedCmdClear(api)
			pos = dType.GetPose(api)
			x = pos[0]
			y = pos[1]
			z = pos[2]
			dType.SetQueuedCmdClear(api)

			indexx = dType.SetPTPCmd(api, 1, x,y,z, pos[3], 1)[0]
			indexx = dType.SetEndEffectorGripper(api, 1,  gripper_state, isQueued=1)[0]
			
			dType.SetQueuedCmdStartExec(api)
			while indexx > dType.GetQueuedCmdCurrentIndex(api)[0]:
				dType.dSleep(100)
			dType.SetQueuedCmdStopExec(api)	

# dType.SetEndEffectorGripper(api, 1,  0, isQueued=1)

def move_home():
	# dType.SetPTPCmd(api, 1, 0, 255, z, rHead, 1)
	if (state == dType.DobotConnect.DobotConnect_NoError):
		dType.SetQueuedCmdClear(api)
		pos = dType.GetPose(api)
		x=pos[0]
		y=pos[1]
		z = pos[2]
		rHead = pos[3]

		indexx = dType.SetPTPCmd(api, 1, x, y, 90, rHead, 1)[0]
		indexx = dType.SetPTPCmd(api, 1, 0, 255, 90, rHead, 1)[0]
		
		
		dType.SetQueuedCmdStartExec(api)
		while indexx > dType.GetQueuedCmdCurrentIndex(api)[0]:
			dType.dSleep(100)
		dType.SetQueuedCmdStopExec(api)	
  
if (state == dType.DobotConnect.DobotConnect_NoError):
		pos = dType.GetPose(api)
		x = pos[0]
		y = pos[1]
		z = pos[2]
		dType.SetQueuedCmdClear(api)

		indexx = dType.SetPTPCmd(api, 1, x,y,z, 0, 1)[0]
		
		
		dType.SetQueuedCmdStartExec(api)
		# print(sd[x1], sd[y1], z1, z2)
		# print(indexx)
		while indexx > dType.GetQueuedCmdCurrentIndex(api)[0]:
			dType.dSleep(100)
		# print("sdf")
		dType.SetQueuedCmdStopExec(api)	
		# print("Asd")