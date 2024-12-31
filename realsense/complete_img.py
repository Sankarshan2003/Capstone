# 1-> move dobot out of the way
# 2-> capture pic and find object
# 3-> move dobot and pick and move and place
from skimage.metrics import structural_similarity
import dobot_pick as dobot
import numpy as np
import cv2
import pyrealsense2 as rs
import time
# import yolo_tt

print("asd")

dobot.move_home()

pipeline = rs.pipeline()
config = rs.config()

config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 6)
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 6)

pipeline_profile = pipeline.start(config)

align_to = rs.stream.color
align = rs.align(align_to)

frames = pipeline.wait_for_frames()
aligned_frames = align.process(frames)
depth_frame = aligned_frames.get_depth_frame()
color_frame = aligned_frames.get_color_frame()

bg_captured = False
dobot.gripper_cmd(0)

def coord_transformation(x,y,z):
    # T =
    #  0    -1     0   227
    # -1     0     0    57
    #  0     0    -1     0
    #  0     0     0     1
    T = np.array([[0, 1, 0, 227],
              	  [1, 0, 0, 57],
              	  [0, 0, -1, 0],
                  [0, 0, 0, 1]])
    coords = np.dot(T,[x,y,z,1])
    return coords

def det_obj(frame):#for isolating objects and finding their center(s)/orientation(s)
	print("Inside det_obj")
	bg_frame = cv2.imread('images\\bg.png', cv2.COLOR_BGR2GRAY)

	before_gray = cv2.cvtColor(bg_frame, cv2.COLOR_BGR2GRAY)
	after_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	(score, diff) = structural_similarity(before_gray, after_gray, full=True)
	# print("Image Similarity: {:.4f}%".format(score * 100))

	diff = (diff * 255).astype("uint8")
	diff_box = cv2.merge([diff, diff, diff])

	thresh = cv2.threshold(
		diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
	contours = cv2.findContours(
		thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	contours = contours[0] if len(contours) == 2 else contours[1]

	mask = np.zeros(bg_frame.shape, dtype='uint8')
	filled_after = frame.copy()

	for c in contours:
		area = cv2.contourArea(c)
		if area > 40:
			cv2.drawContours(mask, [c], 0, (255, 255, 255), -1)
            # cv2.drawContours(filled_after, [c], 0, (0,255,0), -1)

	cv2.imshow('mask_det', mask)
	# cv2.imshow('filled after', filled_after)
	cv2.waitKey()

	mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

	ret, mask = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)
	num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(
        mask, connectivity=8)

	for label in range(1, num_labels):
		mask = np.uint8(labels == label) * 255
		isolated_object = cv2.bitwise_and(mask, mask, mask=mask)

		contours, _ = cv2.findContours(
            isolated_object, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

		if len(contours) > 0:
			largest_contour = max(contours, key=cv2.contourArea)
			area = cv2.contourArea(largest_contour)
			perimeter = cv2.arcLength(largest_contour, True)
			circularity = 4 * np.pi * area / (perimeter * perimeter)

			if circularity > 0.8:
				orientation = 0
			else:
				contour_points = largest_contour.reshape(
					-1, 2).astype(np.float32)
				mean, eigenvectors = cv2.PCACompute(contour_points, mean=None)
				principal_axis = eigenvectors[0]
				orientation = np.arctan2(principal_axis[1], principal_axis[0])
				print("ASdasdasdasdasdasdasd",np.degrees(orientation))
				orientation = orientation + np.pi / 2
				print("ASdasdasdasdasdasdasd",np.degrees(orientation))
				print(orientation > (np.pi / 2))
				if orientation > (np.pi / 2):
					orientation = orientation - np.pi
				print("ASdasdasdasdasdasdasd",np.degrees(orientation))
					

			angle_degrees = np.degrees(orientation)
			print(f"Object {label} orientation: {angle_degrees:.2f} degrees")

			M = cv2.moments(largest_contour)
			cx = int(M['m10'] / M['m00'])
			cy = int(M['m01'] / M['m00'])

			line_length = 30
			x2 = int(cx + line_length * np.cos(orientation))
			x2_i = int(cx - line_length * np.cos(orientation))
			y2 = int(cy + line_length * np.sin(orientation))
			y2_i = int(cy - line_length * np.sin(orientation))
			print(f"center of the object: {cx},{cy}")

			image_with_line = cv2.line(frame.copy(), (cx, cy), (x2, y2), (255, 0, 0), 2)
			# image_with_line = cv2.line(image_with_line, (cx, cy), (x2_i, y2_i), (255, 0, 0), 2)
			# cv2.imshow(f'Image with orientation line', image_with_line)
			# cv2.waitKey()
			dobot_pose = rs_coord([cx, cy, np.degrees(orientation)])
			dobot_pick_place(dobot_pose)
	
	# print(cx, cy, orientation)
	# return cx, cy, np.degrees(orientation)


def capture_bg():
	print("Prep the workspace for background capture...")
	for i in range(3,0):	
		print(i)
		time.sleep(1)
	frames = pipeline.wait_for_frames()
	aligned_frames = align.process(frames)
	depth_frame = aligned_frames.get_depth_frame()
	color_frame = aligned_frames.get_color_frame()

	depth_image = np.asanyarray(depth_frame.get_data())
	color_image = np.asanyarray(color_frame.get_data())
	cv2.imshow("imageeeee", color_image)
	cv2.waitKey()
	cv2.imwrite("images\\bg.png", color_image)

def rs_coord(obj_pose=None):
	print("inside rs")
	# x, y, orientation = obj_pose
	frames = pipeline.wait_for_frames()
	aligned_frames = align.process(frames)
	depth_frame = aligned_frames.get_depth_frame()
	color_frame = aligned_frames.get_color_frame()
	depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(np.asanyarray(depth_frame.get_data()), alpha=0.03), cv2.COLORMAP_JET)

	depth_image = np.asanyarray(depth_frame.get_data())
	color_image = np.asanyarray(color_frame.get_data())

	# cv2.imshow("Depth Map", depth_colormap)
	# cv2.waitKey()
	# obj_pose = det_obj(color_image)
	# print(obj_pose)
	if obj_pose is not None:
		x, y, orientation = obj_pose
	# x=467
	# y=260
	# orientation=0


	depth_intrinsics = depth_frame.profile.as_video_stream_profile().intrinsics
	depth_sensor = pipeline_profile.get_device().first_depth_sensor()

	depth_scale = depth_sensor.get_depth_scale()
	depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(
		np.asanyarray(depth_frame.get_data()), alpha=0.03), cv2.COLORMAP_JET)
	# pixel_x, pixel_y = rs.rs2_project_point_to_pixel(depth_intrinsics, [camera_x, camera_y, camera_z])
	# pixel_x = int(pixel_x)
	# pixel_y = int(pixel_y)

	# x = obj_pose[0]
	# y = obj_pose[1]
	depth_value = depth_frame.get_distance(x, y)

	print(f"Depth value at pixel ({x}, {y}): {depth_value} meters")
	real_world_coords = rs.rs2_deproject_pixel_to_point(
		depth_intrinsics, [x, y], depth_value / depth_scale
	)

	# Print the real-world coordinates
	print(f"Real-world coordinates: {real_world_coords}")
	r_x = 227+1.7-real_world_coords[1]+3-1.5-20
	r_y = 57-4.5-real_world_coords[0]-10
	r_z = real_world_coords[2]+3
	r_rHead = orientation
	print(f"Pickup at {r_x, r_y, r_z, r_rHead} deg")
	
	return r_x,r_y,r_z,r_rHead

