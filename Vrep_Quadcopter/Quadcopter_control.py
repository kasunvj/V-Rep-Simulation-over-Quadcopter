import vrep
import numpy as np
import time
import matplotlib.pyplot as plt
import cv2

plot_floorcamera_pos = [0,1]

vrep.simxFinish(-1) # just in case, close all opened connections
clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5)
print(clientID) # if 1, then we are connected.
if clientID!=-1:
	print ("Connected to remote API server")
else:
	print("Not connected to remote API server")

err_code,floorcamera_handle = vrep.simxGetObjectHandle(clientID,"Quadricopter_floorCamera",vrep.simx_opmode_blocking)
err_code,target_handle = vrep.simxGetObjectHandle(clientID,"Quadricopter_target",vrep.simx_opmode_blocking)
err_code,camera = vrep.simxGetObjectHandle(clientID,"Vision_sensor",vrep.simx_opmode_oneshot_wait)

err_code,target_pos = vrep.simxGetObjectPosition(clientID,target_handle,-1,vrep.simx_opmode_blocking)
err_code,floorcamera_pos = vrep.simxGetObjectPosition(clientID,floorcamera_handle,-1,vrep.simx_opmode_blocking)
err_code,resolution,image = vrep.simxGetVisionSensorImage(clientID,camera,0,vrep.simx_opmode_streaming)

#img = np.array(image, dtype = np.uint8)
#print(resolution)
#img.resize([resolution[0],resolution[1],3])
#plt.imshow(img,origin="lower")
#plt.show()
print("On your mark")
time.sleep(2)
err_code = vrep.simxSetObjectPosition(clientID,target_handle,-1,[0.95,0,3],vrep.simx_opmode_streaming)

print("Get set")
time.sleep(0.2)

print("Go!!")
t = time.time()
while (time.time()-t)<10:
		#getting image
		err_code,resolution,image = vrep.simxGetVisionSensorImage(clientID,camera,0,vrep.simx_opmode_buffer)
		if err_code == vrep.simx_return_ok:
			#print("image Ok")
			img = np.array(image, dtype = np.uint8)
			img.resize([resolution[1],resolution[0],3])
			cv2.imshow('image',img)
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break
			elif err_code == vrep.simx_return_novalue_flag:
				print("no image")
				pass
			

		#get position odf target and copter
		err_code,target_pos = vrep.simxGetObjectPosition(clientID,target_handle,-1,vrep.simx_opmode_blocking)
		err_code,floorcamera_pos = vrep.simxGetObjectPosition(clientID,floorcamera_handle,-1,vrep.simx_opmode_blocking)
		#print(target_pos)
		print(floorcamera_pos)

		#plotting graphs of movement
		plot_floorcamera_pos = floorcamera_pos.append(floorcamera_pos[0])
		#plt.plot(target_pos[0])
		#plt.plot(plot_floorcamera_pos)
		#plt.show()

print("Done")