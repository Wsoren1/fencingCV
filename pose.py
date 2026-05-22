#!/usr/bin/env python3

import pickle
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2
import time
import numpy as np
import sys

def main(sourceFile, targetDirName):
    model_path = 'pose_landmarker_heavy.task'

    BaseOptions = mp.tasks.BaseOptions
    PoseLandmarker = mp.tasks.vision.PoseLandmarker
    PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
    VisionRunningMode = mp.tasks.vision.RunningMode

    # Create a pose landmarker instance with the video mode:
    options = PoseLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=model_path),
        running_mode=VisionRunningMode.VIDEO,
        num_poses=2,
        min_pose_detection_confidence=0.2,
    )

    pose_landmark_model = PoseLandmarker.create_from_options(options)



    # t0 = time.time() * 1000 # this is the time that it takes to process this file actually, not ms of time in the file.
    cap = cv2.VideoCapture(sourceFile)
    fourcc = cv2.VideoWriter_fourcc(*"MP4V")
    banned_points = [*range(11), 17, 18, 19, 20, 21, 22]
    out = None

    export_pose = [] # [(t, [[(x, y)].len(33)].len(2))]
    export_COM = [] # [(t, [(x, y)].len(2))]

    while cap.isOpened():
        success, img = cap.read()
        if not success:
            break

        height, width, _ = img.shape

        if out is None: # then live a life of despair
            fps = cap.get(cv2.CAP_PROP_FPS)
            print('[INFO] Writing to: ' + f'{targetDirName}/annotated_{sourceFile.split('/')[-1]}')
            out = cv2.VideoWriter(f'{targetDirName}/annotated_{sourceFile.split('/')[-1]}', fourcc, fps, (width, height))

        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img)

        # t = int(time.time() * 1000 - t0)
        t = int(cap.get(cv2.CAP_PROP_POS_MSEC))

        pose_landmarker_result = pose_landmark_model.detect_for_video(mp_image, t)
        torso_pts = [11, 12, 23, 24]

        # result: {landmark, world lanmark}
        # "landmark" (2 (pose), 33 (landmark {x: float, y: float, z: float}))
        # (note that landmark is normalized)
        current_frame_pose_data = (t, [])
        current_frame_mass_center_data = (t, [])

        if pose_landmarker_result:
            for pose in pose_landmarker_result.pose_landmarks:
                pose_coords = []
                for i, landmark in enumerate(pose):
                    coords = (int(landmark.x * width), int(landmark.y*height))
                    pose_coords.append(coords)

                    if i in banned_points:
                        # I'm ok with storing these points, but I don't want
                        # them annotated on the video.
                        continue
                    if i in [11, 13, 15]:
                        color = (0, 255, 0)
                    elif i in [12, 14, 16]:
                        color = (255, 0, 0)
                    else:
                        color = (0, 0, 255)

                    cv2.circle(img, coords, radius=4, color=color, thickness=-1)
                current_frame_pose_data[1].append(pose_coords)
                torso_coords = [pose_coords[x] for x in torso_pts]
                x_mean = sum(pt[0] for pt in torso_coords) / len(torso_coords)
                y_mean = sum(pt[1] for pt in torso_coords) / len(torso_coords)
                xy = (int(x_mean), int(y_mean))

                current_frame_mass_center_data[1].append((x_mean, y_mean))
                cv2.circle(img, xy, radius=10, color=(255, 0, 0), thickness=-1)

            export_pose.append(current_frame_pose_data)
            export_COM.append(current_frame_mass_center_data)
        out.write(img)

        cv2.imshow("Image", img)
        cv2.waitKey(1)
   
    pickle.dump(export_pose, open(f"{targetDirName}/save.p", "wb"))
    pickle.dump(export_COM, open(f"{targetDirName}/cmass_timeseries.p", "wb"))

    cap.release()
    out.release()

if __name__ == '__main__':
    srcName = sys.argv[1]
    targetDirName = sys.argv[2]


    main(srcName, targetDirName)
