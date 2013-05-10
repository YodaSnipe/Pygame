"""
 Simulation of 3D Cube Rotation.
"""
import sys, math, pygame, random
from pygame.locals import K_UP, K_DOWN, K_RIGHT, K_LEFT
from operator import itemgetter

"""
Points Class
"""
class Point3D:
    def __init__(self, x = 0, y = 0, z = 0):
        self.x, self.y, self.z = float(x), float(y), float(z)
 
    """ Rotates the point around the X axis by the given angle in degrees. """
    def rotateX(self, angle):
        
        #determines radians
        rad = angle * math.pi / 180
        
        #cos of radians
        cosa = math.cos(rad)
        
        #sin of radians
        sina = math.sin(rad)
        
        #determine new y value
        y = self.y * cosa - self.z * sina
        
        #determine new z value
        z = self.y * sina + self.z * cosa
        
        #return Point3D (rotating around X axis, therefore no change in X value)
        return Point3D(self.x, y, z)
 
    """ Rotates the point around the Y axis by the given angle in degrees. """
    def rotateY(self, angle):
        
        #detemines radians
        rad = angle * math.pi / 180
        
        #cos of radians
        cosa = math.cos(rad)
        
        #sin of radians
        sina = math.sin(rad)
        
        #calculate new z value
        z = self.z * cosa - self.x * sina
        
        #calculate new x value
        x = self.z * sina + self.x * cosa
        
        #return Point3D (rotating around Y axis, therefore no change in Y value)
        return Point3D(x, self.y, z)
 
    """ Rotates the point around the Z axis by the given angle in degrees. """
    def rotateZ(self, angle):
        
        #determines radians
        rad = angle * math.pi / 180
        
        #cos of radians
        cosa = math.cos(rad)
        
        #sin of radians
        sina = math.sin(rad)
        
        #calculate new x value
        x = self.x * cosa - self.y * sina
        
        #calculate new y value
        y = self.x * sina + self.y * cosa
        
        #return Point3D (rotating around Z axis, therefore no change in Z value)
        return Point3D(x, y, self.z)
 
    """ Transforms this 3D point to 2D using a perspective projection. """
    def project(self, win_width, win_height, fov, viewer_distance):
        
        #factor using field of vision
        factor = fov / (viewer_distance + self.z)
        
        #x value
        x = self.x * factor + win_width / 2
        
        #y value
        y = -self.y * factor + win_height / 2
        
        #return Point3D (2D point, z=1)
        return Point3D(x, y, self.z)



