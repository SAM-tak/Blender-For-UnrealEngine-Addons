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




def get_preset_values():
    preset_values = [
            'obj.bfu_export_type',
            'obj.bfu_export_folder_name',
        ]
    return preset_values

class BFU_OT_ObjExportAction(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Action data name", default="Unknown", override={'LIBRARY_OVERRIDABLE'})
    use: bpy.props.BoolProperty(name="use this action", default=False, override={'LIBRARY_OVERRIDABLE'})


# -------------------------------------------------------------------
#   Register & Unregister
# -------------------------------------------------------------------

classes = (
    BFU_OT_ObjExportAction,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.bfu_animation_action_properties_expanded = bbpl.blender_layout.layout_accordion.add_ui_accordion(name="Actions Properties")

    bpy.types.Object.bfu_action_asset_list = bpy.props.CollectionProperty(
        type=BFU_OT_ObjExportAction,
        options={'LIBRARY_EDITABLE'},
        override={'LIBRARY_OVERRIDABLE', 'USE_INSERTION'},
        )

    bpy.types.Object.bfu_active_action_asset_list = bpy.props.IntProperty(
        name="Active Scene Action",
        description="Index of the currently active object action",
        override={'LIBRARY_OVERRIDABLE'},
        default=0
        )

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.bfu_animation_action_properties_expanded