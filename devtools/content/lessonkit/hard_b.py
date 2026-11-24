"""Hard lessons drawn with lessonkit, second half: garden chair, horse and
foal, knitting friends, vulture, two foxes (built by make_hard.py)"""

import math

from lessonkit import (Lesson, arc, circle, cloud, curve, ell, flower, join, leaf, line, moved, rrect, sun,
                       DARK)

YELLOW, ORANGE, RED, BROWN = "#ffd93b", "#ff9f1c", "#e63946", "#9c6644"
BLUE, LBLUE, GREEN, LGREEN = "#3a86ff", "#8ecae6", "#43aa8b", "#90d26d"
PINK, PURPLE, GRAY = "#ff8fab", "#9b5de5", "#a0a4a8"
LBROWN, DBROWN = "#d4a373", "#6f4518"


# ----------------------------------------------------------- garden chair
def garden():
    les = Lesson("garden-chair", "Chair in the garden", "Sedia in giardino")
    back = curve((246, 252), (238, 120), (262, 82), (320, 66), (378, 82), (402, 120), (394, 252), close=True,
                 corners=(0, 6))
    slats = [line((282, 76), (284, 252)), line((320, 66), (320, 252)), line((358, 76), (356, 252))]
    seat = line((214, 252), (426, 252), (448, 300), (192, 300), close=True)
    arms = [rrect(150, 232, 232, 250, 8), rrect(408, 232, 490, 250, 8)]
    legs = [line((166, 250), (166, 402)), line((190, 250), (190, 402)), line((450, 250), (450, 402)),
            line((474, 250), (474, 402)), line((166, 402), (190, 402)), line((450, 402), (474, 402))]
    chair_shapes = [back, seat, *arms, rrect(166, 250, 190, 402, 1), rrect(450, 250, 474, 402, 1)]
    top = rrect(500, 300, 604, 316, 5)
    tlegs = [line((514, 316), (514, 404)), line((590, 316), (590, 404))]
    glass = line((534, 246), (566, 246), (561, 300), (539, 300), close=True)
    straw = line((556, 252), (572, 222))
    lemon = circle(540, 248, 11)
    fence = []
    for x in range(40, 620, 46):
        fence.append(line((x, 330), (x, 190), (x + 15, 172), (x + 30, 190), (x + 30, 330), close=True))
    rails = [line((20, 220), (620, 220)), line((20, 300), (620, 300))]
    ground = join(curve((20, 404), (200, 398), (420, 404), (620, 398)), line((620, 398), (620, 458), (20, 458),
                                                                               (20, 404)))
    flowers = [flower(70, 430, 15), flower(270, 440, 14), flower(390, 432, 15), flower(560, 440, 14)]
    centers = [circle(70, 430, 6), circle(270, 440, 6), circle(390, 432, 6), circle(560, 440, 6)]
    sun_parts = sun(90, 84, 34)
    hidden = [back, seat, *arms, rrect(166, 250, 190, 402, 1), rrect(450, 250, 474, 402, 1), top, glass,
              rrect(514, 316, 515, 404, 0.4), rrect(589, 316, 590, 404, 0.4)]
    les.draw("chair-back", les.shapes(back) + les.lines(*slats),
             "In the middle, draw the back of a chair: tall, with a round top, and three lines down for the boards.",
             "In mezzo disegna lo schienale di una sedia: alto, tondo in cima, con tre righe giù per le assi.")
    les.draw("chair-seat", les.behind(les.shapes(seat), *arms) + les.shapes(*arms) + les.lines(*legs),
             "Draw the seat under the back, a flat armrest on each side and two legs under each armrest.",
             "Sotto lo schienale disegna il sedile, un bracciolo piatto per lato e sotto ogni bracciolo due gambe.")
    les.draw("table", les.shapes(top) + les.lines(*tlegs) + les.behind(les.shapes(glass), lemon)
             + les.behind(les.lines(straw), glass, lemon) + les.shapes(lemon),
             "On the right, draw a small table with a glass of lemonade, a straw and a slice of lemon.",
             "A destra disegna un tavolino con un bicchiere di limonata, la cannuccia e una fetta di limone.")
    les.draw("fence", les.behind(les.shapes(*fence) + les.lines(*rails), *hidden),
             "Behind the chair, draw a fence: boards with a pointed top and two long lines across.",
             "Dietro la sedia disegna uno steccato: assi con la punta e due lunghe righe di traverso.")
    les.draw("garden", les.shapes(ground) + les.shapes(*flowers, *centers, sun_parts[0]) + les.lines(*sun_parts[1:]),
             "Draw the ground, four little flowers in the grass and the sun up on the left.",
             "Disegna il prato, quattro fiorellini nell'erba e in alto a sinistra il sole.")
    les.color("chair-blue", BLUE, [(300, 150), (340, 150), (265, 150), (375, 150), (320, 276), (190, 241), (450, 241),
                                   (178, 330), (462, 330)],
              "Color the chair blue.", "Colora la sedia di blu.", inside=chair_shapes)
    les.color("wood-brown", BROWN, [(552, 308), (55, 260), (101, 260)],
              "Color the fence and the table brown.", "Colora di marrone lo steccato e il tavolino.",
              inside=fence + [top])
    les.color("yellow", YELLOW, [(90, 84), (550, 280), (70, 430), (270, 440), (390, 432), (560, 440), (540, 250)],
              "Color the sun, the lemonade and the middle of the flowers yellow.",
              "Colora di giallo il sole, la limonata e il centro dei fiori.")
    les.color("flowers-pink", PINK, [(70, 414), (270, 425), (390, 416), (560, 425)],
              "Color the petals pink.", "Colora i petali di rosa.",
              inside=flowers)
    les.color("grass-green", GREEN, [(330, 448), (610, 450), (130, 440), (480, 445)],
              "Color the grass green.", "Colora il prato di verde.")
    return les


