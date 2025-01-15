# Unreal Engine Assets Exporter - Release Log
Release Logs: https://github.com/xavier150/Blender-For-UnrealEngine-Addons/wiki/Release-Logs

### Version 4.3.11

- New: Option to show hidden linked properties (debug option in addon preferences).
- New: "Fix Camera Axis" can now choose the warp target degrees for specific use.
- Fixed: NLA export may not use the correct animated influence or blend in/out in NLA Strips.
- Fixed: NLA export always creates a key on the first frame of the animated influence curve.
- Fixed: NLA export loses animated influence curve key data (Select and Handle vectors).
- Fixed: When the Unit Scale is not set to 0.01, keyframes transfer from driver curves fails.
- Fixed: Import script does not import Blender Normals in Unreal 5.5 (Interchange Pipeline).
- Fixed: "Fix Camera Axis" used the wrong warp target (180 degrees previously, now 360 degrees).
- Fixed: Some object types, such as Text or Surface, are duplicated during export.