def dobot_pick_place(pose):	
	r_x,r_y,c_z,r_rHead = pose
	r_rHead = -r_rHead
	m_x = 20
	m_y =30
	# r_z = 45
	r_z = 622-c_z+10-20 - 5
	# r_z = 622-c_z+10
	if r_z<-35:
		r_z = -35
  
	print("dobott",r_x,r_y,r_z,r_rHead)
 
	dobot.dobot(r_x, r_y)
	dobot.dobot(r_x, r_y, rHead=r_rHead)
	# dobot.dobot(r_x, r_y, -35,rHead=r_rHead)
	dobot.dobot(r_x, r_y, r_z,rHead=r_rHead)
	dobot.gripper_cmd(1)
	time.sleep(0.5)
	dobot.dobot(r_x, r_y, 90,rHead=r_rHead)
	
	dobot.dobot(-25,-275,90,rHead=r_rHead)
	# dobot.dobot(-25,-275,r_z,rHead=r_rHead)
 
	# dobot.dobot(r_x+m_x, r_y+m_y, r_z,rHead=r_rHead)
	dobot.gripper_cmd(0)
	time.sleep(0.5)
	dobot.dobot(-25,-275,90,rHead=r_rHead)
	# dobot.dobot(r_x+m_x, r_y+m_y, 90,rHead=r_rHead)
	# dobot.dobot(r_x+m_x, r_y+m_y, 90)
    
    
def yolo(frame):
	tubes = yolo_tt.getmatrix(frame)
	print(tubes)
	for tube in tubes:
		dobot_pose = rs_coord([tube[0], tube[1], 0])
		# dobot_pick_place(dobot_pose)
    

def main():
	while True:
		print("1. Capture Background \n2. Pick and Place \n3. Exit")
		opt = int(input())
		if opt == 1:
			dobot.move_home()
			capture_bg()
		if opt == 2:
			dobot.move_home()
			time.sleep(1)
			frames = pipeline.wait_for_frames()
			aligned_frames = align.process(frames)
			depth_frame = aligned_frames.get_depth_frame()
			color_frame = aligned_frames.get_color_frame()
			color_image = np.asanyarray(color_frame.get_data())
			# cv2.imshow("asd",color_image)
			# cv2.waitKey(0)
			# cv2.destroyAllWindows()
			# yolo(color_image)
			pose = det_obj(np.asanyarray(color_frame.get_data()))
			# dobot_pose = rs_coord()
			# dobot_pick_place(dobot_pose)
		if opt == 3:
			break
  
if __name__ == "__main__":
	try:
		print("asdsd")
		main()
	finally:
		pipeline.stop()
