"""Hard lessons drawn with lessonkit, first half: chicks in a nest, biplane,
gumball machine, gummy bears, cat with a pumpkin (built by make_hard.py)"""

from lessonkit import (Lesson, arc, circle, cloud, curve, ell, join, line, moved, rrect, star, DARK)

YELLOW, ORANGE, RED, BROWN = "#ffd93b", "#ff9f1c", "#e63946", "#9c6644"
BLUE, LBLUE, GREEN, LGREEN = "#3a86ff", "#8ecae6", "#43aa8b", "#90d26d"
PINK, PURPLE, GRAY = "#ff8fab", "#9b5de5", "#a0a4a8"


# ------------------------------------------------------------------ nest
def nest():
    les = Lesson("nest-chicks", "Chicks in the nest", "Pulcini nel nido")
    bowl = curve((120, 300), (135, 375), (220, 428), (320, 436), (420, 428), (505, 375), (520, 300))
    front = join(arc(320, 300, 200, 44, 180, 0), curve((520, 300), (505, 375), (420, 428), (320, 436),
                                                         (220, 428), (135, 375), (120, 300)))
    heads = [circle(212, 252, 58), circle(428, 252, 58), circle(320, 228, 64)]
    shell = curve((262, 196), (270, 150), (320, 132), (370, 150), (378, 196), close=False)
    shell_zig = line((378, 196), (365, 184), (352, 198), (339, 184), (326, 198), (313, 184), (300, 198),
                     (287, 184), (274, 198), (262, 196))
    shell_shape = join(shell, shell_zig)
    tufts = [curve((212, 195), (204, 180), (212, 170), (222, 176)), curve((428, 195), (420, 180), (428, 170),
                                                                         (438, 176))]
    beaks = []
    for cx, cy in ((212, 266), (428, 266), (320, 246)):
        beaks.append(line((cx - 15, cy), (cx, cy - 9), (cx + 15, cy), (cx, cy + 15), close=True))
        beaks.append(line((cx - 15, cy), (cx + 15, cy)))
    eyes = [(194, 240), (230, 240), (410, 240), (446, 240), (300, 214), (340, 214)]
    straw = [curve((165, 345), (195, 360), (225, 366)), curve((250, 392), (285, 402), (318, 404)),
             curve((345, 404), (380, 400), (410, 390)), curve((430, 368), (460, 358), (485, 342)),
             curve((200, 405), (240, 418), (270, 420)), curve((370, 420), (405, 416), (440, 402)),
             line((122, 302), (98, 290)), line((518, 302), (544, 288)), line((140, 340), (112, 342)),
             line((500, 340), (528, 344))]
    les.guide("guides", les.shapes(ell(320, 360, 200, 80), circle(212, 252, 58), circle(320, 228, 64),
                                   circle(428, 252, 58)),
              "With a light pencil, softly draw a big oval at the bottom and three circles on it: they are helpers!",
              "Con la matita leggera disegna piano un grande ovale in basso e sopra tre cerchi: ci aiutano!")
    les.draw("nest", les.lines(arc(320, 300, 200, 44, 180, 0), bowl),
             "Draw the nest: a wide smile for its edge and a big round bowl under it.",
             "Disegna il nido: un grande sorriso per il bordo e sotto una ciotola tonda.")
    les.draw("chicks", les.behind([les.p(heads[0], True), les.p(heads[1], True)], front, heads[2], shell_shape)
             + les.behind([les.p(heads[2], True)], front, shell_shape),
             "Draw three round chicks peeking out of the nest: the one in the middle is the biggest.",
             "Disegna tre pulcini tondi che spuntano dal nido: quello in mezzo è il più grande.")
    les.draw("shell-tufts", [les.p(shell_shape, True)] + les.lines(*tufts),
             "Put half an eggshell with a zigzag edge on the middle chick, and a little curl on the other two.",
             "Metti mezzo guscio d'uovo a zig-zag sul pulcino in mezzo, e un ricciolo sulla testa degli altri due.")
    les.draw("faces", [les.dot(x, y, 7) for x, y in eyes] + les.lines(*beaks),
             "Draw their faces: two dot eyes each and a beak like a diamond, open with a line in the middle.",
             "Disegna i musetti: due occhi a puntino e un becco a rombo, aperto con una riga in mezzo.")
    les.draw("straw", les.lines(*straw),
             "Draw some curved lines on the nest, and a few twigs sticking out of its sides.",
             "Sul nido fai qualche linea curva, e ai lati qualche rametto che spunta fuori.")
    les.erase()
    les.color("chicks-yellow", YELLOW, [(212, 225), (428, 225), (320, 205), (300, 280), (212, 290), (428, 290)],
              "Color the chicks yellow.", "Colora i pulcini di giallo.")
    les.color("beaks-orange", ORANGE, [(212, 261), (212, 271), (428, 261), (428, 271), (320, 241), (320, 251)],
              "Color the beaks orange.", "Colora i becchi di arancione.")
    les.color("nest-brown", BROWN, [(320, 380), (150, 330), (490, 330), (320, 425), (230, 380), (400, 380)],
              "Color the nest brown. The eggshell stays white!", "Colora il nido di marrone. Il guscio resta bianco!")
    return les


