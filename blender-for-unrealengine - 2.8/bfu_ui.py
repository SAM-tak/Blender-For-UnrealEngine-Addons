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
import fnmatch
import time
import addon_utils

if "bpy" in locals():
    import importlib
    if "bfu_export_asset" in locals():
        importlib.reload(bfu_export_asset)
    if "bfu_write_text" in locals():
        importlib.reload(bfu_write_text)
    if "bfu_basics" in locals():
        importlib.reload(bfu_basics)
    if "bfu_utils" in locals():
        importlib.reload(bfu_utils)

from . import bfu_export_asset
from . import bfu_write_text
from . import bfu_basics
from .bfu_basics import *
from . import bfu_utils
from .bfu_utils import *

from bpy.props import (
        StringProperty,
        BoolProperty,
        EnumProperty,
        IntProperty,
        FloatProperty,
        FloatVectorProperty,
        PointerProperty,
        CollectionProperty,
        )

from bpy.types import (
        Operator,
        )


class BFUO_AP_AddonPreferences(bpy.types.AddonPreferences):
    # this must match the addon name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = __package__

    bakeArmatureAction: BoolProperty(
        name='Bake Armature animation',
        description=(
            'Bake Armature animation for export' +
            ' (Export will take more time)'
            ),
        default=False,
        )

    correctExtremUVScale: BoolProperty(
        name='Correct Extrem UV Scale',
        description=(
            'Correct Extrem UV Scale for better UV quality in UE4' +
            ' (Export will take more time)'
            ),
        default=False,
        )

    removeSkeletonRootBone: BoolProperty(
        name='Remove root bone',
        description='Remove the armature root bone',
        default=True,
        )

    skeletonRootBoneName: StringProperty(
        name='Skeleton root bone name',
        description=(
            'Name of the armature when exported.' +
            ' This is used to change the root bone name.' +
            ' If egal "Armature" Ue4 will remove the Armature root bone.'
            ),
        default="ArmatureRoot",
        )

    rescaleFullRigAtExport: EnumProperty(
        name='Rescale exported rig',
        description=(
            'This will rescale the full rig' +
            ' at the export with the all constraints.'
            ),
        items=[
            ("auto",
                "Auto",
                "Rescale only if the the Unit Scale is not = to 0.01",
                "SHADERFX",
                1),
            ("custom_rescale",
                "Custom Rescale",
                "You can choose how rescale the rig at the export",
                "MODIFIER",
                2),
            ("dont_rescale",
                "Dont Rescale",
                "Will not rescale the rig",
                "CANCEL",
                3)
            ]
        )

    newRigScale: FloatProperty(
        name='New scale',
        description=(
            'The new rig scale. AUTO: [New scale} = 100 * [Unit scale]'
            ),
        default=100,
        )

    staticSocketsAdd90X: BoolProperty(
        name='Export StaticMesh Sockets with +90 degrees on X',
        description=(
            'On StaticMesh the sockets are auto imported by unreal' +
            ' with -90 degrees on X'
            ),
        default=True,
        )

    rescaleSocketsAtExport: EnumProperty(
        name='Rescale exported sockets',
        description='This will rescale the all sockets at the export.',
        items=[
            ("auto",
                "Auto",
                "Rescale only if the the Unit Scale is not = to 0.01",
                "SHADERFX",
                1),
            ("custom_rescale",
                "Custom Rescale",
                "You can choose how rescale the sockets at the export",
                "MODIFIER",
                2),
            ("dont_rescale",
                "Dont Rescale",
                "Will not rescale the sockets",
                "CANCEL",
                3)
            ]
        )

    staticSocketsImportedSize: FloatProperty(
        name='StaticMesh sockets import size',
        description=(
            'Size of the socket when imported in Unreal Engine.' +
            ' AUTO: 1 ( [New scale} = 100 / [Unit scale] )'
            ),
        default=1,
        )

    skeletalSocketsImportedSize: FloatProperty(
        name='SkeletalMesh sockets import size',
        description=(
            'Size of the socket when imported in Unreal Engine.' +
            ' AUTO: 1 ( [New scale} = 100 / [Unit scale] )'
            ),
        default=1,
        )

    ignoreNLAForAction: BoolProperty(
        name='Ignore NLA for Actions',
        description=(
            'This will export the action and ignore' +
            ' the all layer in Nonlinear Animation'
            ),
        default=False,
        )

    exportWithCustomProps: BoolProperty(
        name='Export custom properties',
        description=(
            'Process export with custom properties' +
            ' (Can be used for Metadata)'
            ),
        default=False,
        )

    exportWithMetaData: BoolProperty(
        name='Export meta data',
        description='Process export with meta data',
        default=False,
        )

    revertExportPath: BoolProperty(
        name='Revert all export path at each export',
        description=(
            'will remove the folder of' +
            ' the all export path at each export'
            ),
        default=False,
        )

    useGeneratedScripts:  BoolProperty(
        name='Use generated script for import assets and sequencer.',
        description=(
            'If false the all properties that only works' +
            ' with import scripts will be disabled'
            ),
        default=True,
        )

    collisionColor:  FloatVectorProperty(
        name='Collision color.',
        description='Color of the collision in Blender',
        subtype='COLOR',
        size=4,
        default=(0, 0.6, 0, 0.11),
        min=0.0, max=1.0,
        )

    notifyUnitScalePotentialError: BoolProperty(
        name='Notify UnitScale (PotentialError)',
        description=(
            'Notify as potential error' +
            ' if the unit scale is not equal to 0.01.'
            ),
        default=True,
        )

    class BFUO_OT_OpenDocumentationTargetPage(Operator):
        bl_label = "Documentation"
        bl_idname = "bfuo.open_documentation_target_page"
        bl_description = "Clic for open documentation page on GitHub"
        octicon: StringProperty(default="")

        def execute(self, context):
            os.system(
                "start \"\" " +
                "https://github.com/xavier150/" +
                "Blender-For-UnrealEngine-Addons/blob/master/Tuto/" +
                "How%20export%20assets%20from%20Blender.md"+self.octicon
                )
            return {'FINISHED'}

    class BFUO_OT_NewReleaseInfo(Operator):
        bl_label = "Open last release page"
        bl_idname = "bfuo.new_release_info"
        bl_description = "Clic for open latest release page."

        def execute(self, context):
            os.system(
                "start \"\" https://github.com/xavier150/" +
                "Blender-For-UnrealEngine-Addons/releases/latest"
                )
            return {'FINISHED'}

    def draw(self, context):
        layout = self.layout

        def LabelWithDocButton(tagetlayout, name, docOcticon):
            newRow = tagetlayout.row()
            newRow.label(text=name)
            docOperator = newRow.operator(
                "bfuo.open_documentation_target_page",
                icon="HELP",
                text=""
                )
            docOperator.octicon = docOcticon

        def PropWithDocButton(tagetlayout, name, docOcticon):
            newRow = tagetlayout.row()
            newRow.prop(self, name)
            docOperator = newRow.operator(
                "bfuo.open_documentation_target_page",
                icon="HELP",
                text=""
                )
            docOperator.octicon = docOcticon

        boxColumn = layout.column().split(
            factor=0.5
            )

        rootBone = boxColumn.box()

        LabelWithDocButton(
            rootBone,
            "SKELETON & ROOT BONE",
            "#skeleton--root-bone"
            )
        rootBone.prop(self, "removeSkeletonRootBone")
        rootBoneName = rootBone.column()
        rootBoneName.enabled = not self.removeSkeletonRootBone
        rootBoneName.prop(self, "skeletonRootBoneName")

        rootBone.prop(self, "rescaleFullRigAtExport")
        newRigScale = rootBone.column()
        newRigScale.enabled = self.rescaleFullRigAtExport == "custom_rescale"
        newRigScale.prop(self, "newRigScale")

        socket = boxColumn.box()
        socket.label(text='SOCKET')
        socket.prop(self, "staticSocketsAdd90X")
        socket.prop(self, "rescaleSocketsAtExport")
        socketRescale = socket.column()
        socketRescale.enabled = self.rescaleSocketsAtExport == "custom_rescale"
        socketRescale.prop(self, "staticSocketsImportedSize")
        socketRescale.prop(self, "skeletalSocketsImportedSize")

        boxColumn = layout.column().split(factor=0.5)

        data = boxColumn.box()
        data.label(text='DATA')
        data.prop(self, "ignoreNLAForAction")
        PropWithDocButton(data, "correctExtremUVScale", "#uv")
        data.prop(self, "bakeArmatureAction")
        data.prop(self, "exportWithCustomProps")
        data.prop(self, "exportWithMetaData")
        data.prop(self, "revertExportPath")

        script = boxColumn.box()
        script.label(text='IMPORT SCRIPT')
        script.prop(self, "useGeneratedScripts")

        boxColumn = layout.column().split(factor=0.5)

        other = boxColumn.box()
        other.label(text='OTHER')
        other.prop(self, "collisionColor")
        other.prop(self, "notifyUnitScalePotentialError")

        updateButton = layout.row()
        updateButton.scale_y = 2.0
        updateButton.operator("bfuo.new_release_info", icon="TIME")


class BFUO_PT_BlenderForUnrealObject(bpy.types.Panel):
    # Unreal engine export panel

    bl_idname = "BFUO_PT_BlenderForUnrealObject"
    bl_label = "(Select) Blender for Unreal Engine"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Unreal Engine Old"

    class BFUO_OT_OpenDocumentationPage(Operator):
        bl_label = "Documentation"
        bl_idname = "bfuo.open_documentation_page"
        bl_description = "Clic for open documentation page on GitHub"

        def execute(self, context):
            os.system(
                "start \"\" " +
                "https://github.com/xavier150/" +
                "Blender-For-UnrealEngine-Addons/blob/master/" +
                "Tuto/How%20export%20assets%20from%20Blender.md"
                )
            return {'FINISHED'}

    def draw(self, contex):

        releaseVersion = None  # GetGitHubLastRelaseVersion()

        layout = self.layout
        docsButton = layout.row()
        docsButton.operator("bfuo.open_documentation_page", icon="HELP")


