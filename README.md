# RenderMol
This simple Python script is designed to act as a template for loading molecules and animations into Blender.

# Use
1. Remove initial cube from Blender initialization.
2. Load script into Blender editor.
3. Replace "path2.xyz" with the path to your XYZ file.
4. Run script.
5. Set up scene and render!

# Notes
- If a message occurs mentioning an improper keyring then comment out the line "bpy.ops.anim.keying_set_active_set(type='Location')" and rerun (after deleting unnecessary objects).
- Additional atoms can be handled as long as you provide the radii and colors.
