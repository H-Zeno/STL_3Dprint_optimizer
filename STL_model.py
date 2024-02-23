import numpy as np
from math import cos
from math import sin
import logging



# triangle data strucure
# a triangle is defined by 3 vertices and one normal vector
class triangle:
    
    # construct triagles
    def __init__(self, p1, p2, p3, n=None):
        self.vertices = np.array([p1, p2, p3]) # set the vertices
    
        if n != None: 
            self.normal = n
        else:
            self.normal = self.normal_vector(p1, p2, p3) # set the normal vector (if it was not set with the constructor)
            
    def normal_vector(self, p1, p2, p3):
        p12 = p2 - p1
        p13 = p3 - p1
        return np.cross(p12, p13)
    
    
class STL_model():
    
    # Attributes that define an STL model
    def __init__(self, filename):
        self.filename = filename
        self.triangles = []
        self.centroid = None
        self.volume = None
        self.name = None
 
 
    # Read the ASCII STL file
    def read_stl_text(self):
        print("Attempting to read ASCII type STL file:", self.filename)
        
        text = open(self.filename, 'r')
        
        # loop through each text line
        for line in text:
            words = line.split()
            if len(words) > 0:
                
                # Start of the STL file
                if words[0] == "solid":
                    try :
                        self.name = words[1]
                    except IndexError:
                        self.name = "Unnamed"
                    
                # Start of a triangle, read normal vector
                if words[0] == "facet":
                    vertices = []
                    normal = [float(words[2]), float(words[3]), float(words[4])] #edge case: what if normal is not defined?
                    
                # Read the triangle vertices
                if words[0] == "vertex":
                    vertices.append([float(words[1]), float(words[2]), float(words[3])]) #vertex coordinates
                    
                # End of a triangle, append triangle data to the list of triangles
                if words[0] == "endfacet":
                    if len(vertices) == 3: 
                        self.triangles.append(triangle(vertices[0], vertices[1], vertices[2], normal))
                    else:
                        logging.exception("Less than 3 vertices were found (3 vertices are required to define a triangle)")
        
        text.close()
        
        
        
    def write_stl(self, file_path=self.filename, type='text'):
        print("Writing STL file to:", file_path)
        
        # open the file for writing
        if type != 'text':
            try:
                stl_file = open(file_path, 'wb') #wb: write binary
                logging.info("Opening %s for binary write succesfull", file_path)
            except PermissionError:
                logging.exception("Permission Error, Could not write a binary STL file to %s", file_path)
        else:
            try:
                stl_file = open(file_path, 'w')
                logging.info("Opening %s for ASCII (text) write succesfull", file_path)
            except PermissionError:
                logging.exception("Permission Error, Could not write a text STL file to %s", file_path)
        
        # write the content of the STL file in text
        stl_file.write(f'solid {self.name} \n')
        for tri in self.triangles:                
            stl_file.write(f'facet normal {tri.normal[0]} {tri.normal[1]} {tri.normal[2]} \n')
            stl_file.write('outer loop \n')
            for vertex in tri.vertices:
                stl_file.write(f'vertex {vertex[0]} {vertex[1]} {vertex[2]} \n')
            stl_file.write('endloop \n')
            stl_file.write('endfacet \n')
        stl_file.write(f'endsolid {self.name} \n')
         
        stl_file.close()

    
    ######################## Manipulation Methods ######################## 
    
    # scales the model by a factor
    def scale(self, scale):
        for tri in self.triangles:
            for vertex in tri.vertices:
                vertex[0] = scale*vertex[0]
                vertex[1] = scale*vertex[1]
                vertex[2] = scale*vertex[2]
        
    
                

            
            
            
                
        
        
         

    
    





#def read_stl_binary(filename):\

    



# Code to write the new STL file



# workflow

# 1. Load the STL model

# 2. Make manipulations on the loaded STL file

# 3. Export the new STL file (to the same or another file)