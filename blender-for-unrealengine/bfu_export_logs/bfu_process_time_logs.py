import bpy
import os
import time
from .. import bpl

class BFU_OT_ExportProcessTimeLog(bpy.types.PropertyGroup):

    process_info: bpy.props.StringProperty()
    start_time: bpy.props.FloatProperty(default=0.0)
    end_time: bpy.props.FloatProperty(default=0.0)
    sub_step: bpy.props.IntProperty(default=0)
    finished_success: bpy.props.BoolProperty(default=False)

    def start_process(self, process_info, sub_step):
        if not isinstance(process_info, str):
            raise TypeError("process_info is not a string!")
        if not process_info:
            raise ValueError("process_info is empty or None!")

        self.process_info = process_info
        self.sub_step = sub_step
        self.start_time = time.perf_counter()

    def finish_process(self):
        if not isinstance(self.process_info, str):
            raise TypeError("proprty process_info is not a string!")
        if not self.process_info:
            raise ValueError("proprty process_info is empty or None!")

        self.end_time = time.perf_counter()
        self.finished_success = True

    def get_process_detail(self):
        if self.finished_success:
            result = "Success"
        else:
            result = "Never finished"
        str_time = bpl.color_set.yellow(bpl.utils.get_formatted_time(self.end_time - self.start_time))
        str_sub_steps = self.sub_step * 4 * " "
        return f"{str_sub_steps}{self.process_info}, {str_time}, {result}"


classes = (
    BFU_OT_ExportProcessTimeLog,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.bfu_export_process_time_logs = bpy.props.CollectionProperty(
        type=BFU_OT_ExportProcessTimeLog)


def unregister():
    del bpy.types.Scene.bfu_export_process_time_logs

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
