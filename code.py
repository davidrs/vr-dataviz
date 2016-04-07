import bpy
import mathutils
from mathutils import Vector
import csv
#from dateutil.parser import parse
from datetime import datetime
from math import ceil

def run():  
   # Setup Scene.
   scn = bpy.context.scene
   scn.frame_start = 1
   scn.frame_end = 801
   bpy.context.scene.layers[2] = True
   
   # Add a plane
   bpy.ops.mesh.primitive_plane_add(radius=80, location=(0, 0, 0))
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
    
   addLicenses()
   
   #add two suns, not standard practice...
   bpy.ops.object.lamp_add(type='SUN', view_align=False, location=(0, 0, 20))
   bpy.ops.transform.rotate(value=0.45, axis=(-0.172023, 0.980755, -0.0923435), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)
   bpy.ops.object.lamp_add(type='SUN', view_align=False, location=(3, 3, 23))
   bpy.ops.transform.rotate(value=0.45, axis=(-0.17, 0.98, -0.09), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

   createCamera()

def createCamera():
   # add camera
   # TODO: make this a better position
   bpy.ops.object.camera_add(view_align=True, enter_editmode=False, location=(11, 17, 15), rotation=(1.5708,0,0))
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
   bpy.context.scene.frame_set(ceil(bpy.context.scene.frame_end/3))
   # move camera down
   bpy.ops.transform.translate(value=(0,0,-5))
   # snapshot (blender will interprit the movement between frames)
   bpy.ops.anim.keyframe_insert_menu(type='Location')
  
    
def addLicenses():  
   #Add debug variable, if true, than only draw the first 20 cubes
   DEBUG = True
   MOD_DEBUG = 10 # to get a distributed sample.
   mod_counter = 0
   
   reader = csv.DictReader(open('/Users/nickbreen/Code/vr-dataviz/alcohol_locations.csv', newline=''), delimiter=',')
   #reader = csv.DictReader(open('/Users/drustsmith/vr-dataviz/alcohol_locations.csv', newline=''), delimiter=',')

   for row in reader:
       #print(row['License_Ty'])v
       mod_counter = mod_counter + 1
       if row['License_Ty'] == '21':
           if DEBUG and (mod_counter% MOD_DEBUG) != 0:
               continue;
           #print(row)
           issue_date = row['Orig_Iss_D'].split('/')
           # correct shift and scale for lat,long coordinates relative to london (which is 0,0)
           x = (float(row['X']) + 122.41) * 380
           y = (float(row['Y']) - 37.7) * 380
           
           # set the starting frame
           bpy.context.scene.frame_set((float(issue_date[0]) - 1948)*10+ float(issue_date[1]) * 2 - 24)
           #bpy.ops.anim.change_frame(frame = 1)
           bpy.ops.mesh.primitive_cube_add(radius=0.35,location=(x,y,-1)) 
           bpy.ops.transform.resize(value=(1, 1, 1.4), constraint_axis=(False, False, True), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

           ob = bpy.context.object
           me = ob.data
           
           # TODO: abstract to external function
           # Get material
           mat_name = "aaMaterialxxz" + issue_date[0][:-1] #truncate last digit of year, to get decade.
           if bpy.data.materials.get(mat_name) is not None:
                mat = bpy.data.materials[mat_name]
           else:
                # create material
                mat = bpy.data.materials.new(name=mat_name)
                color = 0.15 * (float(issue_date[0][:-1]) - 194)
                print(color)
                mat.diffuse_color = (color,0.7,0.7)
           
           # Assign it to object
           if len(ob.data.materials):
                # assign to 1st material slot
                ob.data.materials[0] = mat
           else:
                # no slots
                ob.data.materials.append(mat)
           
           # TODO: end of material
           
           # create keyframe
           bpy.ops.anim.keyframe_insert_menu(type='Location')
           
           #  move to year keyframe
           appear_frame = (float(issue_date[0]) - 1948)*10 + float(issue_date[1]) * 2
           bpy.context.scene.frame_set(appear_frame)
           # do something with the object. A translation, in this case
           bpy.ops.transform.translate(value=(0,0,2.0))
           
           # create keyframe
           bpy.ops.anim.keyframe_insert_menu(type='Location')
       
    # TODO: remove all materials we've created and no longer need.
   return

if __name__ == "__main__":
   run()