import numpy as np
import matplotlib.pyplot as plt

def interpolate_points(point1, point2, num_points):


    point1 = np.array(point1)
    point2 = np.array(point2)
    
    # Calculate the vector between the two points
    vector = point2 - point1
    
    # Calculate the unit vector representing the direction of the line
    unit_vector = vector / np.linalg.norm(vector)
    
    # Calculate the step size (distance between interpolated points)
    step_size = np.linalg.norm(vector) / (num_points - 1)
    
    # Initialize a list to store the interpolated points
    interpolated_points = []
    
    # Generate the interpolated points
    for i in range(num_points):
        point = point1 + i * step_size * unit_vector
        interpolated_points.append(tuple(point))
    
    return interpolated_points

point1 = (606, 426)
point2 = (76, 434)
num_points = 10

interpolated_points = interpolate_points(point1, point2, num_points+1)
print(interpolated_points)

x_coords, y_coords = zip(*interpolated_points)

# Plot the points
plt.figure(figsize=(8, 6))
plt.plot(x_coords, y_coords, 'ro-')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Interpolated Points')
plt.grid(True)
plt.show()