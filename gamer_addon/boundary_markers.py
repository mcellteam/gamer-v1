import bpy
from bpy.props import BoolProperty, CollectionProperty, EnumProperty, \
    FloatProperty, FloatVectorProperty, IntProperty, IntVectorProperty, \
    PointerProperty, StringProperty, BoolVectorProperty
import mathutils
import gamer

# python imports
import os
import re
import numpy as np


# we use per module class registration/unregistration
def register():
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_module(__name__)


# Object Boundary Marker Operators:

class GAMER_OT_add_boundary(bpy.types.Operator):
    bl_idname = "gamer.add_boundary"
    bl_label = "Add New Boundary"
    bl_description = "Add a new boundary to an object"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        context.object.gamer.add_boundary(context)
        return {'FINISHED'}


class GAMER_OT_remove_boundary(bpy.types.Operator):
    bl_idname = "gamer.remove_boundary"
    bl_label = "Remove Boundary"
    bl_description = "Remove selected boundary from object"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        context.object.gamer.remove_boundary(context)
        return {'FINISHED'}


class GAMER_OT_remove_all_boundaries(bpy.types.Operator):
    bl_idname = "gamer.remove_all_boundaries"
    bl_label = "Remove All Boundaries"
    bl_description = "Remove all boundaries from object"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        context.object.gamer.remove_all_boundaries(context)
        return {'FINISHED'}


class GAMER_OT_assign_boundary_faces(bpy.types.Operator):
    bl_idname = "gamer.assign_boundary_faces"
    bl_label = "Assign Selected Faces To Boundary"
    bl_description = "Assign selected faces to boundary"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bnd = context.object.gamer.get_active_boundary()
        if bnd:
            bnd.assign_boundary_faces(context)
        return {'FINISHED'}


class GAMER_OT_remove_boundary_faces(bpy.types.Operator):
    bl_idname = "gamer.remove_boundary_faces"
    bl_label = "Remove Selected Faces From Boundary"
    bl_description = "Remove selected faces from boundary"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bnd = context.object.gamer.get_active_boundary()
        if bnd:
            bnd.remove_boundary_faces(context)
        return {'FINISHED'}


class GAMER_OT_select_boundary_faces(bpy.types.Operator):
    bl_idname = "gamer.select_boundary_faces"
    bl_label = "Select Faces of Selected Boundary"
    bl_description = "Select faces of selected boundary"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bnd = context.object.gamer.get_active_boundary()
        if bnd:
            bnd.select_boundary_faces(context)
        return {'FINISHED'}


class GAMER_OT_deselect_boundary_faces(bpy.types.Operator):
    bl_idname = "gamer.deselect_boundary_faces"
    bl_label = "Deselect Faces of Selected Boundary"
    bl_description = "Deselect faces of selected boundary"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bnd = context.object.gamer.get_active_boundary()
        if bnd:
            bnd.deselect_boundary_faces(context)
        return {'FINISHED'}


# Object Boundary Panel:

class GAMER_UL_check_boundary(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data,
                  active_propname, index):
        if item.status:
            layout.label(item.status, icon='ERROR')
        else:
            layout.label(item.name, icon='FILE_TICK')


# Boundary Callbacks:

def boundary_name_update(self, context):
    context.object.gamer.boundary_name_update()
    return


# Gamer Property Classes for Boundaries

