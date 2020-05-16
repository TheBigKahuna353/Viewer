#Reader.py 2.0

#import as little as possible, get screen up, then load everything
import pygame as py
py.init()
screen = py.display.set_mode((500,600))

import sys, os, time, easygui
from pygame.locals import *
from os.path import expanduser
from Encryptor import Encrypt, Decrypt

#base colours
white = (255,255,255)
black = (0,0,0)
grey_L = (230,230,230)
grey_D = (200,200,200)

#charachter class, this represesnts each charachter on screen
class Char:
    
    #when first iniatlised, setup vars
    def __init__(self,unicode,size,font,bold,Italic,col):
        self.unicode = unicode
        self.size = size
        self.font = font
        self.bold = bold
        self.Italic = Italic
        self.col = col
        self.obj = py.font.Font(py.font.match_font(self.font),self.size).render(
            self.unicode,True,self.col
        )
        self.width = self.obj.get_width()
        self.height = self.obj.get_height()
    
    #update the letter with new propities
    def Update(self,size = None,font = None, bold = None, Italic = None, col = None):
        self.size = size if not None else self.size
        self.font = font if not None else self.font
        self.bold = bold if not None else self.bold
        self.Italic = Italic if not None else self.Italic
        self.col = col if not None else self.col
        self.obj = py.font.Font(py.font.match_font(self.font),self.size).render(
            self.unicode,True,self.col
        )      
    
    #create a char object using list, same as doing __init__(values*)
    #STATIC
    def From_list(List):
        #make sure only font is a string
        if isinstance(List[3],str):
            bold = True if List[3] == "True" else False
        if isinstance(List[4],str):
            italic = True if List[4] == "True" else False
        if isinstance(List[5],str):
            col = (int(List[5][1]), int(List[5][4]), int(List[5][7]))
        if isinstance(List[1],str):
            List[1] = int(List[1])
        return Char(List[0],List[1],List[2],bold,italic,col)
    
    #looks cleaner when printing it - for debug     
    def __repr__(self):
        string = "Char: '" + self.unicode + "', " + self.font + ", " + str(self.size)
        string += ", Bold" if self.bold else ""
        string += ", Italic" if self.Italic else ""
        return string
    
    #returns the height of a charachter of a font and size
    #STATIC
    def Get_height(font, size):
        return py.font.Font(py.font.match_font(font),size).render(" ",False,(0,0,0)).get_height()

#this handles opening, saving and everything else with files
class File_manager:
    
    #setup vars on startup
    def __init__(self):
        self.Dir = ""
        self.file = None
        self.default = expanduser("~\Documents\\")
        self.key = "this is a key that you can only see if you open it through the text editor, this is so long, wow!"
        #self.key = "my_key"
        self.test = None
    
    #to open a new file
    def Open(self,Dir = None):
        #if the Directory isnt known, open window for user
        if Dir == None:
            Dir = easygui.fileopenbox(default=self.default + "*.tst")
            #if user closed the window instead, exit
            if Dir == None:
                return
        #open file and read it
        with open(Dir,"r") as f:
            lines = f.readlines()
        #decrypt the data, taking out the "\n"
        for line in range(len(lines)):
            lines[line] = Decrypt(lines[line][:-1],self.key)
        #loop through the lines splitting each char into its own list
        for line in range(len(lines)):
            #split each char where '##' represents a new char
            lines[line] = list(lines[line].split("##"))
            #loop through every char
            for char in range(len(lines[line])):
                #split each value of the char where '--' is a new value
                lines[line][char] = list(lines[line][char].split("--"))
                #turn the char into a char object
                lines[line][char] = Char.From_list(lines[line][char])
        #now we have a file
        self.file = True
        self.Dir = Dir
        Win.New_file(os.path.basename(Dir))
        #change the window lines to new lines
        Win.Lines = lines
    
    #create a new file
    def New_file(self):
        self.Dir = easygui.filesavebox(title="New", default=self.default + "document1.tst")
        if self.Dir == None:
            return
        Win.New_file(os.path.basename(Dir))
        Win.Reset_lines()
    
    #save document in a new path/directory 
    #this means a new location on computer and/or different name
    def Save_as(self):
        self.Dir = easygui.filesavebox(default=self.default + "document1.tst")
        if self.Dir == None:
            return
        self.Save()
    
    #to save a file
    def Save(self):
        #if no Dir is given, Save as
        if self.Dir == None:
            self.Save_as()
            return
        #add data to string, then encrypt string, then write on file
        data = ["" for x in range(len(Win.Lines))]
        #loop through each line of window text
        for j,line in enumerate(Win.Lines):
            #for every char in current line, put its values into a list
            file_line = [[x.unicode,x.size,x.font,x.bold,x.Italic,x.col] for x in line]
            #for every char in the line
            for i,char in enumerate(file_line):
                #write the list of values seperated by a "--"
                data[j] += ("--".join(map(str,char)))
                #if end of char and not end of line
                if i < len(file_line) -1:
                    #seperate each char by a "##"
                    data[j] +=("##")
        #encrypt data
        for line in range(len(data)):
            data[line] = Encrypt(data[line],self.key)
        #open the file so can write on it
        with open(self.Dir,"w+") as f:   
            for line in data:
                f.write(line)
                f.write("\n")

