# FlyX.py by Collins Kalyebi, Miguel Sanchez, Jennafer Dankenbring
#FlyX is a flappy bird game simulation
# 12/14/2017
    
from graphics import *
from random import randrange

class GUI:

    def __init__(self):
        #create window and set coordinates
        self.win = GraphWin("FlappyBird", 960, 640, autoflush = False)
        self.win.setCoords(0,-10, 150, 100)

        #insert gif as background
        background = Image(Point(75,50), "background1.gif")
        background.draw(self.win)

        #set lower boundary
        ground = Rectangle(Point(0,1),Point(150,-10))
        ground.setFill("black")
        ground.draw(self.win)

        #set higher boundary
        ceiling = Rectangle(Point(0,100),Point(150,90))
        ceiling.setFill("black")
        ceiling.draw(self.win)
        
                            
                           
        
                           

        
class Bird:

    def __init__(self,GUI):
        #calls GUI class
        self.gui = GUI

        #creates bird parts
        #creates blindside eye
        self.eye2 = Circle(Point(22,42),1)
        self.eye2.setFill("white")
        self.eye2.setOutline('white')

        #creates bird body
        self.body = Circle(Point(20, 40), 3)
        self.body.setFill("black")

        #creates bird beak
        self.beak = Polygon(Point(22.5,41.5),Point(26,40),Point(22.5,38.5))
        self.beak.setFill("orange")
        self.beak.setOutline("orange")

        #creates intial wing
        self.wing1 = Polygon(Point(20,40),Point(17,40),Point(15.5,39.5),Point(18.5,39.5))
        self.wing1.setFill("orange")
        self.wing1.setOutline("orange")

        #creates moving wing
        self.wing2 = Polygon(Point(20,40),Point(17,40),Point(15.5,37),Point(18.5,37))
        self.wing2.setFill("orange")
        self.wing2.setOutline("orange")

        #creates dominant eye
        self.eye = Circle(Point(21,42),1)
        self.eye.setFill("white")
        self.eye.setOutline("white")
        
        #creates pupil of bird
        self.pupil = Circle(Point(21,42),0.25)
        self.pupil.setFill("black")

        #create a list of bird's body parts
        self.birdList = [self.eye2,self.body,self.beak,self.eye,self.pupil,self.wing1, self.wing2]
        #using the list to draw the bird
        for i in self.birdList:
            i.draw(GUI.win)
            self.birdList[6].undraw()

        #set bird velocity to zero
        self.velocity = 0

    def up (self, impulse):
        #this function sets the velocity at which the bird will be moved
        #impulse is inputted from user that moves the bird up
        self.velocity = impulse + self.velocity

    def move( self,dt):
        #this function moves the bird based on gravity and up bird velocity
        #intial value of gravity
        self.gravity = 6

        #get coordinates from bird body to set conditions of movement          
        y = self.body.getCenter().getY()
        r = self.body.getRadius()

        #prevents bird from going above the ceiling
        if y + r >= 90:
            #when bird touches ceiling, the bird experiences a downward velocity
            self.velocity = -self.gravity + 5

        #prevents bird from going below the ground
        elif y- r <=  1:
            #when bird touches ground, the bird experiences a bouncing effect
            self.velocity = self.gravity - 5

        #when no action is placed on the bird, the bird will experience the rate of gravity   
        else:   
            self.velocity = self.velocity-(self.gravity*dt)

        #a loop that moves the bird at set velocity
        for i in self.birdList:  
            i.move(0,self.velocity)

    def hull(self):
        # a function that gathers and checks points for the bird
        # defines limit points for the bird
        self.y = self.body.getCenter().getY()
        self.r = self.body.getRadius()
        self.bottom = Point(20,self.y - self.r)
        self.top = Point(20,self.y + self.r)
        self.butt = Point(20-self.r, self.y)
        # puts the limiting points in a list

        checkpointslst = [self.beak.getPoints()[1],self.beak.getPoints()[0],
                          self.beak.getPoints()[2],self.bottom,
                          self.top,self.butt]
      
        # checks the list of limiting points 
        return checkpointslst
    
    


