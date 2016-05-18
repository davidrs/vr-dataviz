# vr-dataviz

![Alt text](designDiagram.png?raw=true "System diagram")

This is a simple pipeline for taking in a CSV with a ```lat``` and ```lng``` column and generating a 360 video.
The code is written in Python and is animated/rendered in Blender3D.
Blender3D is an awesome free and open source 3d modeling tool.

We have manually create a couple of assets for the cities of San Francisco, Ottawa, and Istanbul to help orient users.
Additional cities are welcome.

360 Videos can be viewed by anyone with a smartphone and the Youtube app. If you have a 'Google Cardboard' you can even enjoy a cheap VR experience.


## Demo (Open on your Phone for Best Experience)
https://www.youtube.com/playlist?list=PLXYeZ3VwLuLsYzMd9unp7_Ig_GJsjh3J8
Current cities with videos: SF, Ottawa, Istanbul

![Alt text](sample.png?raw=true "Sample Render")


## Running the code

### Setup Blender3d

1. Download Blender3d https://www.blender.org/
2. Open Blender or run blender from the cmd line to get console errors, update ```2.76b``` to be your version #:
```$HOME/Downloads/blender-2.76b-OSX_10.6-x86_64/blender.app/Contents/MacOS/blender &```
3. Duplicate and rename ```base.blend``` to ```local.blend``` (This stops your local settings being overridden when you sync with the repo.)
4. Open the 'text editor' view in Blender and open the ```code.py``` file from this repo.
5. Update the config variables at the top of the file to match your environment.
6. Click ```run script``` button in the text editor view of Blender.
7. Alt + S to save your code in the  Blender3d text editor.


### Adding a new datasource

1. Get a csv with location information and add it to the ```/data``` folder.
2. Ensure there is a ```lat``` and ```lng``` column. You may need to run a 'geocoder' to convert addresses into lat and lngs.
3. If your dataset is not for Ottawa, Istanbul, or San Francisco you will need to add the following functions to the code: ```addCITY_NAMECamera()``` and ```addCITY_NAMEData()```
4. Update the config section at the top of ```code.py``` to point to your new CSV.
5. ```run script``` in Blender3d to create your data.
6. Alt + S to save your code in the  Blender3d text editor.


### Rendering the 360 video / VR animation

When you have succesfully run the script to make your data in Blender you will want to render out the animation to upload to YouTube.

1. Under the Encoding subsection (on the right in Blender), confirm the format is MPEG-4 and the codec is set as MPEG-4(divx)
2. Click the animation button (this file will be saved at the location under the ```output``` subsection). 
3. Use the 360 metadata tool on the final animation. https://support.google.com/youtube/answer/6178631?hl=en
4. Upload it to YouTube.


### Helpful Docs

Blender 360 tutorial:
http://pedrogaspar.weebly.com/blog/making-a-360-video-on-blender-to-be-published-on-youtube

Youtube Upload 360 video doc:
https://support.google.com/youtube/answer/6178631?hl=en


### More Datasets

- SF new units: https://data.sfgov.org/Housing-and-Buildings/San-Francisco-Development-Pipeline-2014-Quarter-3/n5ik-nmm3
(Requires geocoding)

- Eviction notices: https://data.sfgov.org/Housing-and-Buildings/Eviction-Notices/5cei-gny5
(Customer locations column)

- Ottawa publicly accesible computers: http://data.ottawa.ca/dataset/publicly-accessible-computers/resource/58c74f28-3656-4c76-8112-331a3478c8d2
(Requires geocoding)

- Ottawa, health inspection data: http://data.ottawa.ca/dataset/public-health-inspection-data/resource/a308afdd-6bc6-4c6e-842f-c8f8a321e79d

- Istanbul: Twitter Streaming API for location data.



### Geocoder Dev
pip install geopy (used for geocoding addresses into lat and longs)


## TODOs
- Make the lat, lng shift & scale more generic, less hardcoded.
- Find solution to no legend for colours.


## Blender Shortcuts and Tips

space bar -> play animation

esc to stop playing the animation

'a' to select all

'x' to delete

Shift + Left keyboard arrow: goes to frame 1 of animation

Shift + Up keyboard arrow: goes forwards 10 frames of the animation.



