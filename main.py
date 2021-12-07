import pygame
pygame.init()
aken = pygame.display.set_mode([1024, 768])
aken.fill([255,255,255])

# Piltide määramine
sein_hor = "sein_horisontaalne.jpg"
sein_ver = "sein_vertikaalne.jpg"
vesi = "vesi.png"
kivi = "kivi.png"
kolmnurk1 = "kolmnurk1.png"
kolmnurk2 = "kolmnurk2.png"
liiv = "liiv.png"

# Panin tasemete valiku esialgu käsureale, kuni täpsustame, kes ja kuidas seda teeb
valik = True
while valik:
    tase = int(input("Vali, mis tasemega väljakul soovite mängida (1 - 5)."))
    if tase in range(1,6):
        valik = False
    else:
        print("Sellist taset pole. Proovige uuesti!")



# Klass Seinad() joonistab aknasse teateriba ning mänguplatsi piiravad seinad 
class Seinad():
    def __init__(self, ekraan, taustapilt_hor, taustapilt_ver):
        self.taustapilt_hor = taustapilt_hor
        self.taustapilt_ver = taustapilt_ver
        self.ekraan = ekraan
                
    def loo_taust(self):
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
                
    def loo_tõke(self):
        self.tõke = pygame.image.load(self.pilt)
        self.ekraan.blit(self.tõke, [self.x,self.y])
        
# Klass Auk() joonistab punkti (x, y) augu  
class Auk():
    def __init__(self, ekraan, x, y):
        self.x = x
        self.y = y
        self.ekraan = ekraan
                
    def loo_auk(self):
        pygame.draw.circle(self.ekraan, [0,0,0], [self.x,self.y], 25, 0)


#----------------------------------------------------------------------

# See on juba mängu enda kood
mäng_käib = True
while mäng_käib:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            mäng_käib = False
    
    # loome isendi klassist Seinad()
    seinad = Seinad(aken,sein_hor,sein_ver)
    # Kutsume seinte loomise meetodit
    seinad.loo_taust()
    
    # loome isendi klassist Auk()
    auk = Auk(aken,900,434)
    # Kutsume augu loomise meetodit
    auk.loo_auk()
    
    #Vastavalt valitud tasemele lisame tõkked; 1. tasemel tõkkeid pole.
    if tase == 2:
        # loome isendid klassist Tõkked()
        tõke1 = Tõkked(aken,kolmnurk1,150,425)
        tõke2 = Tõkked(aken,kolmnurk2,450,180)
        # Kutsume tõkke loomise meetodit
        tõke1.loo_tõke()
        tõke2.loo_tõke()
    elif tase == 3:
        # loome isendid klassist Tõkked()
        tõke1 = Tõkked(aken,kolmnurk1,150,425)
        tõke2 = Tõkked(aken,liiv,450,180)
        # Kutsume tõkke loomise meetodit
        tõke1.loo_tõke()
        tõke2.loo_tõke()
    elif tase == 4:
        # loome isendid klassist Tõkked()
        tõke1 = Tõkked(aken,kolmnurk1,150,425)
        tõke2 = Tõkked(aken,vesi,450,180)
        tõke3 = Tõkked(aken,liiv,600,400)
        # Kutsume tõkke loomise meetodit
        tõke1.loo_tõke()
        tõke2.loo_tõke()
        tõke3.loo_tõke()
    elif tase == 5:
        # loome isendid klassist Tõkked()
        tõke1 = Tõkked(aken,liiv,450,180)
        tõke2 = Tõkked(aken,vesi,600,400)
        tõke3 = Tõkked(aken,kivi,100,550)
        tõke4 = Tõkked(aken,kivi,250,525)
        tõke5 = Tõkked(aken,kivi,360,375)
        # Kutsume tõkke loomise meetodit
        tõke1.loo_tõke()
        tõke2.loo_tõke()
        tõke3.loo_tõke()
        tõke4.loo_tõke()
        tõke5.loo_tõke()

        
    #paus
    pygame.time.delay(17)  
    pygame.display.flip()

pygame.quit()