class BFUO_PT_BlenderForUnreal(bpy.types.Panel):
    # Unreal engine export panel

    bl_idname = "BFUO_PT_BlenderForUnreal"
    bl_label = "(Global) Blender for Unreal Engine"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Unreal Engine Old"

    class BFUO_MT_ObjectGlobalPropertiesPresets(bpy.types.Menu):
        bl_label = 'Global Properties Presets'
        preset_subdir = 'blender-for-unrealengine-old/global-properties-presets'
        preset_operator = 'script.execute_preset'
        draw = bpy.types.Menu.draw_preset

    from bl_operators.presets import AddPresetBase

    class BFUO_OT_AddObjectGlobalPropertiesPreset(AddPresetBase, Operator):
        bl_idname = 'bfuo.add_globalproperties_preset'
        bl_label = 'Add or remove a preset for Global properties'
        bl_description = 'Add or remove a preset for Global properties'
        preset_menu = 'BFUO_MT_ObjectGlobalPropertiesPresets'

        # Common variable used for all preset values
        preset_defines = [
                            'obj = bpy.context.object',
                            'scene = bpy.context.scene'
                         ]

        # Properties to store in the preset
        preset_values = [
                            'obj.exportFolderName',
                            'obj.ExportAsAlembic',
                            'obj.ExportAsLod',
                            'obj.ForceStaticMesh',
                            'obj.exportDeformOnly',
                            'obj.Ue4Lod1',
                            'obj.Ue4Lod2',
                            'obj.Ue4Lod3',
                            'obj.Ue4Lod4',
                            'obj.Ue4Lod5',
                            'obj.CreatePhysicsAsset',
                            'obj.UseTargetCustomSkeletonName',
                            'obj.TargetCustomSkeletonName',
                            'obj.UseStaticMeshLODGroup',
                            'obj.StaticMeshLODGroup',
                            'obj.StaticMeshLightMapEnum',
                            'obj.customStaticMeshLightMapRes',
                            'obj.staticMeshLightMapSurfaceScale',
                            'obj.staticMeshLightMapRoundPowerOfTwo',
                            'obj.useStaticMeshLightMapWorldScale',
                            'obj.GenerateLightmapUVs',
                            'obj.AutoGenerateCollision',
                            'obj.MaterialSearchLocation',
                            'obj.CollisionTraceFlag',
                            'obj.VertexColorImportOption',
                            'obj.exportActionEnum',
                            'obj.PrefixNameToExport',
                            'obj.AnimStartEndTimeEnum',
                            'obj.StartFramesOffset',
                            'obj.EndFramesOffset',
                            'obj.AnimCustomStartTime',
                            'obj.AnimCustomEndTime',
                            'obj.SampleAnimForExport',
                            'obj.SimplifyAnimForExport',
                            'obj.ExportNLA',
                            'obj.NLAAnimName',
                            'obj.bfu_anim_naming_type',
                            'obj.bfu_anim_naming_custom',
                            'obj.exportGlobalScale',
                            'obj.exportAxisForward',
                            'obj.exportAxisUp',
                            'obj.exportPrimaryBoneAxis',
                            'obj.exporSecondaryBoneAxis',
                            'obj.MoveToCenterForExport',
                            'obj.RotateToZeroForExport',
                            'obj.AdditionalLocationForExport',
                            'obj.AdditionalRotationForExport',
                        ]

        # Directory to store the presets
        preset_subdir = 'blender-for-unrealengine-old/global-properties-presets'

    def draw(self, contex):
        pass


class BFUO_PT_ObjectProperties(bpy.types.Panel):
    # Is Object Properties panel

    bl_idname = "BFUO_PT_ObjectProperties"
    bl_label = "Object Properties"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Unreal Engine 4 Old"
    bl_parent_id = "BFUO_PT_BlenderForUnrealObject"

    bpy.types.Object.ExportEnum = EnumProperty(
        name="Export type",
        description="Export procedure",
        items=[
            ("auto",
                "Auto",
                "Exports only if one of the parents is \"Export recursive\"",
                "BOIDS",
                1),
            ("export_recursive",
                "Export recursive",
                "Export self object and all children",
                "KEYINGSET",
                2),
            ("dont_export",
                "Not exported",
                "Will never export",
                "CANCEL",
                3)
            ]
        )

    bpy.types.Object.exportFolderName = StringProperty(
        name="Sub folder name",
        description=(
            'The name of sub folder.' +
            ' You can now use ../ for up one directory.'
            ),

        maxlen=64,
        default="",
        subtype='FILE_NAME'
        )

    bpy.types.Object.bfu_export_procedure = EnumProperty(
        name="Export procedure",
        description=(
            "This will define how the object should" +
            " be exported in case you are using specific Rig."
            ),
        items=[
            ("normal",
                "Normal",
                "No specific Rig.",
                "ARMATURE_DATA",
                1),
            ("auto-rig-pro",
                "AutoRigPro",
                "Export using AutoRigPro.",
                "ARMATURE_DATA",
                2),
            ]
        )

    bpy.types.Object.ExportAsProxy = BoolProperty(
        name="The armature is a Proxy ?",
        description=(
            "If true this mesh will be exported" +
            " with a target child for keed to data"
            ),
        default=False
        )

    bpy.types.Object.ExportProxyChild = PointerProperty(
        name="The armature proxy children",
        description="Select child proxy (The mesh animated by this armature)",
        type=bpy.types.Object
        )

    bpy.types.Object.ExportAsAlembic = BoolProperty(
        name="Export as Alembic animation",
        description=(
            "If true this mesh will be exported as a Alembic animation"
            ),
        default=False
        )

    bpy.types.Object.ExportAsLod = BoolProperty(
        name="Export as lod?",
        description=(
            "If true this mesh will be exported" +
            " as a level of detail for another mesh"
            ),
        default=False
        )

    bpy.types.Object.ForceStaticMesh = BoolProperty(
        name="Force staticMesh",
        description="Force export asset like a StaticMesh if is ARMATURE type",
        default=False
        )

    bpy.types.Object.exportDeformOnly = BoolProperty(
        name="Export only deform Bones",
        description=(
            "Only write deforming bones" +
            " (and non-deforming ones when they have deforming children)"
            ),
        default=True
        )

    def draw(self, context):

        layout = self.layout
        obj = context.object
        addon_prefs = bpy.context.preferences.addons[__package__].preferences

        if obj is not None:

            AssetType = layout.row()
            AssetType.prop(obj, 'name', text="", icon='OBJECT_DATA')
            # Show asset type
            AssetType.label(text='('+GetAssetType(obj)+')')

            ExportType = layout.column()
            ExportType.prop(obj, 'ExportEnum')

            if obj.ExportEnum == "export_recursive":

                row = self.layout.row(align=True)
                row.menu(
                    'BFUO_MT_ObjectGlobalPropertiesPresets',
                    text='Global Properties Presets'
                    )
                row.operator(
                    'bfuo.add_globalproperties_preset',
                    text='',
                    icon='ADD'
                    )
                row.operator(
                    'bfuo.add_globalproperties_preset',
                    text='',
                    icon='REMOVE'
                    ).remove_active = True

                folderNameProperty = layout.column()
                folderNameProperty.prop(
                    obj,
                    'exportFolderName',
                    icon='FILE_FOLDER'
                    )

                if obj.type != "CAMERA":
                    ProxyProp = layout.column()
                    ProxyProp.prop(obj, 'ExportAsProxy')
                    if obj.ExportAsProxy:
                        ProxyProp.prop(obj, 'ExportProxyChild')

                    export_procedure_prop = layout.column()
                    export_procedure_prop.prop(obj, 'bfu_export_procedure')

                    if not obj.ExportAsProxy:
                        AlembicProp = layout.column()
                        AlembicProp.prop(obj, 'ExportAsAlembic')
                        if obj.ExportAsAlembic:
                            AlembicProp.label(
                                text="(Alembic animation are exported" +
                                " with scene position.)"
                                )
                            AlembicProp.label(
                                text="(Use import script for" +
                                " use the origin position.)"
                                )
                        else:
                            if addon_prefs.useGeneratedScripts:
                                LodProp = layout.column()
                                LodProp.prop(obj, 'ExportAsLod')

                            if obj.type == "ARMATURE":
                                AssetType2 = layout.column()
                                # Show asset type
                                AssetType2.prop(obj, "ForceStaticMesh")
                                if GetAssetType(obj) == "SkeletalMesh":
                                    AssetType2.prop(obj, 'exportDeformOnly')

        else:
            layout.label(text='(No properties to show.)')


