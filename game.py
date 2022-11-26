import pygame
from pygame import *
pygame.init()
#----Window-Setting---------------------
win = pygame.display.set_mode((800,600))
pygame.display.set_caption("Untitled by Sepandi")
pygame.display.set_icon(image.load("Data/Assets/icon.png"))
#--On-Load-------------------------------------------------------------------------------------
#--Clock
clock = pygame.time.Clock()
animationTimer = 0.24
deltaTime = 0

#--Fonts
font = pygame.font.Font('Data/Fonts/OpenSens.ttf',13)
font2 = pygame.font.Font('Data/Fonts/OpenSens.ttf',20)
font3 = pygame.font.Font('Data/Fonts/OpenSens.ttf',10)
#--Main-Menu-image
mainMenuImage = image.load("Data/Assets/MainMenuImage.png")
#--Sounds
pygame.mixer.init()

#--Game
class Game():
    def playMusic(filename):
        pygame.mixer.music.set_volume(0)
        pygame.mixer.music.unload()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
    onMenu = True
    cloud1 = image.load("Data/Assets/Environment/cloud1.png")
    cloud1Pos = Vector2(300,30)
    level = 1
    lastLevel = 2
    levelColor = 164,254,244
    deltaTime = 0
    def Loop():
        #--KeyBindings------------------------------------------------------------------------------------------------
        #--Going-Back-to-Menu
        KeyPress = pygame.key.get_pressed()
        if KeyPress[K_ESCAPE]:
            Game.onMenu = True
            Game.level = 1
        #--Moving-Player
        if KeyPress[K_a]:
            Player.Pos.x -= 3
            Player.facingRight = False
            Player.idle = False
        elif KeyPress[K_d]:
            Player.Pos.x += 3
            Player.facingRight = True
            Player.idle = False
        else:
            Player.idle = True
        if KeyPress[K_SPACE]:
            Player.jump = True
            Player.jumpingColdDown += 1
            if Player.jumpingColdDown < 15:
                if KeyPress[K_d] and KeyPress[K_SPACE] or KeyPress[K_a] and KeyPress[K_SPACE]:
                    if Player.facingRight:
                        Player.Pos.yx -= 15,-3
                    else :
                        Player.Pos.yx -= 15,3
                else:
                    Player.Pos.y -= 15
        else :
            Player.jump = False
        
        #--MovingCloud
        Game.cloud1Pos.x += 0.1
        if Game.cloud1Pos.x > win.get_width():
            Game.cloud1Pos.x = -64
        #--Movig-throw-levels
        if not Game.level == 1 and Player.Pos.x <= 0:
            Game.level -= 1
            Player.Pos.x = 780
        elif not Game.level == Game.lastLevel and Player.Pos.x > 780:
            Game.level += 1
            Player.Pos.x = 0
        if Game.level == 1 and Player.Pos.x <= 0:
            Player.Pos.x = 0
        if Game.level == Game.lastLevel and Player.Pos.x >760:
            Player.Pos.x = 760

