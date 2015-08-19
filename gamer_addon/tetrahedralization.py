# This branch was created to work on the tetrahedralization.

import bpy
from bpy.props import BoolProperty, CollectionProperty, EnumProperty, \
    FloatProperty, FloatVectorProperty, IntProperty, IntVectorProperty, \
    PointerProperty, StringProperty, BoolVectorProperty
import mathutils
import gamer

# python imports
import os
import numpy as np


# we use per module class registration/unregistration
def register():
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_module(__name__)


# Tetrahedralization Operators:

class GAMER_OT_tet_domain_add(bpy.types.Operator):
    bl_idname = "gamer.tet_domain_add"
    bl_label = "Add a Tet Domain"
    bl_description = "Add a new tetrahedralization domain"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        context.scene.gamer.tet_group.add_tet_domain(context)
        return {'FINISHED'}

class GAMER_OT_tet_domain_remove(bpy.types.Operator):
    bl_idname = "gamer.tet_domain_remove"
    bl_label = "Remove a Tet Domain"
    bl_description = "Remove a tetrahedralization domain"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        context.scene.gamer.tet_group.remove_active_tet_domain(context)
        self.report({'INFO'}, "Deleted Active Tet Group")
        return {'FINISHED'}


class GAMER_OT_generic_button(bpy.types.Operator):
    bl_idname = "gamer.generic_button"
    bl_label = "Generic Button"
    bl_description = ("Generic Button")
    bl_options = {'REGISTER'}

    def execute(self, context):
        print ( "Executed" )
        return {'FINISHED'}

    def invoke(self, context, event):
        return self.execute(context)


class GAMerTetDomainPropertyGroup(bpy.types.PropertyGroup):
    # name = StringProperty()  # This is a reminder that "name" is already defined for all subclasses of PropertyGroup
    domain_id = IntProperty ( name="ID", default=-1, description="Domain ID" )
    marker = IntProperty ( name="Marker", default=-1, description="Domain Marker Integer" )
    is_hole = BoolProperty ( name="Hole", default=False, description="Use this domain as a hole" )
    constrain_vol  = BoolProperty ( name="Constrain Volume", default=False, description="Constrain Volume" )
    vol_constraint = FloatProperty ( name="Vol Constraint", default=10.0, description="Volume Constraint" )

    min_dihedral = FloatProperty ( name="Min Dihedral", default=10.0, description="Minimum Dihedral in Degrees" )
    max_aspect_ratio = FloatProperty ( name="Max Aspect Ration", default=1.3, description="Maximum Aspect Ratio" )

    dolfin = BoolProperty ( name="DOLFIN", default=False, description="DOLFIN" )
    diffpack = BoolProperty ( name="Diffpack", default=False, description="Diffpack" )
    carp = BoolProperty ( name="Carp", default=False, description="Carp" )
    fetk = BoolProperty ( name="FEtk", default=False, description="FEtk" )
    ho_mesh = BoolProperty ( name="Higher order mesh generation", default=False, description="Higher order mesh generation" )
    
    def draw_layout ( self, layout ):

        row = layout.row()
        col = row.column()
        col.prop ( self, "marker" )
        col = row.column()
        col.prop ( self, "is_hole" )

        row = layout.row()
        col = row.column()
        col.prop ( self, "constrain_vol" )
        if self.constrain_vol:
            col = row.column()
            col.prop ( self, "vol_constraint" )

        row = layout.row()
        col = row.column()
        col.prop ( self, "min_dihedral" )
        col = row.column()
        col.prop ( self, "max_aspect_ratio" )
        
        row = layout.row()
        col = row.column()
        col.prop ( self, "dolfin" )
        col = row.column()
        col.prop ( self, "diffpack" )

        row = layout.row()
        col = row.column()
        col.prop ( self, "carp" )
        col = row.column()
        col.prop ( self, "fetk" )

        row = layout.row()
        col = row.column()
        col.operator ( "gamer.generic_button", text="Tetrahedralize" )
        col = row.column()
        col.prop ( self, "ho_mesh" )


class GAMer_UL_domain(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        # The draw_item function is called for each item of the collection that is visible in the list.
        #   data is the RNA object containing the collection,
        #   item is the current drawn item of the collection,
        #   icon is the "computed" icon for the item (as an integer, because some objects like materials or textures
        #        have custom icons ID, which are not available as enum items).
        #   active_data is the RNA object containing the active property for the collection (i.e. integer pointing to the
        #        active item of the collection).
        #   active_propname is the name of the active property (use 'getattr(active_data, active_propname)').
        #   index is index of the current item in the collection.
        #   flt_flag is the result of the filtering process for this item.
        #   Note: as index and flt_flag are optional arguments, you do not have to use/declare them here if you don't
        #         need them.

        tet = item

        row = layout.row()
        col = row.column()
        col.label ( "Domain ID: " + str(tet.domain_id) )
        col = row.column()
        col.label ( "Domain Marker: " + str(tet.marker) )


class GAMerTetrahedralizationPropertyGroup(bpy.types.PropertyGroup):

  generic_float = FloatProperty( name="Generic Float", default=123.456, min=0.0, max=1000, precision=4, description="A Generic Float Value")
  generic_int = IntProperty( name="Generic Int", default=5, min=1, max=10, description="A Generic Int Value")
  generic_boolean = BoolProperty( name="Generic Bool", default=False, description="A Generic Boolean Value")

  domain_list = CollectionProperty(type=GAMerTetDomainPropertyGroup, name="Domain List")
  active_domain_index = IntProperty(name="Active Domain Index", default=0)
  next_id = IntProperty(name="Counter for Unique Domain IDs", default=1)  # Start ID's at 1 to confirm initialization

  def draw_layout ( self, context, layout ):

      row = layout.row()
      col = row.column()

      col.template_list("GAMer_UL_domain", "",
                        self, "domain_list",
                        self, "active_domain_index",
                        rows=2)

      col = row.column(align=True)
      col.operator("gamer.tet_domain_add", icon='ZOOMIN', text="")
      col.operator("gamer.tet_domain_remove", icon='ZOOMOUT', text="")

      if len(self.domain_list) > 0:
          domain = self.domain_list[self.active_domain_index]

          row = layout.row()
          row.label ( "Active Index = " + str ( self.active_domain_index ) + ", ID = " + str ( domain.domain_id ) )
          
          domain.draw_layout ( layout )

  def add_tet_domain ( self, context):
      print("Adding a Tet Domain")
      """ Add a new tet domain to the list of tet domains and set as the active domain """
      new_dom = self.domain_list.add()
      new_dom.domain_id = self.allocate_available_id()
      self.active_domain_index = len(self.domain_list)-1

  def remove_active_tet_domain ( self, context):
      print("Removing active Tet Domain")
      """ Remove the active tet domain from the list of domains """
      self.domain_list.remove ( self.active_domain_index )
      self.active_domain_index -= 1
      if self.active_domain_index < 0:
          self.active_domain_index = 0
          print ( "That was the last one!!!" )

  def allocate_available_id ( self ):
      """ Return a unique domain ID for a new domain """
      print ( "Next ID is " + str(self.next_id) )
      if len(self.domain_list) <= 0:
          # Reset the ID to 1 when there are no more molecules
          self.next_id = 1
      self.next_id += 1
      return ( self.next_id - 1 )

  def draw_panel ( self, context, panel ):
      layout = panel.layout
      self.draw_layout ( context, layout )


