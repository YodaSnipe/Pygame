"""
 Simulation of 3D Point Rotation.
"""
import sys, math, pygame

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
 
    def rotateZ(self, angle):
        """ Rotates the point around the Z axis by the given angle in degrees. """
        
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
 
    def project(self, win_width, win_height, fov, viewer_distance):
        """ Transforms this 3D point to 2D using a perspective projection. """
        
        #factor using field of vision
        factor = fov / (viewer_distance + self.z)
        
        #x value
        x = self.x * factor + win_width / 2
        
        #y value
        y = -self.y * factor + win_height / 2
        
        #return Point3D (2D point, z=1)
        return Point3D(x, y, 1)

class Simulation:
    def __init__(self, win_width = 640, win_height = 480):
        pygame.init()
 
        #set screen to certain width and height
        self.screen = pygame.display.set_mode((win_width, win_height))
        
        #set caption
        pygame.display.set_caption("Simulation of 3D Point Rotation (http://codentronix.com)")
 
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
 
        #default angles
        self.angleX, self.angleY, self.angleZ = 0, 0, 0
 
    def run(self):
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
 
            #delay
            self.clock.tick(50)
            
            #black screen
            self.screen.fill((0,0,0))
 
            for v in self.vertices:
                
                #Rotate the point around X axis, then around Y axis, and finally around Z axis.
                r = v.rotateX(self.angleX).rotateY(self.angleY).rotateZ(self.angleZ)
                
                #Transform the point from 3D to 2D
                p = r.project(self.screen.get_width(), self.screen.get_height(), 256, 4)
                
                #get x, and y values
                x, y = int(p.x), int(p.y)
                
                #draw point
                self.screen.fill((255,255,255),(x,y,2,2))
 
            #increment angles to simulate rotation
            self.angleX += 1
            self.angleY += 1
            self.angleZ += 1
            
            #updates display surface to screen
            pygame.display.flip()
 
if __name__ == "__main__":
    Simulation().run()