# ---------------------------------------------------------- horse and foal
def horse_parts(T):
    """A horse facing right, in a 'model' space; T maps model points to the sheet"""
    def M(ch):
        return ch.map(T)
    body = M(ell(290, 285, 115, 60))
    neck = M(curve((350, 250), (392, 196), (420, 140), (462, 150), (440, 205), (412, 272), close=True,
                   corners=(0, 5)))
    head = M(curve((436, 120), (460, 100), (492, 108), (528, 136), (540, 160), (524, 176), (496, 172),
                   (462, 156), close=True))
    ears = [M(line((448, 110), (446, 74), (468, 102), close=True))]
    mane = M(curve((448, 104), (424, 104), (420, 126), (404, 132), (400, 154), (386, 162), (384, 184), (368, 194),
                   (370, 214), (356, 226), (362, 244), (392, 206), (420, 150), (444, 118), close=True))
    legs = [M(rrect(200, 300, 224, 430, 6)), M(rrect(232, 300, 256, 425, 6)), M(rrect(330, 300, 354, 430, 6)),
            M(rrect(362, 300, 386, 425, 6))]
    hooves = [M(rrect(196, 416, 228, 436, 4)), M(rrect(228, 411, 260, 431, 4)), M(rrect(326, 416, 358, 436, 4)),
              M(rrect(358, 411, 390, 431, 4))]
    tail = M(curve((182, 262), (150, 268), (128, 300), (130, 350), (144, 380), (156, 352), (164, 312), (184, 292),
                   close=True))
    eye = T((478, 128))
    nostril = T((522, 158))
    mouth = M(curve((506, 170), (520, 168)))
    return dict(body=body, neck=neck, head=head, ears=ears, mane=mane, legs=legs, hooves=hooves, tail=tail,
                eye=eye, nostril=nostril, mouth=mouth)


