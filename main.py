from typing import *
from items import *
import random, pygame, math


screen = pygame.display.set_mode((1200, 800))
pygame.init()

hitboxBlocks = [line.rstrip() for line in open('Tags/hitbox.txt')]


def save_string(file: str, to_write: AnyStr):
    with open(file, 'w') as data:
        data.write(to_write)


class player(object):
    def __init__(self, x, y):
        self.hotbar = [[None, 0] * 9]
        self.x = x
        self.y = y
        self.hitbox = [self.x, self.y, 25, 75]
        self.bx = self.x // 50
        self.by = (self.y + self.hitbox[3]) // 50
        self.yvel = 0
        self.jumpticks = 0
        self.jumping = False

    def draw(self):
        pygame.draw.rect(screen, (255, 0, 0), self.hitbox)

    def checkMove(self, chunks, jumpDuration=11):
        if self.jumping:
            # ----- Defining how much the player should jump -----
            yvels = [50]
            for n in range(int(jumpDuration / 2) - 1):
                yvels.append(yvels[-1] / 2)
            yvels.append(-yvels[-1])
            for n in range(int(jumpDuration / 2) - 1):
                yvels.append(-abs(yvels[-1] * 2))

            for n in range(len(yvels)):
                if yvels[n] < 0:
                    yvels[n] = -math.ceil(yvels[n])
                else:
                    yvels[n] = -math.floor(yvels[n])

            self.yvel = yvels[self.jumpticks - 1]

            # ----- Check for moving in air -----
            if pygame.key.get_pressed()[pygame.K_LEFT]:
                if player.x > 0 and player.checkLeft(gen.chunks):
                    player.x -= 5
            if pygame.key.get_pressed()[pygame.K_RIGHT]:
                if player.x < 1200 and player.checkRight(gen.chunks):
                    player.x += 5

            # ----- If player jumps to a new square, check if that square is solid and move player down -----
            if (self.y + self.yvel) // 50 != self.y // 50:
                if not self.checkDown(chunks):
                    self.y += self.yvel
                else:
                    self.y += 50 - (self.y % 50) % 50
                    self.jumpticks = 0
                    self.jumping = False
            else:
                self.y += self.yvel

            # ----- Finalise -----
            self.hitbox = [self.x, self.y, 25, 75]
            self.bx = self.x // 50
            self.by = (self.y + self.hitbox[3]) // 50

            if jumpDuration > self.jumpticks and not self.jumpticks == 0:
                self.jumpticks += 1
                if self.jumpticks == jumpDuration:
                    self.jumpticks = 0
                    self.jumping = False
                    self.y += (50 - self.y % 50) % 50

    def move_y(self, chunks):
        chunks_to_check = []
        self.bx = self.x // 50
        self.by = (self.y + self.hitbox[3]) // 50

        if self.x % 50 <= self.hitbox[2]:
            chunks_to_check.append(self.bx)
        else:
            chunks_to_check.append(self.bx)
            chunks_to_check.append(self.bx + 1)

        if self.jumpticks == 0:
            down = True
            for xval in chunks_to_check:
                down = not str(chunks[xval][self.by]) in hitboxBlocks
                if not down:
                    break

            if down:
                if str(chunks[self.bx][(self.y + 5) // 50]) not in hitboxBlocks:
                    self.y += 5
                else:
                    self.y += 50 - self.y % 50

        else:
            self.jumping = True
            self.checkMove(chunks)

        self.hitbox = [self.x, self.y, 25, 75]

    def checkLeft(self, chunks):
        self.bx = self.x // 50
        self.by = (self.y + self.hitbox[3]) // 50

        if self.x - 5 < 0:
            return False
        if self.x % 50 != 0:
            return True
        if self.y % 50 == 25:
            if str(chunks[self.bx - 1][self.by - 1]) in hitboxBlocks or str(chunks[self.bx - 1][self.by - 2]) in hitboxBlocks:
                return False
            return True
        else:
            if str(chunks[self.bx - 1][self.by]) in hitboxBlocks or str(chunks[self.bx - 1][self.by - 1]) in hitboxBlocks or str(chunks[self.bx - 1][self.by - 2]) in hitboxBlocks:
                return False
            return True

    def checkRight(self, chunks):
        self.bx = self.x // 50
        self.by = (self.y + self.hitbox[3]) // 50

        if self.x + 5 > 1200:
            return False
        if self.x % 50 < 25:
            return True
        if self.y % 50 == 25:
            if str(chunks[self.bx + 1][self.by - 1]) in hitboxBlocks or str(chunks[self.bx + 1][self.by - 2]) in hitboxBlocks:
                return False
            return True
        else:
            if str(chunks[self.bx + 1][self.by]) in hitboxBlocks or str(chunks[self.bx + 1][self.by - 1]) in hitboxBlocks or str(chunks[self.bx + 1][self.by - 2]) in hitboxBlocks:
                return False
            return True

    def checkTop(self, chunks):
        if self.by - 1 < 0:
            return True
        if chunks[self.bx][self.by - 1] in hitboxBlocks:
            return False
        return True

    def checkDown(self, chunks, world_height=14):
        if math.ceil(self.y / 50) + 1 > world_height:
            return True
        if chunks[self.bx][math.ceil(self.y / 50) + 1] in hitboxBlocks:
            return False
        return True


class generator(object):
    def __init__(self, width: int):
        self.width = width
        self.chunks = []

    def generate(self):
        chunks = []

        for i in range(self.width):
            # Generate Bedrock (last two layers)
            chunkdata = ['0']
            if random.randint(1, 3) == 1:
                chunkdata.append('0')
            else:
                chunkdata.append('2')

            # Generate Stone:
            for n in range(7):
                chunkdata.append('2')

            # Generate Grass:
            if random.randint(1, 2) == 1:
                chunkdata.append('3')
            else:
                chunkdata.append('2')
            chunkdata.append('1')

            # Generate Air:
            for n in range(3):
                chunkdata.append('-1')

            chunkdata.reverse()
            chunks.append(chunkdata)

        self.chunks = chunks

    def generateCave(self):
        xval = random.randint(1, self.width)
        cavewidth = [random.randint(1, 3), random.randint(1, 3)]    # Width on both sides
        if xval - cavewidth[0] < 0:
            cavewidth[0] = xval - 1
        if xval + cavewidth[1] > self.width:
            cavewidth[1] = self.width - xval - 1

        caveDepth = random.randint(1, 2)
        multiplier = 1
        for n in range(sum(cavewidth) + 1):
            chunkToEdit = self.chunks[n + xval - cavewidth[0] - 1]

            for m in range(caveDepth):
                if n in [0, sum(cavewidth) + 1] and m == caveDepth:
                    chunkToEdit[3 + m] = '1'
                else:
                    chunkToEdit[3 + m] = '-1'

            if n < ((sum(cavewidth) + 1) / 2):
                caveDepth += round(random.choice([1, 1, 1, 2]) * multiplier)
            else:
                caveDepth -= round(random.choice([1, 1, 1, 2]) * multiplier)

            multiplier *= 1.1
            if '2' not in chunkToEdit:
                chunkToEdit[-2] = '2'
            if '0' not in chunkToEdit:
                chunkToEdit[-1] = '0'

    def generateVein(self, itemID, chunks):
        xval = random.randint(1, self.width) - 1
        yval = random.randint(7, 11)
        height = random.randint(1, 2)
        width = random.randint(2, 3)
        if xval + width > self.width:
            width = self.width - xval
        for n in range(width):
            for m in range(height):
                chunks[xval + n][yval + m] = itemID
            if n < math.floor(width / 2):
                height += random.randint(1, 2)
            else:
                height -= random.randint(1, 2)

            if yval + height > 13:
                height -= 2

    def draw(self):
        x, y = 0, 0

        for chunk in self.chunks:
            for block in chunk:
                screen.blit(IDs[str(block)]['texture'], (x * 50, y * 50))
                y += 1
            x += 1
            y = 0


def regenerateWorld():
    global gen

    gen.generate()
    for n in range(random.randint(2, 4)):
        gen.generateVein('4', gen.chunks)
    for n in range(random.randint(1, 3)):
        gen.generateCave()
    gen.draw()
    pygame.display.update()


player = player(0, 0)
gen = generator(24)
regenerateWorld()


def draw():
    screen.fill((0, 0, 0))

    gen.draw()
    player.draw()
    player.move_y(gen.chunks)

    pygame.display.update()

    if pygame.event.get(pygame.QUIT):
        pygame.quit()
        quit()


while True:
    draw()

    if pygame.event.get(pygame.QUIT):
        pygame.quit()
        quit()

    if pygame.key.get_pressed()[pygame.K_LEFT]:
        if player.x > 0 and player.checkLeft(gen.chunks):
            player.x -= 5
    if pygame.key.get_pressed()[pygame.K_RIGHT]:
        if player.x < 1200 and player.checkRight(gen.chunks):
            player.x += 5
    if pygame.key.get_pressed()[pygame.K_UP]:
        if not player.checkDown(gen.chunks, 14) and player.jumpticks == 0:
            player.jumpticks = 1
