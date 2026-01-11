# 画像は以下より引用
# Mercury: A complete guide to the closest planet to the sun
# https://www.space.com/36-mercury-the-suns-closest-planetary-neighbor.html

import pyxel

class App:
    def __init__(self):
        pyxel.init(256,256,title="mercury")
        pyxel.load("mercury.pyxres") # 画像の読み込み
        pyxel.run(self.update, self.draw)

    def update(self):
        pass

    def draw(self):
        pyxel.cls(0)
        # 画像を描画する
        pyxel.blt(0, 0, 0, 0, 0, 256, 256)

App()

# End of mercury.py
