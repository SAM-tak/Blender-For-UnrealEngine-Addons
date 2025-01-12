# Unreal Engine Assets Exporter - Release Log
Release Logs: https://github.com/xavier150/Blender-For-UnrealEngine-Addons/wiki/Release-Logs

### Version 4.3.11

- New option to show hiden linked propertys (debug).
- Fixed: NLA export may not use correct animated influence or blend in/out in NLA Strips.
- Fixed: NLA export always create a key on first frame of animated influence curve.
- Fixed: NLA export loose animated influence curve key data. (Select and Handle vectors)
- Fixed: With Unit Scale not at 0.01, keyframes transfert from driver curves fail.
- Fixed: Import script don't import Blender Normals in Unreal 5.5 (Interchange Pipline)
- Fixed: "Fix Camera Axis" use wrong warp target (180 before and 360 when fixed.)