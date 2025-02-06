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


import os
import bpy
from . import bfu_export_text_files_utils
from .. import bfu_export_logs
from .. import languages
from .. import bfu_assets_manager
from .. import bfu_basics
from .. import bfu_socket
from .. import bfu_nanite
from .. import bfu_static_mesh
from .. import bfu_skeletal_mesh
from .. import bfu_vertex_color
from .. import bfu_material

def WriteSingleMeshAdditionalParameter(unreal_exported_asset: bfu_export_logs.bfu_asset_export_logs.BFU_OT_UnrealExportedAssetLog):

    scene = bpy.context.scene
    addon_prefs = bfu_basics.GetAddonPrefs()
    obj = unreal_exported_asset.object

    data = {}

    bfu_export_text_files_utils.add_generated_json_header(data, languages.ti('write_text_additional_track_all'))
    bfu_export_text_files_utils.add_generated_json_meta_data(data)

    # Defaultsettings
    data['DefaultSettings'] = {}
    # config.set('Defaultsettings', 'SocketNumber', str(len(sockets)))

    # Level of detail
    if obj:
        data['LevelOfDetail'] = {}

        def GetLodPath(lod_obj):
            asset_class = bfu_assets_manager.bfu_asset_manager_utils.get_asset_class(lod_obj)
            if asset_class:
                directory_path = asset_class.get_obj_export_directory_path(lod_obj, True)
                file_name = asset_class.get_obj_file_name(lod_obj)
            return os.path.join(directory_path, file_name)

        if obj.bfu_lod_target1 is not None:
            data['LevelOfDetail']['lod_1'] = GetLodPath(obj.bfu_lod_target1)
        if obj.bfu_lod_target2 is not None:
            data['LevelOfDetail']['lod_2'] = GetLodPath(obj.bfu_lod_target2)
        if obj.bfu_lod_target3 is not None:
            data['LevelOfDetail']['lod_3'] = GetLodPath(obj.bfu_lod_target3)
        if obj.bfu_lod_target4 is not None:
            data['LevelOfDetail']['lod_4'] = GetLodPath(obj.bfu_lod_target4)
        if obj.bfu_lod_target5 is not None:
            data['LevelOfDetail']['lod_5'] = GetLodPath(obj.bfu_lod_target5)

    # Sockets
    if obj:
        data['Sockets'] = bfu_socket.bfu_socket_utils.get_skeletal_mesh_sockets(obj)

    # Vertex Color
    if obj:
        if bfu_static_mesh.bfu_static_mesh_utils.is_static_mesh(obj) or bfu_skeletal_mesh.bfu_skeletal_mesh_utils.is_skeletal_mesh(obj):
            vced = bfu_vertex_color.bfu_vertex_color_utils.VertexColorExportData(obj)
            data["vertex_color_import_option"] = vced.export_type
            vertex_override_color = (
                vced.color[0],  # R
                vced.color[1],  # G
                vced.color[2]  # B
            )  # Color to Json
            data["vertex_override_color"] = vertex_override_color
    
    data.update(bfu_material.bfu_material_utils.get_material_asset_additional_data(unreal_exported_asset))
    data.update(bfu_nanite.bfu_nanite_utils.get_nanite_asset_additional_data(unreal_exported_asset))

    data["preview_import_path"] = unreal_exported_asset.GetFilenameWithExtension()

    bfu_export_text_files_utils.add_generated_json_footer(data)
    return data