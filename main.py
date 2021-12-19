import math, pygame, pygame_gui
from pygame.constants import MOUSEBUTTONDOWN, MOUSEBUTTONUP

pygame.init()
pygame.display.set_caption('Minigolf')
aken = pygame.display.set_mode([1024, 768])
manager = pygame_gui.UIManager([1024, 768])
aken.fill([255, 255, 255])

# Pildid
sein_hor = "sein_horisontaalne.jpg"
sein_ver = "sein_vertikaalne.jpg"
kolmnurk1 = "kolmnurk1.png"
kolmnurk2 = "kolmnurk2.png"
liiv = "liiv.png"
vesi = "vesi.png"
juhis = "juhis.png"

#Helid
löök = pygame.mixer.Sound("woosh.mp3")
tabamus = pygame.mixer.Sound("pop.mp3")

# Klasside ja funktsioonide kirjeldused
# Klass Seinad() joonistab aknasse teateriba, mänguplatsi ning seda piiravad seinad
class Seinad():
    def __init__(self, ekraan):
        self.ekraan = ekraan
        
    def loo_seinad(self, taustapilt_hor, taustapilt_ver):    
        self.ekraan.fill((139, 217, 72))
        pygame.draw.rect(self.ekraan, "forestgreen", [0, 0, 1024, 100])
        self.sein_hor = pygame.image.load(taustapilt_hor)
        self.ekraan.blit(self.sein_hor, [0, 100])
        self.ekraan.blit(self.sein_hor, [0, 688])
        self.sein_ver = pygame.image.load(taustapilt_ver)
        self.ekraan.blit(self.sein_ver, [0, 100])
        self.ekraan.blit(self.sein_ver, [944, 100])
        self.sein_hor_mask = pygame.mask.from_surface(self.sein_hor)
        self.sein_ver_mask = pygame.mask.from_surface(self.sein_ver)

# Klass Tõkked() joonistab asukohta (x, y) valitud tõkke
class Tõkked():
    def __init__(self, ekraan):
        self.ekraan = ekraan

    def loo_tokked(self, pilt, x, y):
        self.tõke = pygame.image.load(pilt)
        self.ekraan.blit(self.tõke, [x, y])
        self.tõke_mask = pygame.mask.from_surface(self.tõke)
        return self.tõke_mask, [x,y], pilt

# Klass Auk() joonistab asukohta (x, y) augu
class Auk():
    def __init__(self, ekraan):
        self.ekraan = ekraan
        
    def loo_auk(self, x, y):    
        self.x = x
        self.y = y
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