class GAMerBoundaryMarkersPropertyGroup(bpy.types.PropertyGroup):
    name = StringProperty(
        name="Boundary Name", default="Boundary", update=boundary_name_update)
    id = IntProperty(name="Unique ID of This Boundary",default=-1)
    marker = IntProperty(name="Marker Value", default = 1)
    color = FloatVectorProperty ( name="Boundary Color", min=0.0, max=1.0, default=(0.5,0.5,0.5), subtype='COLOR', description='Boundary Color')
    status = StringProperty(name="Status")


    def check_boundary_name(self, bnd_name_list):
        """Checks for duplicate or illegal boundary name"""

        status = ""

        # Check for duplicate boundary name
        if bnd_name_list.count(self.name) > 1:
            status = "Duplicate boundary: %s" % (self.name)

        # Check for illegal names (Starts with a letter. No special characters)
        bnd_filter = r"(^[A-Za-z]+[0-9A-Za-z_.]*$)"
        m = re.match(bnd_filter, self.name)
        if m is None:
            status = "Boundary name error: %s" % (self.name)

        self.status = status

        return


    def assign_boundary_faces(self, context):
        mesh = context.active_object.data
        if (mesh.total_face_sel > 0):
            face_set = self.get_boundary_faces(context) 
            bpy.ops.object.mode_set(mode='OBJECT')
            for f in mesh.polygons:
                if f.select:
                    face_set.add(f.index)
            bpy.ops.object.mode_set(mode='EDIT')

            self.set_boundary_faces(context, face_set) 

        return {'FINISHED'}


    def remove_boundary_faces(self, context):
        mesh = context.active_object.data
        if (mesh.total_face_sel > 0):
            face_set = self.get_boundary_faces(context) 
            bpy.ops.object.mode_set(mode='OBJECT')
            for f in mesh.polygons:
                if f.select:
                    if f.index in face_set:
                        face_set.remove(f.index)
            bpy.ops.object.mode_set(mode='EDIT')

            self.set_boundary_faces(context, face_set) 

        return {'FINISHED'}


    def select_boundary_faces(self, context):
        mesh = context.active_object.data
        face_set = self.get_boundary_faces(context)
        msm = context.scene.tool_settings.mesh_select_mode[0:3]
        context.scene.tool_settings.mesh_select_mode = (False, False, True)
        bpy.ops.object.mode_set(mode='OBJECT')
        for f in face_set:
            mesh.polygons[f].select = True
        bpy.ops.object.mode_set(mode='EDIT')
        context.scene.tool_settings.mesh_select_mode = msm

        return {'FINISHED'}


    def deselect_boundary_faces(self, context):
        mesh = context.active_object.data
        face_set = self.get_boundary_faces(context)
        msm = context.scene.tool_settings.mesh_select_mode[0:3]
        context.scene.tool_settings.mesh_select_mode = (False, False, True)
        bpy.ops.object.mode_set(mode='OBJECT')
        for f in face_set:
            mesh.polygons[f].select = False
        bpy.ops.object.mode_set(mode='EDIT')
        context.scene.tool_settings.mesh_select_mode = msm

        return {'FINISHED'}


    def destroy_boundary(self, context):
        """Remove all boundary data from mesh"""
        bnd_name = self.name

        obj = context.active_object
        for seg_id in obj["boundaries"][bnd_name]['faces'].keys():
            obj["boundaries"][bnd_name]['faces'][seg_id] = []
        obj["boundaries"][bnd_name].clear()
        obj["boundaries"].pop(bnd_name)


    def face_in_boundary(self, context, face_index):
        """Return True if face is in this boundary"""
        mesh = context.active_object.data
        bnd_faces = self.get_boundary_faces(context)
        return(face_index in bnd_faces)


    def init_boundary(self, context, bnd_name, id):

        self.id = id
        self.name = bnd_name

        obj = context.active_object
        if not obj.get("boundaries"):
            obj['boundaries'] = {}
        if not obj['boundaries'].get(bnd_name):
            obj['boundaries'][bnd_name] = {}
        if not obj['boundaries'][bnd_name].get('marker'):
            obj['boundaries'][bnd_name]['marker'] = self.marker
        if not obj['boundaries'][bnd_name].get('r'):
            obj['boundaries'][bnd_name]['r'] = self.color[0]
        if not obj['boundaries'][bnd_name].get('g'):
            obj['boundaries'][bnd_name]['g'] = self.color[1]
        if not obj['boundaries'][bnd_name].get('b'):
            obj['boundaries'][bnd_name]['b'] = self.color[2]
        if not obj['boundaries'][bnd_name].get('faces'):
            obj['boundaries'][bnd_name]['faces'] = {}


    def reset_boundary(self, context):

        id = str(self.id)

        mesh = context.active_object.data

        for seg_id in mesh["mcell"]["boundaries"][id].keys():
            mesh["mcell"]["boundaries"][id][seg_id] = []
        mesh["mcell"]["boundaries"][id].clear()


    def get_boundary_faces(self, context):
        """Given return the set of boundary face indices for this boundary"""

        obj = context.active_object
        bnd_name = self.name

        face_list = []
        for seg_id in obj["boundaries"][bnd_name]['faces'].keys():
          face_list.extend(obj["boundaries"][bnd_name]['faces'][seg_id].to_list())
        if (len(face_list) > 0): 
            face_set = set(face_list)
        else:
            face_set = set([])

        return(face_set)


    def set_boundary_faces(self, context, face_set):
        """Set the faces of a given boundary on object, given a set of faces """

        obj = context.active_object
        bnd_name = self.name
        face_list = list(face_set)
        face_list.sort()

        # Clear existing faces from this boundary id
        obj["boundaries"][bnd_name]["faces"].clear()

        # segment face_list into pieces <= max_len (i.e. <= 32767)
        #   and assign these segments to the boundary id
        max_len = 32767
        seg_list = face_list
        len_list = len(seg_list)
        seg_idx = 0
        while len_list > 0:
          if len_list <= 32767:
            obj["boundaries"][bnd_name]["faces"]["F"+str(seg_idx)] = seg_list
            len_list = 0
          else:
            obj["boundaries"][bnd_name]["faces"]["F"+str(seg_idx)] = seg_list[0:max_len]
            tmp_list = seg_list[max_len:]
            seg_list = tmp_list
            len_list = len(seg_list)
          seg_idx += 1



