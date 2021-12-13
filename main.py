import math
import pygame
from pygame.constants import MOUSEBUTTONDOWN, MOUSEBUTTONUP
import pygame_gui
from klassid import *

pygame.init()

pygame.display.set_caption('Minigolf')
aken = pygame.display.set_mode([1024, 768])
manager = pygame_gui.UIManager([1024, 768])

aken.fill([255, 255, 255])

# Piltide määramine
sein_hor = "sein_horisontaalne.jpg"
sein_ver = "sein_vertikaalne.jpg"
kolmnurk1 = "kolmnurk1.png"
kolmnurk2 = "kolmnurk2.png"
liiv = "liiv.png"
vesi = "vesi.png"

# Klass Tasemenupp joonistab taseme valimise nupud
class Tasemenupp(pygame_gui.elements.UIButton):
    def __init__(self, ekraan, x, y, tekst):
        self.x = x
        self.y = y
        self.ekraan = ekraan
        self.tekst = tekst
        super().__init__(pygame.Rect((self.x, self.y), (50, 50)), self.tekst, manager)


# Klass Tekstikast väljastab infot
class Tekstikast(pygame_gui.elements.UITextBox):
    def __init__(self, ekraan, x, y, laius, kõrgus, tekst):
        self.x = x
        self.y = y
        self.laius = laius
        self.kõrgus = kõrgus
        self.ekraan = ekraan
        self.tekst = tekst
        super().__init__(self.tekst, pygame.Rect((self.x, self.y), (self.laius, self.kõrgus)), manager)
        
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
lookis = False
#viimased kaks numbrid on x kiirus ja y kiirus et palli liikuma panna
pall = Pall(aken, 200, 434, 0, 0)
pall.loo_pall()
tõkked = Tõkked(aken)
tokked = []
while mäng_käib:
    # Hiire positsiooni saamine
    hiire_x, hiire_y = pygame.mouse.get_pos()
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

        if event.type == MOUSEBUTTONDOWN:
         #Algkoordinaatide salvestamine
            pall.alg_koord[0] = hiire_x
            pall.alg_koord[1] = hiire_y
        if event.type == MOUSEBUTTONUP:
            #Lõppkoordinaatide salvestamine
            pall.lopp_koord[0] = hiire_x
            pall.lopp_koord[1] = hiire_y
            #Et palli ei saaks liikumise ajal uuesti lüüa
            if pall.kiirus_x == 0 and pall.kiirus_y == 0:
                pall.look()


    # loome isendi klassist Seinad()
    seinad = Seinad(aken, sein_hor, sein_ver)

    # loome isendi klassist Auk()
    auk = Auk(aken, 900, 434)
    sein_list_hor1 = seinad.sein_hor_mask, [0, 100],  sein_hor
    sein_list_hor2 = seinad.sein_hor_mask, [0, 688],  sein_hor
    sein_list_ver1 = seinad.sein_ver_mask, [0, 100], sein_ver
    sein_list_ver2 = seinad.sein_ver_mask, [944, 100],sein_ver
    # Vastavalt valitud tasemele lisame tõkked; 1. tasemel tõkkeid pole.
    if tase == 2:
        # loome isendid klassist Tõkked()
        tõke1 = tõkked.loo_tokked(kolmnurk1, 150, 425)
        tõke2 = tõkked.loo_tokked(kolmnurk2, 450, 180)
        tokked = [tõke1, tõke2, sein_list_hor1, sein_list_hor2, sein_list_ver1, sein_list_ver2]
        pall.liikumine(dt, tokked)

    elif tase == 3:
        # loome isendid klassist Tõkked()
        tõke1 = tõkked.loo_tokked(kolmnurk1, 150, 425)
        tõke2 = tõkked.loo_tokked(liiv, 450, 180)
        tokked = [tõke1, tõke2, sein_list_hor1, sein_list_hor2, sein_list_ver1, sein_list_ver2]
        pall.liikumine(dt, tokked)
    elif tase == 4:
        # loome isendid klassist Tõkked()
        tõke1 = tõkked.loo_tokked(kolmnurk1, 150, 425)
        tõke2 = tõkked.loo_tokked(vesi, 450, 180)
        tõke3 = tõkked.loo_tokked(liiv, 600, 400)
        tokked = [tõke1, tõke2, tõke3, sein_list_hor1, sein_list_hor2, sein_list_ver1, sein_list_ver2]
        pall.liikumine(dt, tokked)
    elif tase == 5:
        # loome isendid klassist Tõkked()
        tõke1 = tõkked.loo_tokked(vesi, 90, 180)
        tõke2 = tõkked.loo_tokked(liiv, 600, 500)
        tõke3 = tõkked.loo_tokked(kolmnurk1, 150, 425)
        tõke4 = tõkked.loo_tokked(kolmnurk2, 450, 180)
        tokked = [tõke1, tõke2, tõke3, tõke4, sein_list_hor1, sein_list_hor2, sein_list_ver1, sein_list_ver2]
        pall.liikumine(dt, tokked)
    else:
        tokked = [sein_list_hor1, sein_list_hor2, sein_list_ver1, sein_list_ver2]
        pall.liikumine(dt, tokked)

    manager.update(dt)
    manager.draw_ui(aken)
    pygame.display.flip()

pygame.quit()
