import pygame_gui, pygame, math, sys

sein_hor = "sein_horisontaalne.jpg"
sein_ver = "sein_vertikaalne.jpg"
kolmnurk1 = "kolmnurk1.png"
kolmnurk2 = "kolmnurk2.png"
liiv = "liiv.png"
vesi = "vesi.png"

manager = pygame_gui.UIManager([1024, 768])

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

if __name__ == '__main__':
    print("Käivita main fail")
    sys.exit()