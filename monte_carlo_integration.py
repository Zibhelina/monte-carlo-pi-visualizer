import random 
import math 
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation

PI = math.pi
POINTS_PER_FRAME = 50
TOTAL_TARGET_POINTS = 100000
if TOTAL_TARGET_POINTS % POINTS_PER_FRAME == 0:
    FRAMES = int(TOTAL_TARGET_POINTS / POINTS_PER_FRAME)
else:
    FRAMES = int(TOTAL_TARGET_POINTS / POINTS_PER_FRAME) + 1

current_total_points = 0
current_points_in_circle = 0

all_points_x = []
all_points_y = []
is_inside_flags = []
history_num_points = []
history_error = []

def init():
    global current_total_points, current_points_in_circle, all_points_x, all_points_y, is_inside_flags, history_error, history_num_points
    all_points_x.clear()
    all_points_y.clear()
    is_inside_flags.clear()
    history_num_points.clear()
    history_error.clear()

    current_total_points = 0
    current_points_in_circle = 0

    scatter_inside.set_data([], [])
    scatter_outside.set_data([], [])
    error_line.set_data([], [])

    text_num_samples.set_text('Num Samples: 0')
    text_pi_estimate.set_text('Est. Pi: N/A')
    text_error_val.set_text('Error: N/A')

    return (scatter_inside, scatter_outside, error_line, text_num_samples, text_pi_estimate, text_error_val)

def update(frame):
    global current_total_points, current_points_in_circle, all_points_x, all_points_y, is_inside_flags, history_error, history_num_points
    
    for _ in range(POINTS_PER_FRAME):
        current_point = generate_random_point()

        all_points_x.append(current_point[0])
        all_points_y.append(current_point[1])

        is_current_point_inside_circle = is_point_inside_circle(current_point)
        is_inside_flags.append(is_current_point_inside_circle)

        current_total_points += 1
        if(is_current_point_inside_circle):
            current_points_in_circle += 1
    
    if current_total_points > 0:
        pi_estimate = 4 * (current_points_in_circle / current_total_points)
    else:
        pi_estimate = 0
    
    current_error = abs(pi_estimate - PI)

    history_num_points.append(current_total_points)
    history_error.append(current_error)

    current_inside_x, current_inside_y, current_outside_x, current_outside_y = [],[],[],[]
    for index, item in enumerate(is_inside_flags):
        if(item):
            current_inside_x.append(all_points_x[index])
            current_inside_y.append(all_points_y[index])
        else:
            current_outside_x.append(all_points_x[index])
            current_outside_y.append(all_points_y[index])

    scatter_inside.set_data(current_inside_x, current_inside_y)
    scatter_outside.set_data(current_outside_x, current_outside_y)
    error_line.set_data(history_num_points, history_error)

    text_num_samples.set_text(f"Num Samples: {current_total_points}")
    text_pi_estimate.set_text(f"Est. Pi: {pi_estimate:.5f}")
    text_error_val.set_text(f"Error: {current_error:.5f}")

    if history_num_points:
        ax_error.set_xlim(0, max(history_num_points) * 1.1 if history_num_points else 1000)
    if history_error:
        ax_error.set_ylim(0, max(history_error) * 1.1 if history_error else 0.5)
    
    return (scatter_inside, scatter_outside, error_line, text_num_samples, text_pi_estimate, text_error_val)

def generate_random_point():
    x = random.uniform(-1,1)
    y = random.uniform(-1,1)
    return (x,y)

def is_point_inside_circle(point):
    return (math.pow(point[0], 2) + math.pow(point[1], 2) <= 1)

def estimate_pi_mc(num_points):
    points_inside_circle = 0
    for i in range(num_points):
        point = generate_random_point()
        if (is_point_inside_circle(point)):
            points_inside_circle += 1
    pi_estimate = 4 * (points_inside_circle / float(num_points))
    return pi_estimate

def run_monte_carlo_simulation(num_points):
    points_inside_circle = 0
    points_inside_coords = []
    points_outside_coords = []
    for i in range(num_points):
        point = generate_random_point()
        if (is_point_inside_circle(point)):
            points_inside_circle += 1
            points_inside_coords.append(point)
        else:
            points_outside_coords.append(point)
    pi_estimate = 4 * (points_inside_circle / float(num_points))
    return pi_estimate, points_inside_coords, points_outside_coords

# Setting up figure & plots
fig = plt.figure(figsize=(10,8))

ax_scatter = plt.subplot2grid((2,2), (0,0), rowspan=1, colspan=1)
ax_text = plt.subplot2grid((2,2), (0,1), rowspan=1, colspan=1)
ax_error = plt.subplot2grid((2,2), (1,0), rowspan=1, colspan=2)

# Configuring scatter plot 
ax_scatter.set_title('Monte Carlo Pi Estimation')
ax_scatter.set_xlim(-1,1)
ax_scatter.set_ylim(-1,1)
ax_scatter.set_aspect('equal', adjustable='box')

# Draw square
square = patches.Rectangle((-1,-1), 2, 2, linewidth=2, edgecolor='black', facecolor='none', label='Boundary Square')
ax_scatter.add_patch(square)

# Draw circle
circle = patches.Circle((0,0), 1, linewidth=2, edgecolor='red', facecolor='none', label='Target Circle (r=1)')
ax_scatter.add_patch(circle)

scatter_inside, = ax_scatter.plot([], [], 'o', color='red', markersize=3, label='Inside')
scatter_outside, = ax_scatter.plot([], [], 'o', color='blue', markersize=3, label='Outside')

# Configuring ax_text plot
text_num_samples = ax_text.text(0.05, 0.9, '', transform=ax_text.transAxes, fontsize=10)
text_pi_estimate = ax_text.text(0.05, 0.8, '', transform=ax_text.transAxes, fontsize=10)
text_actual_pi = ax_text.text(0.05, 0.7, f'Actual Pi: {PI:.5f}', transform=ax_text.transAxes, fontsize=10)
text_error_val = ax_text.text(0.05, 0.6, '', transform=ax_text.transAxes, fontsize=10)
ax_text.set_title('Simulation stats')
ax_text.axis('off')

# Configuring ax_error plot
error_line, = ax_error.plot([], [], marker='', linestyle='-', color='purple', label='Error')
ax_error.set_xlim(0,1000)
ax_error.set_ylim(0, 0.5)
ax_error.set_title('Estimation Error vs. Number of Points')
ax_error.set_xlabel('Number of points')
ax_error.set_ylabel('Error')
ax_error.grid(True)

ani = animation.FuncAnimation(fig, update, frames=FRAMES, init_func=init, interval=100, blit=True, repeat=False)

plt.tight_layout()
plt.show()