class GAMerBoundaryMarkersListPropertyGroup(bpy.types.PropertyGroup):
    boundary_list = CollectionProperty(
        type=GAMerBoundaryMarkersPropertyGroup, name="Boundary List")
    active_bnd_index = IntProperty(name="Active Boundary Index", default=0)
    id_counter = IntProperty(name="Counter for Unique Boundary IDs", default=0)
    include = BoolProperty(name="Include Domain in Model", default=False)

    get_boundary_info = BoolProperty(
        name="Toggle to enable/disable boundary_info", default=False)


    def get_boundaries_dictionary (self, context):
        """ Return a dictionary with boundary names """
        bnd_dict = {}
        obj_bnds = self.boundaries.boundary_list
        for bnd in obj_bnds:
            id = str(bnd.id)
            mesh = obj.data
            bnd_faces = list(bnd.get_boundary_faces(context))
            bnd_faces.sort()
            bnd_dict[bnd.name] = bnd_faces
        return bnd_dict


    def get_active_boundary(self):
        bnd = None
        if (len(self.boundary_list) > 0):
            bnd = self.boundary_list[self.active_bnd_index]
        return(bnd)


    def allocate_id(self):
        """ Return a unique boundary ID for a new boundary """
        if (len(self.boundary_list) <= 0):
            # Reset the ID to 0 when there are no more boundaries
            self.id_counter = 0
        id = self.id_counter
        self.id_counter += 1
        return(id)


    def face_get_boundaries(self,context):
        """ Return the list of boundary IDs associated with one selected face """
        bnd_list = ""
        mesh = context.active_object.data
        if (mesh.total_face_sel == 1):
          bpy.ops.object.mode_set(mode='OBJECT')
          face_index = [f.index for f in mesh.polygons if f.select][0]
          bpy.ops.object.mode_set(mode='EDIT')
          for bnd in self.boundary_list: 
            if bnd.face_in_boundary(context,face_index):
              bnd_list = bnd_list + " " + bnd.name
        
        return(bnd_list)


    def faces_get_boundaries(self,context):
        """ Return list of boundary names associated with the selected faces """
        bnd_info = []
        mesh = context.active_object.data
        if (mesh.total_face_sel > 0):
          bpy.ops.object.mode_set(mode='OBJECT')
          selface_set = set([f.index for f in mesh.polygons if f.select])
          bpy.ops.object.mode_set(mode='EDIT')
          for bnd in self.boundary_list: 
            bnd_faces = bnd.get_boundary_faces(context)
            if not selface_set.isdisjoint(bnd_faces):
              bnd_info.append(bnd.name)

        return(bnd_info)


    def add_boundary(self, context):
        """ Add a new boundary to the list of boundaries and set as the active boundary """
        id = self.allocate_id()
        bnd_name = "Boundary_%d" % (id)
        new_bnd = self.boundary_list.add()
# FIXME: CHECK FOR NAME COLLISION HERE: FIX BY ALLOCATING NEXT ID...
        new_bnd.init_boundary(context, bnd_name, id)
        idx = self.boundary_list.find(bnd_name)
        self.active_bnd_index = idx


    def add_boundary_by_name(self, context, bnd_name):
        """ Add a new boundary to the list of boundaries and set as the active boundary """
        curr_bnd = self.get_active_boundary()
        curr_bnd_name = curr_bnd.name

        id = self.allocate_id()
        new_bnd=self.boundary_list.add()
