*Ball Movement Tracking in Video*
This project involves processing a video to track the movement of balls of different colors across various quadrants. The program records events of each ball entering and exiting each numbered quadrant with timestamps and overlays this information on the processed video. Additionally, it outputs the event data to a text file.

*Requirements*
Python 3.x
OpenCV
NumPy

*Explanation*
              The code processes a video to track colored balls moving across four quadrants in a video frame. It divides the frame into four quadrants and uses HSV color ranges to detect balls of specific colors (white, orange, yellow, green). As the video plays, it records events of balls entering and exiting each quadrant with timestamps, and overlays this information on the video. The processed video and a text file logging the events (time, quadrant number, ball color, entry/exit) are saved to specified paths. Quadrants have been reassigned as follows: quadrant 3 is top-left, quadrant 4 is top-right, quadrant 2 is bottom-left, and quadrant 1 is bottom-right.