#this is the class for the window and everything that goes on it
class Window:
    
    FM = File_manager()
    
    #on startup
    #setup variables
    def __init__(self):
        self.file = False
        self.running = True
        #name of button, if clicked, buttons in dropdown box
        self.taskbar = [
            ["File",False,("New",self.FM.New_file),("Open",self.FM.Open),("Save",self.FM.Save),("Save As",self.FM.Save_as)],
            ["Edit",False],
            ["Window",False]
        ]
        #the default fonts for the app, not for actual text
        self.app_font_button = py.font.Font(py.font.match_font("Calibri"),14)
        self.app_font_big = py.font.Font(py.font.match_font("Calibri"),17)
        self.MouseX, self.MouseY = py.mouse.get_pos()
        self.click = False
        #self.Lines is a list of each line which is a list of charachters
        self.Lines = [[]]
        #current size...
        self.cur_size = 28
        self.cur_font = "Calibri"
        self.cur_bold = False
        self.cur_Italic = False
        self.cur_col = black
        self.curs_line_num = 0
        self.curs_col_num = 0
        self.cursor_blink_time = time.time()
        self.cursor_blink_show = True
        self.Lines[0].append(Char("",self.cur_size,self.cur_font,self.cur_bold,self.cur_Italic,self.cur_col))
        self.clock = py.time.Clock()

    def Reset_lines(self):
        self.Lines = [Char("",self.cur_size,self.cur_font,self.cur_bold,self.cur_Italic,self.cur_col)]
        self.curs_line_num = 0
        self.curs_col_num = 0
    
    #after startup, sets things up that aren't vars then runs loop
    def Start(self):
        py.display.set_caption("Viewer")
        while self.running:
            self.Update()        
    
    #when a file is opened, put name at window top
    def New_file(self,name):
        py.display.set_caption("Viewer - " + name[:-4])
        self.file = True
    
    #this happens every frame, update screen, find events, update sys vars
    def Update(self):
        
        #draw screen
        self.Draw()
        
        #if click and not on taskbar, close all panels on taskbar
        if self.click:
            if self.MouseY > 20:
                for button in self.taskbar:
                    button[1] = False        
        
        self.clock.tick(60)
        
        #every 0.6 seconds, the cursor switches from showing to not showing and back
        if time.time() > self.cursor_blink_time + 0.6:
            self.cursor_blink_show = not self.cursor_blink_show
            self.cursor_blink_time = time.time()        
        
        #update sys variables
        self.MouseX, self.MouseY = py.mouse.get_pos()
        self.click = False
        #update the screen
        py.display.update()
        #get events
        for e in py.event.get():
            #if X is pressed, quit
            if e.type == 12:
                py.quit()
                self.running = False
            self.click = True if e.type == MOUSEBUTTONDOWN else False
            #if a key is pressed
            if e.type == KEYDOWN:
                #type if on a file
                if self.file:
                    self.KeyPress(e)
    
    #when a key is pressed
    def KeyPress(self,e):
        #when backspace is pressed, delete last char
        if e.unicode == "":
            #if nothing in line, delete line
            if len(self.Lines[self.curs_line_num]) == 0:
                del self.Lines[self.curs_line_num]
                self.curs_line_num -= 1
                self.curs_col_num = len(self.Lines[self.curs_line_num]) - 1
            else:   
                del self.Lines[self.curs_line_num][self.curs_col_num]
                self.curs_col_num -= 1
        #if key is enter, create line
        elif e.key == 13:
            #add a blank char so line isnt 0 pixels height if no other text on it
            obj = Char("",self.cur_size,self.cur_font,self.cur_bold,self.cur_Italic,self.cur_col)
            self.Lines = self.Lines[:self.curs_line_num+1] + [[obj]] + self.Lines[self.curs_line_num+1:]
            self.curs_line_num += 1
            self.curs_col_num = 0
        #if key is a charachter, put on screen
        elif e.unicode != "":
            obj = Char(e.unicode,self.cur_size,self.cur_font,self.cur_bold,self.cur_Italic,self.cur_col)
            #if the new char would be off the screen, create new line
            leng = 0
            for char in self.Lines[self.curs_line_num]:
                leng += char.width + 1
            #500 = width, 490 so it looks better than next to side of screen
            if leng + obj.width > 490:
                self.Lines.append([])
                self.curs_line_num += 1                
            self.Lines[self.curs_line_num] = self.Lines[self.curs_line_num][:self.curs_col_num + 1] + [obj] + self.Lines[self.curs_line_num][self.curs_col_num+1:]
            self.curs_col_num += 1
        #if the down arrow is pressed
        elif e.key == 274:
            self.curs_line_num += 1 if self.curs_line_num < len(self.Lines)-1 else 0
            self.curs_col_num = min(self.curs_col_num,len(self.Lines[self.curs_line_num])-1)
        #if the up arrow is pressed
        elif e.key == 273:
            self.curs_line_num -= 1 if self.curs_line_num > 0 else 0
            self.curs_col_num = min(self.curs_col_num,len(self.Lines[self.curs_line_num])-1)
        #if the right arrow is pressed
        elif e.key == 275:
            self.curs_col_num += 1 if self.curs_col_num < len(self.Lines[self.curs_line_num])-1 else 0
        #if the left arrow is pressed
        elif e.key == 276:
            self.curs_col_num -= 1 if self.curs_col_num > 0 else 0
    
    #this draws text onto the screen easier
    def DrawText(self,Text,font,X,Y,col = (0,0,0),center = True):
        obj = font.render(Text,True,col)
        X -= obj.get_width()//2 if center else 0
        Y -= obj.get_height()//2 if center else 0
        screen.blit(obj,(X,Y))
    
    #creates a button on the screen, returns True if clicked on
    def Button(self,Text,font,X,Y,W,H):
        #is x coordinate over button
        x_cur = True if self.MouseX > X and self.MouseX < X + W else False
        #is y coordinate over button
        y_cur = True if self.MouseY > Y and self.MouseY < Y + H else False
        #is x and y coordinate over button
        hover = True if x_cur and y_cur else False
        #has the user clicked the button
        pressed = True if hover and self.click else False
        #change background if cursor over it
        col = grey_D if hover else grey_L
        #draw
        py.draw.rect(screen,col,(X,Y,W,H))
        self.DrawText(Text,font,X+(W//2),Y+(H//2))
        #return if button clicked
        return pressed
    
    
    #this draws the main screen
    def Draw(self):
        #reset screen
        screen.fill(white)
        #if no file selected
        if not self.file:
            self.DrawText("No File Open",self.app_font_big,250,300)
        else:
            #draw text
            #start putting text at 20, just below the taskbar
            cur_height = 20
            last_height = 0
            for i,line in enumerate(self.Lines):
                #different letters are different sizes. add the widths of each 
                #letter to find next place
                cur_leng = 0
                #find highest height of the line, so single letters that are bigger than
                #the rest wont overlap
                highest_height = 0
                last_leng = 0
                clicked_on_text = False
                for j,char in enumerate(line):
                    #blit letter onto screen
                    screen.blit(char.obj,(cur_leng,cur_height))
                    last_leng = cur_leng
                    cur_leng += char.width + 1
                    highest_height = max(highest_height,char.height)
                    #if the cursor is showing, put on screen
                    if self.cursor_blink_show:
                        #if the line is currently the one with the cursor on it
                        if j == self.curs_col_num and i == self.curs_line_num:
                            py.draw.line(screen,(0,0,0),(cur_leng + 1, cur_height),(cur_leng + 1,cur_height + Char.Get_height(self.cur_font,self.cur_size)),1)
                    #if click, change cursor to that spot
                    if self.click:
                        if self.MouseX > last_leng and self.MouseX < cur_leng:
                            self.curs_col_num = j
                            clicked_on_text = True
                #update current and last heights
                last_height = cur_height
                cur_height += highest_height
                #if click, change cursor to that spot
                if self.click:                
                    if self.MouseY > last_height and self.MouseY < cur_height:
                        self.curs_line_num = i
                        if not clicked_on_text:
                            self.curs_col_num = len(self.Lines[self.curs_line_num]) -1
        self.Draw_Taskabar()
    
    def Draw_Taskabar(self):
        #taskbar at the top
        py.draw.rect(screen,grey_L,(0,0,500,20))
        for i,Panel in enumerate(self.taskbar):
            #draw button and return True if clicked on
            pressed = self.Button(Panel[0],self.app_font_button,i*60,0,60,20)
            #if clicked on, show or not show the dropdown panel
            Panel[1] = not Panel[1] if pressed else Panel[1]
            #if showing the dropdown menu, draw it
            if Panel[1]:
                for j,button in enumerate(Panel[2:]):
                    clicked = self.Button(button[0],self.app_font_button,i*60,20 + (j*20),60,20)
                    if clicked:
                        button[1]()
    
#create window object
Win = Window()

#if opened with a file, open file
try:
    file = sys.argv[1]
    print(file)
    Win.FM.Open(file)
except:
    pass

#start the program
Win.Start()