class BFUO_PT_ObjectImportProperties(bpy.types.Panel):
    # Is Object Properties panel

    bl_idname = "BFUO_PT_ObjectImportProperties"
    bl_label = "Object Import Properties"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Unreal Engine 4 Old"
    bl_parent_id = "BFUO_PT_BlenderForUnrealObject"

    # Lod list
    bpy.types.Object.Ue4Lod1 = PointerProperty(
        name="LOD1",
        description="Target objet for level of detail 01",
        type=bpy.types.Object
        )

    bpy.types.Object.Ue4Lod2 = PointerProperty(
        name="LOD2",
        description="Target objet for level of detail 02",
        type=bpy.types.Object
        )

    bpy.types.Object.Ue4Lod3 = PointerProperty(
        name="LOD3",
        description="Target objet for level of detail 03",
        type=bpy.types.Object
        )

    bpy.types.Object.Ue4Lod4 = PointerProperty(
        name="LOD4",
        description="Target objet for level of detail 04",
        type=bpy.types.Object
        )

    bpy.types.Object.Ue4Lod5 = PointerProperty(
        name="LOD5",
        description="Target objet for level of detail 05",
        type=bpy.types.Object
        )

    # ImportUI
    # https://api.unrealengine.com/INT/API/Editor/UnrealEd/Factories/UFbxImportUI/index.html

    bpy.types.Object.CreatePhysicsAsset = BoolProperty(
        name="Create PhysicsAsset",
        description="If checked, create a PhysicsAsset when is imported",
        default=True
        )

    bpy.types.Object.UseTargetCustomSkeletonName = BoolProperty(
        name="Skeleton name in Unreal",
        description=(
            "Addon will use armature name" +
            " for found skeleton in Unreal." +
            " If you use a proxy you need set name manually."),
        default=False
        )

    bpy.types.Object.TargetCustomSkeletonName = StringProperty(
        name="",
        description="The name of the Skeleton in Unreal",
        default="SK_MySketonName_Skeleton"
        )


    # StaticMeshImportData
    # https://api.unrealengine.com/INT/API/Editor/UnrealEd/Factories/UFbxStaticMeshImportData/index.html

    bpy.types.Object.UseStaticMeshLODGroup = BoolProperty(
        name="",
        description='',
        default=False
        )

    bpy.types.Object.StaticMeshLODGroup = StringProperty(
        name="LOD Group",
        description=(
            "The LODGroup to associate with this mesh when it is imported." +
            " Default: LevelArchitecture, SmallProp, " +
            "LargeProp, Deco, Vista, Foliage, HighDetail"
            ),
        maxlen=32,
        default="SmallProp"
        )

    bpy.types.Object.StaticMeshLightMapEnum = EnumProperty(
        name="Light map",
        description='Specify how the light map resolution will be generated',
        items=[
            ("Default",
                "Default",
                "Has no effect on light maps",
                1),
            ("CustomMap",
                "Custom map",
                "Set the custom light map resolution",
                2),
            ("SurfaceArea",
                "surface Area",
                "Set light map resolution depending on the surface Area",
                3)
            ]
        )

    bpy.types.Object.customStaticMeshLightMapRes = IntProperty(
        name="Light Map resolution",
        description="This is the resolution of the light map",
        soft_max=2048,
        soft_min=16,
        max=4096,  # Max for unreal
        min=4,  # Min for unreal
        default=64
        )

    bpy.types.Object.computedStaticMeshLightMapRes = FloatProperty(
        name="computed Light Map resolution",
        description="This is the computed resolution of the light map",
        default=64.0
        )

    bpy.types.Object.staticMeshLightMapSurfaceScale = FloatProperty(
        name="Surface scale",
        description="This is for resacle the surface Area value",
        min=0.00001,  # Min for unreal
        default=64
        )

    bpy.types.Object.staticMeshLightMapRoundPowerOfTwo = BoolProperty(
        name="Round power of 2",
        description=(
            "round Light Map resolution to nearest power of 2"
            ),
        default=True
        )

    bpy.types.Object.useStaticMeshLightMapWorldScale = BoolProperty(
        name="Use world scale",
        description=(
            "If not that will use the object scale."
            ),
        default=True
        )

    bpy.types.Object.GenerateLightmapUVs = BoolProperty(
        name="Generate LightmapUVs",
        description=(
            "If checked, UVs for Lightmap will automatically be generated."
            ),
        default=True,
        )

    bpy.types.Object.AutoGenerateCollision = BoolProperty(
        name="Auto Generate Collision",
        description=(
            "If checked, collision will automatically be generated" +
            " (ignored if custom collision is imported or used)."
            ),
        default=True,
        )

    # SkeletalMeshImportData:
    # https://api.unrealengine.com/INT/API/Editor/UnrealEd/Factories/UFbxSkeletalMeshImportData/index.html

    # UFbxTextureImportData:
    # https://api.unrealengine.com/INT/API/Editor/UnrealEd/Factories/UFbxTextureImportData/index.html

    bpy.types.Object.MaterialSearchLocation = EnumProperty(
        name="Material search location",
        description=(
            "Specify where we should search" +
            " for matching materials when importing"
            ),
        # Vania python:
        # https://docs.unrealengine.com/en-US/PythonAPI/class/MaterialSearchLocation.html?highlight=materialsearchlocation
        # C++ API:
        # http://api.unrealengine.com/INT/API/Editor/UnrealEd/Factories/EMaterialSearchLocation/index.html
        items=[
            ("Local",
                "Local",
                "Search for matching material in local import folder only.",
                1),
            ("UnderParent",
                "Under parent",
                "Search for matching material recursively from parent folder.",
                2),
            ("UnderRoot",
                "Under root",
                "Search for matching material recursively from root folder.",
                3),
            ("AllAssets",
                "All assets",
                "Search for matching material in all assets folders.",
                4)
            ]
        )

    bpy.types.Object.CollisionTraceFlag = EnumProperty(
        name="Collision Complexity",
        description="Collision Trace Flag",
        # Vania python
        # https://docs.unrealengine.com/en-US/PythonAPI/class/CollisionTraceFlag.html
        # C++ API
        # https://api.unrealengine.com/INT/API/Runtime/Engine/PhysicsEngine/ECollisionTraceFlag/index.html
        items=[
            ("CTF_UseDefault",
                "Project Default",
                "Create only complex shapes (per poly)." +
                " Use complex shapes for all scene queries" +
                " and collision tests." +
                " Can be used in simulation for" +
                " static shapes only" +
                " (i.e can be collided against but not moved" +
                " through forces or velocity.",
                1),
            ("CTF_UseSimpleAndComplex",
                "Use Simple And Complex",
                "Use project physics settings (DefaultShapeComplexity)",
                2),
            ("CTF_UseSimpleAsComplex",
                "Use Simple as Complex",
                "Create both simple and complex shapes." +
                " Simple shapes are used for regular scene queries" +
                " and collision tests. Complex shape (per poly)" +
                " is used for complex scene queries.",
                3),
            ("CTF_UseComplexAsSimple",
                "Use Complex as Simple",
                "Create only simple shapes." +
                " Use simple shapes for all scene" +
                " queries and collision tests.",
                4)
            ]
        )

    bpy.types.Object.VertexColorImportOption = EnumProperty(
        name="Vertex Color Import Option",
        description="Specify how vertex colors should be imported",
        # Vania python
        # https://docs.unrealengine.com/en-US/PythonAPI/class/VertexColorImportOption.html
        # C++ API
        # https://docs.unrealengine.com/en-US/API/Editor/UnrealEd/Factories/EVertexColorImportOption__Type/index.html
        items=[
            ("VCIO_Ignore",
                "Ignore",
                "Ignore vertex colors from the FBX file," +
                " and keep the existing mesh vertex colors.",
                1),
            ("VCIO_Replace",
                "Replace",
                "Import the static mesh using the" +
                " vertex colors from the FBX file.",
                2)
            ]
        )

    class BFUO_OT_ComputLightMap(Operator):
        bl_label = "Calculate surface area"
        bl_idname = "bfuo.computlightmap"
        bl_description = "Click to calculate the surface of the object"

        def execute(self, context):
            obj = context.object
            obj.computedStaticMeshLightMapRes = GetExportRealSurfaceArea(obj)
            self.report(
                {'INFO'},
                "Light map area updated to " +
                str(round(obj.computedStaticMeshLightMapRes)) + ".")
            return {'FINISHED'}

    class BFUO_OT_ComputAllLightMap(Operator):
        bl_label = "Calculate all surface area"
        bl_idname = "bfuo.computalllightmap"
        bl_description = (
            "Click to calculate the surface of the all object in the scene"
            )

        def execute(self, context):
            updated = UpdateAreaLightMapList()
            self.report(
                {'INFO'},
                "The light maps of " + str(updated) +
                " object(s) have been updated."
                )
            return {'FINISHED'}

    def draw(self, context):

        layout = self.layout
        obj = context.object
        addon_prefs = bpy.context.preferences.addons[__package__].preferences

        if addon_prefs.useGeneratedScripts and obj is not None:
            if obj.ExportEnum == "export_recursive":

                # Lod selection
                if not obj.ExportAsLod:
                    if (GetAssetType(obj) == "StaticMesh" or
                            GetAssetType(obj) == "SkeletalMesh"):
                        LodList = layout.column()
                        LodList.prop(obj, 'Ue4Lod1')
                        LodList.prop(obj, 'Ue4Lod2')
                        LodList.prop(obj, 'Ue4Lod3')
                        LodList.prop(obj, 'Ue4Lod4')
                        LodList.prop(obj, 'Ue4Lod5')

                # MaterialSearchLocation
                if not obj.ExportAsLod:
                    if (GetAssetType(obj) == "StaticMesh" or
                            GetAssetType(obj) == "SkeletalMesh" or
                            GetAssetType(obj) == "Alembic"):
                        MaterialSearchLocation = layout.row()
                        MaterialSearchLocation.prop(
                            obj, 'MaterialSearchLocation')

                # StaticMesh prop
                if GetAssetType(obj) == "StaticMesh":
                    if not obj.ExportAsLod:
                        StaticMeshLODGroup = layout.row()
                        StaticMeshLODGroup.prop(
                            obj,
                            'UseStaticMeshLODGroup',
                            text="")
                        SMLODGroupChild = StaticMeshLODGroup.column()
                        SMLODGroupChild.enabled = obj.UseStaticMeshLODGroup
                        SMLODGroupChild.prop(
                            obj,
                            'StaticMeshLODGroup'
                            )

                    StaticMeshCollisionTraceFlag = layout.row()
                    StaticMeshCollisionTraceFlag.prop(
                        obj,
                        'CollisionTraceFlag'
                        )

                    StaticMeshVertexColorImportOption = layout.row()
                    StaticMeshVertexColorImportOption.prop(
                        obj,
                        'VertexColorImportOption'
                        )

                    StaticMeshLightMapRes = layout.box()
                    StaticMeshLightMapRes.prop(obj, 'StaticMeshLightMapEnum')
                    if obj.StaticMeshLightMapEnum == "CustomMap":
                        CustomLightMap = StaticMeshLightMapRes.column()
                        CustomLightMap.prop(obj, 'customStaticMeshLightMapRes')
                    if obj.StaticMeshLightMapEnum == "SurfaceArea":
                        SurfaceAreaLightMap = StaticMeshLightMapRes.column()
                        SurfaceAreaLightMap.operator(
                            "bfuo.computlightmap",
                            icon='TEXTURE'
                            )
                        SurfaceAreaLightMap.operator(
                            "bfuo.computalllightmap",
                            icon='TEXTURE'
                            )
                        SurfaceAreaLightMap.prop(
                            obj,
                            'useStaticMeshLightMapWorldScale'
                            )
                        SurfaceAreaLightMap.prop(
                            obj,
                            'staticMeshLightMapSurfaceScale'
                            )
                        SurfaceAreaLightMap.prop(
                            obj,
                            'staticMeshLightMapRoundPowerOfTwo'
                            )
                    StaticMeshLightMapRes.label(
                        text='Compunted light map: ' +
                        str(GetCompuntedLightMap(obj))
                        )

                    GenerateLightmapUVs = layout.row()
                    GenerateLightmapUVs.prop(obj, 'GenerateLightmapUVs')

                    if not obj.ExportAsLod:
                        AutoGenerateCollision = layout.row()
                        AutoGenerateCollision.prop(
                            obj,
                            'AutoGenerateCollision'
                            )

                # SkeletalMesh prop
                if GetAssetType(obj) == "SkeletalMesh":
                    if not obj.ExportAsLod:
                        CreatePhysicsAsset = layout.row()
                        CreatePhysicsAsset.prop(obj, "CreatePhysicsAsset")

                        Ue4Skeleton = layout.row()
                        Ue4Skeleton.prop(obj, "UseTargetCustomSkeletonName")
                        useSkeleton = obj.UseTargetCustomSkeletonName
                        Ue4SkeletonText = Ue4Skeleton.column()
                        Ue4SkeletonText.prop(obj, "TargetCustomSkeletonName")
                        Ue4SkeletonText.enabled = useSkeleton

            else:
                layout.label(text='(No properties to show.)')
        else:
            layout.label(text='(Generated scripts are deactivated.)')


class BFUO_OT_ObjExportAction(bpy.types.PropertyGroup):
    name: StringProperty(name="Action data name", default="Unknown")
    use: BoolProperty(name="use this action", default=False)


