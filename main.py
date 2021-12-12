import math
import pygame
from pygame.constants import MOUSEBUTTONDOWN, MOUSEBUTTONUP
import pygame_gui

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

# Klass Seinad() joonistab aknasse teateriba ning mänguplatsi piiravad seinad
class Seinad():
    def __init__(self, ekraan, taustapilt_hor, taustapilt_ver):
        self.taustapilt_hor = taustapilt_hor
        self.taustapilt_ver = taustapilt_ver
        self.ekraan = ekraan
        self.ekraan.fill((139, 217, 72))
        pygame.draw.rect(self.ekraan, "forestgreen", [0, 0, 1024, 100])
        self.sein_hor = pygame.image.load(self.taustapilt_hor)
        self.ekraan.blit(self.sein_hor, [0, 100])
        self.ekraan.blit(self.sein_hor, [0, 688])
        self.sein_ver = pygame.image.load(self.taustapilt_ver)
        self.ekraan.blit(self.sein_ver, [0, 100])
        self.ekraan.blit(self.sein_ver, [944, 100])
        self.sein_hor_mask = pygame.mask.from_surface(self.sein_hor)
        self.sein_ver_mask = pygame.mask.from_surface(self.sein_ver)

# Klass Tõkked() joonistab punkti (x, y) valitud tõkke
class Tõkked():
    def __init__(self, ekraan):
        self.ekraan = ekraan

    def loo_tokked(self, pilt, x, y):
        self.tõke = pygame.image.load(pilt)
        self.ekraan.blit(self.tõke, [x, y])
        self.tõke_mask = pygame.mask.from_surface(self.tõke)
        return self.tõke_mask, [x,y], pilt

# Klass Auk() joonistab punkti (x, y) augu
class Auk():
    def __init__(self, ekraan, x, y):
        self.x = x
        self.y = y
        self.ekraan = ekraan
        pygame.draw.circle(self.ekraan, [0, 0, 0], [self.x, self.y], 25, 0)


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

