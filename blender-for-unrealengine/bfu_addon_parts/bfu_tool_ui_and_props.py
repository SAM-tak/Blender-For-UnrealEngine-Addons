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
from .. import bfu_camera
from .. import bfu_spline
from .. import bfu_collision
from .. import bfu_socket
from .. import bbpl

class BFU_PT_BlenderForUnrealTool(bpy.types.Panel):
    # Tool panel

    bl_idname = "BFU_PT_BlenderForUnrealTool"
    bl_label = "UE AE Tools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Unreal Engine"

    def draw(self, context):

        layout = self.layout
        scene = bpy.context.scene

        bfu_camera.bfu_camera_ui_and_props.draw_ui_scene_camera(layout)
        bfu_spline.bfu_spline_ui_and_props.draw_ui_scene_spline(layout)

        bfu_collision.bfu_collision_ui_and_props.draw_ui_scene_collision(layout)
        bfu_socket.bfu_socket_ui_and_props.draw_ui_scene_socket(layout)

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

        scene.bfu_tools_light_map_properties_expanded.draw(layout)
        if scene.bfu_tools_light_map_properties_expanded.is_expend():
            checkButton = layout.column()
            checkButton.operator("object.comput_all_lightmap", icon='TEXTURE')

# -------------------------------------------------------------------
#   Register & Unregister
# -------------------------------------------------------------------

classes = (
    BFU_PT_BlenderForUnrealTool,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