def horses():
    les = Lesson("horse-foal", "Horse and foal", "Cavallo e puledro")
    big = horse_parts(lambda p: (p[0] - 60, p[1] - 15))
    s = 0.56

    def small_T(p):          # smaller, facing left, on the right
        x, y = 290 + (p[0] - 290) * s, 285 + (p[1] - 285) * s
        return (2 * 290 - x + 220, y + 60)
    foal = horse_parts(small_T)
    lines_big = (les.behind(les.shapes(*big["ears"]), big["head"]) + [les.p(big["head"], True)]
                 + les.behind(les.shapes(big["neck"]), big["head"], big["mane"])
                 + les.behind(les.shapes(big["body"]), big["neck"])
                 + les.behind([les.p(big["mane"], True)], big["head"]))
    rest_big = (les.behind(les.shapes(*big["legs"]), big["body"], *big["hooves"]) + les.shapes(*big["hooves"])
                + les.behind(les.shapes(big["tail"]), big["body"]))
    foal_lines = (les.behind(les.shapes(*foal["ears"]), foal["head"]) + [les.p(foal["head"], True)]
                  + les.behind(les.shapes(foal["neck"]), foal["head"], foal["mane"])
                  + les.behind(les.shapes(foal["body"]), foal["neck"])
                  + les.behind(les.shapes(*foal["legs"]), foal["body"], *foal["hooves"]) + les.shapes(*foal["hooves"])
                  + les.behind(les.shapes(foal["tail"]), foal["body"])
                  + les.behind([les.p(foal["mane"], True)], foal["head"]))
    faces = [les.dot(*big["eye"], 6), les.p(ell(*big["nostril"], 5, 4), True, DARK), les.p(big["mouth"]),
             les.dot(*foal["eye"], 5), les.p(ell(*foal["nostril"], 3.5, 3), True, DARK), les.p(foal["mouth"])]
    grass = []
    for x in (60, 170, 300, 420):
        grass += [curve((x - 8, 456), (x - 13, 440)), curve((x, 456), (x, 434)), curve((x + 8, 456), (x + 13, 440))]
    les.guide("guides", les.shapes(ell(230, 270, 115, 60), ell(510, 345, 64, 34)),
              "With a light pencil, softly draw a big oval on the left and a small one on the right: they are helpers!",
              "Con la matita leggera disegna piano un ovale grande a sinistra e uno piccolo a destra: ci aiutano!")
    les.draw("horse", lines_big,
             "Draw the big horse: the oval body, a long neck with a wavy mane, and a long head with a pointy ear.",
             "Disegna il cavallo grande: il corpo ovale, il collo lungo con la criniera a onde e la testa con l'orecchio.")
    les.draw("horse-legs", rest_big,
             "Give it four long legs with hooves and a long tail.",
             "Fagli quattro zampe lunghe con gli zoccoli e una lunga coda.")
    les.draw("foal", foal_lines,
             "On the right, draw the foal the same way, but small and looking at the horse.",
             "A destra disegna il puledro allo stesso modo, ma piccolo e girato verso il cavallo.")
    les.draw("faces", faces + les.lines(*grass),
             "Draw their faces: an eye, a nostril and a little mouth. Add some grass on the ground.",
             "Disegna i musi: un occhio, la narice e la bocca. Aggiungi qualche ciuffo d'erba per terra.")
    les.erase()
    les.color("horse-brown", BROWN, [(240, 270)], "Color the big horse brown.", "Colora il cavallo grande di marrone.",
              inside=[big["body"], big["neck"], big["head"], *big["ears"], *big["legs"]])
    les.color("foal-light-brown", LBROWN, [(510, 345)], "Color the foal light brown.",
              "Colora il puledro di marrone chiaro.",
              inside=[foal["body"], foal["neck"], foal["head"], *foal["ears"], *foal["legs"]])
    les.color("manes-dark", DBROWN, [],
              "Color the manes, the tails and the hooves dark brown.",
              "Colora di marrone scuro le criniere, le code e gli zoccoli.",
              inside=[big["mane"], big["tail"], *big["hooves"], foal["mane"], foal["tail"], *foal["hooves"]])
    return les