#-Player-------------------------------------------------------------------------
class Player():
    username = "Player"
    runningImage1 = pygame.image.load("Data/Assets/Player/playerRunning1.png")
    runningImage2 = pygame.image.load("Data/Assets/Player/playerRunning2.png")
    idleImage = pygame.image.load("Data/Assets/Player/playerIdle.png")
    jumpImage = pygame.image.load("Data/Assets/Player/jumping.png")
    Pos = Vector2(100,300)
    idle = True
    facingRight = True
    rect = Rect(Pos.x,Pos.y,15,56)
    GRAVITY = 5
    jumpingColdDown = 0
    jump = True
    health = 5
    heart = image.load("Data/Assets/Player/heart.png")
    canGetHurt = True
    def Respawn():
        Player.Pos = Vector2(100,300)
        Player.health = 5
        Game.level = 1
    sword = image.load("Data/Assets/Player/sword.png")
    swordRect = sword.get_rect()
    inAtack = False
    AtackTimeOut = 0
    animationTimer = 0.24
    def Update():
        #--Make-Sword-Stick-to-Player
        if Player.facingRight:
            Player.swordRect.x , Player.swordRect.y = Player.Pos.x+40, Player.Pos.y+20
        else: Player.swordRect.x , Player.swordRect.y = Player.Pos.x-80 , Player.Pos.y+20
        
        #--Player-Get-Hurt
        if Player.rect.colliderect(Enemies.rect):
            if Player.canGetHurt:
                Player.health -= 1
                Player.canGetHurt = False 
        else :
            Player.canGetHurt = True
        #--Player-Respawn
        if Player.health <= 0:
            Player.Respawn()
            Enemies.RESET()
            
        
    def Draw():
        if Player.facingRight:
            if not Player.jump:
                if Player.idle == False:
                    if animationTimer <= 0.06 and animationTimer >= 0:
                        win.blit(Player.idleImage,Player.Pos)
                    elif animationTimer <= 0.12 and animationTimer >= 0.06:
                        win.blit(Player.runningImage1,Player.Pos)
                    elif animationTimer <= 0.18 and animationTimer >= 0.12:
                        win.blit(Player.idleImage,Player.Pos)
                    elif animationTimer <= 0.24 and animationTimer >= 0.18:
                        win.blit(Player.runningImage2,Player.Pos)
                elif Player.idle:
                    win.blit(Player.idleImage,Player.Pos)
            else:
                win.blit(Player.jumpImage,Player.Pos)
        elif Player.facingRight == False:
            if not Player.jump:
                if Player.idle == False:
                    if animationTimer <= 0.06 and animationTimer >= 0:
                        win.blit(transform.flip(Player.idleImage,True,False),Player.Pos)
                    elif animationTimer <= 0.12 and animationTimer >= 0.06:
                        win.blit(transform.flip(Player.runningImage1 ,True,False),Player.Pos)
                    elif animationTimer <= 0.18 and animationTimer >= 0.12:
                        win.blit(transform.flip(Player.idleImage ,True,False),Player.Pos)
                    elif animationTimer <= 0.24 and animationTimer >= 0.18:
                        win.blit(transform.flip(Player.runningImage2 ,True,False),Player.Pos)
                elif Player.idle:
                    win.blit(transform.flip(Player.idleImage ,True,False),Player.Pos)
            else:
                win.blit(transform.flip(Player.jumpImage ,True,False),Player.Pos)
        #--Draw-hearts
        for i in range(Player.health):
            win.blit(Player.heart,(20+i*40,win.get_height()-Player.heart.get_height()))
        #--Draw-Player-Username
        usernamePanel = font3.render(Player.username,True,(0,0,0))
        win.blit(usernamePanel,(Player.Pos.x,Player.Pos.y-20))

#-Enemies-------------------------------------------------------------------------
class Enemies():
    image = image.load("Data/Assets/Enemies/Enemy1.png")
    Pos = Vector2(500,345)
    rect = Rect(Pos.x + 10,345,16,image.get_height())
    facingRight = True
    HEALTH = 10
    health = 10
    canGetHurt = True
    def Update():
        print(Enemies.canGetHurt)
        #--Detect-Sword-with-Enemie-Collision  
        if Enemies.rect.colliderect(Player.swordRect):
            Enemies.health -= 1
            Enemies.canGetHurt = False
        else:
                Enemies.canGetHurt = True
        #--Enemies-Health-Restorer
        if Enemies.health <= 0:
            Enemies.Pos.x = 700
            Enemies.health = Enemies.HEALTH
        #--Enemies-AI
        if Player.Pos.x < Enemies.Pos.x:
            Enemies.Pos.x -= 2
            Enemies.facingRight = False
        elif Player.Pos.x > Enemies.Pos.x:
            Enemies.Pos.x += 2
            Enemies.facingRight = True
        Enemies.rect.x = Enemies.Pos.x + 10
        Enemies.Draw()
    def Draw():
        #--Draw-Enmeies-Health
        healthViewer = font3.render(str(Player.health),True,(0,0,0))
        win.blit(healthViewer,(Enemies.Pos.x,Enemies.Pos.y-20))
    #--RESET-Enemies
    def RESET():
        Enemies.Pos = Vector2(500,345)
        Enemies.rect.x = Enemies.Pos.x + 10


