import bpy
import mathutils
from mathutils import Vector
import csv
#from dateutil.parser import parse
from datetime import datetime
 
def run():    
    scn = bpy.context.scene
    scn.frame_start = 1
    scn.frame_end = 803
    reader = csv.DictReader(open('/Users/drustsmith/vr-dataviz/alcohol_locations.csv', newline=''), delimiter=',')
    bpy.context.scene.layers[2] = True

    for row in reader:
        #print(row['License_Ty'])
        if row['License_Ty'] == '21':
            print(row)
            issue_date = row['Orig_Iss_D'].split('/')
            y = (float(row['X']) + 122.41) * 130
            x = (float(row['Y']) - 37.7) * 130
            
            # move to frame 1
            bpy.context.scene.frame_set(1)
            #bpy.ops.anim.change_frame(frame = 1)
            bpy.ops.mesh.primitive_cube_add(radius=0.4,location=(x,y,-1)) 
            ob = bpy.context.object
            me = ob.data
            
            # create keyframe
            bpy.ops.anim.keyframe_insert_menu(type='Location')
            
            #  move to year keyframe
            appear_frame = (float(issue_date[0]) - 1948)*8 + float(issue_date[1]) * 1
            bpy.context.scene.frame_set(appear_frame)
            # do something with the object. A translation, in this case
            bpy.ops.transform.translate(value=(0,0,2))
            
            # todo sset the colour.
            
            # create keyframe
            bpy.ops.anim.keyframe_insert_menu(type='Location')
            
    return
 
if __name__ == "__main__":
    run()