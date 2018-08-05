import pygame

# Each instance has a name and image
class Element:
    def __init__(self,name):
        self.name = name

        try:
            self.image = pygame.image.load(f"Images/{self.name}.jpg")
        except:
            try:
                self.image = pygame.image.load("Images/fire.jpg")
            except:
                raise

class Inventory:
    def __init__(self,surface,font):
        # raw data: "name1; name2,name3" ----> processed data: {name1:[name2,name3]}
        self.elementData = {info.split("; ")[0]:info.split("; ")[-1].split(",") for info in open("elementData.txt","r").read().split("\n")}

        # makes element grid from element data
        self.grid = []
        tmp = []
        for key in self.elementData.keys():
            tmp.append([Element(key),False if not key in "fire,water,earth,air".split(",") else True])

            if len(tmp) >= 14:
                self.grid.append(tmp)
                tmp = []

        # inventory interface dimensions
        self.inventory_dim = [800,400]

        # rect object for each icon
        self.rects = [[pygame.Rect(105+(p1*(self.inventory_dim[0]/len(row))),305+(p0*(self.inventory_dim[1]/len(self.grid))),50,50) for p1,item in enumerate(row)] for p0,row in enumerate(self.grid)]

        # surface and font used
        self.surface = surface
        self.font = font

    def select(self,mouse,merger):
        # finds icon clicked
        for p0,i in enumerate(self.rects):
            for p1,j in enumerate(i):
                if self.grid[p0][p1][1] and pygame.Rect(mouse[0]-1,mouse[1]-1,2,2).colliderect(j):
                    self.grid[p0][p1][1] = True
                    return self.grid[p0][p1][0]

    def draw(self):
        basex = 105
        basey = 305

        # outline
        pygame.draw.rect(self.surface,(0,0,0),(100,300,self.inventory_dim[0],self.inventory_dim[1]),4)

        # icon + name
        for p0,row in enumerate(self.grid):#each img is 50px by 50px
            for p1,item in enumerate(row):
                if item[1]:
                    self.surface.blit(item[0].image,(basex+(p1*(self.inventory_dim[0]/len(row))),basey+(p0*(self.inventory_dim[1]/len(self.grid)))))
                    txt = self.font.render(str(item[0].name),True,(0,0,0))
                    self.surface.blit(txt,txt.get_rect(center=(basex+25+(p1*(self.inventory_dim[0]/len(row))),(85 if not p1 % 2 else 65)+basey+(p0*(self.inventory_dim[1]/len(self.grid))))))
                else:
                    pygame.draw.rect(self.surface,(150,150,150),(basex+(p1*(self.inventory_dim[0]/len(row))),basey+(p0*(self.inventory_dim[1]/len(self.grid))),50,50),0)                   

class Merger:
    def __init__(self,surface,font):
        self.inputs = []
        self.output = None

        # design features
        self.boxes = [[250,100],[450,100],[650,100]]
        self.other1 = [350,100]
        self.other2 = [550,100]

        # surface and font used
        self.surface = surface
        self.font = font
        
        self.elementData = {info.split("; ")[0]:info.split("; ")[-1].split(",") for info in open("elementData.txt","r").read().split("\n")}

    def update(self,Object=None):
        # appends new element to inputs if queue is not full
        if Object is not None and not len(self.inputs) >= 2:
            self.inputs.append(Object)

    def get_output(self,inputs):
        # checks in recipes for a matching combination
        for product,param in self.elementData.items():
            if inputs[0].name in param:
                tmp = param[:]
                del tmp[tmp.index(inputs[0].name)]
                if inputs[1].name in tmp:
                    return Element(product)

    def draw(self):
        if len(self.inputs) == 2:
            self.output = self.get_output(self.inputs)
        else:
            self.output = None

        # draws outlines, icons and names
        for p,box in enumerate(self.boxes):
            try:
                pygame.draw.rect(self.surface,(0,0,0),[box[0],box[1],100,100],4)

                if p < 2:
                    self.surface.blit(self.inputs[p].image,[i+25 for i in box])
                    text = self.font.render(self.inputs[p].name,True,(0,0,0))
                else:
                    self.surface.blit(self.output.image,[i+25 for i in box])
                    text = self.font.render(self.output.name,True,(0,0,0))
                self.surface.blit(text,text.get_rect(center=[box[0]+50,box[1]+90]))
            except:
                pass

        # design features -> "+","="
        pygame.draw.line(self.surface,(0,0,0),(self.other1[0]+50,self.other1[1]+20),(self.other1[0]+50,self.other1[1]+80),10)
        pygame.draw.line(self.surface,(0,0,0),(self.other1[0]+20,self.other1[1]+50),(self.other1[0]+80,self.other1[1]+50),10)
        pygame.draw.line(self.surface,(0,0,0),(self.other2[0]+20,self.other2[1]+40),(self.other2[0]+80,self.other2[1]+40),10)
        pygame.draw.line(self.surface,(0,0,0),(self.other2[0]+20,self.other2[1]+60),(self.other2[0]+80,self.other2[1]+60),10)

    def interact(self,mouse,inventory):
        # if mouse collided with input[0] and input[0] is filled
        if len(self.inputs) > 0 and self.inputs[0] is not None and pygame.Rect(mouse[0]-1,mouse[1]-1,2,2).colliderect(self.boxes[0][0],self.boxes[0][1],100,100):
            del self.inputs[0]

        # if mouse collided with input[1] and input[1] is filled
        if len(self.inputs) > 1 and self.inputs[1] is not None and pygame.Rect(mouse[0]-1,mouse[1]-1,2,2).colliderect(self.boxes[1][0],self.boxes[1][1],100,100):
            del self.inputs[1]

        # if mouse collided with output and output is filled
        if pygame.Rect(mouse[0]-1,mouse[1]-1,2,2).colliderect(self.boxes[-1][0],self.boxes[-1][1],100,100) and self.output is not None:
            for p1,row in enumerate(inventory.grid):
                for p2,item in enumerate(row):
                    if item[0].name == self.output.name:
                        inventory.grid[p1][p2][1] = True
            # clears inputs
            self.inputs = []
            self.output = None

        return inventory
