mkdir runs
mkdir sourceVideos

wget -O sourceVideos/testVideo.mp4 -q "https://clips.fencingdatabase.com/eurosepee2023/embarrassedNaegleriaChinstrapPenguin.mp4"
wget -O pose_landmarker.task -q "https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_heavy/float16/1/pose_landmarker_heavy.task"

python -m virtualenv env
source env/bin/activate

pip install -r requirements.txt
