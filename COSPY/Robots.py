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
    def __init__(self,
                 x,
                 y,
                 speed,
                 angle_speed,
                 randomness,
                 deposit_size,
                 deposit_rate,
                 pheromone_dist,
                 robot_dist,
                 boundary_function,
                 stop_time,
                 immune_time,
                 use_temperature,
                 leaders_follow):
        self.x = x
        self.y = y 
        self.angle=0
        self.pheromone_dist = pheromone_dist
        self.robot_dist = robot_dist
        self.colour = [255,255,255,255]
        self.leader=False
        self.leaders_follow=leaders_follow
        self.waiting = 0
        self.edge_mode = boundary_function#wrap,bounce,none
        self.angle_speed = angle_speed
        self.speed = speed
        self.randomness = randomness
        self.deposit_size = deposit_size
        self.deposit_rate = deposit_rate
        self.stop_time = stop_time
        self.immune_time = immune_time
        self.use_temperature = use_temperature

    def move(self,pixels):
        if self.waiting>self.immune_time:
            self.waiting-=1
            return
        #Go towards pheromone
        #Check 4 positions and turn more towards strongest pheromone
        if self.leader and not self.leaders_follow:#self.leader:
            self.angle+=random.uniform(-self.randomness,self.randomness)
        else:
            #Check 2 positions first
            check_left_angle = self.angle-1
            check_left_x = int(self.x+math.cos(check_left_angle)*self.pheromone_dist)
            check_left_y = int(self.y+math.sin(check_left_angle)*self.pheromone_dist)

            check_right_angle = self.angle+1
            check_right_x = int(self.x+math.cos(check_right_angle)*self.pheromone_dist)
            check_right_y = int(self.y+math.sin(check_right_angle)*self.pheromone_dist)
    

            #Check scanners are not outside range, unless wrap
            if self.edge_mode!="Wrap":
                if check_left_x>len(pixels)-1 or check_left_x<0 or check_left_y>len(pixels[0])-1 or check_left_y<0:
                    px_left = [0,0,0,0]
                else:
                    px_left = pixels[check_left_x][check_left_y]
                if check_right_x>len(pixels)-1 or check_right_x<0 or check_right_y>len(pixels[0])-1 or check_right_y<0:
                    px_right = [0,0,0,0]
                else:
                    px_right = pixels[check_right_x][check_right_y]
            else:
                px_left = pixels[loop_value(check_left_x,len(pixels)-1)][loop_value(check_left_y,len(pixels[0])-1)]
                px_right = pixels[loop_value(check_right_x,len(pixels)-1)][loop_value(check_right_y,len(pixels[0])-1)]

            #IT'S ONLY DETECTING RED RIGHT NOW! Find strongest pheromone colour
            #Create function to do detection dependent on pheromone colour
            if self.get_strength(px_left)>self.get_strength(px_right):
                self.angle-=self.angle_speed
            elif self.get_strength(px_left)<self.get_strength(px_right):
                self.angle+=self.angle_speed
            else:
                self.angle+=random.uniform(-self.randomness,self.randomness)

            
        new_x = self.x+math.cos(self.angle)*self.speed
        new_y = self.y+math.sin(self.angle)*self.speed

        #MOVING ON THE X-AXIS
        if new_x>0 and new_x<len(pixels):
            self.x=new_x
        elif self.edge_mode=="Bounce":
            self.angle+=math.pi
        elif self.edge_mode=="Wrap":
            #Wrap back around
            #If above
            self.x = new_x % (len(pixels)-1)
            #If below

        #MOVING ON THE Y-AXIS
        if new_y>0 and new_y<len(pixels[0]):
            self.y=new_y
        elif self.edge_mode=="Bounce":
            self.angle+=math.pi
        elif self.edge_mode=="Wrap":
            #Wrap back around
            #If above
            self.y = new_y % (len(pixels[0])-1)
            #if below


        #ITERATE THE WAITING VALUE
        if self.waiting>0:
            self.waiting-=1

        

    def deposit(self,renderer):
        if self.leader:
            renderer.add_pheromone(self.x,self.y,self.deposit_size,self.deposit_rate)

    def get_strength(self,pixel):
        return pixel[3]

    def __array__(self) -> np.ndarray:
        return np.array([self.x, self.y])
    
    def in_pheromone(self,pixels):
        if pixels[int(self.x)][int(self.y)][3]>0:
            return True
        return False

    
    def encounter(self):
        if self.waiting<=0:
            self.waiting = self.stop_time+self.immune_time

    def temperature_linear_encounter(self,env_pixels):
        if self.waiting<=0:
            self.waiting = (self.stop_time+self.immune_time)*(env_pixels[int(self.x)][int(self.y)][3]/255)#

    def temperature_exponential_encounter(self,env_pixels):
        if self.waiting<=0:
            self.waiting = (self.stop_time+self.immune_time)*((env_pixels[int(self.x)][int(self.y)][3]/255)**2)


def loop_value(val,threshold):
    return val%threshold