# --------------------------------------------------------------- biplane
def biplane():
    les = Lesson("biplane", "Biplane", "Biplano")
    body = curve((150, 214), (230, 202), (360, 202), (450, 212), (488, 228), (490, 252), (455, 266),
                 (360, 272), (230, 266), (150, 238), close=True, corners=(0, 9))
    fin = curve((158, 216), (160, 170), (178, 158), (196, 166), (214, 206), close=False, corners=(0, 4))
    fin_shape = curve((158, 216), (160, 170), (178, 158), (196, 166), (214, 206), (180, 212), close=True,
                      corners=(0, 4, 5))
    tailwing = rrect(122, 224, 214, 240, 8)
    upper = rrect(226, 146, 436, 170, 12)
    lower = rrect(240, 266, 420, 288, 11)
    struts = [line((262, 170), (262, 206)), line((402, 170), (402, 210))]
    prop = [ell(500, 240, 8, 50), circle(493, 240, 7)]
    pilot = circle(330, 192, 15)
    goggles = line((318, 188), (343, 188))
    legs = [line((300, 288), (322, 330)), line((345, 288), (322, 330))]
    wheel = circle(322, 340, 20)
    speed = [line((60, 196), (110, 196)), line((44, 226), (100, 226)), line((64, 256), (112, 256))]
    clouds = [cloud(470, 70, 600, 130), cloud(60, 330, 200, 400), cloud(450, 360, 560, 410)]
    les.guide("guides", [les.p(ell(320, 236, 175, 36), True), les.p(line((220, 158), (440, 158))),
                         les.p(line((235, 277), (425, 277)))],
              "With a light pencil, softly draw a long oval in the middle and two long lines, above and under it.",
              "Con la matita leggera disegna piano un ovale lungo in mezzo e due righe lunghe, sopra e sotto.")
    les.draw("body", les.behind([les.p(body, True)], lower, tailwing, fin_shape)
             + les.behind([les.p(fin)], tailwing) + [les.p(tailwing, True)]
             + les.behind([les.p(pilot, True), les.p(goggles)], body, upper),
             "Draw the plane's long body, a fin on its tail, a small tail wing, and the pilot's head on top.",
             "Disegna il corpo lungo dell'aereo, la pinna sulla coda, una piccola ala dietro e la testa del pilota.")
    les.draw("wings", les.shapes(upper, lower),
             "Draw two long wings with round ends: one above the plane and one under it.",
             "Disegna due ali lunghe con le punte tonde: una sopra l'aereo e una sotto.")
    les.draw("struts-propeller", les.lines(*struts) + les.shapes(*prop),
             "Join the wings with two sticks, and draw the propeller on the nose: a tall thin oval.",
             "Unisci le ali con due bastoncini e sul muso disegna l'elica: un ovale alto e sottile.")
    les.draw("wheels", les.behind(les.lines(*legs), wheel) + [les.p(wheel, True)] + [les.dot(322, 340, 6)],
             "Under the plane, draw two little legs like a V and a round wheel.",
             "Sotto l'aereo disegna due gambette a V e una ruota tonda.")
    les.draw("sky", les.shapes(*clouds) + les.lines(*speed),
             "Draw three fluffy clouds and some lines behind the plane: it's going fast!",
             "Disegna tre nuvole soffici e qualche riga dietro l'aereo: va velocissimo!")
    les.erase()
    les.color("body-red", RED, [(300, 236), (190, 196), (168, 232), (420, 225)],
              "Color the plane's body red.", "Colora il corpo dell'aereo di rosso.")
    les.color("wings-yellow", YELLOW, [(330, 158), (330, 277), (500, 205), (500, 275), (500, 240)],
              "Color the wings and the propeller yellow.", "Colora di giallo le ali e l'elica.")
    les.color("wheel-gray", GRAY, [(322, 325), (322, 355)],
              "Color the wheel gray.", "Colora la ruota di grigio.")
    return les


