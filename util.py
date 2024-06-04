import numpy as np

# Using this function we find the angle of the index finger
# When we bend the finger from point 6. So, to ger the angle we need to find the angle between the point 8, 6 and 5. From this, we can calculate whether the index finger is bend or not.
def get_angle(a, b, c):
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(np.degree(radians))
    return angle