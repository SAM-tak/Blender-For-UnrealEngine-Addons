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


def draw_ui(layout: bpy.types.UILayout, context: bpy.types.Context):
    scene = context.scene
    addon_prefs = bfu_basics.GetAddonPrefs()
    
    scene.bfu_export_filter_properties_expanded.draw(layout)
    if scene.bfu_export_filter_properties_expanded.is_expend():

        # Assets
        row = layout.row()
        AssetsCol = row.column()
        AssetsCol.label(text="Asset types to export", icon='PACKAGE')
        AssetsCol.prop(scene, 'static_export')
        AssetsCol.prop(scene, 'static_collection_export')
        AssetsCol.prop(scene, 'skeletal_export')
        AssetsCol.prop(scene, 'anin_export')
        AssetsCol.prop(scene, 'alembic_export')
        AssetsCol.prop(scene, 'groom_simulation_export')
        AssetsCol.prop(scene, 'camera_export')
        AssetsCol.prop(scene, 'spline_export')
        layout.separator()

        # Additional file
        FileCol = row.column()
        FileCol.label(text="Additional file", icon='PACKAGE')
        FileCol.prop(scene, 'text_ExportLog')
        FileCol.prop(scene, 'text_ImportAssetScript')
        FileCol.prop(scene, 'text_ImportSequenceScript')
        if addon_prefs.useGeneratedScripts:
            FileCol.prop(scene, 'text_AdditionalData')

        # exportProperty
        export_by_select = layout.row()
        export_by_select.prop(scene, 'bfu_export_selection_filter')