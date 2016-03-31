import bpy
import mathutils
from mathutils import Vector
import csv
#from dateutil.parser import parse
from datetime import datetime


def run():    
   #Add debug variable, if true, than only draw the first 20 cubes
   DEBUG = True
   numberOfCubesPrinted = 0
   
   scn = bpy.context.scene
   scn.frame_start = 1
   scn.frame_end = 801
   reader = csv.DictReader(open('/Users/nickbreen/Downloads/alcohol_locations.csv', newline=''), delimiter=',')
   bpy.context.scene.layers[2] = True
   
   # Add a plane
   bpy.ops.mesh.primitive_plane_add(radius=10, location=(0, 0, 0), layers=(False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False))


   for row in reader:
       #print(row['License_Ty'])
       if row['License_Ty'] == '21':
           numberOfCubesPrinted = numberOfCubesPrinted + 1
           if numberOfCubesPrinted == 100 and DEBUG == True:
                break
           print(row)
           issue_date = row['Orig_Iss_D'].split('/')
           # correct shift and scale for lat,long coordinates relative to london (which is 0,0)
           y = (float(row['X']) + 122.41) * 130
           x = (float(row['Y']) - 37.7) * 130
           
           # move to frame 1
           bpy.context.scene.frame_set((float(issue_date[0]) - 1948)*10+ float(issue_date[1]) * 2 - 24)
           #bpy.ops.anim.change_frame(frame = 1)
           bpy.ops.mesh.primitive_cube_add(radius=0.3,location=(x,y,-1)) 
           ob = bpy.context.object
           me = ob.data
           
           # create keyframe
           bpy.ops.anim.keyframe_insert_menu(type='Location')
           
           #  move to year keyframe
           appear_frame = (float(issue_date[0]) - 1948)*10 + float(issue_date[1]) * 2
           bpy.context.scene.frame_set(appear_frame)
           # do something with the object. A translation, in this case
           bpy.ops.transform.translate(value=(0,0,1.5))
           
           # todo sset the colour.
           
           # create keyframe
           bpy.ops.anim.keyframe_insert_menu(type='Location')
           
       

   return

if __name__ == "__main__":
   run()