# FIXME: CHECK FOR NAME COLLISION HERE: FIX BY ALLOCATING NEXT ID...
        new_bnd.init_boundary(context, bnd_name, id)

        idx = self.boundary_list.find(curr_bnd_name)
        self.active_bnd_index = idx


    def remove_all_boundaries(self, context):
        for i in range(len(self.boundary_list)):
            # First remove boundary data from mesh:
            bnd = self.boundary_list[0]
            bnd.destroy_boundary(context)

            # Now remove the boundary from the object
            self.boundary_list.remove(0)

        self.active_bnd_index = 0


    def remove_boundary(self, context):

        # First remove ID prop boundary data from object:
        bnd = self.get_active_boundary()
        if bnd:
            bnd.destroy_boundary(context)

            # Now remove the RNA boundary from the object
            self.boundary_list.remove(self.active_bnd_index)
            self.active_bnd_index -= 1
            if (self.active_bnd_index < 0):
                self.active_bnd_index = 0


    def boundary_name_update(self):
        """Performs checks and sorts boundary list after update of boundary names"""

        if self.boundary_list:
            bnd = self.get_active_boundary()
            bnd.check_boundary_name(self.boundary_list.keys())
            self.sort_boundary_list()

        return


    def sort_boundary_list(self):
        """Sorts boundary list"""

        act_bnd = self.get_active_boundary()
        act_bnd_name = act_bnd.name

        # Sort the boundary list
        self.inplace_quicksort(self.boundary_list, 0, len(self.boundary_list)-1)

        act_i = self.boundary_list.find(act_bnd_name)
        self.active_bnd_index = act_i

        return


    def inplace_quicksort(self, v, beg, end):  # collection array, int, int
        """
          Sorts a collection array, v, in place.
          Sorts according values in v[i].name
        """

        if ((end - beg) > 0):  # only perform quicksort if we are dealing with > 1 values
            pivot = v[beg].name  # we set the first item as our initial pivot
            i, j = beg, end

            while (j > i):
                while ((v[i].name <= pivot) and (j > i)):
                    i += 1
                while ((v[j].name > pivot) and (j >= i)):
                    j -= 1
                if (j > i):
                    v.move(i, j)
                    v.move(j-1, i)

            if (not beg == j):
                v.move(beg, j)
                v.move(j-1, beg)
            self.inplace_quicksort(v, beg, j-1)
            self.inplace_quicksort(v, j+1, end)
        return


    def draw_panel(self, context, panel):
        layout = panel.layout
        self.draw_layout ( context, layout )

    def draw_layout(self, context, layout):
        active_obj = context.active_object

        if active_obj and (active_obj.type == 'MESH'):
            row = layout.row()
            # row.label(text="Defined Boundaries:", icon='FORCE_LENNARDJONES')
            row.label(text="Defined Boundaries:", icon='SNAP_FACE')
            row = layout.row()
            col = row.column()
            col.template_list("GAMER_UL_check_boundary", "boundary_list_1",
                          active_obj.gamer, "boundary_list",
                          active_obj.gamer, "active_bnd_index",
                          rows=2)
            col = row.column(align=True)
            col.operator("gamer.add_boundary", icon='ZOOMIN', text="")
            col.operator("gamer.remove_boundary", icon='ZOOMOUT', text="")
            col.operator("gamer.remove_all_boundaries", icon='X', text="")

            # Could have boundary item draw itself in new row here:
            active_bnd = self.get_active_boundary()
            if active_bnd:

                row = layout.row()
                row.prop(active_bnd, "name")

                row = layout.row()
                col = row.column()
                col.label(text="Marker:")
                col = row.column()
                col.prop(active_bnd, "marker", text="")

                row = layout.row()
                col = row.column()
                col.label(text="Color:")
                col = row.column()
                col.prop(active_bnd, "color", text="")

            if active_obj.mode == 'EDIT' and active_bnd:
                row = layout.row()
                sub = row.row(align=True)
                sub.operator("gamer.assign_boundary_faces", text="Assign")
                sub.operator("gamer.remove_boundary_faces", text="Remove")
                sub = row.row(align=True)
                sub.operator("gamer.select_boundary_faces", text="Select")
                sub.operator("gamer.deselect_boundary_faces", text="Deselect")

#                # Option to Get Boundary Info
#                box = layout.box()
#                row = box.row(align=True)
#                row.alignment = 'LEFT'
#                if self.get_boundary_info:
#                    row.prop(self, "get_boundary_info", icon='TRIA_DOWN',
#                             text="Boundary Info for Selected Faces",
#                              emboss=False)
#                    bnd_info = self.faces_get_boundaries(context)
#                    for bnd_name in bnd_info:
#                        row = box.row()
#                        row.label(text=bnd_name)
#                else:
#                    row.prop(self, "get_boundary_info", icon='TRIA_RIGHT',
#                             text="Boundary Info for Selected Faces",
#                             emboss=False)



