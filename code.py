import bpy
import mathutils
from mathutils import Vector
import csv
#from dateutil.parser import parse
from datetime import datetime
from math import ceil
import os 

# If true, we only create a subset of data points.
DEBUG=False
# If DEBUG is true, this is how frequently to take a sample from the dataset
# ie. 5 would take every 5th row from the csv.
MOD_DEBUG = 5

# Switch for city: sf, istanbul, or ottawa
CITY = "ottawa" 

# csv path
CSV_PATH = 'TODO: currently 1:1 data set for cities, so hardcoded below'

# Absolute path to your repo.
path, filename = os.path.split(os.path.dirname(os.path.realpath(__file__)))
REPO_PATH = path + '/'


def run():  
  global CSV_PATH
  # Setup Scene.
  scn = bpy.context.scene
  scn.frame_start = 1
  scn.frame_end = 801
  bpy.context.scene.layers[3] = True
  
  # array index 3 maps to layer 4
  dynamic_layer = 3
  
  # Delete dynamic objects.
  generated_objects = [ob for ob in bpy.context.scene.objects if ob.layers[dynamic_layer]]
  for obj in generated_objects:
      print(obj)
      obj.select =True
      bpy.ops.object.delete() 
  
  # hide city layers
  bpy.context.scene.layers[0] = False
  bpy.context.scene.layers[1] = False
  bpy.context.scene.layers[2] = False
  bpy.context.scene.layers[dynamic_layer] = True # sets dynamic layer to active.

  # TODO: hide/unhide right layers for each city.
  if CITY == "ottawa":
    CSV_PATH = REPO_PATH + 'data/ottawa-publicly-accessible-computers.csv'
    addObjects(getOttawaData())
    createOttawaCamera()
    bpy.context.scene.layers[1] = True # must be after all objects are added.
  elif CITY == "sf":
    CSV_PATH = REPO_PATH + 'data/alcohol_locations.csv'
    addObjects(getSfData())
    createSfCamera()
    bpy.context.scene.layers[0] = True # must be after all objects are added.
  elif CITY == "istanbul":
    CSV_PATH = REPO_PATH + 'data/tweetsIstanbul.csv'
    addObjects(getIstanbulData())
    createIstanbulCamera()
    bpy.context.scene.layers[2] = True # must be after all objects are added.
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

# TODO: named params so it's more readable.
def createOttawaCamera():
  createCameraCommon((15, 5, 3.66), (-22, -20, -0.6), (0,0, 9))
    
def createSfCamera():
  createCameraCommon((-24, 50, 3.66), (23, -18, -0.6), (0,0, 5))

def createIstanbulCamera():
  createCameraCommon((-24, 50, 2.66), (23, -18, -0.6), (0,0, 7))


# Return an array of objects of the form:
# {x: 123, y:32, z:22, startFrame: 1234, colour: (0.5, 0.2, 0.8), colourName: 'someNameForThisColour'}
def getOttawaData():
  return_data = []
  mod_counter = 0

  reader = csv.DictReader(open(CSV_PATH, newline=''), delimiter=',')
  for row in reader:
    #print(row['License_Ty'])
    mod_counter = mod_counter + 1
    if DEBUG and (mod_counter% MOD_DEBUG) != 0:
         continue;
    #TODO: helper to get lat,lng max, min, and avg to avoid manual calbiration.
    return_data.append({
        'x': (float(row['lng']) + 75.63) * 120,
        'y': (float(row['lat']) - 45.45) * 165,
        'z': float(row['COMPUTERS']),
        'startFrame': mod_counter + 3 * float(row['COMPUTERS']),
        'colour': (0.6, 0.9, 0.6),
        'colourName': "MaterialOttawa"
    })
  return return_data

# Return an array of objects of the form:
# {x: 123, y:32, z:22, startFrame: 1234, colour: (0.5, 0.2, 0.8), colourName: 'someNameForThisColour'}
def getSfData():
  mod_counter = 0

  return_data = []

  reader = csv.DictReader(open(CSV_PATH, newline=''), delimiter=',')
  for row in reader:
    mod_counter = mod_counter + 1
    # Filter which rows are used based on the License_Ty column.
    if row['License_Ty'] == '21':
      if DEBUG and (mod_counter% MOD_DEBUG) != 0:
           continue;

      issue_date = row['Orig_Iss_D'].split('/')
      decade = (float(issue_date[0][:-1]) - 194)
      
      return_data.append({
        'x': (float(row['lng']) + 122.41) * 380, 
        'y': (float(row['lat']) - 37.7) * 380,
        'z': 5.5 + float(issue_date[1])*0.05,
        'startFrame': (float(issue_date[0]) - 1949) * 10 + float(issue_date[1])*2 - 30,
        'colour': ( decade*0.1, 0.1 + decade*0.15,  0.2 + decade*0.11),
        'colourName': "CubeMaterialz" + issue_date[0][:-1] # Truncate last digit of year, to get decade.
      })

  return return_data

# Return an array of objects of the form:
# {x: 123, y:32, z:22, startFrame: 1234, colour: (0.5, 0.2, 0.8), colourName: 'someNameForThisColour'}
def getIstanbulData():
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
      'colourName': "tweet"
    })

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
     bpy.context.scene.frame_set(point['startFrame'])
     #bpy.ops.anim.change_frame(frame = 1)
     bpy.ops.mesh.primitive_cube_add(radius=0.35,location=(x,y,(-z * 0.35))) 
     bpy.ops.transform.resize(value=(0.05, 0.05, 2*z*0.35), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

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
     
     # Move to end keyframe (TODO: add option animation_duration key
     appear_frame = point['startFrame'] + 75
     bpy.context.scene.frame_set(appear_frame)
     # do something with the object. A translation, in this case
     bpy.ops.transform.translate(value=(0, 0, z*0.35))
     
     # create keyframe
     bpy.ops.anim.keyframe_insert_menu(type='Location')
 
    # TODO: remove all materials we've created and no longer need.
   return


def createCameraCommon(start_location, translation1, translation2):
   # add camera
   bpy.ops.object.camera_add(view_align=True, enter_editmode=False, location=start_location, rotation=(1.5708,0,3.14159))
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
   bpy.ops.transform.translate(value=translation1)
   # snapshot (blender will interprit the movement between frames)
   bpy.ops.anim.keyframe_insert_menu(type='Location')
     
   # near last frame
   bpy.context.scene.frame_set(bpy.context.scene.frame_end - 15)
   # move camera up
   bpy.ops.transform.translate(value=translation2)
   # snapshot (blender will interprit the movement between frames)
   bpy.ops.anim.keyframe_insert_menu(type='Location')


if __name__ == "__main__":
   run()