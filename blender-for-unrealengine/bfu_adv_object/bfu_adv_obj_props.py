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
from .. import languages




def get_preset_values():
    preset_values = [
        ]
    return preset_values

# -------------------------------------------------------------------
#   Register & Unregister
# -------------------------------------------------------------------

classes = (
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.bfu_object_advanced_properties_expanded = bbpl.blender_layout.layout_accordion.add_ui_accordion(name="Object Advanced Properties")

    bpy.types.Object.bfu_export_with_meta_data = bpy.props.BoolProperty(
        name=(languages.ti('export_with_meta_data_name')),
        description=(languages.tt('export_with_meta_data_desc')),
        override={'LIBRARY_OVERRIDABLE'},
        default=False,
        )


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.bfu_export_with_meta_data
    del bpy.types.Scene.bfu_object_advanced_properties_expanded