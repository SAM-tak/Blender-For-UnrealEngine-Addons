# Unreal Engine Assets Exporter - Release Log
Release Logs: https://github.com/xavier150/Blender-For-UnrealEngine-Addons/wiki/Release-Logs

### Version 4.3.12

- New: Console logs show now how details about the export steps and how many time it take.
- New: New option to force Nanite build or set non Nanite.
- New: Support for Blender 4.4
- Change: Better logs details + clear logs after export to avoid useless used space in blender file.
- Fixed: In the import script origin_skeleton may produce issue when not found.
- Fixed: Import a sequencer set the level as unsaved. (Spawned cameras was not set as transient.)