class BFUO_PT_AnimProperties(bpy.types.Panel):
    # Is Animation Properties panel

    bl_idname = "BFUO_PT_AnimProperties"
    bl_label = "Animation Properties"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Unreal Engine 4 Old"
    bl_parent_id = "BFUO_PT_BlenderForUnrealObject"

    # Animation :

    class BFUO_UL_ActionExportTarget(bpy.types.UIList):
        def draw_item(
                self,
                context,
                layout,
                data,
                item,
                icon,
                active_data,
                active_propname
                ):
            ActionIsValid = False
            if item.name in bpy.data.actions:
                bpy.data.actions[item.name]
                ActionIsValid = True

            if self.layout_type in {'DEFAULT', 'COMPACT'}:
                if ActionIsValid:  # If action is valid
                    layout.prop(
                        bpy.data.actions[item.name],
                        "name",
                        text="",
                        emboss=False,
                        icon="ACTION"
                        )
                    layout.prop(item, "use", text="")
                else:
                    dataText = (
                        'Action data named "' + item.name +
                        '" Not Found. Please clic on update'
                        )
                    layout.label(text=dataText, icon="ERROR")
            # Not optimised for 'GRID' layout type.
            elif self.layout_type in {'GRID'}:
                layout.alignment = 'CENTER'
                layout.label(text="", icon_value=icon)

    bpy.types.Object.exportActionEnum = EnumProperty(
        name="Action to export",
        description="Export procedure for actions (Animations and poses)",
        items=[
            ("export_auto",
                "Export auto",
                "Export all actions connected to the bones names",
                "FILE_SCRIPT",
                1),
            ("export_specific_list",
                "Export specific list",
                "Export only actions that are checked in the list",
                "LINENUMBERS_ON",
                3),
            ("export_specific_prefix",
                "Export specific prefix",
                "Export only actions with a specific prefix" +
                " or the beginning of the actions names",
                "SYNTAX_ON",
                4),
            ("dont_export",
                "Not exported",
                "No action will be exported",
                "MATPLANE",
                5),
            ("export_current",
                "Export Current",
                "Export only the current actions",
                "FILE_SCRIPT",
                6),
            ]
        )

    bpy.types.Object.active_ObjectAction = IntProperty(
        name="Active Scene Action",
        description="Index of the currently active object action",
        default=0
        )

    bpy.types.Object.PrefixNameToExport = StringProperty(
        # properties used with ""export_specific_prefix" on exportActionEnum
        name="Prefix name",
        description="Indicate the prefix of the actions that must be exported",
        maxlen=32,
        default="Example_",
        )

    bpy.types.Object.AnimStartEndTimeEnum = EnumProperty(
        name="Animation start/end time",
        description="Set when animation starts and end",
        items=[
            ("with_keyframes",
                "Auto",
                "The time will be defined according" +
                " to the first and the last frame",
                "KEYTYPE_KEYFRAME_VEC",
                1),
            ("with_sceneframes",
                "Scene time",
                "Time will be equal to the scene time",
                "SCENE_DATA",
                2),
            ("with_customframes",
                "Custom time",
                'The time of all the animations of this object' +
                ' is defined by you.' +
                ' Use "AnimCustomStartTime" and "AnimCustomEndTime"',
                "HAND",
                3),
            ]
        )

    bpy.types.Object.StartFramesOffset = IntProperty(
        name="Offset at start frame",
        description="Offset for the start frame.",
        default=1
    )

    bpy.types.Object.EndFramesOffset = IntProperty(
        name="Offset at end frame",
        description=(
            "Offset for the end frame. +1" +
            " is recommended for the sequences, 0 is recommended" +
            " for UnrealEngine cycles, -1 is recommended for Sketchfab cycles"
            ),
        default=0
    )

    bpy.types.Object.AnimCustomStartTime = IntProperty(
        name="Custom start time",
        description="Set when animation start",
        default=0
        )

    bpy.types.Object.AnimCustomEndTime = IntProperty(
        name="Custom end time",
        description="Set when animation end",
        default=1
        )

    bpy.types.Object.SampleAnimForExport = FloatProperty(
        name="Sampling Rate",
        description="How often to evaluate animated values (in frames)",
        min=0.01, max=100.0,
        soft_min=0.01, soft_max=100.0,
        default=1.0,
        )

    bpy.types.Object.SimplifyAnimForExport = FloatProperty(
        name="Simplify animations",
        description=(
            "How much to simplify baked values" +
            " (0.0 to disable, the higher the more simplified)"
            ),
        # No simplification to up to 10% of current magnitude tolerance.
        min=0.0, max=100.0,
        soft_min=0.0, soft_max=10.0,
        default=0.0,
        )

    bpy.types.Object.ExportNLA = BoolProperty(
        name="Export NLA (Nonlinear Animation)",
        description=(
            "If checked, exports the all animation of the scene with the NLA"
            ),
        default=False
        )

    bpy.types.Object.NLAAnimName = StringProperty(
        name="NLA export name",
        description='Export NLA name',
        maxlen=64,
        default="NLA_animation",
        subtype='FILE_NAME'
        )

    bpy.types.Object.bfu_anim_naming_type = EnumProperty(
        name="Naming type",
        items=[
            ('action_name', "Action name", 'Exemple: "Anim_MyAction"'),
            ('include_armature_name',
                "Include Armature Name",
                'Include armature name in animation export file name.' +
                ' Exemple: "Anim_MyArmature_MyAction"'),
            ('include_custom_name', 
                "Include custom name", 
                'Include custom name in animation export file name.' +
                ' Exemple: "Anim_MyCustomName_MyAction"'),
            ],
        default='include_armature_name'
        )

    bpy.types.Object.bfu_anim_naming_custom = StringProperty(
        name="Export name",
        default='MyCustomName'
        )

    class BFUO_OT_UpdateObjActionListButton(Operator):
        bl_label = "Update action list"
        bl_idname = "bfuo.updateobjactionlist"
        bl_description = "Update action list"

        def execute(self, context):
            def UpdateExportActionList(obj):
                # Update the provisional action list known by the object

                def SetUseFromLast(list, ActionName):
                    for item in list:
                        if item[0] == ActionName:
                            if item[1]:
                                return True
                    return False

                animSave = [["", False]]
                for Anim in obj.exportActionList:  # CollectionProperty
                    name = Anim.name
                    use = Anim.use
                    animSave.append([name, use])
                obj.exportActionList.clear()
                for action in bpy.data.actions:
                    obj.exportActionList.add().name = action.name
                    useFromLast = SetUseFromLast(animSave, action.name)
                    obj.exportActionList[action.name].use = useFromLast
            UpdateExportActionList(bpy.context.object)
            return {'FINISHED'}

    class BFUO_OT_SelectAllActionsButton(Operator):
        bl_label = "Select All"
        bl_idname = "bfuo.selectallactions"
        bl_description = "Select all actions"

        def execute(self, context):
            for Anim in context.object.exportActionList:  # CollectionProperty
                Anim.use = True
            return {'FINISHED'}

    class BFUO_OT_DeselectAllActionsButton(Operator):
        bl_label = "Deselect All"
        bl_idname = "bfuo.deselectallactions"
        bl_description = "Deselect all actions"

        def execute(self, context):
            for Anim in context.object.exportActionList:  # CollectionProperty
                Anim.use = False
            return {'FINISHED'}

    class BFUO_OT_ShowActionToExport(Operator):
        bl_label = "Show action(s)"
        bl_idname = "bfuo.showobjaction"
        bl_description = (
            "Click to show actions that are" +
            " to be exported with this armature."
            )

        def execute(self, context):
            obj = context.object
            animation_to_export = GetActionToExport(obj)

            popup_title = "Action list"
            if len(animation_to_export) > 0:
                animationNumber = len(animation_to_export)
                if obj.ExportNLA:
                    animationNumber += 1
                popup_title = (
                    str(animationNumber) +
                    ' animation(s) found for obj named "'+obj.name+'".'
                    )
            else:
                popup_title = (
                    'No animation found for obj named "' +
                    obj.name+'".')

            def draw(self, context):
                col = self.layout.column()

                def addAnimRow(
                        action_name,
                        action_type,
                        frame_start,
                        frame_end):
                    row = col.row()
                    row.label(
                        text="- ["+action_name +
                        "] Frame "+frame_start+" to "+frame_end +
                        " ("+action_type+")"
                        )

                for action in animation_to_export:
                    Frames = GetDesiredActionStartEndTime(obj, action)
                    frame_start = str(Frames[0])
                    frame_end = str(Frames[1])
                    addAnimRow(
                        action.name,
                        GetActionType(action),
                        frame_start,
                        frame_end)
                if obj.ExportNLA:
                    scene = context.scene
                    addAnimRow(
                        obj.NLAAnimName,
                        "NlAnim",
                        str(scene.frame_start + obj.StartFramesOffset),
                        str(scene.frame_end + obj.EndFramesOffset)
                        )

            bpy.context.window_manager.popup_menu(
                draw,
                title=popup_title,
                icon='ACTION'
                )
            return {'FINISHED'}

    def draw(self, context):

        layout = self.layout
        obj = context.object
        if obj is not None:
            if obj.ExportEnum == "export_recursive" and not obj.ExportAsLod:
                if (GetAssetType(obj) == "SkeletalMesh" or
                        GetAssetType(obj) == "Camera" or
                        GetAssetType(obj) == "Alembic"):

                    # Action time
                    if obj.type != "CAMERA":
                        ActionTimeProperty = layout.column()
                        ActionTimeProperty.prop(obj, 'AnimStartEndTimeEnum')
                        if obj.AnimStartEndTimeEnum == "with_customframes":
                            OfsetTime = ActionTimeProperty.row()
                            OfsetTime.prop(obj, 'AnimCustomStartTime')
                            OfsetTime.prop(obj, 'AnimCustomEndTime')
                        if obj.AnimStartEndTimeEnum != "with_customframes":
                            OfsetTime = ActionTimeProperty.row()
                            OfsetTime.prop(obj, 'StartFramesOffset')
                            OfsetTime.prop(obj, 'EndFramesOffset')

                    else:
                        layout.label(
                            text=(
                                "Note: animation start/end use scene frames" +
                                " with the camera for the sequencer.")
                            )

                    if GetAssetType(obj) == "SkeletalMesh":
                        # Action list
                        ActionListProperty = layout.column()
                        ActionListProperty.prop(obj, 'exportActionEnum')
                        if obj.exportActionEnum == "export_specific_list":
                            ActionListProperty.template_list(
                                # type and unique id
                                "BFUO_UL_ActionExportTarget", "",
                                # pointer to the CollectionProperty
                                obj, "exportActionList",
                                # pointer to the active identifier
                                obj, "active_ObjectAction",
                                maxrows=5,
                                rows=5
                            )
                            ActionListProperty.operator(
                                "bfuo.updateobjactionlist",
                                icon='RECOVER_LAST')
                            ActionSelectionButtons = layout.row()
                            ActionSelectionButtons.operator("bfuo.selectallactions")
                            ActionSelectionButtons.operator("bfuo.deselectallactions")
                        if obj.exportActionEnum == "export_specific_prefix":
                            ActionListProperty.prop(obj, 'PrefixNameToExport')

                    # NLA
                    if GetAssetType(obj) == "SkeletalMesh":
                        NLAAnim = layout.row()
                        NLAAnim.prop(obj, 'ExportNLA')
                        NLAAnimChild = NLAAnim.column()
                        NLAAnimChild.enabled = obj.ExportNLA
                        NLAAnimChild.prop(obj, 'NLAAnimName')

                    # Animation fbx properties
                    if (GetAssetType(obj) != "Alembic"):
                        propsFbx = layout.row()
                        propsFbx.prop(obj, 'SampleAnimForExport')
                        propsFbx.prop(obj, 'SimplifyAnimForExport')

                    # Nomenclature
                    if GetAssetType(obj) == "SkeletalMesh":
                        export_anim_naming = layout.column()
                        export_anim_naming.prop(obj, 'bfu_anim_naming_type')
                        if obj.bfu_anim_naming_type == "include_custom_name":
                            export_anim_naming_text = export_anim_naming.column()
                            export_anim_naming_text.prop(obj, 'bfu_anim_naming_custom')

                    # Armature export action list feedback
                    if GetAssetType(obj) == "SkeletalMesh":
                        layout.label(
                            text='Note: The Action with only one' +
                            ' frame are exported like Pose.')
                        ArmaturePropertyInfo = (
                            layout.row().box().split(factor=0.75)
                            )
                        ActionNum = len(GetActionToExport(obj))
                        if obj.ExportNLA:
                            ActionNum += 1
                        actionFeedback = (
                            str(ActionNum) +
                            " Animation(s) will be exported with this object.")
                        ArmaturePropertyInfo.label(
                            text=actionFeedback,
                            icon='INFO')
                        ArmaturePropertyInfo.operator("bfuo.showobjaction")

                else:
                    layout.label(
                        text='(This assets is not a SkeletalMesh or Camera)')
            else:
                layout.label(text='(No properties to show.)')
        else:
            layout.label(text='(No properties to show.)')


class BFUO_OT_SceneCollectionExport(bpy.types.PropertyGroup):
    name: StringProperty(name="collection data name", default="Unknown")
    use: BoolProperty(name="export this collection", default=False)