"""
Simulation Class
"""
class Simulation:
    
    """ init """
    def __init__(self, win_width = 640, win_height = 480):
        
        pygame.init()
 
        #set screen to certain width and height
        self.screen = pygame.display.set_mode((win_width, win_height))
        
        #set caption
        pygame.display.set_caption("Simulation of 3D Cube Rotation")
 
        #system clock time
        self.clock = pygame.time.Clock()
 
        #create box vertices
        self.vertices = [
            Point3D(-1,1,-1),
            Point3D(1,1,-1),
            Point3D(1,-1,-1),
            Point3D(-1,-1,-1),
            Point3D(-1,1,1),
            Point3D(1,1,1),
            Point3D(1,-1,1),
            Point3D(-1,-1,1)
        ]
        
        #Faces correspond to 4 Point3Ds
        self.faces  = [(0,1,2,3),(1,5,6,2),(5,4,7,6),(4,0,3,7),(0,4,5,1),(3,2,6,7)]

        # Define colors for each face
        self.colors = [(255,0,255),(255,0,0),(0,255,0),(0,0,255),(0,255,255),(255,255,0)]

        self.angleX, self.angleY, self.angleZ = 0, 0, 0
        
    """ Rotates the cube in the given direction """
    def rotate(self, direction):
        
        # It will hold transformed vertices.
        tVertices = []
        
        for vertex in self.vertices:
            # Rotate the point around X axis, then around Y axis, and finally around Z axis.
            rotation = vertex.rotateX(self.angleX).rotateY(self.angleY).rotateZ(self.angleZ)
            # Transform the point from 3D to 2D
            projection = rotation.project(self.screen.get_width(), self.screen.get_height(), 256, 4)
            # Put the point in the list of transformed vertices
            tVertices.append(projection)

        # Calculate the average Z values of each face.
        avgZ = []
        i = 0
        for f in self.faces:
            z = (tVertices[f[0]].z + tVertices[f[1]].z + tVertices[f[2]].z + tVertices[f[3]].z) / 4.0
            avgZ.append([i,z])
            i = i + 1

        #Sort the "z" values in reverse and display the foremost faces last
        for zVal in sorted(avgZ,key=itemgetter(1),reverse=True):
            fIndex = zVal[0]
            f = self.faces[fIndex]
            pointList = [(tVertices[f[0]].x, tVertices[f[0]].y), (tVertices[f[1]].x, tVertices[f[1]].y),
                         (tVertices[f[1]].x, tVertices[f[1]].y), (tVertices[f[2]].x, tVertices[f[2]].y),
                         (tVertices[f[2]].x, tVertices[f[2]].y), (tVertices[f[3]].x, tVertices[f[3]].y),
                         (tVertices[f[3]].x, tVertices[f[3]].y), (tVertices[f[0]].x, tVertices[f[0]].y)]
            pygame.draw.polygon(self.screen,self.colors[fIndex],pointList)
 
        #increment angles to simulate rotation in the given direction
        if (direction == "UP"):
            self.angleX += 2
        elif (direction == "DOWN"):
            self.angleX -= 2
        elif (direction == "LEFT"):
            self.angleY += 2
        elif (direction == "RIGHT"):
            self.angleY -= 2
        
        #updates display surface to screen
        pygame.display.flip()
 
 
    
    def colorFade(self, origColor, fadeInColor):
        #check background color status
        if (origColor[0] != fadeInColor[0]):
            if (origColor[0] < fadeInColor[0]):
                origColor[0]+= 1
            else:
                origColor[0]-= 1
        
        if (origColor[1] != fadeInColor[1]):
            if (origColor[1] < fadeInColor[1]):
                origColor[1]+= 1
            else:
                origColor[1]-= 1
                
        if (origColor[2] != fadeInColor[2]):
            if (origColor[2] < fadeInColor[2]):
                origColor[2]+= 1
            else:
                origColor[2]-= 1
            
        #update background color
        self.screen.fill(origColor)
 
    def run(self):
        
        #starting background color
        origColor = [255,0,0]
        
        #fade in color background
        fadeInColor = [random.randint(0,255),random.randint(0,255),random.randint(0,255)]
        
        #fill background
        self.screen.fill(origColor)
        
        #initial display
        self.rotate("UP")
        
        #updates display surface to screen
        pygame.display.flip()
        
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            
            #delay
            self.clock.tick(50)
            
            if (origColor == fadeInColor):
                #fade in color background
                fadeInColor = [random.randint(0,255),random.randint(0,255),random.randint(0,255)]
            
            #grabs the pressed keys
            keys = pygame.key.get_pressed()
            if (keys[K_UP]):
                #Rotation
                self.rotate("UP")
                
                #Color Fading
                self.colorFade(origColor, fadeInColor)
                
            if (keys[K_DOWN]):
                #Rotation
                self.rotate("DOWN")
                
                #Color Fading
                self.colorFade(origColor, fadeInColor)
                
            if (keys[K_LEFT]):
                #Rotation
                self.rotate("LEFT")
                
                #Color Fading
                self.colorFade(origColor, fadeInColor)
                
            if (keys[K_RIGHT]):
                #Rotation
                self.rotate("RIGHT")
                
                #Color Fading
                self.colorFade(origColor, fadeInColor)
                

if __name__ == "__main__":
    Simulation().run()
