import bpy
import os
import time
from .. import bfu_export_logs


class BFU_OT_ExportProcessTimeLog(bpy.types.PropertyGroup):

    start_time: bpy.props.FloatProperty(default=0.0)
    end_time: bpy.props.FloatProperty(default=0.0)
    finished_success: bpy.props.BoolProperty(default=False)

    def start_process(self, process_name):
        self.name = process_name
        self.start_time = time.perf_counter()

    def finish_process(self):
        self.end_time = time.perf_counter()
        self.finished_success = True

    def get_str_time(self):
        """
        Get the elapsed str time since the timer started.

        Returns:
            str: Elapsed time formatted as a string.
        """
        elapsed_time = self.end_time - self.start_time
        if elapsed_time < 60:
            return f"{elapsed_time:.2f} secondes"
        elif elapsed_time < 3600:
            minutes, seconds = divmod(elapsed_time, 60)
            return f"{int(minutes)} minutes et {seconds:.2f} secondes"
        else:
            hours, remainder = divmod(elapsed_time, 3600)
            minutes, seconds = divmod(remainder, 60)
            return f"{int(hours)} heures, {int(minutes)} minutes et {seconds:.2f} secondes"

    def get_process_detail(self):
        if self.finished_success:
            result = "Success"
        else:
            result = "Never finished"
        str_time = self.get_str_time()
        return f"{self.name}, {str_time}, {result}"


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