# ------------------------------------------------------- knitting friends
def knitting():
    les = Lesson("knitting-friends", "Knitting friends", "Amici a maglia")
    k_head = circle(190, 200, 68)
    k_ears = [line((138, 162), (130, 106), (176, 136), close=True), line((204, 136), (250, 106), (242, 162), close=True)]
    k_inner = [line((142, 150), (138, 120), (164, 138), close=True), line((216, 138), (242, 120), (238, 150), close=True)]
    k_body = curve((145, 250), (122, 320), (128, 392), (170, 412), (210, 412), (252, 392), (258, 320), (235, 250),
                   close=True)
    k_paws = [ell(168, 330, 17, 13), ell(212, 330, 17, 13)]
    k_tail = curve((132, 390), (88, 400), (72, 360), (90, 320), (104, 330), (92, 360), (104, 380), (134, 372),
                   close=True, corners=(3, 4))
    b_head = circle(450, 212, 64)
    b_ears = [ell(422, 112, 21, 58, -10), ell(482, 110, 21, 58, 12)]
    b_inner = [ell(422, 118, 9, 40, -10), ell(482, 116, 9, 40, 12)]
    b_body = curve((408, 260), (386, 330), (392, 395), (430, 414), (470, 414), (508, 395), (514, 330), (492, 260),
                   close=True)
    b_paws = [ell(428, 330, 16, 12), ell(472, 330, 16, 12)]
    b_feet = [ell(420, 414, 26, 14), ell(480, 414, 26, 14)]
    ball = circle(322, 392, 44)
    wraps = [arc(322, 392, 44, 20, 200, 340), arc(322, 392, 20, 44, 110, 250), arc(322, 392, 30, 44, -70, 70)]
    needles = [line((150, 300), (240, 360)), line((230, 300), (150, 368))]
    knit = rrect(170, 340, 222, 380, 6)
    stitches = [line((176, 362), (184, 354), (192, 364), (200, 354), (208, 364), (216, 356))]
    thread = curve((222, 372), (262, 400), (282, 372))
    thread2 = curve((362, 380), (392, 352), (432, 330))
    k_eyes = [arc(166, 200, 11, 9, 200, 340), arc(214, 200, 11, 9, 200, 340)]
    b_eyes = [(428, 205), (472, 205)]
    noses = [line((183, 222), (197, 222), (190, 230), close=True), ell(450, 228, 7, 5)]
    mouths = [curve((178, 236), (184, 241), (190, 234)), curve((190, 234), (196, 241), (202, 236)),
              curve((440, 240), (445, 245), (450, 238)), curve((450, 238), (455, 245), (460, 240))]
    whiskers = [line((150, 222), (112, 216)), line((150, 230), (114, 238)), line((230, 222), (268, 216)),
                line((230, 230), (266, 238))]
    cheeks = [ell(152, 236, 11, 7), ell(228, 236, 11, 7), ell(414, 236, 10, 7), ell(486, 236, 10, 7)]
    les.guide("guides", les.shapes(circle(190, 200, 68), circle(450, 212, 64), circle(322, 392, 44)),
              "With a light pencil, softly draw two big circles side by side and a small one between them, lower down.",
              "Con la matita leggera disegna piano due cerchi grandi vicini e uno piccolo più in basso, in mezzo.")
    les.draw("kitten", les.behind(les.shapes(*k_ears), k_head) + [les.p(k_head, True)]
             + les.behind(les.shapes(k_body), k_head, k_tail) + les.shapes(k_tail, *k_paws),
             "On the left, draw a kitten: a round head with two pointy ears, a round body, two paws and a tail.",
             "A sinistra disegna un gattino: la testa tonda con due orecchie a punta, il corpo, due zampine e la coda.")
    les.draw("bunny", les.behind(les.shapes(*b_ears), b_head) + [les.p(b_head, True)]
             + les.behind(les.shapes(b_body), b_head, *b_feet) + les.shapes(*b_paws, *b_feet),
             "On the right, draw a bunny: a round head with two long ears, a body, two paws and two big feet.",
             "A destra disegna un coniglietto: la testa tonda con due orecchie lunghe, il corpo, due zampine e i piedi.")
    les.draw("faces", les.shapes(*k_inner) + les.behind(les.shapes(*b_inner), b_head) + les.lines(*k_eyes)
             + [les.dot(x, y, 7) for x, y in b_eyes] + [les.p(n, True, DARK) for n in noses]
             + les.lines(*mouths, *whiskers) + les.shapes(*cheeks),
             "Draw their faces: happy eyes, a little nose, a smile, round cheeks, and lines inside the ears.",
             "Disegna i musetti: occhi felici, il nasino, il sorriso, le guance tonde e le righe dentro le orecchie.")
    les.draw("yarn", les.behind(les.shapes(ball) + les.lines(*wraps), *k_paws)
             + les.behind(les.lines(*needles), knit, *k_paws) + les.shapes(knit) + les.lines(*stitches)
             + les.behind(les.lines(thread, thread2), ball, *b_paws, knit),
             "Draw a ball of yarn between them, and the kitten's two needles with a little piece of knitting.",
             "In mezzo disegna un gomitolo, e al gattino due ferri con un pezzetto di maglia.")
    les.erase()
    les.color("kitten-orange", ORANGE, [(190, 175)], "Color the kitten orange.", "Colora il gattino di arancione.",
              inside=[k_head, *k_ears, k_body, *k_paws, k_tail])
    les.color("bunny-gray", GRAY, [(450, 180), (428, 330), (472, 330)], "Color the bunny gray.", "Colora il coniglietto di grigio.",
              inside=[b_head, *b_ears, b_body, *b_paws, *b_feet])
    les.color("pink", PINK, [(422, 118), (482, 116), (150, 144), (230, 144)] + [(c.start[0] - 9, c.start[1])
                                                                                  for c in cheeks],
              "Color the cheeks and the inside of the ears pink.", "Colora di rosa le guance e l'interno delle orecchie.",
              inside=[*k_inner, *b_inner, *cheeks])
    les.color("yarn-purple", PURPLE, [(322, 392), (196, 346), (196, 373)], "Color the ball of yarn and the knitting purple.",
              "Colora di viola il gomitolo e la maglia.", inside=[ball, knit])
    return les


