import pygame
from pygame.constants import MOUSEBUTTONDOWN, MOUSEBUTTONUP
import pygame_gui

pygame.init()

pygame.display.set_caption('Minigolf')
aken = pygame.display.set_mode([1024, 768])
manager = pygame_gui.UIManager([1024, 768])

aken.fill([255,255,255])

# Piltide määramine
sein_hor = "sein_horisontaalne.jpg"
sein_ver = "sein_vertikaalne.jpg"
vesi = "vesi.png"
kivi = "kivi.png"
kolmnurk1 = "kolmnurk1.png"
kolmnurk2 = "kolmnurk2.png"
liiv = "liiv.png"

#Klass Pall()
class Pall():
    def __init__(self, ekraan, x, y, kiirus):
        self.x = x
        self.y = y
        self.kiirus = kiirus
        self.ekraan = ekraan
    
    #Joonistab ekraanile palli
    def loo_pall(self):
        pygame.draw.circle(self.ekraan, "azure", [self.x, self.y], 18)


# Klass Seinad() joonistab aknasse teateriba ning mänguplatsi piiravad seinad 
class Seinad():
    def __init__(self, ekraan, taustapilt_hor, taustapilt_ver):
        self.taustapilt_hor = taustapilt_hor
        self.taustapilt_ver = taustapilt_ver
        self.ekraan = ekraan
        self.ekraan.fill((139, 217, 72))
        pygame.draw.rect(self.ekraan, "forestgreen", [0,0,1024,100])
        self.sein_hor = pygame.image.load(self.taustapilt_hor)
        self.ekraan.blit(self.sein_hor, [0,100])
        self.ekraan.blit(self.sein_hor, [0,688])
        self.sein_ver = pygame.image.load(self.taustapilt_ver)
        self.ekraan.blit(self.sein_ver, [0,100])
        self.ekraan.blit(self.sein_ver, [944,100])

# Klass Tõkked() joonistab punkti (x, y) valitud tõkke 
class Tõkked():
    def __init__(self, ekraan, pilt, x, y):
        self.pilt = pilt
        self.x = x
        self.y = y
        self.ekraan = ekraan
        self.tõke = pygame.image.load(self.pilt)
        self.ekraan.blit(self.tõke, [self.x,self.y])
        
# Klass Auk() joonistab punkti (x, y) augu  
class Auk():
    def __init__(self, ekraan, x, y):
        self.x = x
        self.y = y
        self.ekraan = ekraan
        pygame.draw.circle(self.ekraan, [0,0,0], [self.x,self.y], 25, 0)

# Klass Tasemenupp joonistab taseme valimise nupud
class Tasemenupp(pygame_gui.elements.UIButton):
    def __init__(self, ekraan, x, y, tekst):
        self.x = x
        self.y = y
        self.ekraan = ekraan
        self.tekst = tekst
        super().__init__(pygame.Rect((self.x,self.y), (50, 50)), self.tekst, manager)
        
#Klass Tekstikast väljastab infot
class Tekstikast(pygame_gui.elements.UITextBox):
    def __init__(self, ekraan, x, y, laius, kõrgus, tekst):
        self.x = x
        self.y = y
        self.laius = laius
        self.kõrgus = kõrgus
        self.ekraan = ekraan
        self.tekst = tekst
        super().__init__(self.tekst, pygame.Rect((self.x,self.y), (self.laius, self.kõrgus)), manager)

#----------------------------------------------------------------------
# See on juba mängu enda kood

# Teade taseme valimiseks
tasemed = Tekstikast(aken, 50, 5, 110, 35, "Vali tase")

# Tasemenupud
tasemenupp1 = Tasemenupp(aken, 50, 40, '1')
tasemenupp2 = Tasemenupp(aken, 110, 40, '2')
tasemenupp3 = Tasemenupp(aken, 170, 40, '3')
tasemenupp4 = Tasemenupp(aken, 230, 40, '4')
tasemenupp5 = Tasemenupp(aken, 290, 40, '5')

kell = pygame.time.Clock()
tase = 1
mäng_käib = True

while mäng_käib:
    dt = kell.tick() / 1000
        
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            mäng_käib = False
            
        elif event.type == pygame.USEREVENT: 
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED: 
                if event.ui_element == tasemenupp1: 
                    tase = 1
                elif event.ui_element == tasemenupp2: 
                    tase = 2
                elif event.ui_element == tasemenupp3: 
                    tase = 3
                elif event.ui_element == tasemenupp4: 
                    tase = 4
                elif event.ui_element == tasemenupp5: 
                    tase = 5

        manager.process_events(event)
    
    # loome isendi klassist Seinad()
    seinad = Seinad(aken,sein_hor,sein_ver)
    
    #palli isend
    pall = Pall(aken , 200, 434, 0)
    #joonistab palli
    pall.loo_pall()
    
    # loome isendi klassist Auk()
    auk = Auk(aken,900,434)
        
    #Vastavalt valitud tasemele lisame tõkked; 1. tasemel tõkkeid pole.
    if tase == 2:
        # loome isendid klassist Tõkked()
        tõke1 = Tõkked(aken,kolmnurk1,150,425)
        tõke2 = Tõkked(aken,kolmnurk2,450,180)
    elif tase == 3:
        # loome isendid klassist Tõkked()
        tõke1 = Tõkked(aken,kolmnurk1,150,425)
        tõke2 = Tõkked(aken,liiv,450,180)
    elif tase == 4:
        # loome isendid klassist Tõkked()
        tõke1 = Tõkked(aken,kolmnurk1,150,425)
        tõke2 = Tõkked(aken,vesi,450,180)
        tõke3 = Tõkked(aken,liiv,600,400)
    elif tase == 5:
        # loome isendid klassist Tõkked()
        tõke1 = Tõkked(aken,liiv,450,180)
        tõke2 = Tõkked(aken,vesi,600,400)
        tõke3 = Tõkked(aken,kivi,100,550)
        tõke4 = Tõkked(aken,kivi,250,525)
        tõke5 = Tõkked(aken,kivi,360,375)
    
    manager.update(dt) 
    manager.draw_ui(aken) 
    pygame.display.flip()
    
pygame.quit()
