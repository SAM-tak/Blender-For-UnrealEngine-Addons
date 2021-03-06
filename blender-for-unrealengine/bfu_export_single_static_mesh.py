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
import time
import math

from mathutils import Matrix
from bpy_extras.io_utils import axis_conversion

if "bpy" in locals():
    import importlib
    if "bfu_write_text" in locals():
        importlib.reload(bfu_write_text)
    if "bfu_basics" in locals():
        importlib.reload(bfu_basics)
    if "bfu_utils" in locals():
        importlib.reload(bfu_utils)
    if "bfu_export_utils" in locals():
        importlib.reload(bfu_export_utils)
    if "bfu_check_potential_error" in locals():
        importlib.reload(bfu_check_potential_error)
    if "export_fbx_bin" in locals():
        importlib.reload(export_fbx_bin)

from . import bfu_write_text
from . import bfu_basics
from .bfu_basics import *
from . import bfu_utils
from .bfu_utils import *
from . import bfu_export_utils
from .bfu_export_utils import *
from . import bfu_check_potential_error
from .fbxio import export_fbx_bin


def ProcessStaticMeshExport(op, obj):
    addon_prefs = bpy.context.preferences.addons[__package__].preferences
    dirpath = GetObjExportDir(obj)
    absdirpath = bpy.path.abspath(dirpath)
    scene = bpy.context.scene

    MyAsset = scene.UnrealExportedAssetsList.add()
    MyAsset.StartAssetExport(obj)

    ExportSingleStaticMesh(op, dirpath, GetObjExportFileName(obj), obj)
    file = MyAsset.files.add()
    file.name = GetObjExportFileName(obj)
    file.path = dirpath
    file.type = "FBX"

    if not obj.ExportAsLod:
        if (scene.text_AdditionalData and addon_prefs.useGeneratedScripts):
            ExportSingleAdditionalParameterMesh(absdirpath, GetObjExportFileName(obj, "_AdditionalTrack.json"), obj)
            file = MyAsset.files.add()
            file.name = GetObjExportFileName(obj, "_AdditionalTrack.json")
            file.path = dirpath
            file.type = "AdditionalTrack"

    MyAsset.EndAssetExport(True)
    return MyAsset


def ExportSingleStaticMesh(
        op,
        dirpath,
        filename,
        obj
        ):

    '''
    #####################################################
            #STATIC MESH
    #####################################################
    '''
    # Export a single Mesh

    scene = bpy.context.scene
    addon_prefs = bpy.context.preferences.addons[__package__].preferences

    SafeModeSet('OBJECT')

    SelectParentAndDesiredChilds(obj)
    AddSubObjectTempName(obj)
    asset_name = PrepareExportName(obj, False)
    data_to_remove = DuplicateSelectForExport()
    CorrectExtremUVAtExport()

    ApplyNeededModifierToSelect()

    active = bpy.context.view_layer.objects.active
    asset_name.target_object = active



    ApplyExportTransform(active)
    absdirpath = bpy.path.abspath(dirpath)
    VerifiDirs(absdirpath)
    fullpath = os.path.join(absdirpath, filename)
    meshType = GetAssetType(active)
    SetSocketsExportTransform(active)

    RemoveDuplicatedSubObjectTempName(active)

    TryToApplyCustomSocketsName(active)
    asset_name.SetExportName()

    bfu_check_potential_error.UpdateNameHierarchy(
        GetAllCollisionAndSocketsObj(bpy.context.selected_objects)
        )

    export_fbx_bin.save(
        op,
        bpy.context,
        filepath=fullpath,
        check_existing=False,
        use_selection=True,
        global_matrix=axis_conversion(to_forward=active.exportAxisForward, to_up=active.exportAxisUp).to_4x4(),
        apply_unit_scale=True,
        global_scale=GetObjExportScale(active),
        apply_scale_options='FBX_SCALE_NONE',
        object_types={'EMPTY', 'CAMERA', 'LIGHT', 'MESH', 'OTHER'},
        use_custom_props=addon_prefs.exportWithCustomProps,
        mesh_smooth_type="FACE",
        add_leaf_bones=False,
        use_armature_deform_only=active.exportDeformOnly,
        bake_anim=False,
        path_mode='AUTO',
        embed_textures=False,
        batch_mode='OFF',
        use_batch_own_dir=True,
        use_metadata=addon_prefs.exportWithMetaData,
        primary_bone_axis=active.exportPrimaryBoneAxis,
        secondary_bone_axis=active.exporSecondaryBoneAxis,
        reverse_symmetry_rightside_bone_forwarding=True,
        axis_forward=active.exportAxisForward,
        axis_up=active.exportAxisUp,
        bake_space_transform=False
        )

    asset_name.ResetNames()

    CleanDeleteObjects(bpy.context.selected_objects)
    for data in data_to_remove:
        data.RemoveData()

    RemoveSubObjectTempName(obj)
