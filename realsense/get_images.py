

import pyrealsense2 as rs
import numpy as np
import cv2
import time

# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()

# Get device product line for setting a supporting resolution
pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)
device = pipeline_profile.get_device()
device_product_line = str(device.get_info(rs.camera_info.product_line))

found_rgb = False
for s in device.sensors:
    if s.get_info(rs.camera_info.name) == 'RGB Camera':
        found_rgb = True
        break
if not found_rgb:
    print("The demo requires Depth camera with Color sensor")
    exit(0)

config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 6)

config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 6)

# Start streaming
pipeline.start(config)

try:
	while True:

        # Wait for a coherent pair of frames: depth and color
		frames = pipeline.wait_for_frames()
		depth_frame = frames.get_depth_frame()
		color_frame = frames.get_color_frame()
		if not depth_frame or not color_frame:
			continue

		# Convert images to numpy arrays
		depth_image = np.asanyarray(depth_frame.get_data())
		color_image = np.asanyarray(color_frame.get_data())

        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
		depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
        
		k = cv2.waitKey(5)
		now = time.time()
		if k == 27:
			break
		elif k == ord('s'): # wait for 's' key to save and exit
			cv2.imwrite('images/img' + (str(now % 60)) + '.png', color_image)
			print("image saved!")

		cv2.imshow('Img',color_image)


finally:

    # Stop streaming
    pipeline.stop()