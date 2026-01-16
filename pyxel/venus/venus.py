# 画像は以下より引用
# Radar Observations of Venus
# https://science.nasa.gov/image-detail/amf-ed32cd82-638b-4693-867b-d0574d769e54/

import pyxel

class App:
    def __init__(self):
        pyxel.init(256,256,title="venus")
        pyxel.load("venus.pyxres") # 画像の読み込み
        pyxel.run(self.update, self.draw)

    def update(self):
        pass

    def draw(self):
        pyxel.cls(0)
        # 画像を描画する
        pyxel.blt(0, 0, 0, 0, 0, 256, 256)

App()

# End of venus.py
