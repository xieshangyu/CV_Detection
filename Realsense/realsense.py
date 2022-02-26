import statistics

# Processes frame and returns median depth
def process_frame(depth_frame, x_min, y_min, x_max, y_max):     
    values = []
    for x in range(x_min - 1, x_max):
        for y in range(y_min - 1, y_max):
            values.append(depth_frame[y, x])

    med = statistics.median(values)
    return med