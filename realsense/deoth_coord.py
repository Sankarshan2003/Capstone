import numpy as np
import cv2
import pyrealsense2 as rs

# Create a pipeline
pipeline = rs.pipeline()
config = rs.config()

config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

# Start streaming
# pipeline.start(config)
pipeline_profile = pipeline.start(config)

# Create align object
align_to = rs.stream.color
align = rs.align(align_to)

while True:
    # Wait for a coherent pair of frames: depth and color
    frames = pipeline.wait_for_frames()
    aligned_frames = align.process(frames)
    depth_frame = aligned_frames.get_depth_frame()
    color_frame = aligned_frames.get_color_frame()
    
    depth_intrinsics = depth_frame.profile.as_video_stream_profile().intrinsics
    depth_sensor = pipeline_profile.get_device().first_depth_sensor()

    depth_scale = depth_sensor.get_depth_scale()    
    if not depth_frame or not color_frame:
        continue

    depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(np.asanyarray(depth_frame.get_data()), alpha=0.03), cv2.COLORMAP_JET)
    # color_image = cv2.cvtColor(np.asanyarray(color_frame.get_data()), cv2.COLOR_BGR2RGB)
    color_image = np.asanyarray(color_frame.get_data())
    
    
    camera_x = 0
    camera_y = 0
    camera_z = 1.0

    # Project the 3D camera coordinates to 2D pixel coordinates
    pixel_x, pixel_y = rs.rs2_project_point_to_pixel(depth_intrinsics, [camera_x, camera_y, camera_z])
    pixel_x = int(pixel_x)
    pixel_y = int(pixel_y)
    cv2.circle(color_image, (pixel_x, pixel_y), 5, (0, 255, 0), 2)
    # Display the RGB image
    cv2.imshow("RGB Image", color_image)
    cv2.imshow("Depth Image", depth_colormap)
    
    # Get the depth value at the clicked point
    def on_mouse_click(event, x, y, flags, param):
        # x=467
        # y=260
        # x=507
        # y=313
        if event == cv2.EVENT_LBUTTONDOWN:
            depth_value = depth_frame.get_distance(x, y)
            print(f"Depth value at pixel ({x}, {y}): {depth_value} meters")
            real_world_coords = rs.rs2_deproject_pixel_to_point(
            depth_intrinsics, [x, y], depth_value / depth_scale
            )

            # Print the real-world coordinates
            print(f"Real-world coordinates: {real_world_coords}")
            r_x = 227+1.7-real_world_coords[1]+3 - 1.5 -20 + 1.8
            r_y = 57-4.5-real_world_coords[0] - 10 + 4.3
            print(f"Pickup at {r_x,{r_y}}")
    
    cv2.setMouseCallback("RGB Image", on_mouse_click)
    
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

# Stop streaming
pipeline.stop()
cv2.destroyAllWindows()
