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
        output_video_path = os.path.join('static', 'annotated_videos', f"{filename[:-4]}_annotated.mp4")
        output_image_folder = os.path.join('static', 'annotated_images')
        os.makedirs(output_image_folder, exist_ok=True)

        fps = int(cap.get(cv2.CAP_PROP_FPS))
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_video_path, fourcc, fps, (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))

        # Initialize the vehicle count
        vehicle_count = 0

        # Initialize a dictionary to keep track of the unique vehicle IDs in each frame
        unique_vehicle_ids = {}

        # Loop through the video frames
        while cap.isOpened():
            # Read a frame from the video
            success, frame = cap.read()

            if success:
                # Run YOLOv8 tracking on the frame
                results = model.track(frame)

                # Increment the vehicle count for each unique vehicle ID
                for box in results[0].boxes.data:
                    vehicle_id = int(box.cpu().numpy()[4])
                    if vehicle_id not in unique_vehicle_ids:
                        unique_vehicle_ids[vehicle_id] = True
                        vehicle_count += 1

                # Visualize the results on the frame
                annotated_frame = results[0].plot()

                # Write the annotated frame to the output video file
                out.write(annotated_frame)

                # Save annotated image
                image_filename = f"{filename[:-4]}_frame{cap.get(cv2.CAP_PROP_POS_FRAMES)}.jpg"
                image_output_path = os.path.join(output_image_folder, image_filename)
                cv2.imwrite(image_output_path, annotated_frame)

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

    return [output_video_path for _ in video_paths]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python counted_vehicles.py <video_path1> [<video_path2> ...]")
        sys.exit(1)

    video_paths = sys.argv[1:]
    annotated_videos = vehicle_detection(video_paths)
    for video in annotated_videos:
        print(f"Annotated video: {video}")