# --------------------------------------------------------- gumball machine
def gumball():
    les = Lesson("gumball-machine", "Gumball machine", "Distributore di palline")
    globe = circle(320, 175, 115)
    cap = curve((262, 68), (268, 40), (320, 28), (372, 40), (378, 68), close=True, corners=(0, 4))
    knob = circle(320, 24, 11)
    collar = rrect(222, 270, 418, 296, 8)
    base = line((232, 296), (210, 434), (430, 434), (408, 296), close=True)
    dial = circle(320, 345, 30)
    bar = rrect(298, 340, 342, 350, 5)
    door = rrect(290, 392, 350, 422, 6)
    shine = arc(320, 175, 92, 92, 205, 245)
    balls = []
    for y, xs in ((252, (300, 340)), (214, (240, 280, 320, 360, 400)), (176, (260, 300, 340, 380))):
        balls += [(x, y) for x in xs]
    floor_balls = [(150, 418), (490, 420)]
    les.guide("guides", les.shapes(circle(320, 175, 115), rrect(212, 280, 428, 434, 4)),
              "With a light pencil, softly draw a big circle on top and a rectangle under it: they are helpers!",
              "Con la matita leggera disegna piano un grande cerchio in alto e sotto un rettangolo: ci aiutano!")
    les.draw("globe", les.behind([les.p(globe, True)], cap, collar) + les.lines(shine),
             "Go over the big circle: it's the glass ball. Add a little curved line inside for the shine.",
             "Ripassa il grande cerchio: è la palla di vetro. Dentro aggiungi una lineetta curva per il riflesso.")
    les.draw("cap-base", les.behind([les.p(knob, True)], cap) + les.shapes(cap, collar, base),
             "Draw a little cap with a knob on top, and under the ball a band and a big base.",
             "Disegna in alto un cappellino con il pomello, e sotto la palla una fascia e una grande base.")
    les.draw("dial-door", les.shapes(dial, bar, door),
             "On the base, draw a round knob with a little bar to turn it, and a small door at the bottom.",
             "Sulla base disegna una manopola tonda con una sbarretta per girarla, e in basso una porticina.")
    les.draw("gumballs", les.shapes(*[circle(x, y, 16) for x, y in balls + floor_balls]),
             "Fill the glass ball with round gumballs, and draw two more on the floor.",
             "Riempi la palla di vetro di palline tonde, e disegnane altre due per terra.")
    les.erase()
    les.color("red", RED, [(320, 50), (320, 24), (320, 283), (250, 400), (390, 400), (320, 375)],
              "Color the cap, the band and the base red.", "Colora di rosso il cappellino, la fascia e la base.")
    allb = balls + floor_balls
    les.color("yellow", YELLOW, [allb[k] for k in range(0, len(allb), 3)],
              "Color some gumballs yellow.", "Colora alcune palline di giallo.")
    les.color("blue", BLUE, [allb[k] for k in range(1, len(allb), 3)],
              "Color some gumballs blue.", "Colora altre palline di blu.")
    les.color("green", GREEN, [allb[k] for k in range(2, len(allb), 3)],
              "Color the last gumballs green.", "Colora di verde le palline che restano.")
    return les


# ------------------------------------------------------------ gummy bears
def bear_parts(cx, top, s):
    def P(x, y):
        return (cx + x * s, top + y * s)
    head = circle(*P(0, 0), 42 * s)
    ears = [circle(*P(-34, -30), 15 * s), circle(*P(34, -30), 15 * s)]
    body = ell(*P(0, 88), 50 * s, 58 * s)
    belly = ell(*P(0, 96), 26 * s, 30 * s)
    arms = [ell(*P(-48, 72), 14 * s, 26 * s, 30), ell(*P(48, 72), 14 * s, 26 * s, -30)]
    feet = [ell(*P(-26, 142), 21 * s, 15 * s), ell(*P(26, 142), 21 * s, 15 * s)]
    eyes = [P(-15, -6), P(15, -6)]
    nose = P(0, 8)
    mouth = curve(P(-10, 18), P(0, 24), P(10, 18))
    seeds = [P(0, -25), P(-34, -30), P(34, -30), P(0, 50), P(-40, 120), P(40, 120), P(0, 96),
             P(-55, 72), P(55, 72), P(-26, 146), P(26, 146)]
    return dict(head=head, ears=ears, body=body, belly=belly, arms=arms, feet=feet, eyes=eyes, nose=nose,
                mouth=mouth, seeds=seeds, s=s)