class Barrier:

    def __init__(self,GUI):
        # creates the top barrier
        self.y= randrange(10,70)
        self.obstacle1 = Rectangle(Point(140,90),Point(150,self.y+25))
        self.obstacle1.setFill("black")
        self.obstacle1.draw(GUI.win)
        
        # creates the bottom barrier

        self.obstacle2 = Rectangle(Point(140,0),Point(150,self.y))
        self.obstacle2.setFill("black")
        self.obstacle2.draw(GUI.win)

    def move(self,dt):
        # moves the barriers from the right to left side of the window
        #sets initial velocity for the barriers

        self.velbarriers = -1

        self.obstacle1.move(self.velbarriers,0)
        self.obstacle2.move(self.velbarriers,0)
        

    def checkImpact(self,checkpointslst):
        #function checks if the bird points are inside the barriers
        # gathers the Y and X coordinates from the barriers
        
        x1, y1 = self.obstacle1.p1.getX(),self.obstacle1.p1.getY()
        x2, y2 = self.obstacle1.p2.getX(),self.obstacle1.p2.getY()

        a1, b1 = self.obstacle2.p1.getX(),self.obstacle2.p1.getY()
        a2, b2 = self.obstacle2.p1.getX(),self.obstacle2.p2.getY()

        #loop gets the X and Y points from the Bird list
        for pt in checkpointslst:
             
            x = pt.getX()
            y = pt.getY()

            # two conditions determine if the bird points are inside the barrier points
            # returns true if the points are inside the barrier
            if x1 <= x <= x2 and y2 <= y <= y1:
                 
                 return True

            
            if a1 <= x <= a2 and b1 <= y <= b2:
                return True

            