# --------------------------------------------------------------- vulture
def vulture():
    les = Lesson("vulture", "Flying vulture", "Avvoltoio in volo")
    head = circle(320, 132, 30)
    beak = curve((308, 150), (320, 146), (334, 152), (334, 172), (322, 186), (316, 176), (310, 164), close=True,
                 corners=(0,))
    beak = curve((306, 148), (334, 148), (336, 170), (326, 188), (318, 178), (322, 168), (312, 160), close=True,
                 corners=(0, 1, 3))
    neck = [line((308, 158), (306, 198)), line((332, 158), (334, 198))]
    ruff_pts = []
    for k in range(18):
        a = math.radians(20 * k)
        r = 1.0 if k % 2 == 0 else 0.8
        ruff_pts.append((320 + 54 * r * math.cos(a), 208 + 24 * r * math.sin(a)))
    ruff = curve(*ruff_pts, close=True)
    body = ell(320, 280, 56, 76)
    wing_l = line((276, 228), (200, 170), (120, 150), (44, 186), (70, 222), (84, 206), (104, 246), (120, 230),
                  (140, 270), (160, 252), (180, 290), (206, 274), (230, 306), (268, 300), close=True)
    wing_l = curve((276, 228), (200, 170), (120, 150), (44, 186), (70, 222), (84, 206), (104, 246), (120, 230),
                   (140, 270), (160, 252), (180, 290), (206, 274), (230, 306), (268, 300), close=True,
                   corners=tuple(range(3, 14)))
    wing_r = moved(wing_l, flip=True, ox=320)
    tail = line((292, 342), (276, 400), (300, 388), (320, 404), (340, 388), (364, 400), (348, 342))
    tail_shape = line((292, 342), (276, 400), (300, 388), (320, 404), (340, 388), (364, 400), (348, 342), close=True)
    brows = [line((302, 118), (314, 124)), line((338, 118), (326, 124))]
    sun_parts = sun(548, 80, 34)
    clouds = [cloud(40, 360, 190, 430), cloud(450, 340, 610, 420)]
    les.guide("guides", les.shapes(ell(320, 280, 56, 76), circle(320, 132, 30)) + les.lines(line((40, 190), (600, 190))),
              "With a light pencil, softly draw an oval in the middle, a small circle on top and a long line across.",
              "Con la matita leggera disegna piano un ovale in mezzo, sopra un cerchietto e una lunga riga di traverso.")
    les.draw("head", les.behind([les.p(head, True)], beak) + les.shapes(beak) + les.lines(*brows)
             + [les.dot(308, 130, 5), les.dot(332, 130, 5)],
             "Draw the vulture's bald head: a circle with two eyes, grumpy eyebrows and a big hooked beak.",
             "Disegna la testa pelata dell'avvoltoio: un cerchio con due occhi, le sopracciglia e un grosso becco a uncino.")
    les.draw("body", les.behind(les.lines(*neck), head, beak, ruff) + les.behind(les.shapes(body), ruff)
             + les.shapes(ruff),
             "Draw a short neck, a fluffy collar with soft points and the body under it, like a big oval.",
             "Disegna il collo corto, un collare soffice a punte morbide e sotto il corpo, come un grande ovale.")
    les.draw("wings", les.behind(les.shapes(wing_l, wing_r), body, ruff),
             "Draw two big open wings, one on each side, with long feathers at the ends like fingers.",
             "Disegna due grandi ali aperte, una per lato, con le piume lunghe in fondo come dita.")
    les.draw("tail", les.behind(les.lines(tail), body),
             "Under the body, draw the tail like a fan with three points.",
             "Sotto il corpo disegna la coda come un ventaglio con tre punte.")
    les.draw("sky", les.shapes(sun_parts[0], *clouds) + les.lines(*sun_parts[1:]),
             "Draw the sun up on the right and two fluffy clouds down below.",
             "In alto a destra disegna il sole e in basso due nuvole soffici.")
    les.erase()
    les.white((320, 212))
    les.color("brown", BROWN, [(320, 290)], "Color the body, the wings and the tail brown.",
              "Colora di marrone il corpo, le ali e la coda.", inside=[body, wing_l, wing_r, tail_shape])
    les.color("head-pink", PINK, [(320, 112), (312, 166)], "Color the head and the neck pink.",
              "Colora di rosa la testa e il collo.", inside=[head])
    les.color("yellow", YELLOW, [(548, 80)], "Color the beak and the sun yellow.", "Colora di giallo il becco e il sole.",
              inside=[beak])
    return les


