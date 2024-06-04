import sys
import cv2
from ultralytics import YOLO
import os

def vehicle_detection(video_paths):
    # Load the YOLOv8 model
    model = YOLO('yolov8m.pt')

    for video_path in video_paths:
        # Open the video file
        cap = cv2.VideoCapture(video_path)

        # Define the output video file
        filename = os.path.basename(video_path)
        output_path = os.path.join('static', 'annotated_videos', f"{filename[:-4]}_annotated.mp4")
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))

        # Initialize the vehicle count
        vehicle_count = 0

        # Loop through the video frames
        while cap.isOpened():
            # Read a frame from the video
            success, frame = cap.read()

            if success:
                # Run YOLOv8 tracking on the frame
                results = model.track(frame)

                # Increment the vehicle count
                vehicle_count += len(results[0].boxes.data)

                # Visualize the results on the frame
                annotated_frame = results[0].plot()

                # Write the annotated frame to the output video file
                out.write(annotated_frame)

            else:
                # Break the loop if the end of the video is reached
                break

        # Release the video capture object and the output video file
        cap.release()
        out.release()

        # Print the total number of vehicles detected for each video
        print(f"{vehicle_count}")

        # Write the total vehicle count to out.txt
        with open('out.txt', 'a') as file:
            file.write(f"{vehicle_count}\n")

    return [output_path for _ in video_paths]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python counted_vehicles.py <video_path1> [<video_path2> ...]")
        sys.exit(1)

    video_paths = sys.argv[1:]
    annotated_videos = vehicle_detection(video_paths)
    for video in annotated_videos:
        print(f"Annotated video: {video}")
