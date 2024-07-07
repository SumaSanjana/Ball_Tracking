import cv2
import numpy as np

def process_video(input_video_path, output_text_file, ball_colors):
    # Load the video
    cap = cv2.VideoCapture(input_video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file {input_video_path}")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    # Define the quadrants
    quadrants = {
        3: [(0, 0), (frame_width // 2, frame_height // 2)],          # Top-left
        4: [(frame_width // 2, 0), (frame_width, frame_height // 2)], # Top-right
        2: [(0, frame_height // 2), (frame_width // 2, frame_height)],# Bottom-left
        1: [(frame_width // 2, frame_height // 2), (frame_width, frame_height)] # Bottom-right
    }

    # Function to detect the ball based on determined color ranges
    def detect_ball(frame, ball_colors, ball_states):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        events = []
        for color_name, (lower_color, upper_color) in ball_colors.items():
            mask = cv2.inRange(hsv, lower_color, upper_color)
            contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            if contours:  # Check if contours were found
                contour = max(contours, key=cv2.contourArea)  # Find the largest contour
                if cv2.contourArea(contour) > 500:  # Minimum area to be considered a ball
                    (x, y, w, h) = cv2.boundingRect(contour)
                    ball_center = (x + w // 2, y + h // 2)
                    for q_num, ((x1, y1), (x2, y2)) in quadrants.items():
                        if x1 < ball_center[0] < x2 and y1 < ball_center[1] < y2:
                            if ball_states[color_name] == 0:
                                events.append((timestamp, q_num, color_name, "Entry"))
                                ball_states[color_name] = q_num  # Track which quadrant the ball is in
                            elif ball_states[color_name] != q_num:
                                events.append((timestamp, ball_states[color_name], color_name, "Exit"))
                                events.append((timestamp, q_num, color_name, "Entry"))
                                ball_states[color_name] = q_num  # Update quadrant
                            break
                    else:
                        if ball_states[color_name] != 0:
                            events.append((timestamp, ball_states[color_name], color_name, "Exit"))
                            ball_states[color_name] = 0  # No longer in any quadrant

        return events

    # Initialize variables
    ball_states = {color_name: 0 for color_name in ball_colors.keys()}
    events = []

    frame_count = 0
    with open(output_text_file, 'w') as f:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frame_count += 1
            timestamp = frame_count / fps

            # Detect balls and record events
            frame_events = detect_ball(frame, ball_colors, ball_states)
            events.extend(frame_events)

            # Show frame with detections
            cv2.imshow('Frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            # Write events to text file immediately
            for event in frame_events:
                f.write(f"{event[0]:.2f}, {event[1]}, {event[2]}, {event[3]}\n")

    cap.release()
    cv2.destroyAllWindows()

# Example usage with provided color ranges
input_video_path = r'C:\Users\nvsur\Downloads\AI Assignment video.mp4'
output_text_file = r'C:\Users\nvsur\Downloads\output_events.txt'

# Color ranges determined from previous session
ball_colors = {
    "white": (np.array([16, 7, 212]), np.array([36, 27, 232])),
    "orange": (np.array([0, 147, 229]), np.array([17, 167, 249])),
    "yellow": (np.array([14, 150, 132]), np.array([34, 170, 152])),
    "green": (np.array([79, 129, 69]), np.array([99, 149, 89]))
}

process_video(input_video_path, output_text_file, ball_colors)