class Pall():
    def __init__(self, ekraan, x, y, kiirus_x, kiirus_y):
        self.x = x
        self.y = y
        self.sein = False
        self.liiv = False
        self.vesi = False
        self.last_x = x
        self.last_y = y
        self.aeglustus = 5
        self.kiirus_x = kiirus_x
        self.kiirus_y = kiirus_y
        self.ekraan = ekraan
        self.alg_koord = [0, 0]
        self.lopp_koord = [0, 0]

    # Joonistab ekraanile palli
    def loo_pall(self):
        self.pall = pygame.Surface((18 * 2, 18 * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.pall, (255,255,255), (18, 18), 18)
        self.ekraan.blit(self.pall,(self.x, self.y))
        self.pall_mask = pygame.mask.from_surface(self.pall)

    def liikumine(self, dt, tokked):
        #palli liikumine
        if self.kiirus_x == 0 and self.kiirus_y == 0 and not self.vesi:
            self.last_x = self.x
            self.last_y = self.y
        self.x += self.kiirus_x * dt
        self.y -= self.kiirus_y * dt

        # Palli põrkamine
        for toke in tokked:
            ox = toke[1][0]
            oy = toke[1][1]
            offset = int(self.x - ox), int(self.y -  oy)
            collision = toke[0].overlap(self.pall_mask, offset)
            if collision:
                if toke[2] == sein_ver and not self.sein:
                    vector = pygame.Vector2(self.kiirus_x,self.kiirus_y)
                    vector = vector.reflect([0, 1])
                    self.kiirus_x = -vector.x
                    self.kiirus_y = -vector.y
                    self.sein = True
                if toke[2] == sein_hor and not self.sein:
                    vector = pygame.Vector2(self.kiirus_x, self.kiirus_y)
                    vector = vector.reflect([1, 0])
                    self.kiirus_x = -vector.x
                    self.kiirus_y = -vector.y
                    self.sein = True
                if toke[2] == kolmnurk1:
                    if self.x < (ox + toke[0].get_size()[0]/2) and self.y >= oy - 30:
                        vector = pygame.Vector2(self.kiirus_x, self.kiirus_y)
                        vector = vector.reflect([1, 1.7])
                        self.kiirus_x = -vector.x
                        self.kiirus_y = -vector.y
                    elif self.x > (ox + toke[0].get_size()[0]/2) and self.y >= oy - 30:
                        vector = pygame.Vector2(self.kiirus_x, self.kiirus_y)
                        vector = vector.reflect([-1, 1.7])
                        self.kiirus_x = -vector.x
                        self.kiirus_y = -vector.y
                    elif self.y < oy - 30:
                        vector = pygame.Vector2(self.kiirus_x, self.kiirus_y)
                        vector = vector.reflect([1, 0])
                        self.kiirus_x = -vector.x
                        self.kiirus_y = -vector.y
                if toke[2] == kolmnurk2:
                    if self.x < (ox + toke[0].get_size()[0]/2) and self.y <= oy + toke[0].get_size()[1] - 3:
                        vector = pygame.Vector2(self.kiirus_x, self.kiirus_y)
                        vector = vector.reflect([-1, 1.7])
                        self.kiirus_x = -vector.x
                        self.kiirus_y = -vector.y
                    elif self.x > (ox + toke[0].get_size()[0]/2) and self.y <= oy + toke[0].get_size()[1] - 3:
                        vector = pygame.Vector2(self.kiirus_x, self.kiirus_y)
                        vector = vector.reflect([1, 1.7])
                        self.kiirus_x = -vector.x
                        self.kiirus_y = -vector.y
                    elif self.y > oy + toke[0].get_size()[1] - 3:
                        print(toke[0].get_size())
                        vector = pygame.Vector2(self.kiirus_x, self.kiirus_y)
                        vector = vector.reflect([1, 0])
                        self.kiirus_x = -vector.x
                        self.kiirus_y = -vector.y
                if toke[2] == liiv:
                    self.aeglustus = 50
                    self.liiv = True
                if toke[2] == vesi:
                    self.aeglustus = 60
                    self.vesi = True
                    if self.kiirus_x == 0 and self.kiirus_y == 0:
                        self.x = self.last_x
                        self.y = self.last_y
            elif not collision:
                if toke[2] == liiv and not self.vesi:
                    self.aeglustus = 5
                    self.liiv = False
                if toke[2] == sein_ver or toke[2] == sein_hor:
                    self.sein = False
                if toke[2] == vesi and not self.liiv:
                    self.aeglustus = 5
                    self.vesi = False
        # Aeglustus
        vector = pygame.Vector2(self.kiirus_x, self.kiirus_y)
        if vector.length() > 0 and self.kiirus_x != 0:
            angle = abs(math.atan(self.kiirus_y/self.kiirus_x))
            if self.kiirus_x > 0:
                self.kiirus_x = round((vector.length() - self.aeglustus) * math.cos(angle))
            elif self.kiirus_x < 0:
                self.kiirus_x = round(-((vector.length() - self.aeglustus) * math.cos(angle)))
            if self.kiirus_y > 0:
                self.kiirus_y = round((vector.length() - self.aeglustus) * math.sin(angle))
            elif self.kiirus_y < 0:
                self.kiirus_y = round(-((vector.length() - self.aeglustus) * math.sin(angle)))
        elif self.kiirus_x == 0 and abs(self.kiirus_y > 0):
            if self.kiirus_y > 0:
                self.kiirus_y -= self.aeglustus
            elif self.kiirus_y > 0:
                self.kiirus_y += self.aeglustus
        if vector.length() <= 30:
            self.kiirus_x = 0
            self.kiirus_y = 0

        #Auku sisse loomine saamine
        if self.ekraan.get_at([int(self.x + self.pall_mask.get_size()[0]/2), int(self.y + self.pall_mask.get_size()[1]/2)]) == pygame.Color(0, 0, 0, 255):
            self.ekraan.blit(self.pall,(900 - self.pall_mask.get_size()[0]/2, 434 - self.pall_mask.get_size()[0]/2))
            self.kiirus_y = 0
            self.kiirus_x = 0
        else:
            self.ekraan.blit(self.pall,(self.x, self.y))


    #X ja Y kiiruse arvutamine koordinaatide muudu järgi
    def look(self):
        loogi_tugevus = 5

        x_muutus = self.alg_koord[0] - self.lopp_koord[0]
        y_muutus = self.alg_koord[1] - self.lopp_koord[1]

        self.kiirus_x = x_muutus * loogi_tugevus
        #palli y liikumise pidi teistpidi keerama millegipärast
        self.kiirus_y = y_muutus * loogi_tugevus * -1

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
