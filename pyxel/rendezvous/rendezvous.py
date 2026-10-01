#
# 「つぶやきProcessing」の生き物シリーズ（仮称）
# 「逢瀬（rendezvous）」をPythonに移植
# cf. https://x.com/yuruyurau/status/2091203263811199186
#
# Sep 27, 2026 ver.1 converted to Pyxel/Python with Grok4
# Oct 01, 2026 ver.2 debug and refactor
#
# -*- coding: utf-8 -*-
import pyxel
import math

t = 0.0

def update():
    global t
    t += math.pi / 80

def draw():
    pyxel.cls(0)  # 黒背景
    for i in range(15000, 0, -1):  # 負荷に応じて調整してください
        y = i / 663.0
        k = (4 + math.cos(y)) * math.cos(i)
        e = y / 5 - 11
        d = math.sqrt(k * k + e * e) - 5
        c = d / 2.5 - t / 2 + (i % 2) * 8
        x = (79 + k * k) * math.cos(c) + 200
        ypos = (99 * math.sin(c / 3) + 200
                + d * d * math.sin(t * 2 - d)
                + 3 * math.sin(k * 2)
                + math.sin(y / 9 + 6) * k * (e + math.sin(e * 4 - d * 4)))
        
        sx = int(x)
        sy = int(ypos)
        if 0 <= sx < 400 and 0 <= sy < 400:
            pyxel.pset(sx, sy, 7)

pyxel.init(400, 400, title="rendezvous", fps=30)
pyxel.run(update, draw)

# End of rendezvous.py
