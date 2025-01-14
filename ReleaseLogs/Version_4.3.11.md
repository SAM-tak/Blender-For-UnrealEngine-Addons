# Unreal Engine Assets Exporter - Release Log
Release Logs: https://github.com/xavier150/Blender-For-UnrealEngine-Addons/wiki/Release-Logs

### Version 4.3.11

- New option to show hiden linked propertys (debug).
- Change: "Fix Camera Axis" can now choose the warp target degress for specific use.
- Fixed: NLA export may not use correct animated influence or blend in/out in NLA Strips.
- Fixed: NLA export always create a key on first frame of animated influence curve.
- Fixed: NLA export loose animated influence curve key data. (Select and Handle vectors)
- Fixed: With Unit Scale not at 0.01, keyframes transfert from driver curves fail.
- Fixed: Import script don't import Blender Normals in Unreal 5.5 (Interchange Pipline)
- Fixed: "Fix Camera Axis" use wrong warp target (180 degress before and 360 degress now.)
- Fixed: Some object type as Text or Surface is duplicated during export.