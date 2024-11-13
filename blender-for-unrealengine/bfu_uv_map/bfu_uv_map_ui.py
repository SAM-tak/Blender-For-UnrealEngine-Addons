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
from .. import bfu_basics
from .. import bfu_utils
from .. import bfu_ui
from .. import bbpl


def draw_obj_ui(layout: bpy.types.UILayout, obj: bpy.types.Object):

    if obj is None:
        return
    
    scene = bpy.context.scene 
    addon_prefs = bfu_basics.GetAddonPrefs()

    # Hide filters
    if obj is None:
        return
    if bfu_utils.GetExportAsProxy(obj):
        return
    if obj.bfu_export_type != "export_recursive":
        return
    
    if bfu_ui.bfu_ui_utils.DisplayPropertyFilter("OBJECT", "GENERAL"):
        scene.bfu_object_uv_map_properties_expanded.draw(layout)
        if scene.bfu_object_uv_map_properties_expanded.is_expend():
            pass

def draw_tools_ui(layout: bpy.types.UILayout, context: bpy.types.Context):
    scene = context.scene
    scene.bfu_tools_uv_map_properties_expanded.draw(layout)
    if scene.bfu_tools_uv_map_properties_expanded.is_expend():
        ready_for_correct_extrem_uv_scale = False
        obj = bpy.context.object
        if obj and obj.type == "MESH":
            if bbpl.utils.active_mode_is("EDIT"):
                ready_for_correct_extrem_uv_scale = True
            else:
                layout.label(text="Switch to Edit Mode.", icon='INFO')
        else:
            layout.label(text="Select an mesh object", icon='INFO')


            # Draw buttons (correct_extrem_uv)
        Buttons_correct_extrem_uv_scale = layout.row()
        Button_correct_extrem_uv_scale = Buttons_correct_extrem_uv_scale.column()
        Button_correct_extrem_uv_scale.enabled = ready_for_correct_extrem_uv_scale
        Button_correct_extrem_uv_scale.operator("object.correct_extrem_uv", icon='UV')
        bbpl.blender_layout.layout_doc_button.add_doc_page_operator(Buttons_correct_extrem_uv_scale, url="https://github.com/xavier150/Blender-For-UnrealEngine-Addons/wiki/UV-Maps#extreme-uv-scale")
