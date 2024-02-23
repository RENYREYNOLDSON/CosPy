import random
import math

# CLASS FOR VIRTUAL ROBOTS
class Robot:
    def __init__(self,x,y):
        self.x = x
        self.y = y 
        self.angle=0
        self.radius=25
        self.colour=[255,255,255]
        self.leader=True
    def move(self,pixels):
        #Go towards pheromone
        #Check 4 positions and turn more towards strongest pheromone
        if 2>1:#self.leader:
            self.angle+=random.uniform(-0.4,0.4)
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
                    self.angle-=0.4
                elif px_right[2]>px_left[2]:
                    self.angle+=0.4
                else:
                    self.angle+=random.uniform(-0.4,0.4)
            except:
                pass
            
        new_x = self.x+math.cos(self.angle)
        new_y = self.y+math.sin(self.angle)

        if new_x>self.radius and new_x<len(pixels)-self.radius:
            self.x=new_x
        if new_y>self.radius and new_y<len(pixels[0])-self.radius:
            self.y=new_y
        

    def deposit(self,renderer):
        if self.leader:
            renderer.add_pheromone(self.x+self.radius*renderer.scale,self.y+self.radius*renderer.scale)

    #draw
    #move
    #disperse
    #detect
        