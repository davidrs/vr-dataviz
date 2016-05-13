import bpy
import mathutils
from mathutils import Vector
import csv
#from dateutil.parser import parse
from datetime import datetime
from math import ceil
import os 

DEBUG=True
# Switch for city
CITY = "ottawa" 

# Absolute path to your repo.
path, filename = os.path.split(os.path.dirname(os.path.realpath(__file__)))
REPO_PATH = path + '/'

# csv path
CSV_PATH = 'TODO: currently 1:1 data set for cities, so hardcoded below'


def run():  
  global CSV_PATH
  # Setup Scene.
  scn = bpy.context.scene
  scn.frame_start = 1
  scn.frame_end = 801
  bpy.context.scene.layers[3] = True
  
  # TODO: hide/unhide right layers for each city.
  if CITY == "ottawa":
    CSV_PATH = REPO_PATH + 'data/ottawa-publicly-accessible-computers.csv'
    addObjects(getOttawaData())
    createOttawaCamera()
  elif CITY == "sf":
    CSV_PATH = REPO_PATH + 'data/alcohol_locations.csv'
    addObjects(getSfData())
    createSfCamera()
  elif CITY == "istanbul":
    CSV_PATH = REPO_PATH + 'data/tweetsIstanbul.csv'
    addObjects(getIstanbulData())
    createIstanbulCamera()
  else:
    print("unrecognized CITY name, try: sf, ottawa, or istanbul")
   


  # Add two suns, not standard practice...but best lighting.
  bpy.ops.object.lamp_add(type='SUN', view_align=False, location=(0, 0, 20))
  bpy.ops.transform.rotate(value=0.45, axis=(-0.172023, 0.980755, -0.0923435), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
  bpy.ops.object.lamp_add(type='SUN', view_align=False, location=(3, 3, 23))
  bpy.ops.transform.rotate(value=0.45, axis=(-0.17, 0.98, -0.09), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

  createWater()


def createWater():
   # Add a plane
   bpy.ops.mesh.primitive_plane_add(radius=100, location=(0, 0, 0))
   mat_name = 'water'
   if bpy.data.materials.get(mat_name) is not None:
        mat = bpy.data.materials[mat_name]
   else:
        # create material
        mat = bpy.data.materials.new(name=mat_name)
        mat.diffuse_color = (0.74,0.74,1.0)
   # assign to 1st material slot
   ob = bpy.context.object
   ob.data.materials.append(mat)


#TODO: abstract out common camera pieces, maybe even automate based on bounds of data set.
def createOttawaCamera():
   # add camera
   bpy.ops.object.camera_add(view_align=True, enter_editmode=False, location=(15, 5, 3.66), rotation=(1.5708,0,1.14159))
   # Camera is current selected item because we just created camera
   bpy.context.object.data.type = 'PANO'
   bpy.context.object.data.cycles.panorama_type = 'EQUIRECTANGULAR'
   # not working: bpy.context.scene.format = 'MPEG4'
   # not working: bpy.context.scene.codec = 'MPEG4'
   
   # set frame to frame 1
   bpy.context.scene.frame_set(1)
   # snapshot
   bpy.ops.anim.keyframe_insert_menu(type='Location')
   
   # move camera to frame 300
   bpy.context.scene.frame_set(ceil(bpy.context.scene.frame_end/2))
   # move camera down
   bpy.ops.transform.translate(value=(-22, -20, -0.6))
   # snapshot (blender will interprit the movement between frames)
   bpy.ops.anim.keyframe_insert_menu(type='Location')
     
   # near last frame
   bpy.context.scene.frame_set(bpy.context.scene.frame_end - 15)
   # move camera up
   bpy.ops.transform.translate(value=(0,0,9))
   # snapshot (blender will interprit the movement between frames)
   bpy.ops.anim.keyframe_insert_menu(type='Location')
    
def createSfCamera():

   # add camera
   bpy.ops.object.camera_add(view_align=True, enter_editmode=False, location=(-24, 50, 3.66), rotation=(1.5708,0,3.14159))
   # Camera is current selected item because we just created camera
   bpy.context.object.data.type = 'PANO'
   bpy.context.object.data.cycles.panorama_type = 'EQUIRECTANGULAR'
   # not working: bpy.context.scene.format = 'MPEG4'
   # not working: bpy.context.scene.codec = 'MPEG4'
   
   # set frame to frame 1
   bpy.context.scene.frame_set(1)
   # snapshot
   bpy.ops.anim.keyframe_insert_menu(type='Location')
   
   # move camera to frame 300
   bpy.context.scene.frame_set(ceil(bpy.context.scene.frame_end/2))
   # move camera down
   bpy.ops.transform.translate(value=(23, -18, -0.6))
   # snapshot (blender will interprit the movement between frames)
   bpy.ops.anim.keyframe_insert_menu(type='Location')
     
   # near last frame
   bpy.context.scene.frame_set(bpy.context.scene.frame_end - 15)
   # move camera up
   bpy.ops.transform.translate(value=(0,0, 5))
   # snapshot (blender will interprit the movement between frames)
   bpy.ops.anim.keyframe_insert_menu(type='Location')
    
def createIstanbulCamera():

   # add camera
   bpy.ops.object.camera_add(view_align=True, enter_editmode=False, location=(-24, 50, 2.66), rotation=(1.5708,0,3.14159))
   # Camera is current selected item because we just created camera
   bpy.context.object.data.type = 'PANO'
   bpy.context.object.data.cycles.panorama_type = 'EQUIRECTANGULAR'
   # not working: bpy.context.scene.format = 'MPEG4'
   # not working: bpy.context.scene.codec = 'MPEG4'
   
   # set frame to frame 1
   bpy.context.scene.frame_set(1)
   # snapshot
   bpy.ops.anim.keyframe_insert_menu(type='Location')
   
   # move camera to frame 300
   bpy.context.scene.frame_set(ceil(bpy.context.scene.frame_end/2))
   # move camera down
   bpy.ops.transform.translate(value=(23, -18, -0.6))
   # snapshot (blender will interprit the movement between frames)
   bpy.ops.anim.keyframe_insert_menu(type='Location')
     
   # near last frame
   bpy.context.scene.frame_set(bpy.context.scene.frame_end - 15)
   # move camera up
   bpy.ops.transform.translate(value=(0,0, 7))
   # snapshot (blender will interprit the movement between frames)
   bpy.ops.anim.keyframe_insert_menu(type='Location')



# Return an array of objects of the form:
# {x: 123, y:32, z:22, startFrame: 1234, colour: (0.5, 0.2, 0.8), colourName: 'someNameForThisColour'}
def getOttawaData():
  DEBUG = True
  MOD_DEBUG = 1
  return_data = []
  mod_counter = 0

  reader = csv.DictReader(open(CSV_PATH, newline=''), delimiter=',')
  for row in reader:
    #print(row['License_Ty'])
    mod_counter = mod_counter + 1
    if DEBUG and (mod_counter% MOD_DEBUG) != 0:
         continue;
    #print(row["ADDRESS_EN"])
    #TODO: helper to get lat,lng max, min, and avg to avoid manual calbiration.
    return_data.append({
        'x': (float(row['lng']) + 75.63) * 120,
        'y': (float(row['lat']) - 45.45) * 165,
        'z': float(row['COMPUTERS']),
        'startFrame': mod_counter + 3 * float(row['COMPUTERS']),
        'colour': (0.6, 0.9, 0.6),
        'colourName': "MaterialOttawa"
    })
    #if(mod_counter > 2):
     # break
    
  print(return_data)

  return return_data

# Return an array of objects of the form:
# {x: 123, y:32, z:22, startFrame: 1234, colour: (0.5, 0.2, 0.8), colourName: 'someNameForThisColour'}
def getSfData():
  # Add debug variable, if true, than only draw the first 20 cubes
  DEBUG = False
  MOD_DEBUG = 5# to get a distributed sample.
  mod_counter = 0

  return_data = []

  reader = csv.DictReader(open(CSV_PATH, newline=''), delimiter=',')
  for row in reader:
    mod_counter = mod_counter + 1
    if row['License_Ty'] == '21':
      if DEBUG and (mod_counter% MOD_DEBUG) != 0:
           continue;

      issue_date = row['Orig_Iss_D'].split('/')
      return_data.append({
        'x': (float(row['lng']) + 122.41) * 380, 
        'y': (float(row['lat']) - 37.7) * 380,
        'z': 1,
        'startFrame': (float(issue_date[0]) - 1948)*10+ float(issue_date[1]) * 2,
        'colour': (0.15 * (float(issue_date[0][:-1]) - 194), 0.7, 0.7),
        'colourName': "aaMaterialxxz" + issue_date[0][:-1] # Truncate last digit of year, to get decade.
      })

  return return_data

# Return an array of objects of the form:
# {x: 123, y:32, z:22, startFrame: 1234, colour: (0.5, 0.2, 0.8), colourName: 'someNameForThisColour'}
def getIstanbulData():
  # Add debug variable, if true, than only draw the first 20 cubes
  DEBUG = False
  MOD_DEBUG = 5# to get a distributed sample.
  mod_counter = 0

  return_data = []

  reader = csv.DictReader(open(CSV_PATH, newline=''), delimiter=',')
  for row in reader:
    mod_counter = mod_counter + 1
    if DEBUG and (mod_counter% MOD_DEBUG) != 0:
         continue;

    return_data.append({
      'x': (float(row['lng']) - 28.996) * 1180, 
      'y': (float(row['lat']) - 41.008) * 1390,
      'z': (float(row['follower_count']) / 100 + 0.2),
      'startFrame': mod_counter,
      'colour': (0.15, 0.7, 0.7), #TODO off of row["source"]
      'colourName': "tweet" # Truncate last digit of year, to get decade.
    })
    #if mod_counter>3:
    #b4    break

  return return_data



# Given an ordered array of objects, create objects on the map.
def addObjects(all_points):  
   for point in all_points:
     # print(row)
     # TODO: Auto Shift and scale the lat,lng automagically based on the range of values.
     # correct shift and scale for lat,long coordinates relative to which is 0,0
     x = point['x']
     y = point['y']
     z = point['z']
     
     # set the starting frame
     bpy.context.scene.frame_set(point['startFrame'] - 24)
     #bpy.ops.anim.change_frame(frame = 1)
     bpy.ops.mesh.primitive_cube_add(radius=0.35,location=(x,y,(-z * 0.35))) 
     bpy.ops.transform.resize(value=(1, 1, 2*z*0.35), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

     ob = bpy.context.object
     me = ob.data
     
     # TODO: abstract to external function
     # Get material
     mat_name = point['colourName']
     if bpy.data.materials.get(mat_name) is not None:
          mat = bpy.data.materials[mat_name]
     else:
          # create material
          mat = bpy.data.materials.new(name=mat_name)
          mat.diffuse_color = point['colour']
     
     # Assign it to object
     if len(ob.data.materials):
          # assign to 1st material slot
          ob.data.materials[0] = mat
     else:
          # no slots
          ob.data.materials.append(mat)
     
     # TODO: end of material
     
     # Create keyframe
     bpy.ops.anim.keyframe_insert_menu(type='Location')
     
     # Move to year keyframe
     appear_frame = point['startFrame'] * 2
     bpy.context.scene.frame_set(appear_frame)
     # do something with the object. A translation, in this case
     bpy.ops.transform.translate(value=(0, 0, z*0.35))
     
     # create keyframe
     bpy.ops.anim.keyframe_insert_menu(type='Location')
 
    # TODO: remove all materials we've created and no longer need.
   return

if __name__ == "__main__":
   run()