#--Floor
floorImage = image.load("Data/Assets/Environment/floor.png")
floor = floorImage.get_rect()
floor.y = 400
Game.playMusic("Data/Sounds/theme.mp3")

#--Updates------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------
while True:
    draw.rect(win,(0,0,0),Enemies.rect)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
    KeyPress = pygame.key.get_pressed()
    if not Game.onMenu:
        
        Game.Loop()
        Player.Update()
        Enemies.Update()
        #--Gravity
        Player.Pos.y += Player.GRAVITY
        


        #--Rect-Detect-for-Floor
        collection_trolerance = 20
        if Player.rect.colliderect(floor):
            if abs(floor.top - Player.rect.bottom < collection_trolerance):
                Player.Pos.y -= Player.GRAVITY
                if Player.jumpingColdDown > 5:
                    Player.jumpingColdDown = 0
                    Player.jump = False
        pillers_collection_trolerance = 10
        

        #-Respawn-sitations
        if Player.Pos.y > win.get_height():
            Player.Respawn()

        #--Atack
        if KeyPress[K_RIGHT]:
            Player.inAtack = True
            Player.AtackTimeOut += 1
        else :
            Player.inAtack = False
            Player.AtackTimeOut = 0





        #--Draws-------------------------------------------------------------------------------------------------------------------------
        #--------------------------------------------------------------------------------------------------------------------------------
        #--Draw Rects
        Player.rect.x = Player.Pos.x+13
        Player.rect.y = Player.Pos.y
        draw.rect(win,Game.levelColor,Player.rect)
        if Enemies.facingRight:
            win.blit(Enemies.image,Enemies.Pos)
        else :
            win.blit(transform.flip(Enemies.image ,True,False),Enemies.Pos)
        #--Draw-Floor
        win.blit(floorImage,floor)

        #--Draw-Clouds
        win.blit(Game.cloud1,Game.cloud1Pos)
        #--Animation-Timer-Restorer

        animationTimer -= deltaTime
        if animationTimer <= 0:
                    animationTimer = 0.24

        #--Player-Draws
        Player.Draw()

        #--Sword-Draw
        if Player.inAtack and Player.AtackTimeOut < 10:
            if Player.facingRight:
                win.blit(Player.sword,Player.swordRect)
            else:
                win.blit(transform.flip(Player.sword,True,False),Player.swordRect)

        #--DEBUG-MENU------------------------------------------------------
        fps = "FPS : "+str(int(clock.get_fps()))+" | "
        PlayerInWorldPos = (Game.level - 1)*win.get_width()+Player.Pos.x
        cord = "Position : "+ str(int(PlayerInWorldPos))+ "-" + str(int(Player.Pos.y)) + "|"
        levelDebug = "Level="+str(int(Game.level))
        debugMenu = font.render(fps + cord + levelDebug,True,[0,0,255])
        win.blit(debugMenu,Vector2(10,10))
    #--On-Menu-Loop----------------------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------------------------------------
    elif Game.onMenu:
        win.blit(mainMenuImage,Vector2(0,0))
        startGuide = font2.render("Press 'Enter' to start",True,[0,0,255])
        win.blit(startGuide,Vector2(win.get_width()/2-startGuide.get_width()/2,win.get_height()/2))
        if KeyPress[K_RETURN]:
            Game.onMenu = False
            Player.Respawn()



    pygame.display.update()
    win.fill(Game.levelColor)
    deltaTime = clock.tick(60) / 1000
