# ====================== BEGIN GPL LICENSE BLOCK ============================
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	 See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.	 If not, see <http://www.gnu.org/licenses/>.
#  All rights reserved.
#
# ======================= END GPL LICENSE BLOCK =============================

import bpy
from .. import bbpl

classes = (
)



def register():
    for cls in classes:
        bpy.utils.register_class(cls)


    bpy.types.Scene.bfu_socket_expanded = bbpl.blender_layout.layout_accordion.add_ui_accordion(name="Socket")
    

    bpy.types.Scene.bfu_nomenclature_properties_expanded = bbpl.blender_layout.layout_accordion.add_ui_accordion(name="Nomenclature")
    bpy.types.Scene.bfu_export_filter_properties_expanded = bbpl.blender_layout.layout_accordion.add_ui_accordion(name="Export filters")
    bpy.types.Scene.bfu_export_process_properties_expanded = bbpl.blender_layout.layout_accordion.add_ui_accordion(name="Export process")
    bpy.types.Scene.bfu_script_tool_expanded = bbpl.blender_layout.layout_accordion.add_ui_accordion(name="Copy Import Script")

    bpy.types.Scene.bfu_active_tab = bpy.props.EnumProperty(
        items=(
            ('OBJECT', 'Object', 'Object tab.'),
            ('SCENE', 'Scene', 'Scene and world tab.')
            )
        )

    bpy.types.Scene.bfu_active_object_tab = bpy.props.EnumProperty(
        items=(
            ('GENERAL', 'General', 'General object tab.'),
            ('ANIM', 'Animations', 'Animations tab.'),
            ('MISC', 'Misc', 'Misc tab.'),
            ('ALL', 'All', 'All tabs.')
            )
        )

    bpy.types.Scene.bfu_active_scene_tab = bpy.props.EnumProperty(
        items=(
            ('GENERAL', 'Scene', 'General scene tab'),
            ('ALL', 'All', 'All tabs.')
            )
        )


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    
    del bpy.types.Scene.bfu_socket_expanded
    
    del bpy.types.Scene.bfu_nomenclature_properties_expanded
    del bpy.types.Scene.bfu_export_filter_properties_expanded
    del bpy.types.Scene.bfu_export_process_properties_expanded
    del bpy.types.Scene.bfu_script_tool_expanded

    del bpy.types.Scene.bfu_active_object_tab

