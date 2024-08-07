import pygame
import random

pygame.init()
fps = 60
WIDTH = 1000 ; HEIGHT = 600
J_WIDTH = 200; J_HEIGHT = 200
timer=pygame.time.Clock()
screen=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('GAME')
bg_img = pygame.image.load('bg2.png')
img_width, img_height = bg_img.get_size()
crop_width = min(J_WIDTH, img_width)
crop_height = min(J_HEIGHT, img_height)
crop_x = (img_width - crop_width) // 2
crop_y = (img_height - crop_height) // 2
zoom = 30
bg_img = pygame.transform.scale(bg_img.subsurface((zoom, zoom, img_width - 2*zoom, img_height - 2*zoom)), (J_WIDTH, J_HEIGHT))
cars=[]
for i in range(4):
    img=pygame.transform.scale(pygame.image.load(f'car{i+1}.png'),(28,15))
    cars.append(img)
class Car(pygame.sprite.Sprite) :
    choice=0
    def __init__(self,spawn_direction,turn_dir,ambu, junction) :
        super().__init__()
        self.is_ambulance = ambu
        if self.is_ambulance:
            self.carimg=pygame.transform.scale(pygame.image.load("ambulance.png"),(28,15))
            self.image=self.carimg
        else:    
            self.choice=random.randint(0,3)
            self.carimg=cars[self.choice]
            self.image=self.carimg
        #0 - North, 1 - East, 2 - South, 3 - West
        self.displacement = 12
        self.s_dir = spawn_direction
        self.turn_dir = turn_dir
        #print(self.s_dir,self.turn_dir)
        self.notstopped = True
        
        self.turned = False
        self.j = junction
        self.speed = self.j.speed
        self.image_update()
        self.rect = self.image.get_rect(center = (self.cx,self.cy))
        self.spawnx = 0
        self.spawny =0
        
        
        
        self.centerrect = pygame.Rect(self.j.cx-displacement, self.j.cy-displacement, displacement*2,displacement*2)
        
        self.displace()
        self.signal0 = self.j.signal0
        self.signal1 = self.j.signal1
        self.signal2 = self.j.signal2
        self.signal3 = self.j.signal3
        self.next_dir = None
        self.type = None
        
    def image_update(self) :
        dis = 5
        if self.s_dir == 0 :
            self.image = pygame.transform.rotate(self.carimg,-90)
            self.cx = self.j.cx ; self.cy = self.j.y+dis
            self.dy = self.speed
        if self.s_dir == 1 :
            self.image = pygame.transform.rotate(self.carimg,180)
            self.cx = self.j.x + J_WIDTH - dis ; self.cy = self.j.cy
            self.dx = -self.speed
            self.dy = self.speed
        if self.s_dir == 2 :
            self.image = pygame.transform.rotate(self.carimg,90)
            self.cx = self.j.cx ; self.cy = self.j.y + J_HEIGHT - dis
            self.dx = self.speed
            self.dy = -self.speed
        if self.s_dir == 3 :
            self.image = self.carimg
            
            self.cx = self.j.x + dis ; self.cy = self.j.cy
            self.dx = self.speed
            self.dy = self.speed

    def update(self) :
        #self.counter += 1
        self.move_flag = 1
        if self.s_dir == 0 :
            #if self.rect.bottom == HEIGHT : self.dy *= -1
            if not(self.notstopped and not self.signal0.state and self.rect.bottom == self.centerrect.top) :  
                projRect = self.image.get_rect(center = (self.rect.centerx,self.rect.centery + 20))
                for car in car_group :
                    if projRect.colliderect(car) :
                        if projRect.bottom > car.rect.top and projRect.bottom < car.rect.bottom :
                            self.move_flag = 0
                          
                
                if self.move_flag : self.rect.centery += self.dy

        if self.s_dir == 1 :
            #if self.rect.left == 0 : self.dx *= -1
            if not(self.notstopped and not self.signal1.state and self.rect.left == self.centerrect.right) : 
                projRect = self.image.get_rect(center = (self.rect.centerx-20,self.rect.centery))
                for car in car_group :
                    if projRect.colliderect(car) :
                        if projRect.left < car.rect.right and projRect.right > car.rect.right :
                            self.move_flag = 0
                if self.move_flag: self.rect.centerx += self.dx

        if self.s_dir == 2 :
            #if self.rect.top == 0 : self.dy *= -1
            if not(self.notstopped and not self.signal2.state and self.rect.top == self.centerrect.bottom) :
                projRect = self.image.get_rect(center = (self.rect.centerx,self.rect.centery - 20))
                for car in car_group :
                    if projRect.colliderect(car) :
                        if projRect.top < car.rect.bottom and projRect.bottom > car.rect.bottom :
                            self.move_flag = 0
                if self.move_flag: self.rect.centery += self.dy
                
        if self.s_dir == 3 :
            #if self.rect.right == WIDTH : self.dx *= -1
            if not(self.notstopped and not self.signal3.state and self.rect.right == self.centerrect.left) : 
                projRect = self.image.get_rect(center = (self.rect.centerx+20,self.rect.centery))
                for car in car_group :
                    if projRect.colliderect(car) :
                        if projRect.right > car.rect.left and projRect.left < car.rect.left :
                            self.move_flag = 0
                if self.move_flag: self.rect.centerx += self.dx

        
        
        
        self.turn()
        self.junction_update()
        self.ambulance_signal_update()
        #print(self.rect.centerx,self.rect.centery)

    def inner_image_update(self) :
            self.notstopped = False
            self.s_dir = self.turn_dir

            self.image_update()
            cen = (self.j.x + J_WIDTH/2, self.j.y + J_HEIGHT/2)
            if self.s_dir == 0:
                self.rect = self.image.get_rect(center = cen)
            if self.s_dir == 1:
                self.rect = self.image.get_rect(center = cen)
            if self.s_dir == 2:
                self.rect = self.image.get_rect(center = cen)
            if self.s_dir == 3:
                self.rect = self.image.get_rect(center = cen)
            self.displace()


    def turn(self) :
        

        if self.s_dir == 0 or self.s_dir == 2 :
            if self.rect.centery == self.j.y+ J_HEIGHT/2:
                self.inner_image_update()
        if self.s_dir == 1 or self.s_dir == 3 :
            if self.rect.centerx == self.j.x+ J_WIDTH/2:
                self.inner_image_update()
        

        
    
    def displace(self) :
        if self.s_dir == 0 : self.rect.centerx += self.displacement
        if self.s_dir == 1 : self.rect.centery += self.displacement
        if self.s_dir == 2 : self.rect.centerx -= self.displacement
        if self.s_dir == 3 : self.rect.centery -= self.displacement


    def junction_update(self):
        
        x = self.rect.centerx; y = self.rect.centery
        jxx = (x // J_WIDTH)*J_WIDTH
        jyy = (y // J_HEIGHT)*J_HEIGHT
        
        if (self.j.x != jxx or self.j.y != jyy) and (x>=0 and x<WIDTH and y >= 0 and y < HEIGHT) :
            junc_name = str(self.rect.centerx // J_WIDTH) + " " + str(self.rect.centery // J_HEIGHT)
            self.j = junctions[junc_name]
            self.centerrect = pygame.Rect(self.j.cx-displacement, self.j.cy-displacement, displacement*2,displacement*2)
            self.speed = self.j.speed
            self.s_dir = self.turn_dir
            self.turn_dir = random.randint(0,3)
            #print(junc_name,"start dir :",self.s_dir,"turn dir:",self.turn_dir)
            self.notstopped = True

            self.turned = False
            self.signal0 = self.j.signal0
            self.signal1 = self.j.signal1
            self.signal2 = self.j.signal2
            self.signal3 = self.j.signal3
            #print(self.signal0.state,self.signal1.state,self.signal2.state,self.signal3.state,)

            if self.is_ambulance:
                global move_num
                move_num += 1
                self.turn_dir = calculate_turn(moves[move_num+1],moves[move_num])
                #print('amb turndir:',self.turn_dir)

    def ambulance_signal_update(self):
        if self.is_ambulance and self.notstopped: 
            for i in range(4):
                self.j.signals[i].update_state(0)
            self.j.signals[self.s_dir].update_state(1)
                

class Signal(pygame.sprite.Sprite) :
    def __init__(self,dir,j) :
        super().__init__()
        self.direction = dir
        #0 - stop | 1 - go
        self.state = 0
        self.redstate = (255,0,0)
        self.greenstate = (0,0,0)
        self.rad = 10
        self.color = (255,0,0)
        self.x = j.cx
        self.y = j.cy
        


        


        if dir == 0: self.x += self.rad*3 ; self.y -= self.rad*3
        if dir == 1: self.x += self.rad*3 ; self.y += self.rad*3
        if dir == 2: self.x -= self.rad*3 ; self.y += self.rad*3
        if dir == 3: self.x -= self.rad*3 ; self.y -= self.rad*3

        

    def update(self) :
        self.draw_circle()
        #print("yes")
        
        if count == self.direction: 
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                self.update_state(0)
            if keys[pygame.K_DOWN]:
                self.update_state(1)

        
    def update_state(self,state) :
        
        self.state = state
        
        if self.state == 1 : 
            self.color = (0,255,0)
        if self.state == 0 : 
            self.color = (255,0,0)

    def draw_circle(self) :
        pygame.draw.circle(screen, self.color, (self.x,self.y), self.rad)
        if count == self.direction : pygame.draw.rect(screen,(255,255,0), (self.x-self.rad,self.y-self.rad,self.rad*2,self.rad*2),2)




class Junction:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.cx = x+(J_WIDTH/2)
        self.cy = y+(J_HEIGHT/2)
        self.in_cars = []
        self.signal0,self.signal1,self.signal2,self.signal3 = 0,0,0,0
        self.signals = [self.signal0,self.signal1,self.signal2,self.signal3]
        self.ticks = 0
        self.round = random.randint(3,10)*fps
        self.signal_no = 0
        self.weights = [] #weights is a list of weights (distance) of the roads [up,down,left,right]
        self.speed = random.randint(1,2)


    def update(self):
        self.ticks += 1
        if self.ticks >= self.round :
            self.ticks = 0
            for i in range(4):
                if i == self.signal_no:
                    self.signals[i].update_state(1)
                else:
                    self.signals[i].update_state(0)
            self.signal_no = (self.signal_no+1)%4




centerrect = pygame.Rect(WIDTH/2 - 30, HEIGHT/2 - 30, 90,90)
    

junction_group = []
junctions = {}
def add_junctions():
    for x in range(WIDTH//J_WIDTH):
        for y in range(HEIGHT//J_HEIGHT):
            J = Junction(x*J_WIDTH,y*J_HEIGHT)
            junction_group.append(J)
            junctions[str(x)+' '+str(y)] = J



add_junctions()

#signal2 = Signal(2)


    

'''
signal0 = Signal(0,500,100)
signal1 = Signal(1,500,500)
signal2 = Signal(2,100,500)
signal3 = Signal(3,100,100)
car0 = Car(2,3,False)

'''


car_group = pygame.sprite.Group()
signal_group = pygame.sprite.Group()
#car_group.add(car0)
#car_group.add(Car(1,0))
#car_group.add(Car(3,2))
#car_group.add(Car(0,3))
#car_group.add(Car(0,1))


for j in junction_group:
    signal0 = Signal(0,j)
    signal1 = Signal(1,j)
    signal2 = Signal(2,j)
    signal3 = Signal(3,j)

    j.signal0 = signal0
    j.signal1 = signal1
    j.signal2 = signal2
    j.signal3 = signal3

    j.signals = [j.signal0,j.signal1,j.signal2,j.signal3]

    signal_group.add(signal0)
    signal_group.add(signal1)
    signal_group.add(signal2)
    signal_group.add(signal3)



#signal_list = [signal0,signal1,signal2,signal3]

cars_no = [0,0,0,0]


count = 0
green_signal = 0
there_is_a_car = False
there_is_an_ambulance = False

displacement = 30



def generate_moves(start, end):
    start_x, start_y = map(int, start.split())
    end_x, end_y = map(int, end.split())
    
    moves = []
    
    while start_x < end_x :
        start_x += 1
        moves.append(str(start_x)+" "+str(start_y))

    while start_y < end_y :
        start_y += 1
        moves.append(str(start_x)+" "+str(start_y))
    
    return moves

# Example usage:
start = "0 0"
end = "4 3"
moves = generate_moves(start, end)
print(moves)
move_num = 0
def calculate_turn(coord1, coord2):
    x1, y1 = map(int, coord1.split())
    x2, y2 = map(int, coord2.split())
    
    diff_x = x2 - x1
    diff_y = y2 - y1

    if (diff_x, diff_y) == (0,-1) : turn = 0
    if (diff_x, diff_y) == (1,0) : turn = 1
    if (diff_x, diff_y) == (0,1) : turn = 2
    if (diff_x, diff_y) == (-1,0) : turn = 3

    return turn

initial_turn = calculate_turn(moves[1],moves[0])

ambulance = Car(3,initial_turn,True,junctions[start])
car_group.add(ambulance)


#signals = [signal0,signal1,signal2,signal3]
def get_car_number() :
    for car in car_group :
        if car.notstopped :
            cars_no[car.s_dir] += 1
    return cars_no.index(max(cars_no))

def select_junction() :
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        junction_i = (junction_i-1)%(WIDTH/J_WIDTH)
    if keys[pygame.K_d]:
        junction_i = (junction_i+1)%(WIDTH/J_WIDTH)
    if keys[pygame.K_w]:
        junction_y = (junction_i-1)%(HEIGHT/J_HEIGHT)     
    if keys[pygame.K_s]:
        junction_y = (junction_i+1)%(HEIGHT/J_HEIGHT)    


def check_signal() :
    global green_signal
    global there_is_a_car
    global there_is_an_ambulance
    there_is_a_car = False
    there_is_an_ambulance = False
    for car in car_group :
        if car.s_dir == green_signal and car.notstopped :
            there_is_a_car = True

        if car.is_ambulance and car.notstopped : 
            green_signal = car.s_dir
            there_is_an_ambulance = True
    
    if there_is_an_ambulance : 
        signal_list[0].update_state(0)
        signal_list[1].update_state(0)
        signal_list[2].update_state(0)
        signal_list[3].update_state(0)
        signal_list[green_signal].update_state(1)
    
    elif there_is_a_car == False :
        signal_list[green_signal].update_state(0)
        green_signal = get_car_number()
        signal_list[green_signal].update_state(1)





def add_cars() :
    md = 100; f = 100
    x,y = pygame.mouse.get_pos()
    
    junction = junctions[str(x//J_WIDTH) + " " + str(y//J_HEIGHT)]
    
    if x< junction.cx :
        if y < junction.cy : sdir = 3
        else : sdir = 2
    else:
        if y < junction.cy : sdir = 0
        else : sdir = 1

        

    car_group.add(Car(sdir,random.randint(0,3),False,junction))

    

def add_ambulance() :
    f = 100
    x,y = pygame.mouse.get_pos()
    if x <WIDTH/2 + f/2 and x  > WIDTH/2 - f/2 and y < f and y > 0 :
        car_group.add(Car(0,random.randint(0,3),True))

    if x <WIDTH/2 + f/2 and x  > WIDTH/2 - f/2 and y < HEIGHT and y > HEIGHT-f :
        car_group.add(Car(2,random.randint(0,3),True))

    if x <f and x  > 0   and y > HEIGHT/2 - f/2 and y < HEIGHT/2 + f/2 :
        car_group.add(Car(3,random.randint(0,3),True))

    if x > WIDTH-f and x < WIDTH and y > HEIGHT/2 - f/2 and y < HEIGHT/2 + f/2:
        car_group.add(Car(1,random.randint(0,3),True))

def lines():
    displacement = 20
    for j in junction_group:
        pass
        #middleline
        #pygame.draw.line(screen, (255,0,0), (j.cx,j.y), (j.cx,j.y+J_HEIGHT), 1)
        #pygame.draw.line(screen, (255,0,0), (j.x,j.cy), (j.x+J_WIDTH,j.cy), 1)
        
        #borderline
        #pygame.draw.line(screen, (0,255,0), (j.cx + displacement,j.y), (j.cx + displacement,j.y+J_HEIGHT), 1)
        #pygame.draw.line(screen, (0,255,0), (j.x,j.cy + displacement), (j.x+J_WIDTH,j.cy + displacement), 1)
        #pygame.draw.line(screen, (0,255,0), (j.cx - displacement,j.y), (j.cx - displacement,j.y+J_HEIGHT), 1)
        #pygame.draw.line(screen, (0,255,0), (j.x,j.cy - displacement), (j.x+J_WIDTH,j.cy - displacement), 1)

        
        #centerrect
        #pygame.draw.rect(screen,(255,0,255), (j.cx-displacement, j.cy-displacement, displacement*2,displacement*2),1)
        
        #junctionborder
        #pygame.draw.rect(screen,(0,34,73),(j.x,j.y,J_WIDTH,J_HEIGHT),1)

def draw_background():
    for x in range(WIDTH//J_WIDTH):
        for y in range(HEIGHT//J_HEIGHT):
            screen.blit(bg_img,(x*J_WIDTH,y*J_HEIGHT))

run = True
#signal0.update_state(1)
while run :
    timer.tick(fps)
    screen.fill((64,64,64))
    
    
    draw_background()
    lines()
 

    car_group.draw(screen)
    #signal_group.draw(screen)
    
    for event in pygame.event.get() :
        if event.type==pygame.QUIT:
            run=False
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_LEFT :
                count -= 1
                count %= 4
            if event.key == pygame.K_RIGHT :
                count += 1
                count %= 4
        if event.type == pygame.MOUSEBUTTONDOWN :
            if event.button == 1 :
                add_cars()
            if event.button == 3:
                add_ambulance()
        
        
    for junction in junction_group:
        junction.update()
    car_group.update()
    signal_group.update()
    
    #check_signal()
    pygame.display.flip()

pygame.quit()