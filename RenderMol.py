# Imports
import os
import mathutils
import bpy

# Functions
def element_radius(element):
    '''
    Return covalent radius of element.
    '''

    # Variables
    standard = 67.
    radii = {'H' : 53, 'He' : 31, 'Li' : 167, 'Be' : 112,
             'B' : 87, 'C' : 67, 'N' : 56, 'O' : 48,
             'F' : 42, 'Ne' : 38, 'Na' : 190, 'Mg' : 145,
             'Al' : 118, 'Si' : 111, 'P' : 98, 'S' : 88,
             'Cl' : 79, 'Ar' : 71,}

    return radii[element]/standard

def element_color(element):
    '''
    Return element colors.
    '''

    colors = {'H':(210/256.,203/256.,157/256.,1.0),
              'C':(44/256.,63/256.,65/256.,1.0),
              'O':(203/256.,77/256.,199/256.,1.0),
              'Si':(87/256.,131/256.,181/256.,1.0),
              'N':(109/256.,129/256.,177/256.,1.0)}

    return colors[element]

def load_xyz(inFileName):
    '''
    Load XYZ file.

    INPUT
        inFileName: (str) Name of XYZ file.

    NOTES
        Assumes units are in Angstroms.
        Assumes each frame has the same number of atoms.
    '''

    # Variables
    keyFrameList = []
    elementList = []
    posList = []

    # Read file lines
    with open(inFileName,'r') as inFile:
        fileLines = inFile.readlines()

    # Determine number of frames (molecules)
    numAtoms = int(fileLines[0])
    numMolecules = int(len(fileLines)/(numAtoms+2))

    # Read each frame (molecule)
    for molIdx in range(numMolecules):
        # Initialize lists
        elementList = []
        posList = []

        # Read lines associated with frame
        for idx,line in enumerate(fileLines[molIdx*(numAtoms+2):(molIdx+1)*(numAtoms+2)]):
            # Skip top lines
            if (idx < 2):
                continue

            # Store atom information
            line = line.strip().split()
            elementList.append(line[0])
            posVec = mathutils.Vector((float(line[1]),float(line[2]),float(line[3])))
            posList.append(posVec)

        # Add frame information
        keyFrameList.append([elementList,posList])

    return keyFrameList

def name_objects(objList):
    '''
    Create names for objects which are part of a list.
    
    INPUT
        objList: (list of str) Object identifiers.
        
    OUTPUT
        nameList: (list of str) List of unique names of objects.
        
    NOTES
        Only implemented for atoms currently. Number and ordering of atoms is assumed constant.
    '''
    
    # Variables
    numObjs = len(objList)
    numDigits = len(str(numObjs))
    nameList = []
    
    # Iterate over objects
    for idx,obj in enumerate(objList):
        nameList.append(obj+'_'+str(idx).zfill(numDigits+1))
        
    return nameList

def setup_style_vdw(keyFrameList):
    '''
    Create structure with VDW style.
    '''

    # Set up scene
    numFrames = len(keyFrameList)
    scene = bpy.context.scene
    scene.frame_start = 1
    scene.frame_end = numFrames+1
    currFrame = bpy.context.scene.frame_start
    bpy.ops.anim.keying_set_active_set(type='Location')

    # Get object names
    nameList = name_objects(keyFrameList[0][0])
    
    # Iterate over atoms in list
    for idx,name in enumerate(nameList):
        # Create initial object
        ele = keyFrameList[0][0][idx]
        pos = keyFrameList[0][1][idx]
        
        # Radius
        radius = element_radius(ele)
        
        # Create sphere
        bpy.ops.mesh.primitive_uv_sphere_add(radius=radius,location=pos)
        activeObject = bpy.context.active_object
        activeObject.name = name
        bpy.ops.object.shade_smooth()
        
        # Set color
        mat = bpy.data.materials.new(name=str(idx))
        mat.diffuse_color = element_color(ele)
        activeObject.data.materials.append(mat)
        
        # Iterate over keyframes
        for frame in range(len(keyFrameList)):
            # Update frame
            bpy.context.scene.frame_set(frame+1)
            
            if (frame > 0):
                # Calculate translation
                oldPos = keyFrameList[frame-1][1][idx]
                newPos = keyFrameList[frame][1][idx]
                transform = newPos-oldPos
            
                # Perform translation
                bpy.ops.transform.translate(value=transform)
                
            # Set keyframe
            bpy.ops.anim.keyframe_insert()
        
############
### Main ###
############
# Variables
xyzName = 'path2.xyz'

# Load XYZ
xyzList = load_xyz(xyzName)

# Display
setup_style_vdw(xyzList)
