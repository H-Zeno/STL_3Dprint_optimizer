import logging
from math import cos, sin
import numpy as np



# helper functions to calculate the rotation matrix (theta is in radians)
def rotX(theta):
    R = np.array([[1, 0, 0],[0, cos(theta), sin(theta)],[0, -sin(theta), cos(theta)]])
    return R

def rotY(theta):
    R = np.array([[cos(theta), 0, -sin(theta)],[0, 1, 0],[sin(theta), 0, cos(theta)]])
    return R

def rotZ(theta):
    R = np.array([[cos(theta), sin(theta), 0],[-sin(theta), cos(theta), 0],[0, 0, 1]])
    return R
    

# triangle data strucure: a triangle is defined by 3 vertices and one normal vector
class triangle:
    
    # construct triagles
    def __init__(self, p1, p2, p3, n=None):
        self.vertices = np.array([p1, p2, p3]) # set the vertices
    
        if n is None: 
            self.normal = self.normal_vector(p1, p2, p3) # set the normal vector (if it was not set with the constructor) #Still needs to be tested! 
        else:
            self.normal = n
            
    def normal_vector(self, p1, p2, p3):
        p12 = p2 - p1
        p13 = p3 - p1
        return np.cross(p12, p13)
    
class STL_model():
    
    # Attributes that define an STL model
    def __init__(self, filename):
        self.filename = filename
        self.triangles = []
        self.volumes = []
        self.centroid = None
        self.volume = None
        self.name = None
        

    # Read the ASCII STL file
    def read_stl_text(self):
        print("Attempting to read STL file (ASCII type):", self.filename)
        text = open(self.filename, 'r', encoding='ASCII')
       
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
        
        # read the centroid and the total volume of the STL model
        self.calc_centroid()
        
        print('Read ACII STL file', self.filename, 'succesfully!')
        text.close()
        
    # extra functionality (possible extension) -> Read the binary STL file 
    # def read_stl_bin(self):
    #     print("Attempting to read STL file (binary type):", self.filename)
    #     text = open(self.filename, 'rb')
        
    # write the STL file (in text (ASCII) or binary format)
    def write_stl_text(self, file_path=None):
        
        if file_path is None:
            file_path = self.filename
        print("Writing STL file (ASCII format) to:", file_path)
        
        # open the file for writing
        try:
            stl_file = open(file_path, 'w', encoding='ASCII') #wb: write binary
            logging.info("Opening %s for binary write succesfull", file_path)
        except PermissionError:
            logging.exception("Permission Error, Could not write a binary STL file to %s", file_path)
            
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
        
    # Possible Extension -> write the binary STL file

    # To calculate the centroid of the model (necessary for the rotation functionality), we calculate the centroid of each tetrahedron (origin + 3 vertices of the triangle)
    # we weigh the centre of mass of each tetrahedron by the volume of the respective tetrahedron
    def calc_centroid(self):
        triangle_centroids = []
        self.volumes = []
        self.volume = 0
        
        for tri in self.triangles:
            p1, p2, p3 = tri.vertices[0], tri.vertices[1], tri.vertices[2]
            volume = 1/6 * abs(np.linalg.det(np.array([p1, p2, p3]).T)) # scalar triple product, equivalent to determinant (volume of the tetrahedron)
            triangle_centroids.append((p1 + p2 + p3)/4) #4 since the origin (0,0,0) is the fourth vertex of the tetrahedron
            self.volume += volume 
            self.volumes.append(volume)
        
        print('Volumes:', self.volumes)
        self.centroid = np.average(triangle_centroids, axis=0, weights=self.volumes)
    
    
    ######################## Manipulation Methods ######################## 
    
    # scales the model by a factor
    def scale(self, scale):
        for tri in self.triangles:
            for vertex in tri.vertices:
                vertex[0] = scale*vertex[0]
                vertex[1] = scale*vertex[1]
                vertex[2] = scale*vertex[2]
                
    # translate the model by a vector
    def translate(self, vector):
        for tri in self.triangles:
            for vertex in tri.vertices:
                vertex[0] = vertex[0] + vector[0]
                vertex[1] = vertex[1] + vector[1]
                vertex[2] = vertex[2] + vector[2]
              
    # rotate the STL model (with a rotation matrix as an imput)
    def rotate(self, R):
        
        # to rotate the model, we need to find the centre of mass (centroid) of the model
        if self.centroid is None:
            self.calc_centroid()
        
        # update the vertices of each triangle
        for tri in self.triangles:
            for i, vertex in enumerate(tri.vertices):
                tri.vertices[i] = R @ (vertex - self.centroid) + self.centroid
        # update the normal vector of each triangle
        for tri in self.triangles:
            tri.normal = tri.normal_vector(tri.vertices[0], tri.vertices[1], tri.vertices[2])
        
        print('Model rotated succesfully!')
        
        # reset the centroid to None (since the model has been moved)
        self.centroid = None
        self.volumes = []
    
        