def gummy():
    les = Lesson("gummy-bears", "Gummy bears", "Orsetti gommosi")
    bears = [bear_parts(140, 208, 1.2), bear_parts(500, 208, 1.2), bear_parts(320, 160, 1.45)]
    heads, bodies, limbs, faces = [], [], [], []
    for b in bears:
        heads += les.behind(les.shapes(*b["ears"]), b["head"]) + [les.p(b["head"], True)]
        bodies += les.behind(les.shapes(b["body"]), b["head"], *b["feet"]) + [les.p(b["belly"], True)]
        limbs += les.behind(les.shapes(*b["arms"]), b["body"]) + les.shapes(*b["feet"])
        faces += [les.dot(x, y, 6 * b["s"]) for x, y in b["eyes"]]
        faces += [les.p(ell(*b["nose"], 8 * b["s"], 6 * b["s"]), True, DARK), les.p(b["mouth"])]
    les.guide("guides", les.shapes(*[b["head"] for b in bears], *[b["body"] for b in bears]),
              "With a light pencil, softly draw three circles and an oval under each one: they are helpers!",
              "Con la matita leggera disegna piano tre cerchi e sotto ognuno un ovale: ci aiutano!")
    les.draw("heads", heads,
             "Draw three round heads, each with two small round ears. The middle bear is the biggest.",
             "Disegna tre teste tonde, ognuna con due orecchie tonde piccole. L'orsetto in mezzo è il più grande.")
    les.draw("bodies", bodies,
             "Under each head draw a round body, with an oval on the tummy.",
             "Sotto ogni testa disegna un corpo tondo, con un ovale sulla pancia.")
    les.draw("arms-legs", limbs,
             "Give each bear two short round arms on the sides and two round feet at the bottom.",
             "A ogni orsetto disegna due braccine corte e tonde ai lati e due piedini tondi in basso.")
    les.draw("faces", faces,
             "Draw the faces: two dot eyes, a little black nose and a small smile.",
             "Disegna i musetti: due occhi a puntino, un nasino nero e un piccolo sorriso.")
    les.erase()
    les.color("bear-red", RED, bears[0]["seeds"], "Color the bear on the left red.",
              "Colora di rosso l'orsetto a sinistra.")
    les.color("bear-green", GREEN, bears[2]["seeds"], "Color the bear in the middle green.",
              "Colora di verde l'orsetto in mezzo.")
    les.color("bear-yellow", YELLOW, bears[1]["seeds"], "Color the bear on the right yellow.",
              "Colora di giallo l'orsetto a destra.")
    return les


