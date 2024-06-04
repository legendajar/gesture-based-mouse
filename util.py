import numpy as np

"""
    Using this function we find the angle of the index finger.

    When we bend the finger from point 6. So, to ger the angle we need to find the angle between the point 8, 6 and 5. From this, we can calculate whether the index finger is bend or not.

    In this we calculate the angle between (a,b) line from x axis and angle between (b,c) line from y axis. After finding the angle we subtract both of them. So, from the resultant angle we can figure out whether the index finger in straight or bent.

    Calculate the angle between three points in a 2D plane.

    Parameters:
        a (tuple): The coordinates of the first point (x, y).
        b (tuple): The coordinates of the second point (x, y).
        c (tuple): The coordinates of the third point (x, y).

    Returns:
        float: The angle in degrees between the lines formed by the three points.


"""
def get_angle(a, b, c):
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(np.degrees(radians))
    return angle


"""
    This function will calculate the distance between two points.

    Parameters:
        landmark_list (list): A list of tuples representing the coordinates of the points.
    Returns:
        float: The distance between the two points.

"""

def get_distance(landmark_list):
    if len(landmark_list) < 2:
        return
    
    (x1, y1), (x2, y2) = landmark_list[0], landmark_list[1]
    L = np.hypot(x2-x1, y2-y1)
    return np.interp(L, [0, 1], [0, 1000])