# -------------------------------------------------------------- two foxes
def fox_parts(cx, flip=False):
    def F(ch):
        return ch

    def P(x, y):
        return (cx - x, y) if flip else (cx + x, y)
    head = F(curve(P(-58, 196), P(-42, 156), P(-34, 146), P(-46, 92), P(-10, 130), P(0, 128), P(10, 130), P(46, 92),
                   P(34, 146), P(42, 156), P(58, 196), P(18, 232), P(0, 236), P(-18, 232), close=True,
                   corners=(0, 3, 4, 8, 7, 10)))
    inner_ears = [F(line(P(-38, 140), P(-42, 106), P(-18, 132))), F(line(P(38, 140), P(42, 106), P(18, 132)))]
    muzzle = [F(curve(P(-58, 196), P(-30, 182), P(-12, 196), P(0, 212))),
              F(curve(P(58, 196), P(30, 182), P(12, 196), P(0, 212)))]
    eyes = [P(-24, 170), P(24, 170)]
    nose = F(ell(*P(0, 212), 8, 6))
    body = F(curve(P(-30, 228), P(-56, 290), P(-62, 360), P(-44, 400), P(0, 404), P(44, 400), P(62, 360),
                   P(56, 290), P(30, 228), close=True))
    chest = F(curve(P(-30, 221), P(-20, 290), P(0, 318), P(20, 290), P(30, 221)))
    legs = [F(line(P(-18, 330), P(-18, 400))), F(line(P(18, 330), P(18, 400)))]
    paws = [F(arc(*P(-30, 400), 12, 8, 180, 360)), F(arc(*P(30, 400), 12, 8, 180, 360))]
    tail = F(curve(P(-50, 392), P(-110, 400), P(-140, 350), P(-128, 290), P(-96, 262), P(-80, 290), P(-84, 330),
                   P(-60, 360), close=True, corners=(0, 7)))
    tip = F(curve(P(-129, 306), P(-112, 300), P(-96, 304), P(-82, 296)))
    return dict(head=head, inner_ears=inner_ears, muzzle=muzzle, eyes=eyes, nose=nose, body=body, chest=chest,
                legs=legs, paws=paws, tail=tail, tip=tip)


