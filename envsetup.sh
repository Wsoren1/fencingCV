mkdir runs
mkdir sourceVideos

cd sourceVideos
curl -L -O "https://clips.fencingdatabase.com/eurosepee2023/embarrassedNaegleriaChinstrapPenguin.mp4"
cd ..

python -m virtualenv env
source env/bin/activate

pip install -r requirements.txt
