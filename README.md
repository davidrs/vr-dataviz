# vr-dataviz
Blender project rendered as a 360 video to data viz  geo spatial csvs.

## Demo (Open on your Phone for Best Experience)
https://www.youtube.com/watch?v=mL7tVlfyWhk

![Alt text](sample.png?raw=true "Sample Render")

## Running the code

To run blender from cmd to get console errors, update "2.76b-" to be your version #:
```$HOME/Downloads/blender-2.76b-OSX_10.6-x86_64/blender.app/Contents/MacOS/blender &```


Blender 360 tutorial:
http://pedrogaspar.weebly.com/blog/making-a-360-video-on-blender-to-be-published-on-youtube

Youtube Upload 360 video doc:
https://support.google.com/youtube/answer/6178631?hl=en


### First time setup

Create a new project.

Open 'text editor' view.

Open the code.py file.




### Normal Dev
Change the code

Run the script

Alt+s to save the code.


## TODOs
- Make the lat, lng shift & scale more generic, less hardcoded.
- Find solution to no legend for colours.
- Cleanely seperate config values from generic code.
- Add a second city



## Shortcuts and Blender Tips

space bar -> play animation

esc to stop playing the animation

'a' to select all

'x' to delete

Shift + Left arrow: goes to frame 1 of animation.

## Creating a VR animation
We strongly recommend Youtube's Carboard for your viewing pleasure. 

Under the Encoding subsection (on the right in Blender), confirm the format is MPEG-4 and the codec is set as MPEG-4(divx)

Click run script and after the script is fully run, Under the Render subsections (on the right in Blender) click the animation button (this file will be saved at the location under the output subsection). 