class BFUO_PT_CollectionProperties(bpy.types.Panel):
    # Is Collection Properties panel

    bl_idname = "BFUO_PT_CollectionProperties"
    bl_label = "Collection Properties panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Unreal Engine 4 Old"
    bl_parent_id = "BFUO_PT_BlenderForUnreal"

    class BFUO_UL_CollectionExportTarget(bpy.types.UIList):
        def draw_item(
                self,
                context,
                layout,
                data,
                item,
                icon,
                active_data,
                active_propname
                ):

            CollectionIsValid = False
            if item.name in bpy.data.collections:
                bpy.data.collections[item.name]
                CollectionIsValid = True

            if self.layout_type in {'DEFAULT', 'COMPACT'}:
                if CollectionIsValid:  # If action is valid
                    layout.prop(
                        bpy.data.collections[item.name],
                        "name",
                        text="",
                        emboss=False,
                        icon="GROUP")
                    layout.prop(item, "use", text="")
                else:
                    dataText = (
                        'Collection named "' +
                        item.name +
                        '" Not Found. Please clic on update')
                    layout.label(text=dataText, icon="ERROR")
            # Not optimised for 'GRID' layout type.
            elif self.layout_type in {'GRID'}:
                layout.alignment = 'CENTER'
                layout.label(text="", icon_value=icon)

    class BFUO_OT_UpdateCollectionButton(Operator):
        bl_label = "Update collection list"
        bl_idname = "bfuo.updatecollectionlist"
        bl_description = "Update collection list"

        def execute(self, context):
            def UpdateExportCollectionList(scn):
                # Update the provisional collection list known by the object

                def SetUseFromLast(list, CollectionName):
                    for item in list:
                        if item[0] == CollectionName:
                            if item[1]:
                                return True
                    return False

                colSave = [["", False]]
                for col in scn.CollectionExportList:  # CollectionProperty
                    name = col.name
                    use = col.use
                    colSave.append([name, use])
                scn.CollectionExportList.clear()
                for col in bpy.data.collections:
                    scn.CollectionExportList.add().name = col.name
                    useFromLast = SetUseFromLast(colSave, col.name)
                    scn.CollectionExportList[col.name].use = useFromLast
            UpdateExportCollectionList(context.scene)
            return {'FINISHED'}

    class BFUO_OT_ShowCollectionToExport(Operator):
        bl_label = "Show action(s)"
        bl_idname = "bfuo.showscenecollection"
        bl_description = "Click to show collections to export"

        def execute(self, context):
            scn = context.scene
            collections = GetCollectionToExport(scn)
            popup_title = "Collection list"
            if len(collections) > 0:
                popup_title = (
                    str(len(collections))+' collection(s) to export found.')
            else:
                popup_title = 'No collection to export found.'

            def draw(self, context):
                col = self.layout.column()
                for collection in collections:
                    row = col.row()
                    row.label(text="- "+collection)
            bpy.context.window_manager.popup_menu(
                draw,
                title=popup_title,
                icon='GROUP')
            return {'FINISHED'}

    bpy.types.Scene.active_CollectionExportList = IntProperty(
        name="Active Collection",
        description="Index of the currently active collection",
        default=0
        )

    def draw(self, context):
        scn = context.scene
        layout = self.layout
        collectionListProperty = layout.column()
        collectionListProperty.template_list(
            # type and unique id
            "BFUO_UL_CollectionExportTarget", "",
            # pointer to the CollectionProperty
            scn, "CollectionExportList",
            # pointer to the active identifier
            scn, "active_CollectionExportList",
            maxrows=5,
            rows=5
        )
        collectionListProperty.operator(
            "bfuo.updatecollectionlist",
            icon='RECOVER_LAST')

        collectionPropertyInfo = layout.row().box().split(factor=0.75)
        collectionNum = len(GetCollectionToExport(scn))
        collectionFeedback = (
            str(collectionNum) +
            " Collection(s) will be exported with this armature.")
        collectionPropertyInfo.label(text=collectionFeedback, icon='INFO')
        collectionPropertyInfo.operator("bfuo.showscenecollection")
        layout.label(text='Note: The collection are exported like StaticMesh.')


class BFUO_PT_AvancedObjectProperties(bpy.types.Panel):
    # Is Avanced object properties panel

    bl_idname = "BFUO_PT_AvancedObjectProperties"
    bl_label = "Avanced object properties panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Unreal Engine 4 Old"
    bl_parent_id = "BFUO_PT_BlenderForUnrealObject"

    bpy.types.Object.exportGlobalScale = FloatProperty(
        name="Global scale",
        description="Scale, change is not recommended with SkeletalMesh.",
        default=1.0
        )

    bpy.types.Object.exportAxisForward = EnumProperty(
        name="Axis Forward",
        items=[
            ('X', "X Forward", ""),
            ('Y', "Y Forward", ""),
            ('Z', "Z Forward", ""),
            ('-X', "-X Forward", ""),
            ('-Y', "-Y Forward", ""),
            ('-Z', "-Z Forward", ""),
            ],
        default='-Z',
        )

    bpy.types.Object.exportAxisUp = EnumProperty(
        name="Axis Up",
        items=[
            ('X', "X Up", ""),
            ('Y', "Y Up", ""),
            ('Z', "Z Up", ""),
            ('-X', "-X Up", ""),
            ('-Y', "-Y Up", ""),
            ('-Z', "-Z Up", ""),
            ],
        default='Y',
        )

    bpy.types.Object.exportPrimaryBoneAxis = EnumProperty(
        name="Primary Axis Bone",
        items=[
            ('X', "X", ""),
            ('Y', "Y", ""),
            ('Z', "Z", ""),
            ('-X', "-X", ""),
            ('-Y', "-Y", ""),
            ('-Z', "-Z", ""),
            ],
        default='X',
        )

    bpy.types.Object.exporSecondaryBoneAxis = EnumProperty(
        name="Secondary Axis Bone",
        items=[
            ('X', "X", ""),
            ('Y', "Y", ""),
            ('Z', "Z", ""),
            ('-X', "-X", ""),
            ('-Y', "-Y", ""),
            ('-Z', "-Z", ""),
            ],
        default='-Z',
        )

    bpy.types.Object.MoveToCenterForExport = BoolProperty(
        name="Move to center",
        description=(
            "If true use object origin else use scene origin." +
            " | If true the mesh will be moved to the center" +
            " of the scene for export." +
            " (This is used so that the origin of the fbx file" +
            " is the same as the mesh in blender)"
            ),
        default=True
        )

    bpy.types.Object.RotateToZeroForExport = BoolProperty(
        name="Rotate to zero",
        description=(
            "If true use object rotation else use scene rotation." +
            " | If true the mesh will use zero rotation for export."
            ),
        default=False
        )

    bpy.types.Object.AdditionalLocationForExport = FloatVectorProperty(
        name="Additional location",
        description=(
            "This will add a additional absolute rotation to the mesh"
            ),
        subtype="TRANSLATION",
        default=(0, 0, 0)
        )

    bpy.types.Object.AdditionalRotationForExport = FloatVectorProperty(
        name="Additional rotation",
        description=(
            "This will add a additional absolute rotation to the mesh"
            ),
        subtype="EULER",
        default=(0, 0, 0)
        )

    def draw(self, context):
        scn = context.scene
        layout = self.layout
        obj = context.object
        if obj is not None:
            if obj.ExportEnum == "export_recursive":

                transformProp = layout.column()
                if GetAssetType(obj) != "Alembic":
                    transformProp.prop(obj, "MoveToCenterForExport")
                    transformProp.prop(obj, "RotateToZeroForExport")
                    transformProp.prop(obj, "AdditionalLocationForExport")
                    transformProp.prop(obj, "AdditionalRotationForExport")
                    transformProp.prop(obj, 'exportGlobalScale')

                AxisProperty = layout.column()
                AxisProperty.prop(obj, 'exportAxisForward')
                AxisProperty.prop(obj, 'exportAxisUp')
                if GetAssetType(obj) == "SkeletalMesh":
                    BoneAxisProperty = layout.column()
                    BoneAxisProperty.prop(obj, 'exportPrimaryBoneAxis')
                    BoneAxisProperty.prop(obj, 'exporSecondaryBoneAxis')
        else:
            layout.label(text='(No properties to show.)')


class BFUO_PT_CollisionsAndSockets(bpy.types.Panel):
    # Is Collisions And Sockets panel

    bl_idname = "BFUO_PT_CollisionsAndSockets"
    bl_label = "Collisions And Sockets"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Unreal Engine 4 Old"
    bl_parent_id = "BFUO_PT_BlenderForUnreal"

    bpy.types.Object.usesocketcustomName = BoolProperty(
        name="Socket custom name",
        description='Use a custom name in Unreal Engine for this socket?',
        default=False
        )

    bpy.types.Object.socketcustomName = StringProperty(
        name="",
        description='',
        default="MySocket"
        )

    class BFUO_OT_ConvertToCollisionButtonBox(Operator):
        bl_label = "Convert to box (UBX)"
        bl_idname = "bfuo.converttoboxcollision"
        bl_description = (
            "Convert selected mesh(es) to Unreal" +
            " collision ready for export (Boxes type)")

        def execute(self, context):
            ConvertedObj = Ue4SubObj_set("Box")
            if len(ConvertedObj) > 0:
                self.report(
                    {'INFO'},
                    str(len(ConvertedObj)) +
                    " object(s) of the selection have be" +
                    " converted to UE4 Box collisions.")
            else:
                self.report(
                    {'WARNING'},
                    "Please select two objects." +
                    " (Active object is the owner of the collision)")
            return {'FINISHED'}

    class BFUO_OT_ConvertToCollisionButtonCapsule(Operator):
        bl_label = "Convert to capsule (UCP)"
        bl_idname = "bfuo.converttocapsulecollision"
        bl_description = (
            "Convert selected mesh(es) to Unreal collision" +
            " ready for export (Capsules type)")

        def execute(self, context):
            ConvertedObj = Ue4SubObj_set("Capsule")
            if len(ConvertedObj) > 0:
                self.report(
                    {'INFO'},
                    str(len(ConvertedObj)) +
                    " object(s) of the selection have be converted" +
                    " to UE4 Capsule collisions.")
            else:
                self.report(
                    {'WARNING'},
                    "Please select two objects." +
                    " (Active object is the owner of the collision)")
            return {'FINISHED'}

    class BFUO_OT_ConvertToCollisionButtonSphere(Operator):
        bl_label = "Convert to sphere (USP)"
        bl_idname = "bfuo.converttospherecollision"
        bl_description = (
            "Convert selected mesh(es)" +
            " to Unreal collision ready for export (Spheres type)")

        def execute(self, context):
            ConvertedObj = Ue4SubObj_set("Sphere")
            if len(ConvertedObj) > 0:
                self.report(
                    {'INFO'},
                    str(len(ConvertedObj)) +
                    " object(s) of the selection have" +
                    " be converted to UE4 Sphere collisions.")
            else:
                self.report(
                    {'WARNING'},
                    "Please select two objects." +
                    " (Active object is the owner of the collision)")
            return {'FINISHED'}

    class BFUO_OT_ConvertToCollisionButtonConvex(Operator):
        bl_label = "Convert to convex shape (UCX)"
        bl_idname = "bfuo.converttoconvexcollision"
        bl_description = (
            "Convert selected mesh(es) to Unreal" +
            " collision ready for export (Convex shapes type)")

        def execute(self, context):
            ConvertedObj = Ue4SubObj_set("Convex")
            if len(ConvertedObj) > 0:
                self.report(
                    {'INFO'},
                    str(len(ConvertedObj)) +
                    " object(s) of the selection have be" +
                    " converted to UE4 Convex Shape collisions.")
            else:
                self.report(
                    {'WARNING'},
                    "Please select two objects." +
                    " (Active object is the owner of the collision)")
            return {'FINISHED'}

    class BFUO_OT_ConvertToStaticSocketButton(Operator):
        bl_label = "Convert to StaticMesh socket"
        bl_idname = "bfuo.converttostaticsocket"
        bl_description = (
            "Convert selected Empty(s) to Unreal sockets" +
            " ready for export (StaticMesh)")

        def execute(self, context):
            ConvertedObj = Ue4SubObj_set("ST_Socket")
            if len(ConvertedObj) > 0:
                self.report(
                    {'INFO'},
                    str(len(ConvertedObj)) +
                    " object(s) of the selection have be" +
                    " converted to to UE4 Socket.")
            else:
                self.report(
                    {'WARNING'},
                    "Please select two objects." +
                    " (Active object is the owner of the socket)")
            return {'FINISHED'}

    class BFUO_OT_ConvertToSkeletalSocketButton(Operator):
        bl_label = "Convert to SkeletalMesh socket"
        bl_idname = "bfuo.converttoskeletalsocket"
        bl_description = (
            "Convert selected Empty(s)" +
            " to Unreal sockets ready for export (SkeletalMesh)")

        def execute(self, context):
            ConvertedObj = Ue4SubObj_set("SK_Socket")
            if len(ConvertedObj) > 0:
                self.report(
                    {'INFO'},
                    str(len(ConvertedObj)) +
                    " object(s) of the selection have" +
                    " be converted to to UE4 Socket.")
            else:
                self.report(
                    {'WARNING'},
                    "Please select two objects. " +
                    "(Active object is the owner of the socket)")
            return {'FINISHED'}

    def draw(self, context):

        addon_prefs = bpy.context.preferences.addons[__package__].preferences

        def ActiveModeIs(targetMode):
            # Return True is active mode ==
            obj = bpy.context.active_object
            if obj is not None:
                if obj.mode == targetMode:
                    return True
            return False

        def ActiveTypeIs(targetType):
            # Return True is active type ==
            obj = bpy.context.active_object
            if obj is not None:
                if obj.type == targetType:
                    return True
            return False

        def FoundTypeInSelect(targetType):
            # Return True if a specific type is found
            for obj in bpy.context.selected_objects:
                if obj != bpy.context.active_object:
                    if obj.type == targetType:
                        return True
            return False

        layout = self.layout
        layout.label(
            text="Convert selected object to Unreal collision or socket",
            icon='PHYSICS')

        layout.label(
            text="Select your collider shape(s)" +
            " or Empty(s) then the owner object.")
        convertButtons = layout.row().split(factor=0.80)
        convertStaticCollisionButtons = convertButtons.column()
        if (ActiveModeIs("OBJECT") and
                ActiveTypeIs("MESH") and
                FoundTypeInSelect("MESH")):
            convertStaticCollisionButtons.enabled = True
        else:
            convertStaticCollisionButtons.enabled = False
        convertStaticCollisionButtons.operator(
            "bfuo.converttoboxcollision",
            icon='MESH_CUBE')
        convertStaticCollisionButtons.operator(
            "bfuo.converttoconvexcollision",
            icon='MESH_ICOSPHERE')
        convertStaticCollisionButtons.operator(
            "bfuo.converttocapsulecollision",
            icon='MESH_CAPSULE')
        convertStaticCollisionButtons.operator(
            "bfuo.converttospherecollision",
            icon='MESH_UVSPHERE')

        convertButtons = self.layout.row().split(factor=0.80)
        convertStaticSocketButtons = convertButtons.column()
        if (ActiveModeIs("OBJECT") and
                ActiveTypeIs("MESH") and
                FoundTypeInSelect("EMPTY")):
            convertStaticSocketButtons.enabled = True
        else:
            convertStaticSocketButtons.enabled = False
        convertStaticSocketButtons.operator(
            "bfuo.converttostaticsocket",
            icon='OUTLINER_DATA_EMPTY')

        if addon_prefs.useGeneratedScripts:
            layout.label(
                text="Select the Empty(s)" +
                " then the owner bone in PoseMode.")
            convertButtons = self.layout.row().split(factor=0.80)
            convertSkeletalSocketButtons = convertButtons.column()
            if (ActiveModeIs("POSE") and
                    ActiveTypeIs("ARMATURE") and
                    FoundTypeInSelect("EMPTY")):
                convertSkeletalSocketButtons.enabled = True
            else:
                convertSkeletalSocketButtons.enabled = False
            convertSkeletalSocketButtons.operator(
                "bfuo.converttoskeletalsocket",
                icon='OUTLINER_DATA_EMPTY')

        obj = context.object
        if obj is not None:
            if obj.type == "EMPTY":
                socketName = layout.column()
                socketName.prop(obj, "usesocketcustomName")
                socketNameText = socketName.column()
                socketNameText.enabled = obj.usesocketcustomName
                socketNameText.prop(obj, "socketcustomName")