def foxes():
    les = Lesson("two-foxes", "Two foxes in the woods", "Due volpi nel bosco")
    a, b = fox_parts(200), fox_parts(440, flip=True)
    mush = [(320, 400, 34), (276, 420, 22)]
    caps, stems, dots = [], [], []
    for x, y, r in mush:
        caps.append(join(arc(x, y - 0.3 * r, r, r * 0.9, 180, 360), line((x + r, y - 0.3 * r), (x - r, y - 0.3 * r))))
        stems.append(rrect(x - 0.35 * r, y - 0.3 * r, x + 0.35 * r, y + 0.9 * r, 5))
        dots += [circle(x - 0.45 * r, y - 0.75 * r, 0.17 * r), circle(x + 0.35 * r, y - 0.85 * r, 0.15 * r)]
    grass = []
    for x in (96, 384, 536):
        grass += [curve((x - 8, 456), (x - 13, 440)), curve((x, 456), (x, 434)), curve((x + 8, 456), (x + 13, 440))]
    leaves = [leaf((300, 120), (340, 100), 9, 0), leaf((360, 180), (330, 160), 8, 0), leaf((90, 90), (120, 70), 8, 0),
              leaf((550, 80), (520, 60), 8, 0)]
    les.guide("guides", les.shapes(circle(200, 180, 55), circle(440, 180, 55), ell(200, 320, 60, 85),
                                   ell(440, 320, 60, 85)),
              "With a light pencil, softly draw two circles and an oval under each one: they are helpers!",
              "Con la matita leggera disegna piano due cerchi e sotto ognuno un ovale: ci aiutano!")
    les.draw("heads", les.shapes(a["head"], b["head"]),
             "Draw two fox heads looking at each other: big pointy ears on top and pointy cheeks on the sides.",
             "Disegna due teste di volpe che si guardano: grandi orecchie a punta in alto e guance a punta ai lati.")
    les.draw("faces", les.lines(*a["inner_ears"], *b["inner_ears"], *a["muzzle"], *b["muzzle"])
             + [les.dot(x, y, 7) for x, y in a["eyes"] + b["eyes"]]
             + [les.p(a["nose"], True, DARK), les.p(b["nose"], True, DARK)],
             "Draw the faces: a line in each ear, a line like two hills on the cheeks, two eyes and a black nose.",
             "Disegna i musi: una riga in ogni orecchio, una linea a due collinette sulle guance, gli occhi e il naso.")
    les.draw("bodies", les.behind(les.shapes(a["body"], b["body"]), a["head"], b["head"], a["tail"], b["tail"])
             + les.lines(a["chest"], b["chest"], *a["legs"], *b["legs"], *a["paws"], *b["paws"]),
             "Under each head draw a round body with a U on the chest, two front legs and round paws.",
             "Sotto ogni testa disegna un corpo tondo con una U sul petto, due zampe davanti e le zampette tonde.")
    les.draw("tails", les.shapes(a["tail"], b["tail"]) + les.behind(les.lines(a["tip"], b["tip"])),
             "Draw a big fluffy tail on the outer side of each fox, and a line near the tip.",
             "Disegna una grande coda soffice sul lato esterno di ogni volpe, e una riga vicino alla punta.")
    les.draw("woods", les.behind(les.shapes(*stems), *caps) + les.shapes(*caps, *dots) + les.lines(*grass)
             + les.shapes(*leaves),
             "Between the foxes, draw two mushrooms with dots. Add grass and a few falling leaves.",
             "Tra le volpi disegna due funghi con i pallini. Aggiungi l'erba e qualche foglia che cade.")
    les.erase()
    les.white(*[pt for fx in (200, 440) for pt in ((fx, 226), (fx, 270))], (200 - 105, 282), (440 + 105, 282))
    les.color("foxes-orange", ORANGE, [(200, 150), (440, 150)], "Color the foxes orange. Leave white the cheeks, the chest and the tail tips!",
              "Colora le volpi di arancione. Lascia bianchi le guance, il petto e la punta della coda!",
              inside=[a["head"], b["head"], a["body"], b["body"], a["tail"], b["tail"]])
    les.color("mushrooms-red", RED, [(x, y - r * 0.5) for x, y, r in mush], "Color the mushroom caps red, but not the dots.",
              "Colora di rosso i cappelli dei funghi, ma non i pallini.")
    les.color("leaves-green", GREEN, [(320, 110), (345, 170), (105, 80), (535, 70)],
              "Color the falling leaves green.", "Colora di verde le foglie che cadono.")
    return les


LESSONS = [garden, horses, knitting, vulture, foxes]
