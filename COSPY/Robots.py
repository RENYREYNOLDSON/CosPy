########################
########################
########################  ROBOT TEMPLATE CODE FOR COSPY
######################## 
########################
########################


import random
import math
import numpy as np

# CLASS FOR VIRTUAL ROBOTS
class Robot:
    def __init__(self,x,y):
        self.x = x
        self.y = y 
        self.angle=0
        self.radius=25
        self.colour=[255,255,255]
        self.leader=False
        self.leaders_follow=False
        self.edge_mode = "Bounce"#wrap,bounce,none
        self.angle_speed = 0.4
        self.speed = 0.5

    def move(self,pixels):
        #Go towards pheromone
        #Check 4 positions and turn more towards strongest pheromone
        if self.leader and not self.leaders_follow:#self.leader:
            self.angle+=random.uniform(-self.angle_speed,self.angle_speed)
        else:
            #Check 2 positions first
            check_left_angle = self.angle-1
            check_left_x = int(self.x+math.cos(check_left_angle)*self.radius)
            check_left_y = int(self.y+math.sin(check_left_angle)*self.radius)

            check_right_angle = self.angle+1
            check_right_x = int(self.x+math.cos(check_right_angle)*self.radius)
            check_right_y = int(self.y+math.sin(check_right_angle)*self.radius)
    
            try:
                px_left = pixels[check_left_x][check_left_y]
                px_right = pixels[check_right_x][check_right_y]

                if px_left[2]>px_right[2]:
                    self.angle-=self.angle_speed
                elif px_right[2]>px_left[2]:
                    self.angle+=self.angle_speed
                else:
                    self.angle+=random.uniform(-self.angle_speed,self.angle_speed)
            except:
                pass
            
        new_x = self.x+math.cos(self.angle)*self.speed
        new_y = self.y+math.sin(self.angle)*self.speed
        #Check if not hitting wall
        if new_x>0 and new_x<len(pixels):
            self.x=new_x
        elif self.edge_mode=="Bounce":
            self.angle+=math.pi
        elif self.edge_mode=="Wrap":
            #Wrap back around
            #If above
            self.x = new_x % (len(pixels)-1)
            #If below
        if new_y>0 and new_y<len(pixels[0]):
            self.y=new_y
        elif self.edge_mode=="Bounce":
            self.angle+=math.pi
        elif self.edge_mode=="Wrap":
            #Wrap back around
            #If above
            self.y = new_y % (len(pixels[0])-1)
            #if below

        

    def deposit(self,renderer):
        if self.leader:
            renderer.add_pheromone(self.x,self.y)
    def __array__(self) -> np.ndarray:
        return np.array([self.x, self.y])
    #draw
    #move
    #disperse
    #detect
    #Reproduce
    #Can have custom variables for resources
            
# Focus on the robot programming interface
# This must be for each time step, but could be written more generally maybe?
            
#Get left value, Get right value
#Increment angle in direction
#Place pheromone
#Detect objects
#Detect pheromone
#Detect other robots
#The robot class will import/use this custom function inteface
            
#Rules for what to do for each colour
#Rules for how to move normally
#Rules for objects

#Pseudocode, pheromone ordered in priority
"""
Agent Name: Ant

iterator:
check pheremones
release pheromones
move

pheromone 1:
turn angle towards = 1

pheromone 2 :
turn angle away = 2
move away

pheromone 3: 
angle and move around value

{
    name:"Ant",
    pheromones:{
        "(255,0,0,0)":{
            turn_towards = 1
        },
        "(0,255,0,0)":{
            turn_towards = -1
        }
    }
}

"""        

#Use Beeclust for 1sts tests
#Multiple pheromone types
#Add if we can view layers
#Add export features