class BFUO_PT_Nomenclature(bpy.types.Panel):
    # Is FPS Export panel

    bl_idname = "BFUO_PT_Nomenclature"
    bl_label = "Nomenclature"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Unreal Engine 4 Old"
    bl_parent_id = "BFUO_PT_BlenderForUnreal"

    class BFUO_MT_NomenclaturePresets(bpy.types.Menu):
        bl_label = 'Nomenclature Presets'
        preset_subdir = 'blender-for-unrealengine/nomenclature-presets'
        preset_operator = 'script.execute_preset'
        draw = bpy.types.Menu.draw_preset

    from bl_operators.presets import AddPresetBase

    class BFUO_OT_AddNomenclaturePreset(AddPresetBase, Operator):
        bl_idname = 'bfuo.add_nomenclature_preset'
        bl_label = 'Add or remove a preset for Nomenclature'
        bl_description = 'Add or remove a preset for Nomenclature'
        preset_menu = 'BFUO_MT_NomenclaturePresets'

        # Common variable used for all preset values
        preset_defines = [
                            'obj = bpy.context.object',
                            'scene = bpy.context.scene'
                         ]

        # Properties to store in the preset
        preset_values = [
                            'scene.static_prefix_export_name',
                            'scene.skeletal_prefix_export_name',
                            'scene.alembic_prefix_export_name',
                            'scene.anim_prefix_export_name',
                            'scene.pose_prefix_export_name',
                            'scene.camera_prefix_export_name',
                            'scene.anim_subfolder_name',
                            'scene.export_static_file_path',
                            'scene.export_skeletal_file_path',
                            'scene.export_alembic_file_path',
                            'scene.export_camera_file_path',
                            'scene.export_other_file_path',
                            'scene.file_export_log_name',
                            'scene.file_import_asset_script_name',
                            'scene.file_import_sequencer_script_name',
                            # Import location:
                            'scene.unreal_import_location',
                            'scene.unreal_levelsequence_import_location',
                            'scene.unreal_levelsequence_name',
                        ]

        # Directory to store the presets
        preset_subdir = 'blender-for-unrealengine/nomenclature-presets'

    SceneProp = bpy.types.Scene

    # Prefix
    SceneProp.static_prefix_export_name = bpy.props.StringProperty(
        name="StaticMesh Prefix",
        description="Prefix of staticMesh",
        maxlen=32,
        default="SM_")

    SceneProp.skeletal_prefix_export_name = bpy.props.StringProperty(
        name="SkeletalMesh Prefix ",
        description="Prefix of SkeletalMesh",
        maxlen=32,
        default="SK_")

    SceneProp.alembic_prefix_export_name = bpy.props.StringProperty(
        name="Alembic Prefix ",
        description="Prefix of Alembic (SkeletalMesh in unreal)",
        maxlen=32,
        default="SK_")

    SceneProp.anim_prefix_export_name = bpy.props.StringProperty(
        name="AnimationSequence Prefix",
        description="Prefix of AnimationSequence",
        maxlen=32,
        default="Anim_")

    SceneProp.pose_prefix_export_name = bpy.props.StringProperty(
        name="AnimationSequence(Pose) Prefix",
        description="Prefix of AnimationSequence with only one frame",
        maxlen=32,
        default="Pose_")

    SceneProp.camera_prefix_export_name = bpy.props.StringProperty(
        name="Camera anim Prefix",
        description="Prefix of camera animations",
        maxlen=32,
        default="Cam_")

    # Sub folder
    SceneProp.anim_subfolder_name = bpy.props.StringProperty(
        name="Animations sub folder name",
        description=(
            "The name of sub folder for animations New." +
            " You can now use ../ for up one directory."),
        maxlen=32,
        default="Anim")

    # File path
    SceneProp.export_static_file_path = bpy.props.StringProperty(
        name="StaticMesh export file path",
        description="Choose a directory to export StaticMesh(s)",
        maxlen=512,
        default=os.path.join("//", "ExportedFbx", "StaticMesh"),
        subtype='DIR_PATH')

    SceneProp.export_skeletal_file_path = bpy.props.StringProperty(
        name="SkeletalMesh export file path",
        description="Choose a directory to export SkeletalMesh(s)",
        maxlen=512,
        default=os.path.join("//", "ExportedFbx", "SkeletalMesh"),
        subtype='DIR_PATH')

    SceneProp.export_alembic_file_path = bpy.props.StringProperty(
        name="Alembic export file path",
        description="Choose a directory to export Alembic(s)",
        maxlen=512,
        default=os.path.join("//", "ExportedFbx", "Alembic"),
        subtype='DIR_PATH')

    SceneProp.export_camera_file_path = bpy.props.StringProperty(
        name="Camera export file path",
        description="Choose a directory to export Camera(s)",
        maxlen=512,
        default=os.path.join("//", "ExportedFbx", "Sequencer"),
        subtype='DIR_PATH')

    SceneProp.export_other_file_path = bpy.props.StringProperty(
        name="Other export file path",
        description="Choose a directory to export text file and other",
        maxlen=512,
        default=os.path.join("//", "ExportedFbx"),
        subtype='DIR_PATH')

    # File name
    SceneProp.file_export_log_name = bpy.props.StringProperty(
        name="Export log name",
        description="Export log name",
        maxlen=64,
        default="ExportLog.txt")

    SceneProp.file_import_asset_script_name = bpy.props.StringProperty(
        name="Import asset script Name",
        description="Import asset script name",
        maxlen=64,
        default="ImportAssetScript.py")

    default = "file_import_sequencer_script_namea.py"

    SceneProp.file_import_sequencer_script_name = bpy.props.StringProperty(
        name="Import sequencer script Name1",
        description="Import sequencer script name",
        maxlen=64,
        default="ImportSequencerScript.py")

    def draw(self, context):
        scn = context.scene
        addon_prefs = bpy.context.preferences.addons[__package__].preferences

        # Presets
        row = self.layout.row(align=True)
        row.menu('BFUO_MT_NomenclaturePresets', text='Nomenclature Presets')
        row.operator('bfuo.add_nomenclature_preset', text='', icon='ADD')
        row.operator(
            'bfuo.add_nomenclature_preset',
            text='',
            icon='REMOVE').remove_active = True

        # Prefix
        propsPrefix = self.layout.row()
        propsPrefix = propsPrefix.column()
        propsPrefix.prop(scn, 'static_prefix_export_name', icon='OBJECT_DATA')
        propsPrefix.prop(
            scn,
            'skeletal_prefix_export_name',
            icon='OBJECT_DATA')
        propsPrefix.prop(scn, 'alembic_prefix_export_name', icon='OBJECT_DATA')
        propsPrefix.prop(scn, 'anim_prefix_export_name', icon='OBJECT_DATA')
        propsPrefix.prop(scn, 'pose_prefix_export_name', icon='OBJECT_DATA')
        propsPrefix.prop(scn, 'camera_prefix_export_name', icon='OBJECT_DATA')

        # Sub folder
        propsSub = self.layout.row()
        propsSub = propsSub.column()
        propsSub.prop(scn, 'anim_subfolder_name', icon='FILE_FOLDER')

        # File path
        filePath = self.layout.row()
        filePath = filePath.column()
        filePath.prop(scn, 'export_static_file_path')
        filePath.prop(scn, 'export_skeletal_file_path')
        filePath.prop(scn, 'export_alembic_file_path')
        filePath.prop(scn, 'export_camera_file_path')
        filePath.prop(scn, 'export_other_file_path')

        # File name
        fileName = self.layout.row()
        fileName = fileName.column()
        fileName.prop(scn, 'file_export_log_name', icon='FILE')
        if addon_prefs.useGeneratedScripts:
            fileName.prop(
                scn,
                'file_import_asset_script_name',
                icon='FILE')
            fileName.prop(
                scn,
                'file_import_sequencer_script_name',
                icon='FILE')


class BFUO_PT_ImportScript(bpy.types.Panel):
    # Is Import script panel

    bl_idname = "BFUO_PT_ImportScript"
    bl_label = "Import Script"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Unreal Engine 4 Old"
    bl_parent_id = "BFUO_PT_BlenderForUnreal"

    SceneProp = bpy.types.Scene
    SceneProp.unreal_import_location = bpy.props.StringProperty(
        name="Unreal import location",
        description="Unreal assets import location in /Game/",
        maxlen=512,
        default='ImportedFbx')

    SceneProp.unreal_levelsequence_import_location = bpy.props.StringProperty(
        name="Unreal sequencer import location",
        description="Unreal sequencer import location in /Game/",
        maxlen=512,
        default=r'ImportedFbx/Sequencer')

    SceneProp.unreal_levelsequence_name = bpy.props.StringProperty(
        name="Unreal sequencer name",
        description="Unreal sequencer name",
        maxlen=512,
        default='MySequence')

    def draw(self, context):
        scn = context.scene
        addon_prefs = bpy.context.preferences.addons[__package__].preferences

        # Sub folder
        if addon_prefs.useGeneratedScripts:
            propsSub = self.layout.row()
            propsSub = propsSub.column()
            propsSub.prop(
                scn,
                'unreal_import_location',
                icon='FILE_FOLDER')
            propsSub.prop(
                scn,
                'unreal_levelsequence_import_location',
                icon='FILE_FOLDER')
            propsSub.prop(
                scn,
                'unreal_levelsequence_name',
                icon='FILE')
        else:
            self.layout.label(text='(Generated scripts are deactivated.)')