# --------------------------------------------------------- Halloween cat
def halloween():
    les = Lesson("halloween-cat", "Cat and pumpkin", "Gatto e zucca")
    pumpkin = ell(420, 335, 135, 92)
    ribs = [curve((408, 245), (350, 290), (350, 380), (408, 426)), curve((432, 245), (490, 290), (490, 380),
                                                                         (432, 426))]
    stem = curve((404, 248), (402, 212), (414, 200), (430, 206), (436, 248), corners=(0, 4))
    stem_shape = curve((404, 248), (402, 212), (414, 200), (430, 206), (436, 248), close=True, corners=(0, 4))
    leaf_ = curve((432, 222), (460, 196), (494, 206), (468, 228), (432, 222), corners=(0, 2, 4))
    eyes = [line((340, 330), (358, 296), (376, 330), close=True), line((464, 330), (482, 296), (500, 330), close=True)]
    nose = line((410, 352), (420, 336), (430, 352), close=True)
    mouth = join(curve((338, 362), (380, 410), (460, 410), (502, 362)),
                 line((502, 362), (478, 376), (474, 366), (452, 380), (447, 370)),
                 curve((447, 370), (420, 382), (393, 370)),
                 line((393, 370), (388, 380), (366, 366), (362, 376), (338, 362)))
    head = circle(170, 225, 56)
    ears = [line((122, 200), (122, 148), (162, 172), close=True), line((178, 172), (218, 148), (218, 200), close=True)]
    body = curve((140, 270), (118, 330), (112, 400), (140, 430), (200, 430), (228, 400), (222, 330), (200, 270),
                 close=True)
    legs = [line((158, 360), (158, 428)), line((182, 360), (182, 428))]
    tail = curve((222, 410), (262, 420), (282, 380), (268, 330), (252, 318), (244, 330), (258, 360), (254, 392),
                 (226, 396), close=True, corners=(4, 5))
    c_eyes = [ell(150, 220, 11, 13), ell(190, 220, 11, 13)]
    pupils = [ell(150, 220, 3, 9), ell(190, 220, 3, 9)]
    c_nose = line((164, 240), (176, 240), (170, 248), close=True)
    c_mouth = [curve((158, 256), (164, 260), (170, 252)), curve((170, 252), (176, 260), (182, 256))]
    whiskers = [line((140, 246), (100, 240)), line((140, 254), (102, 262)), line((200, 246), (240, 240)),
                line((200, 254), (238, 262))]
    moon = join(arc(95, 90, 48, 48, 60, 300), arc(115, 90, 41.8, 41.8, 275.5, 84.5))
    stars = [star(300, 70, 16, 7), star(540, 110, 14, 6), star(250, 140, 10, 4.5)]
    les.draw("pumpkin", les.behind([les.p(pumpkin, True)], stem_shape)
             + les.behind(les.lines(*ribs), stem_shape, *eyes, nose, mouth)
             + [les.p(stem_shape, True)] + les.behind([les.p(leaf_, True)], stem_shape),
             "On the right, draw a big round pumpkin with two curved lines inside, a stem on top and a leaf.",
             "A destra disegna una grande zucca tonda con due linee curve dentro, il gambo in alto e una foglia.")
    les.draw("pumpkin-face", les.shapes(*eyes, nose, mouth),
             "Give the pumpkin a funny face: two triangle eyes, a small triangle nose and a smile with teeth.",
             "Fai alla zucca una faccia buffa: due occhi a triangolo, un nasino a triangolo e un sorriso coi denti.")
    les.draw("cat", les.behind(les.shapes(*ears), head) + [les.p(head, True)]
             + les.behind([les.p(body, True)], head, tail) + les.lines(*legs) + [les.p(tail, True)],
             "On the left, draw a cat sitting: a round head with two pointy ears, a body, two legs and a curly tail.",
             "A sinistra disegna un gatto seduto: testa tonda con due orecchie a punta, il corpo, due zampe e la coda.")
    les.draw("cat-face", les.shapes(*c_eyes) + [les.p(pp, True, DARK) for pp in pupils]
             + [les.p(c_nose, True, DARK)] + les.lines(*c_mouth, *whiskers),
             "Draw the cat's face: two oval eyes with a thin black line inside, a nose, a mouth and long whiskers.",
             "Disegna il muso del gatto: occhi ovali con una righetta nera dentro, il naso, la bocca e i baffi.")
    les.draw("sky", les.shapes(moon, *stars),
             "Up in the sky, draw a moon like a big letter C and three little stars.",
             "In cielo disegna una luna come una grande lettera C e tre stelline.")
    les.color("pumpkin-orange", ORANGE, [(420, 280)],
              "Color the pumpkin orange.", "Colora la zucca di arancione.", inside=[pumpkin])
    les.color("yellow", YELLOW, [(358, 320), (482, 320), (420, 347), (420, 392), (300, 70), (540, 110),
                                 (250, 140), (150, 230), (190, 230), (60, 90)],
              "Color the pumpkin's face, the cat's eyes, the moon and the stars yellow.",
              "Colora di giallo la faccia della zucca, gli occhi del gatto, la luna e le stelle.")
    les.color("cat-gray", GRAY, [(170, 195)],
              "Color the cat gray.", "Colora il gatto di grigio.", inside=[head, *ears, body, tail])
    les.color("stem-green", GREEN, [(418, 225), (465, 213)],
              "Color the stem and the leaf green.", "Colora di verde il gambo e la foglia.")
    return les


LESSONS = [nest, biplane, gumball, gummy, halloween]
