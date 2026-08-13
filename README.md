# FencingCV
FencingCV is a new project aimed at providing an analytics platform for annotating fencing videos for the research of athlete performance.

![Showcase of a time series analysis of a fencing bout](./showcase.gif)

## What it does
Uses MediaPipe to capture poses of fencers and use positional data to capture numerous features, which currently support:
- Weapon Arm Extensions
- Fencer positions on screen
Then takes representation and provides a tkinter GUI which allows the user to playback annotated video and record additional metrics which can export to additional time stamped CSVs.
This allows for users of this platform to mark time-critical features in fencing videos and export their data to a CSV. 

## Current Limitations
For position / distance analysis, accuracy will only be kept if the camera's zoom and angle relative to the piste is static.

## Future directions
Custom CV modeling for fencing poses
Handling of dynamic camera angles and zoom 
Increase UX for rapid data entry
