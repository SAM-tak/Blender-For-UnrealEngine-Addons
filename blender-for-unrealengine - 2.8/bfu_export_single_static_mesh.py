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

from . import bfu_write_text
from . import bfu_basics
from .bfu_basics import *
from . import bfu_utils
from .bfu_utils import *
from . import bfu_export_utils
from .bfu_export_utils import *

from .fbxio import export_fbx_bin
importlib.reload(export_fbx_bin)


def ExportSingleStaticMesh(
        op,
        originalScene,
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

    filename = ValidFilenameForUnreal(filename)
    s = CounterStart()

    if bpy.ops.object.mode_set.poll():
        bpy.ops.object.mode_set(mode='OBJECT')

    SelectParentAndDesiredChilds(obj)
    AddSocketsTempName(obj)
    DuplicateSelectForExport()

    if addon_prefs.correctExtremUVScale:
        SavedSelect = GetCurrentSelection()
        if GoToMeshEditMode():
            CorrectExtremeUV(2)
        bpy.ops.object.mode_set(mode='OBJECT')
        SetCurrentSelection(SavedSelect)

    ApplyNeededModifierToSelect()

    active = bpy.context.view_layer.objects.active

    UpdateNameHierarchy(
        GetAllCollisionAndSocketsObj(bpy.context.selected_objects)
        )

    ApplyExportTransform(active)

    absdirpath = bpy.path.abspath(dirpath)
    VerifiDirs(absdirpath)
    fullpath = os.path.join(absdirpath, filename)
    meshType = GetAssetType(active)

    SetSocketsExportTransform(active)

    RemoveDuplicatedSocketsTempName(active)
    TryToApplyCustomSocketsName(active)

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
        reverse_symmetry_rightside_bone_forwarding = True,
        axis_forward=active.exportAxisForward,
        axis_up=active.exportAxisUp,
        bake_space_transform=False
        )

    CleanDeleteObjects(bpy.context.selected_objects)
    RemoveSocketsTempName(obj)

    exportTime = CounterEnd(s)

    MyAsset = originalScene.BFUO_ExportedAssetsList.add()
    MyAsset.assetName = filename
    MyAsset.assetType = meshType
    MyAsset.exportPath = absdirpath
    MyAsset.exportTime = exportTime
    MyAsset.object = obj
    return MyAsset