class BFUO_OT_UnrealExportedAsset(bpy.types.PropertyGroup):
    # [AssetName , AssetType , ExportPath, ExportTime]
    assetName: StringProperty(default="None")
    assetType: StringProperty(default="None")  # return from GetAssetType()
    exportPath: StringProperty(default="None")
    exportTime: FloatProperty(default=0)
    object: PointerProperty(type=bpy.types.Object)


class BFUO_OT_UnrealPotentialError(bpy.types.PropertyGroup):
    type: IntProperty(default=0)  # 0:Info, 1:Warning, 2:Error
    object: PointerProperty(type=bpy.types.Object)
    ###
    selectObjectButton: BoolProperty(default=True)
    selectVertexButton: BoolProperty(default=False)
    selectPoseBoneButton: BoolProperty(default=False)
    ###
    selectOption: StringProperty(default="None")  # 0:VertexWithZeroWeight
    itemName: StringProperty(default="None")
    text: StringProperty(default="Unknown")
    correctRef: StringProperty(default="None")
    correctlabel: StringProperty(default="Fix it !")
    correctDesc: StringProperty(default="Correct target error")
    docsOcticon: StringProperty(default="None")


class BFUO_PT_Export(bpy.types.Panel):
    # Is Export panel

    bl_idname = "BFUO_PT_Export"
    bl_label = "Export"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Unreal Engine 4 Old"
    bl_parent_id = "BFUO_PT_BlenderForUnreal"

    class BFUO_OT_ShowAssetToExport(Operator):
        bl_label = "Show asset(s)"
        bl_idname = "bfuo.showasset"
        bl_description = "Click to show assets that are to be exported."

        def execute(self, context):
            obj = context.object
            assets = GetFinalAssetToExport()
            popup_title = "Assets list"
            if len(assets) > 0:
                popup_title = str(len(assets))+' asset(s) will be exported.'
            else:
                popup_title = 'No exportable assets were found.'

            def draw(self, context):
                col = self.layout.column()
                for asset in assets:
                    row = col.row()
                    if asset.obj is not None:
                        if asset.action is not None:
                            if (type(asset.action) is bpy.types.Action):
                                # Action name
                                action = asset.action.name
                            elif (type(asset.action) is bpy.types.AnimData):
                                # Nonlinear name
                                action = asset.obj.NLAAnimName
                            else:
                                action = "..."
                            row.label(
                                text="- ["+asset.obj.name+"] --> " +
                                action+" ("+asset.type+")")
                        else:
                            if asset.type != "Collection StaticMesh":
                                row.label(
                                    text="- "+asset.obj.name +
                                    " ("+asset.type+")")
                            else:
                                row.label(
                                    text="- "+asset.obj +
                                    " ("+asset.type+")")

                    else:
                        row.label(text="- ("+asset.type+")")
            bpy.context.window_manager.popup_menu(
                draw,
                title=popup_title,
                icon='PACKAGE')
            return {'FINISHED'}

    class BFUO_OT_CheckPotentialErrorPopup(Operator):
        bl_label = "Check potential errors"
        bl_idname = "bfuo.checkpotentialerror"
        bl_description = "Check potential errors"
        correctedProperty = 0

        class BFUO_OT_FixitTarget(Operator):
            bl_label = "Fix it !"
            bl_idname = "bfuo.fixit_objet"
            bl_description = "Correct target error"
            errorIndex: bpy.props.IntProperty(default=-1)

            def execute(self, context):
                result = TryToCorrectPotentialError(self.errorIndex)
                self.report({'INFO'}, result)
                return {'FINISHED'}

        class BFUO_OT_SelectObjectButton(Operator):
            bl_label = "Select(Object)"
            bl_idname = "bfuo.select_error_objet"
            bl_description = "Select target Object."
            errorIndex: bpy.props.IntProperty(default=-1)

            def execute(self, context):
                result = SelectPotentialErrorObject(self.errorIndex)
                return {'FINISHED'}

        class BFUO_OT_SelectVertexButton(Operator):
            bl_label = "Select(Vertex)"
            bl_idname = "bfuo.select_error_vertex"
            bl_description = "Select target Vertex."
            errorIndex: bpy.props.IntProperty(default=-1)

            def execute(self, context):
                result = SelectPotentialErrorVertex(self.errorIndex)
                return {'FINISHED'}

        class BFUO_OT_SelectPoseBoneButton(Operator):
            bl_label = "Select(PoseBone)"
            bl_idname = "bfuo.select_error_posebone"
            bl_description = "Select target Pose Bone."
            errorIndex: bpy.props.IntProperty(default=-1)

            def execute(self, context):
                result = SelectPotentialErrorPoseBone(self.errorIndex)
                return {'FINISHED'}

        class BFUO_OT_OpenPotentialErrorDocs(Operator):
            bl_label = "Open docs"
            bl_idname = "bfuo.open_potential_error_docs"
            bl_description = "Open potential error docs."
            octicon: StringProperty(default="")

            def execute(self, context):
                os.system(
                    "start \"\" " +
                    "https://github.com/xavier150/" +
                    "Blender-For-UnrealEngine-Addons/" +
                    "blob/master/Tuto/" +
                    "Potential%20Error%20with%20Blender%20export%20" +
                    "to%20Unreal.md#"+self.octicon)
                return {'FINISHED'}

        def execute(self, context):
            self.correctedProperty = CorrectBadProperty()
            UpdateNameHierarchy()
            UpdateUnrealPotentialError()
            return {'FINISHED'}

        def invoke(self, context, event):
            self.correctedProperty = CorrectBadProperty()
            UpdateNameHierarchy()
            UpdateUnrealPotentialError()
            wm = context.window_manager
            return wm.invoke_popup(self, width=1020)

        def check(self, context):
            return True

        def draw(self, context):

            layout = self.layout
            if len(bpy.context.scene.potentialErrorList) > 0:
                popup_title = (
                    str(len(bpy.context.scene.potentialErrorList)) +
                    " potential error(s) found!")
            else:
                popup_title = "No potential error to correct!"

            if self.correctedProperty > 0:
                potentialErrorInfo = (
                    str(self.correctedProperty) +
                    "- properties corrected.")
            else:
                potentialErrorInfo = "- No properties to correct."

            layout.label(text=popup_title)
            layout.label(text="- Hierarchy names updated")
            layout.label(text=potentialErrorInfo)
            layout.separator()
            row = layout.row()
            col = row.column()
            for x in range(len(bpy.context.scene.potentialErrorList)):
                error = bpy.context.scene.potentialErrorList[x]

                myLine = col.box().split(factor=0.85)
                # ----
                if error.type == 0:
                    msgType = 'INFO'
                    msgIcon = 'INFO'
                elif error.type == 1:
                    msgType = 'WARNING'
                    msgIcon = 'ERROR'
                elif error.type == 2:
                    msgType = 'ERROR'
                    msgIcon = 'CANCEL'
                # ----

                # Text
                TextLine = myLine.column()
                errorFullMsg = msgType+": "+error.text
                splitedText = errorFullMsg.split("\n")

                for text, Line in enumerate(splitedText):
                    if (text < 1):

                        FisrtTextLine = TextLine.row()
                        if (error.docsOcticon != "None"):  # Doc button
                            props = FisrtTextLine.operator(
                                "bfuo.open_potential_error_docs",
                                icon="HELP",
                                text="")
                            props.octicon = error.docsOcticon

                        FisrtTextLine.label(text=Line, icon=msgIcon)
                    else:
                        TextLine.label(text=Line)

                # Select and fix button
                ButtonLine = myLine.column()
                if (error.correctRef != "None"):
                    props = ButtonLine.operator(
                        "bfuo.fixit_objet",
                        text=error.correctlabel)
                    props.errorIndex = x
                if (error.object is not None):
                    if (error.selectObjectButton):
                        props = ButtonLine.operator(
                            "bfuo.select_error_objet")
                        props.errorIndex = x
                    if (error.selectVertexButton):
                        props = ButtonLine.operator(
                            "bfuo.select_error_vertex")
                        props.errorIndex = x
                    if (error.selectPoseBoneButton):
                        props = ButtonLine.operator(
                            "bfuo.select_error_posebone")
                        props.errorIndex = x

    class BFUO_OT_ExportForUnrealEngineButton(Operator):
        bl_label = "Export for UnrealEngine 4"
        bl_idname = "bfuo.exportforunreal"
        bl_description = "Export all assets of this scene."

        def execute(self, context):
            scene = bpy.context.scene

            def GetIfOneTypeCheck():
                if (scene.static_export
                        or scene.static_collection_export
                        or scene.skeletal_export
                        or scene.anin_export
                        or scene.alembic_export
                        or scene.camera_export):
                    return True
                else:
                    return False

            if GetIfOneTypeCheck():
                # Primary check	if file is saved
                # to avoid windows PermissionError

                if bpy.data.is_saved:
                    scene.BFUO_ExportedAssetsList.clear()
                    s = CounterStart()
                    UpdateNameHierarchy()
                    bfu_export_asset.ExportForUnrealEngine(self)
                    bfu_write_text.WriteAllTextFiles()

                    if len(scene.BFUO_ExportedAssetsList) > 0:
                        self.report(
                            {'INFO'},
                            "Export of " +
                            str(len(scene.BFUO_ExportedAssetsList)) +
                            " asset(s) has been finalized in " +
                            str(round(CounterEnd(s), 2)) +
                            "seconds. Look in console for more info.")
                        print(
                            "=========================" +
                            " Exported asset(s) " +
                            "=========================")
                        print("")
                        lines = bfu_write_text.WriteExportLog().splitlines()
                        for line in lines:
                            print(line)
                        print("")
                        print(
                            "=========================" +
                            " ... " +
                            "=========================")
                    else:
                        self.report(
                            {'WARNING'},
                            "Not found assets with" +
                            " \"Export recursive\" properties " +
                            "or collection to export.")
                else:
                    self.report(
                        {'WARNING'},
                        "Please save this blend file before export")
            else:
                self.report({'WARNING'}, "No asset type is checked.")
                return {'FINISHED'}
            return {'FINISHED'}

    # Categories :
    bpy.types.Scene.static_export = bpy.props.BoolProperty(
        name="StaticMesh(s)",
        description="Check mark to export StaticMesh(s)",
        default=True
        )

    bpy.types.Scene.static_collection_export = bpy.props.BoolProperty(
        name="Collection(s) ",
        description="Check mark to export Collection(s)",
        default=False
        )

    bpy.types.Scene.skeletal_export = bpy.props.BoolProperty(
        name="SkeletalMesh(s)",
        description="Check mark to export SkeletalMesh(s)",
        default=True
        )

    bpy.types.Scene.anin_export = bpy.props.BoolProperty(
        name="Animation(s)",
        description="Check mark to export Animation(s)",
        default=True
        )

    bpy.types.Scene.alembic_export = bpy.props.BoolProperty(
        name="Alembic animation(s)",
        description="Check mark to export Alembic animation(s)",
        default=False
        )

    bpy.types.Scene.camera_export = bpy.props.BoolProperty(
        name="Camera(s)",
        description="Check mark to export Camera(s)",
        default=False
        )

    # Additional file
    bpy.types.Scene.text_ExportLog = bpy.props.BoolProperty(
        name="Export Log",
        description="Check mark to write export log file",
        default=True
        )

    bpy.types.Scene.text_ImportAssetScript = bpy.props.BoolProperty(
        name="Import assets script",
        description="Check mark to write import asset script file",
        default=True
        )

    bpy.types.Scene.text_ImportSequenceScript = bpy.props.BoolProperty(
        name="Import sequence script",
        description="Check mark to write import sequencer script file",
        default=True
        )

    bpy.types.Scene.text_AdditionalData = bpy.props.BoolProperty(
        name="Additional data",
        description=(
            "Check mark to write additional data" +
            " like parameter or anim tracks"),
        default=True
        )

    # exportProperty
    bpy.types.Scene.export_ExportOnlySelected = bpy.props.BoolProperty(
        name="Export only select",
        description=(
            "Check mark to export only selected export group." +
            " (export_recursive objects and auto childs) "),
        default=False
        )

    def draw(self, context):
        scn = context.scene
        addon_prefs = bpy.context.preferences.addons[__package__].preferences

        # Categories :
        layout = self.layout
        row = layout.row()
        col = row.column()

        # Assets
        AssetsCol = row.column()
        AssetsCol.label(text="Asset types to export", icon='PACKAGE')
        AssetsCol.prop(scn, 'static_export')
        AssetsCol.prop(scn, 'static_collection_export')
        AssetsCol.prop(scn, 'skeletal_export')
        AssetsCol.prop(scn, 'anin_export')
        AssetsCol.prop(scn, 'alembic_export')
        AssetsCol.prop(scn, 'camera_export')
        layout.separator()

        # Additional file
        FileCol = row.column()
        FileCol.label(text="Additional file", icon='PACKAGE')
        FileCol.prop(scn, 'text_ExportLog')
        FileCol.prop(scn, 'text_ImportAssetScript')
        FileCol.prop(scn, 'text_ImportSequenceScript')
        if addon_prefs.useGeneratedScripts:
            FileCol.prop(scn, 'text_AdditionalData')

        # Feedback info :
        AssetNum = len(GetFinalAssetToExport())
        AssetInfo = layout.row().box().split(factor=0.75)
        AssetFeedback = str(AssetNum) + " Asset(s) will be exported."
        AssetInfo.label(text=AssetFeedback, icon='INFO')
        AssetInfo.operator("bfuo.showasset")

        # Export button :
        checkButton = layout.column()
        checkButton.operator("bfuo.checkpotentialerror", icon='FILE_TICK')
        checkButton.operator("bfuo.computalllightmap", icon='TEXTURE')

        # exportProperty
        exportOnlySelect = layout.row()
        exportOnlySelect.prop(scn, 'export_ExportOnlySelected')

        exportButton = layout.row()
        exportButton.scale_y = 2.0
        exportButton.operator("bfuo.exportforunreal", icon='EXPORT')


