import pyrealsense2 as rs

# Initialize the pipeline and configure the streams
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
# pipeline.start(config)
pipeline_profile = pipeline.start(config)


try:
	while True:
		# Get the frames
		frames = pipeline.wait_for_frames()
		depth_frame = frames.get_depth_frame()
		color_frame = frames.get_color_frame()

		# Get the depth intrinsics
		depth_intrinsics = depth_frame.profile.as_video_stream_profile().intrinsics

		# Define the pixel coordinates
		pixel_x = 320
		pixel_y = 240

		# Get the depth value at the pixel coordinates
		depth_value = depth_frame.get_distance(pixel_x, pixel_y)
		# depth_sensor = depth_frame.profile.get_device().first_depth_sensor()
		depth_sensor = pipeline_profile.get_device().first_depth_sensor()

		depth_scale = depth_sensor.get_depth_scale()

        # Deproject the pixel coordinates to real-world coordinates
		real_world_coords = rs.rs2_deproject_pixel_to_point(
            depth_intrinsics, [pixel_x, pixel_y], depth_value / depth_scale
        )

        # Print the real-world coordinates
		print(f"Real-world coordinates: {real_world_coords}")

finally:
    # Stop the pipeline and release resources
    pipeline.stop()