# Klass Pall tekitab palli ning liigutab, lööb ja põrgatab palli
class Pall(): 
    def __init__(self, ekraan = aken, x = 200, y = 434, kiirus_x = 0, kiirus_y = 0):
        self.x = x
        self.y = y
        self.sein_hor1 = False
        self.sein_hor2 = False
        self.sein_ver1 = False
        self.sein_ver2 = False
        self.kolmnurk2 = False
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
        self.augus = False

    # Joonistab ekraanile palli
    def loo_pall(self):
        self.pall = pygame.Surface((18 * 2, 18 * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.pall, (255,255,255), (18, 18), 18)
        self.ekraan.blit(self.pall,(self.x, self.y))
        self.pall_mask = pygame.mask.from_surface(self.pall)

    #Joonistab joone palli külge, näitab planeeritava löögi suunda
    def joonista_joon(self):
        x = (self.x + self.pall_mask.get_size()[0]/2) - hiire_x
        y = (self.y + self.pall_mask.get_size()[1]/2) - hiire_y
        alg_x = self.x + self.pall_mask.get_size()[0]/2
        alg_y = self.y + self.pall_mask.get_size()[0]/2
        lop_x = self.x + self.pall_mask.get_size()[0]/2 + x
        lop_y = self.y + self.pall_mask.get_size()[0]/2 + y
        rotation = math.degrees(math.atan2(alg_y - lop_y, lop_x - alg_x)) + 90
        pygame.draw.polygon(aken, (255, 255, 255), ((lop_x+10*math.sin(math.radians(rotation)), lop_y+10*math.cos(math.radians(rotation))), (lop_x+10*math.sin(math.radians(rotation-120)), lop_y+10*math.cos(math.radians(rotation-120))), (lop_x+10*math.sin(math.radians(rotation+120)), lop_y+10*math.cos(math.radians(rotation+120)))))
        pygame.draw.line(aken, (255, 255, 255),(alg_x, alg_y), (lop_x, lop_y), 4)
    
    #Palli liikumine
    def liikumine(self, det, takistused):
        if self.kiirus_x == 0 and self.kiirus_y == 0 and not self.vesi:
            self.last_x = self.x
            self.last_y = self.y
        self.x += self.kiirus_x * det
        self.y -= self.kiirus_y * det

        # Palli põrkamine
        if abs(self.kiirus_x) > 0 or abs(self.kiirus_y) > 0:
            for toke in takistused:
                ox = toke[1][0]
                oy = toke[1][1]
                offset = int(self.x - ox), int(self.y - oy)
                collision = toke[0].overlap(self.pall_mask, offset)
                if collision:
                    if toke[2] == sein_ver and not self.sein_ver1 and not self.sein_ver2:
                        if toke[1] == [0, 100]:
                            self.sein_ver1 = True
                        elif toke[1] == [944, 100]:
                            self.sein_ver2 = True
                        vector = pygame.Vector2(self.kiirus_x,self.kiirus_y)
                        vector = vector.reflect([0, 1])
                        self.kiirus_x = -vector.x
                        self.kiirus_y = -vector.y
                    if toke[2] == sein_hor and not self.sein_hor1 and not self.sein_hor2:
                        if toke[1] == [0, 100]:
                            self.sein_hor1 = True
                        elif toke[1] == [0, 688]:
                            self.sein_hor2 = True
                        vector = pygame.Vector2(self.kiirus_x, self.kiirus_y)
                        vector = vector.reflect([1, 0])
                        self.kiirus_x = -vector.x
                        self.kiirus_y = -vector.y
                    if toke[2] == kolmnurk1 and not self.kolmnurk1:
                        if self.x <= (ox + toke[0].get_size()[0]/2 - 60):
                            vector = pygame.Vector2(self.kiirus_x, self.kiirus_y)
                            vector = vector.reflect([1, 1.7])
                            self.kiirus_x = -vector.x
                            self.kiirus_y = -vector.y
                            self.kolmnurk1 = True
                        elif self.x >= (ox + toke[0].get_size()[0]/2 + 60):
                            vector = pygame.Vector2(self.kiirus_x, self.kiirus_y)
                            vector = vector.reflect([-1, 1.7])
                            self.kiirus_x = -vector.x
                            self.kiirus_y = -vector.y
                            self.kolmnurk1 = True
                        else:
                            vector = pygame.Vector2(self.kiirus_x, self.kiirus_y)
                            vector = vector.reflect([1, 0])
                            self.kiirus_x = -vector.x
                            self.kiirus_y = -vector.y
                            self.kolmnurk1 = True
                    if toke[2] == kolmnurk2 and not self.kolmnurk2:
                        if self.x <= (ox + toke[0].get_size()[0]/2 - 60):
                            vector = pygame.Vector2(self.kiirus_x, self.kiirus_y)
                            vector = vector.reflect([-1, 1.7])
                            self.kiirus_x = -vector.x
                            self.kiirus_y = -vector.y
                            self.kolmnurk2 = True
                        elif self.x >= (ox + toke[0].get_size()[0]/2 + 60):
                            vector = pygame.Vector2(self.kiirus_x, self.kiirus_y)
                            vector = vector.reflect([1, 1.7])
                            self.kiirus_x = -vector.x
                            self.kiirus_y = -vector.y
                            self.kolmnurk2 = True
                        else:
                            vector = pygame.Vector2(self.kiirus_x, self.kiirus_y)
                            vector = vector.reflect([1, 0])
                            self.kiirus_x = -vector.x
                            self.kiirus_y = -vector.y
                            self.kolmnurk2 = True
                    if toke[2] == liiv:
                        self.aeglustus = 50
                        self.liiv = True
                    if toke[2] == vesi:
                        vector = pygame.Vector2(self.kiirus_x, self.kiirus_y)
                        self.aeglustus = 100
                        self.vesi = True
                elif not collision:
                    if toke[2] == liiv and not self.vesi:
                        self.aeglustus = 5
                        self.liiv = False
                    if toke[2] == sein_ver and toke[1] == [0, 100] and self.sein_ver1:
                        self.sein_ver1 = False
                    if toke[2] == sein_ver and toke[1] == [944, 100] and self.sein_ver2:
                        self.sein_ver2 = False
                    if toke[2] == sein_hor and toke[1] == [0, 100] and self.sein_hor1:
                        self.sein_hor1 = False
                    if toke[2] == sein_hor and toke[1] == [0, 688] and self.sein_hor2:
                        self.sein_hor2 = False
                    if toke[2] == kolmnurk1:
                        self.kolmnurk1 = False
                    if toke[2] == kolmnurk2:
                        self.kolmnurk2 = False
        if self.vesi and self.kiirus_x == 0 and self.kiirus_y == 0:
            self.x = self.last_x
            self.y = self.last_y
            self.aeglustus = 5
            self.vesi = False

        # Palli aeglustus (liivas)
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
        if vector.length() <= 50:
            self.kiirus_x = 0
            self.kiirus_y = 0

        #Auku sisse löömine 
        if self.ekraan.get_at([int(self.x + self.pall_mask.get_size()[0]/2), int(self.y + self.pall_mask.get_size()[1]/2)]) == pygame.Color(0, 0, 0, 255):
            self.ekraan.blit(self.pall,(900 - self.pall_mask.get_size()[0]/2, 434 - self.pall_mask.get_size()[0]/2))
            self.kiirus_y = 0
            self.kiirus_x = 0
            self.augus = True
        else:
            self.ekraan.blit(self.pall,(self.x, self.y))

    #X ja Y kiiruse arvutamine koordinaatide muudu järgi
    def look(self):
        loogi_tugevus = 5

        x_muutus = self.x + self.pall_mask.get_size()[0]/2 - self.lopp_koord[0]
        y_muutus = self.y + self.pall_mask.get_size()[1]/2 - self.lopp_koord[1]

        self.kiirus_x = x_muutus * loogi_tugevus
        self.kiirus_y = y_muutus * loogi_tugevus * -1
        
# Funktsioonid (augu tabamisel)
def augus(palli_isend):
    if palli_isend.augus:
        #Tabamuse heli
        tabamus.play()
        palli_isend.augus = False
        return True
    else:
        return False

def uusTaseJaPall(hetke_tase):   
    hetke_tase += 1
    uus_pall = Pall(aken, 200, 434, 0, 0)
    uus_pall.loo_pall()
    return hetke_tase, uus_pall

##########################################

# Muutujate algväärtustamine
kell = pygame.time.Clock()
avaekraan = True
mäng_käib = True
hiir = False
tokked = []
tase = 1
tase_valitud = 0
löökide_arv = 0


# Loome isendi klassist Seinad()
seinad = Seinad(aken)   

# Loome isendi klassist tõkked
tõkked = Tõkked(aken)

# Loome isendi klassist Auk()
auk = Auk(aken)

# Loome taseme valimise nupud 
tasemenupp1 = Tasemenupp(aken, 190, 620, '1')
tasemenupp2 = Tasemenupp(aken, 250, 620, '2')
tasemenupp3 = Tasemenupp(aken, 310, 620, '3')
tasemenupp4 = Tasemenupp(aken, 370, 620, '4')
tasemenupp5 = Tasemenupp(aken, 430, 620, '5')

#Loome palli
pall = Pall(aken, 200, 434, 0, 0)
pall.loo_pall()

# Näitame avaekraani
while avaekraan:
    dt = kell.tick() / 1000
    
    # Loome mänguplatsi ja seinad
    seinad.loo_seinad(sein_hor, sein_ver)
    #Kuvame pildina avaekraani info
    aken.blit(pygame.image.load(juhis), (81,181))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            avaekraan = False
            mäng_käib = False
        # Taseme valimine
        elif event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == tasemenupp1:
                    tase_valitud = 1
                elif event.ui_element == tasemenupp2:
                    tase_valitud = 2
                elif event.ui_element == tasemenupp3:
                    tase_valitud = 3
                elif event.ui_element == tasemenupp4:
                    tase_valitud = 4
                elif event.ui_element == tasemenupp5:
                    tase_valitud = 5
            if tase_valitud != 0:
                tasemenupp1.hide()
                tasemenupp2.hide()
                tasemenupp3.hide()
                tasemenupp4.hide()
                tasemenupp5.hide()
                avaekraan = False
        manager.process_events(event)
    
    manager.update(dt)
    manager.draw_ui(aken)
    pygame.display.flip()

# Mängu enda algus

#Loome tekstikastid teadete edastamiseks
aktiivne_tase = Tekstikast(aken, 100, 20, 200, 40, "Mängid tasemel "+str(tase))
löögid = Tekstikast(aken, 400, 20, 200, 40, "Löökide arv "+str(löökide_arv))

while mäng_käib:
    
    dt = kell.tick() / 1000
    
    # Loome mänguplatsi ja seinad
    seinad.loo_seinad(sein_hor, sein_ver)   
    sein_list_hor1 = seinad.sein_hor_mask, [0, 100],  sein_hor
    sein_list_hor2 = seinad.sein_hor_mask, [0, 688],  sein_hor
    sein_list_ver1 = seinad.sein_ver_mask, [0, 100], sein_ver
    sein_list_ver2 = seinad.sein_ver_mask, [944, 100], sein_ver
    
    # Loome augu
    auk.loo_auk(900, 434)

    # Hiire positsiooni saamine
    hiire_x, hiire_y = pygame.mouse.get_pos()
    
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            mäng_käib = False
        
        # Kuvame tehtud löökide arvu
        löögid.html_text = "Löökide arv "+str(löökide_arv)
        löögid.rebuild()
        #Kuvame aktiivset taset
        aktiivne_tase.html_text = "Mängid tasemel "+str(tase)
        aktiivne_tase.rebuild()
        manager.process_events(event)

        # Hiire lohistamine löögiks
        if event.type == MOUSEBUTTONDOWN:
        #Algkoordinaatide salvestamine
            pall.alg_koord[0] = hiire_x
            pall.alg_koord[1] = hiire_y
            hiir = True

        if event.type == MOUSEBUTTONUP:
            #Lõppkoordinaatide salvestamine
            pall.lopp_koord[0] = hiire_x
            pall.lopp_koord[1] = hiire_y
            hiir = False
            #Tingimus, et palli ei saaks liikumise ajal uuesti lüüa
            if pall.kiirus_x == 0 and pall.kiirus_y == 0:
                #palli löömine
                pall.look()
                #löögi heli
                löök.play()
                #löökide loendamine
                löökide_arv += 1
    
    # Mäng ise erinevatel tasemetel
    if tase == 1:
        #List tasemel olevatest tõketest (sh seinad)
        tokked = [sein_list_hor1, sein_list_hor2, sein_list_ver1, sein_list_ver2]
        #palli liikumine ja põrkamine, sh aeglustumine ja uppumine
        pall.liikumine(dt, tokked)
        #Kui pall on augus, lähme järgmisele tasemele
        if augus(pall):
            #Kontrollime, kas tuleb minna järgmisele tasemele
            if tase < tase_valitud:
                tase, pall = uusTaseJaPall(tase)
            else:
                break
        
    elif tase == 2:       
        tõke1 = tõkked.loo_tokked(kolmnurk1, 150, 425)
        tõke2 = tõkked.loo_tokked(kolmnurk2, 450, 180)
        tokked = [tõke1, tõke2, sein_list_hor1, sein_list_hor2, sein_list_ver1, sein_list_ver2]
        pall.liikumine(dt, tokked)
        
        if augus(pall):
            if tase < tase_valitud:
                tase, pall = uusTaseJaPall(tase)
            else:
                break
            
    elif tase == 3:
        tõke1 = tõkked.loo_tokked(kolmnurk1, 150, 425)
        tõke2 = tõkked.loo_tokked(liiv, 450, 180)
        tokked = [tõke1, tõke2, sein_list_hor1, sein_list_hor2, sein_list_ver1, sein_list_ver2]
        pall.liikumine(dt, tokked)
        
        if augus(pall):
            if tase < tase_valitud:
                tase, pall = uusTaseJaPall(tase)
            else:
                break
        
    elif tase == 4:
        tõke1 = tõkked.loo_tokked(kolmnurk1, 150, 425)
        tõke2 = tõkked.loo_tokked(vesi, 450, 180)
        tõke3 = tõkked.loo_tokked(liiv, 600, 400)
        tokked = [tõke1, tõke2, tõke3, sein_list_hor1, sein_list_hor2, sein_list_ver1, sein_list_ver2]
        pall.liikumine(dt, tokked)
        
        if augus(pall):
            if tase < tase_valitud:
                tase, pall = uusTaseJaPall(tase)
            else:
                break
        
    elif tase == 5:      
        tõke1 = tõkked.loo_tokked(vesi, 90, 180)
        tõke2 = tõkked.loo_tokked(liiv, 600, 500)
        tõke3 = tõkked.loo_tokked(kolmnurk1, 150, 425)
        tõke4 = tõkked.loo_tokked(kolmnurk2, 450, 180)
        tokked = [tõke1, tõke2, tõke3, tõke4, sein_list_hor1, sein_list_hor2, sein_list_ver1, sein_list_ver2]
        pall.liikumine(dt, tokked)
        
        if augus(pall):
            break

    # Löögi suuna joonestamine
    if hiir and pall.kiirus_x == 0 and pall.kiirus_y == 0:
        pall.joonista_joon()

    manager.update(dt)
    manager.draw_ui(aken)
    pygame.display.flip()

löögid.hide()
aktiivne_tase.hide()

# Mängu kokkuvõtte väljastamine 
while mäng_käib:
    dt = kell.tick() / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mäng_käib = False
       #Teatekast kokkuvõttega
        kokkuvõte = Tekstikast(aken, 400, 20, 200, 60, "Mäng sai läbi! <BR>Löökide arv "+str(löökide_arv))
        
        manager.process_events(event)
        
    manager.update(dt)
    manager.draw_ui(aken)
    pygame.display.flip()
      
pygame.quit()