class BFUO_PT_Clipboard(bpy.types.Panel):

    # Is Clipboard panel

    bl_idname = "BFUO_PT_Clipboard"
    bl_label = "Clipboard Copy"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Unreal Engine 4 Old"
    bl_parent_id = "BFUO_PT_BlenderForUnreal"

    class BFUO_OT_CopyImportAssetScriptCommand(Operator):
        bl_label = "ImportAssetScript"
        bl_idname = "bfuo.copy_importassetscript_command"
        bl_description = "Copy Import Asset Script command"

        def execute(self, context):
            scn = context.scene
            setWindowsClipboard(GetImportAssetScriptCommand())
            self.report(
                {'INFO'},
                "command for "+scn.file_import_asset_script_name +
                " copied")
            return {'FINISHED'}

    class BFUO_OT_CopyImportSequencerScriptCommand(Operator):
        bl_label = "ImportSequencerScript"
        bl_idname = "bfuo.copy_importsequencerscript_command"
        bl_description = "Copy Import Sequencer Script command"

        def execute(self, context):
            scn = context.scene
            setWindowsClipboard(GetImportSequencerScriptCommand())
            self.report(
                {'INFO'},
                "command for "+scn.file_import_sequencer_script_name +
                " copied")
            return {'FINISHED'}

    def draw(self, context):
        scn = context.scene
        layout = self.layout
        addon_prefs = bpy.context.preferences.addons[__package__].preferences

        if addon_prefs.useGeneratedScripts:
            layout.label(
                text="Click on one of the buttons to copy the import command.",
                icon='INFO')
            copyButton = layout.row()
            copyButton.operator("bfuo.copy_importassetscript_command")
            copyButton.operator("bfuo.copy_importsequencerscript_command")
            layout.label(
                text="Then you can paste it into the python console of unreal",
                icon='INFO')
        else:
            layout.label(text='(Generated scripts are deactivated.)')


class BFUO_PT_CorrectAndImprov(bpy.types.Panel):
    # Is Clipboard panel

    bl_idname = "BFUO_PT_CorrectAndImprov"
    bl_label = "Correct and improv"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Unreal Engine 4 Old bis"
    bl_parent_id = "BFUO_PT_BlenderForUnreal"

    class BFUO_OT_CorrectExtremUV(Operator):
        bl_label = "Correct extrem UV For Unreal"
        bl_idname = "bfuo.correct_extrem_uv"
        bl_description = (
            "Correct extrem UV island of the selected object" +
            " for better use in real time engines"
            )
        bl_options = {'REGISTER', 'UNDO'}

        stepScale: bpy.props.IntProperty(
            name="Step scale",
            default=2,
            min=1,
            max=100)

        def execute(self, context):
            if bpy.context.active_object.mode == "EDIT":
                CorrectExtremeUV(stepScale=self.stepScale)
                self.report(
                    {'INFO'},
                    "UV corrected!")
            else:
                self.report(
                    {'WARNING'},
                    "Move to Edit mode for correct extrem UV.")
            return {'FINISHED'}


classes = (
    BFUO_AP_AddonPreferences,
    BFUO_AP_AddonPreferences.BFUO_OT_NewReleaseInfo,
    BFUO_AP_AddonPreferences.BFUO_OT_OpenDocumentationTargetPage,

    BFUO_PT_BlenderForUnrealObject,
    BFUO_PT_BlenderForUnrealObject.BFUO_OT_OpenDocumentationPage,

    BFUO_PT_BlenderForUnreal,
    BFUO_PT_BlenderForUnreal.BFUO_MT_ObjectGlobalPropertiesPresets,
    BFUO_PT_BlenderForUnreal.BFUO_OT_AddObjectGlobalPropertiesPreset,




    BFUO_PT_ObjectProperties,
    BFUO_PT_ObjectImportProperties,
    BFUO_PT_ObjectImportProperties.BFUO_OT_ComputLightMap,
    BFUO_PT_ObjectImportProperties.BFUO_OT_ComputAllLightMap,

    BFUO_PT_AnimProperties,
    BFUO_PT_AnimProperties.BFUO_UL_ActionExportTarget,
    BFUO_PT_AnimProperties.BFUO_OT_UpdateObjActionListButton,
    BFUO_PT_AnimProperties.BFUO_OT_SelectAllActionsButton,
    BFUO_PT_AnimProperties.BFUO_OT_DeselectAllActionsButton,
    BFUO_PT_AnimProperties.BFUO_OT_ShowActionToExport,

    BFUO_PT_CollectionProperties,
    BFUO_PT_CollectionProperties.BFUO_UL_CollectionExportTarget,
    BFUO_PT_CollectionProperties.BFUO_OT_UpdateCollectionButton,
    BFUO_PT_CollectionProperties.BFUO_OT_ShowCollectionToExport,

    BFUO_PT_AvancedObjectProperties,


    BFUO_PT_CollisionsAndSockets,
    BFUO_PT_CollisionsAndSockets.BFUO_OT_ConvertToCollisionButtonBox,
    BFUO_PT_CollisionsAndSockets.BFUO_OT_ConvertToCollisionButtonCapsule,
    BFUO_PT_CollisionsAndSockets.BFUO_OT_ConvertToCollisionButtonSphere,
    BFUO_PT_CollisionsAndSockets.BFUO_OT_ConvertToCollisionButtonConvex,
    BFUO_PT_CollisionsAndSockets.BFUO_OT_ConvertToStaticSocketButton,
    BFUO_PT_CollisionsAndSockets.BFUO_OT_ConvertToSkeletalSocketButton,

    BFUO_PT_Nomenclature,
    BFUO_PT_Nomenclature.BFUO_MT_NomenclaturePresets,
    BFUO_PT_Nomenclature.BFUO_OT_AddNomenclaturePreset,

    BFUO_PT_ImportScript,

    BFUO_PT_Export,
    BFUO_PT_Export.BFUO_OT_ShowAssetToExport,
    BFUO_PT_Export.BFUO_OT_CheckPotentialErrorPopup,
    BFUO_PT_Export.BFUO_OT_CheckPotentialErrorPopup.BFUO_OT_FixitTarget,
    BFUO_PT_Export.BFUO_OT_CheckPotentialErrorPopup.BFUO_OT_SelectObjectButton,
    BFUO_PT_Export.BFUO_OT_CheckPotentialErrorPopup.BFUO_OT_SelectVertexButton,
    BFUO_PT_Export.BFUO_OT_CheckPotentialErrorPopup.BFUO_OT_SelectPoseBoneButton,
    BFUO_PT_Export.BFUO_OT_CheckPotentialErrorPopup.BFUO_OT_OpenPotentialErrorDocs,
    BFUO_PT_Export.BFUO_OT_ExportForUnrealEngineButton,

    BFUO_PT_Clipboard,
    BFUO_PT_Clipboard.BFUO_OT_CopyImportAssetScriptCommand,
    BFUO_PT_Clipboard.BFUO_OT_CopyImportSequencerScriptCommand,

    BFUO_PT_CorrectAndImprov.BFUO_OT_CorrectExtremUV
)


def menu_func(self, context):
    layout = self.layout
    col = layout.column()
    col.separator(factor=1.0)
    col.operator(BFUO_PT_CorrectAndImprov.BFUO_OT_CorrectExtremUV.bl_idname)


def register():
    from bpy.utils import register_class

    for cls in classes:
        register_class(cls)

    bpy.utils.register_class(BFUO_OT_ObjExportAction)
    bpy.types.Object.exportActionList = CollectionProperty(
        type=BFUO_OT_ObjExportAction)
    bpy.utils.register_class(BFUO_OT_SceneCollectionExport)
    bpy.types.Scene.CollectionExportList = CollectionProperty(
        type=BFUO_OT_SceneCollectionExport)
    bpy.utils.register_class(BFUO_OT_UnrealExportedAsset)
    bpy.types.Scene.BFUO_ExportedAssetsList = CollectionProperty(
        type=BFUO_OT_UnrealExportedAsset)
    bpy.utils.register_class(BFUO_OT_UnrealPotentialError)
    bpy.types.Scene.potentialErrorList = CollectionProperty(
        type=BFUO_OT_UnrealPotentialError)

    bpy.types.VIEW3D_MT_uv_map.append(menu_func)


def unregister():
    from bpy.utils import unregister_class

    for cls in reversed(classes):
        unregister_class(cls)

    bpy.utils.unregister_class(BFUO_OT_ObjExportAction)
    bpy.utils.unregister_class(BFUO_OT_SceneCollectionExport)
    bpy.utils.unregister_class(BFUO_OT_UnrealExportedAsset)
    bpy.utils.unregister_class(BFUO_OT_UnrealPotentialError)

    bpy.types.VIEW3D_MT_uv_map.remove(menu_func)