import bpy
import os
import time
from . import bfu_utils
from . import bfu_naming
from . import bfu_export_logs


class BFU_OT_FileExport(bpy.types.PropertyGroup):
    file_name: bpy.props.StringProperty() # type: ignore
    file_extension: bpy.props.StringProperty() # type: ignore
    file_path: bpy.props.StringProperty() # type: ignore
    file_type: bpy.props.StringProperty()  # FBX, AdditionalTrack # type: ignore

    def __init__(self, name):
        pass

    def GetFileWithExtension(self):
        return self.file_name + "." + self.file_extension

    def GetRelativePath(self):
        return os.path.join(self.file_path, self.GetFileWithExtension())

    def GetAbsolutePath(self):
        return os.path.join(bpy.path.abspath(self.file_path), self.GetFileWithExtension())


class BFU_OT_UnrealExportedAsset(bpy.types.PropertyGroup):
    # [AssetName , AssetType , ExportPath, ExportTime]

    asset_name: bpy.props.StringProperty(default="None") # type: ignore
    asset_global_scale: bpy.props.FloatProperty(default=1.0) # type: ignore
    skeleton_name: bpy.props.StringProperty(default="None") # type: ignore
    asset_type: bpy.props.StringProperty(default="None")  # return from bfu_utils.GetAssetType() # type: ignore
    folder_name: bpy.props.StringProperty(default="") # type: ignore
    files: bpy.props.CollectionProperty(type=BFU_OT_FileExport) # type: ignore
    object: bpy.props.PointerProperty(type=bpy.types.Object) # type: ignore
    collection: bpy.props.PointerProperty(type=bpy.types.Collection) # type: ignore
    export_start_time: bpy.props.FloatProperty(default=0.0) # type: ignore
    export_end_time: bpy.props.FloatProperty(default=0.0) # type: ignore
    export_success: bpy.props.BoolProperty(default=False) # type: ignore
    animation_start_frame: bpy.props.IntProperty(default=0) # type: ignore
    animation_end_frame: bpy.props.IntProperty(default=0) # type: ignore

    def StartAssetExport(self):
        self.export_start_time = time.perf_counter()

    def EndAssetExport(self, success):
        self.export_end_time = time.perf_counter()
        self.export_success = success

    def GetExportTime(self):
        return self.export_end_time - self.export_start_time

    def GetFileByType(self, file_type: str):
        for file in self.files:
            file: bfu_export_logs.BFU_OT_FileExport
            if file.file_type == file_type:
                return file

    def GetFilename(self):
        main_file = self.files[0]
        return main_file.file_name

    def GetFilenameWithExtension(self):
        main_file = self.files[0]
        return main_file.GetFileWithExtension()


classes = (
    BFU_OT_FileExport,
    BFU_OT_UnrealExportedAsset,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.UnrealExportedAssetsList = bpy.props.CollectionProperty(
        type=BFU_OT_UnrealExportedAsset)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

