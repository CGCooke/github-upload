import os
import bpy
import numpy as np

#blender --background --python myscript.py

def create_material(object_name,material_name, rgba):
	mat = bpy.data.materials.new(name=material_name)
	bpy.data.objects[object_name].active_material = mat
	
	mat.use_nodes = True
	nodes = mat.node_tree.nodes
	nodes["Principled BSDF"].inputs[0].default_value = rgba
	nodes["Principled BSDF"].inputs[5].default_value = 1
	nodes["Principled BSDF"].inputs[7].default_value = 0.1


def configure_camera():
	bpy.data.objects["Camera"].location[0] = 0.7
	bpy.data.objects["Camera"].location[1] = -4
	bpy.data.objects["Camera"].location[2] = 3

	bpy.data.objects["Camera"].rotation_euler[0] = np.radians(60)
	bpy.data.objects["Camera"].rotation_euler[1] = 0.0
	bpy.data.objects["Camera"].rotation_euler[2] = 0.0



def configure_light():
	bpy.data.objects["Light"].data.type = 'AREA'
	bpy.data.objects["Light"].scale[0] = 10
	bpy.data.objects["Light"].scale[1] = 10

	bpy.data.objects["Light"].location[0] = 0
	bpy.data.objects["Light"].location[1] = 0
	bpy.data.objects["Light"].location[2] = 6

	bpy.data.objects["Light"].rotation_euler[0] = 0
	bpy.data.objects["Light"].rotation_euler[1] = 0
	bpy.data.objects["Light"].rotation_euler[2] = 0
	
def configure_render():
	bpy.context.scene.render.engine = 'CYCLES'

	bpy.context.scene.render.filepath = os.getcwd()+"/Simple4.png"
	bpy.context.scene.render.resolution_x = 1600
	bpy.context.scene.render.resolution_y = 1200
	bpy.context.scene.cycles.samples = 2*1280

objs = bpy.data.objects
objs.remove(objs['Cube'], do_unlink = True)


bpy.ops.mesh.primitive_plane_add(size=1000,location=(0, 0, 0), scale=(1, 1, 1))

create_material("Plane","Plane_material",(0.7,0.7,0.7,1))

bpy.ops.import_scene.obj(filepath=os.getcwd()+"/stanford_bunny.obj")
ob = bpy.data.objects["stanford_bunny"]
ob.scale = (10,10,10)
ob.location[0] = 1
ob.location[1] = 0
ob.location[2] = -0.35


ob.name = 'Bunny'



#bpy.ops.object.modifier_add(type='SUBSURF')
#bpy.context.object.modifiers["Subdivision"].render_levels = 3


#ob.modifier_add(type='SUBSURF')
#ob.modifiers["Subdivision"].render_levels = 3

bevel_mod = ob.modifiers.new('Subsurf', 'SUBSURF')
bevel_mod.render_levels = 3




object_name = ob.name

object_name = 'Bunny'
material_name = 'Bunny_Material'

mat = bpy.data.materials.new(name=material_name)
bpy.data.objects[object_name].active_material = mat

mat.use_nodes = True
nodes = mat.node_tree.nodes

nodes.new("ShaderNodeBsdfGlass")
nodes.new("ShaderNodeVolumeAbsorption")


nodes["Glass BSDF"].inputs[0].default_value = (0.603828, 1, 0.707399, 1)
nodes["Glass BSDF"].inputs[1].default_value = 0.25
nodes["Glass BSDF"].inputs[2].default_value = 1.5
nodes["Volume Absorption"].inputs[0].default_value = (0.604999, 1, 0.707, 1)

  
nodes.remove(nodes["Principled BSDF"])


links = ob.active_material.node_tree.links
links.new(nodes["Glass BSDF"].outputs[0], nodes["Material Output"].inputs[0])
links.new(nodes["Volume Absorption"].outputs[0], nodes["Material Output"].inputs[1])


configure_camera()
configure_light()
configure_render()




bpy.ops.render.render(write_still=True)


