#
# 「つぶやきProcessing」の生き物シリーズ（仮称）
# 「クラゲ（jellyfish）」をPythonに移植
# cf. https://x.com/yuruyurau/status/2093710258120331463
#
# Sep 21, 2026 ver.1 converted to Pyxel/Python with Grok4
# Sep 22, 2026 ver.2 debug and refactor
#
# -*- coding: utf-8 -*-
import math
import pyxel

t = 0.0

def update():
    global t
    t += math.pi / 80

def draw():
    pyxel.cls(0)  # ほぼ黒背景
    for i in range(10000, 0, -1):
        y = i / 99.0
        k = (8 + math.sin(i / 19 + t)) * math.cos(i / 49)
        e = y / 8 - 12
        d = (k * k + e * e) / 79 + 1

        x = (k / d * 4
             - e * math.sin(k)
             + k / (d * d) * (12 + d * 6 * math.sin(
                 d * d - t + math.cos(t / 3) + 0.3 * math.sin(e)))
             + 200)

        yy = 12 * math.sin(d * 2.6 - t) + d * 66 + 40

        # 400→400にスケール
        sx = x 
        sy = yy 

        if 0 <= sx < 400 and 0 <= sy < 400:
            pyxel.pset(int(sx), int(sy), 7)  # 明るい色

pyxel.init(400, 400, title="jellyfish", fps=30)
pyxel.run(update, draw)

# End of jellyfish.py