class Game:

    def __init__(self,gui):
        # calls all classes
        self.gui = gui
        self.flyingbird = Bird(gui)
        self.barriers = [Barrier(gui)]
        

    def play(self):
        #function plays the game

        #initiating variables for dt, score and impulse
        dt = 1/30
        impulse = 2.2
        timer = randrange(3,5)
        self.score = 0
        
        # creates and draws the score in the window
        self.scr = Text(Point(145,-5), str(self.score))
        self.scr.setTextColor("white")
        self.scr.setStyle("bold")
        self.scr.setFace("courier")
        self.scr.setSize(24)
        self.scr.draw(self.gui.win)
        #creates and draws menu
        menu = Rectangle(Point(28,65),Point(123,35))
        menu.setFill("black")
        menu.draw(self.gui.win)
        
        #score title
        scoreTitle = Text(Point(130,-5), "Score:")
        scoreTitle.setTextColor("white")
        scoreTitle.setStyle("bold")
        scoreTitle.setFace("courier")
        scoreTitle.setSize(24)
        scoreTitle.draw(self.gui.win)
        

        title = Text(Point(75,60), "Fly X") # game name
        title.setSize(36)
        title.setStyle("bold")
        title.setFace("courier")
        title.setTextColor("white")
        title.draw(self.gui.win)
        # introduction
        start = Text(Point(75,50), "Welcome to Fly X! \n Use the SpaceBar to navigate the bird through the barriers.\n\n  Stay in space to avoid crashing ")
        start.setStyle("bold")
        start.setFace("courier")
        start.setTextColor("white")
        start.draw(self.gui.win)
        # waiting for key to continue
        self.gui.win.getKey()
        # undraws introduction messages once the game starts
        start.undraw()
        title.undraw()
        menu.undraw()
        # redrawing text at the corner
        title = Text(Point(135,95), "Fly X")
        title.setSize(36)
        title.setStyle("bold")
        title.setFace("courier")
        title.setTextColor("white")
        title.draw(self.gui.win)
        # displays pause menu
        pause = Text(Point(15,-5), " P:is for pause   \n Q:is for quit    \nY:is for restart")
        pause.setStyle("bold")
        pause.setFace("courier")
        pause.setTextColor("white")
        pause.draw(self.gui.win)

        
        
        # main loop
        while True:
            #defines necessary variables
            key = self.gui.win.checkKey()
            timer = timer - dt
            hull = self.flyingbird.hull()
            
            
          # space moves the bird up and draws wing2 for flying effect
            if key == "space":
                self.flyingbird.up(impulse)
                self.flyingbird.wing2.draw(self.gui.win)
            # P pauses the game and draws the pause menu, and asks the user for the key   
            elif key == "p":

                pausetext= Text(Point(75,55), "You have Paused the Game, Use the space key to continue or Q to quit")
                pausetext.setFill("white")
                pausetext.setFace("courier")
                pausetext.draw(self.gui.win)
                k1 =self.gui.win.getKey()
                # undraws the pause menu if P or space is pressed
                if k1 == "space":
                    pausetext.undraw()
                elif k1 == 'p':
                    pausetext.undraw()
            
                # closes window if Q is pressed after pause
                elif k1 == "q":
                    break                  
            #closes the window anytime Q is pressed        
            elif key == "q":
                break

            else:
                self.flyingbird.wing2.undraw() # if nothing is pressed wing2 is undrawn
                
            # adds barriers when time is zero
            if timer <= 0:
                self.barriers.append(Barrier(self.gui))                
                timer = randrange(3,5) # resets timer

                         
            # gets X cordinates from the position of the bird
            birdposition = self.flyingbird.body.getCenter().getX()
            # a loop that moves the barriers 
            for i in self.barriers:
                i.move(dt)
                position = i.obstacle1.p2.getX()
                # undraws and removes the barriers when they reach the left side of the screen
                if position < 0:
                    i.obstacle1.undraw()
                    i.obstacle2.undraw()
                    self.barriers.remove(i)
                 # assigns points when the bird and barriers are in the same X position  
                if position == birdposition:
                    self.score += 5
                    self.scr.setText(self.score)



                    
        

                  
            dead = False #initial condition for crashing the bird
            for b in self.barriers: # loop checks if the bird has crashed 
                
                if b.checkImpact(hull):  
                    dead = True
             # if the bird has crashed gane is stopped and the stop menu is displayed   
            if dead:
                self.gameover = Text(Point(75,55), "Game Over! Thanks for flying X")
                self.gameover.setSize(20)
                self.gameover.setFill("white")
                self.gameover.setFace("courier")
                self.gameover.draw(self.gui.win)
                
                self.textmessage = Text(Point(75,52), "\nThe Bird has Crashed")
                self.textmessage.setFill("white")
                self.textmessage.setFace("courier")
                self.textmessage.draw(self.gui.win)               

                self.restart= Text((Point(75,40)),"Press Y to restart or Q to quit ")
                self.restart.setFill("white")
                self.restart.setFace("courier")
                self.restart.draw(self.gui.win)
                k2 =self.gui.win.getKey() # waits for the user key to restart or quit
                paused = True
                
                while paused:
                    if k2 == "y":
                        reset(self)
                        paused = False
                    elif k2 =="q":
                        self.gui.win.close()
                    else:

                        reset(self)

                        
                                         
                        
                        


        
            self.flyingbird.move(dt) # updates the movement of the bird
            update(30)

        self.gui.win.close()
              
# function that resets the game 
def reset(self):

    self.score = 0
    for i in self.barriers:
        i.obstacle1.undraw()
        i.obstacle2.undraw()
        self.barriers.remove(i)

        self.gameover.undraw()
        self.textmessage.undraw()
        self.restart.undraw()
        self.scr.undraw()

    mygame.play()


        

        

            



if __name__ == "__main__":

    mygui = GUI()
    mygame = Game(mygui)
    mygame.play()

# THANK YOU##

