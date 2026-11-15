import pyxel
from pyxel.cube import Camera, Mat4, Node, Shading, Vec3

# --- 設定 ---
SCREEN_W = 240
SCREEN_H = 180
PLAYER_SPEED = 2.0
BULLET_SPEED = 4.0
ENEMY_SPEED = 1.2
SPAWN_INTERVAL = 40  # フレーム


class Bullet(Node):
    def __init__(self, pos):
        super().__init__()
        self.transform = Mat4.from_translation(pos)
        self.life = 90  # 寿命

    def on_update(self):
        # 前方向（-Z）に進む
        self.transform = self.transform.translate(Vec3(0, 0, -BULLET_SPEED))
        self.life -= 1
        if self.life <= 0:
            self.destroy()

    def on_draw(self):
#        self.sphere(Mat4.IDENTITY, 3, 11)  # 小さな球
#        self.sphere(Vec3.ZERO, 3, 11)  # 小さな球
        # 縦長のレーザーっぽく
        self.box(Mat4.IDENTITY, Vec3(2, 2, 8), 10)

class Enemy(Node):
    def __init__(self, x):
        super().__init__()
        self.transform = Mat4.from_translation(Vec3(x, 0, -180))
        self.hp = 1
        # 少し回転させてバリエーションを出す
        self.rot = pyxel.rndi(0, 360)

    def on_update(self):
        self.transform = self.transform.translate(Vec3(0, 0, ENEMY_SPEED))
        self.rot += 2  # ゆっくり回転
        if self.transform.pos.z > 40:
            self.destroy()

    def on_draw(self):
        # 回転を加える
        rot_mat = Mat4.from_euler(Vec3(0, self.rot, 0))

        # 本体（ひし形っぽい感じ）
        self.box(rot_mat * Mat4.from_translation(Vec3(0, 0, 0)), Vec3(14, 4, 14), 8)

        # 中央のコア
        self.box(rot_mat * Mat4.from_translation(Vec3(0, 2, 0)), Vec3(6, 4, 6), 10)

        # 4方向の突起
        self.box(rot_mat * Mat4.from_translation(Vec3(0, 0, -9)), Vec3(4, 3, 6), 2)
        self.box(rot_mat * Mat4.from_translation(Vec3(0, 0, 9)), Vec3(4, 3, 6), 2)
        self.box(rot_mat * Mat4.from_translation(Vec3(-9, 0, 0)), Vec3(6, 3, 4), 2)
        self.box(rot_mat * Mat4.from_translation(Vec3(9, 0, 0)), Vec3(6, 3, 4), 2)
        


class Player(Node):
    def __init__(self):
        super().__init__()
        self.transform = Mat4.from_translation(Vec3(0, 0, 20))
        self.cooldown = 0

    def on_update(self):
        # 左右移動
        dx = 0
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A):
            dx -= PLAYER_SPEED
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D):
            dx += PLAYER_SPEED

        pos = self.transform.pos
        new_x = max(-60, min(60, pos.x + dx))
        self.transform = Mat4.from_translation(Vec3(new_x, 0, 20))

        # 弾発射
        if self.cooldown > 0:
            self.cooldown -= 1
        if (pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_Z)) and self.cooldown <= 0:
            bullet = Bullet(self.transform.pos + Vec3(0, 0, -10))
            self.parent.add_child(bullet)
            self.cooldown = 8
            pyxel.play(0, 0)

    def on_draw(self):
        # 本体（細長い胴体）
        self.box(Mat4.from_translation(Vec3(0, 0, 0)), Vec3(6, 4, 22), 12)

        # 機首（尖った感じ）
        self.box(Mat4.from_translation(Vec3(0, 0, -13)), Vec3(4, 3, 6), 7)

        # 主翼
        self.box(Mat4.from_translation(Vec3(0, 0, 2)), Vec3(28, 1.5, 8), 5)

        # 翼端の少し厚み
        self.box(Mat4.from_translation(Vec3(-12, 0, 2)), Vec3(4, 2, 6), 6)
        self.box(Mat4.from_translation(Vec3(12, 0, 2)), Vec3(4, 2, 6), 6)

        # 垂直尾翼
        self.box(Mat4.from_translation(Vec3(0, 5, 8)), Vec3(1.5, 8, 6), 12)

        # コックピット風
        self.box(Mat4.from_translation(Vec3(0, 2.5, -4)), Vec3(4, 2, 6), 1)
        

class Scene(Node):
    def __init__(self):
        super().__init__()
        self.shading = Shading(pyxel.colors)
        self.shading.direction = Vec3(-0.4, -1.0, -0.6)

        self.camera = Camera()
        self.camera.clear_color = 1
        self.camera.near = 5
        self.camera.far = 300
        self.camera.transform = Mat4.look_at(Vec3(0, 50, 80), Vec3(0, 0, -20))

        self.player = Player()
        self.add_child(self.player)

        self.score = 0
        self.spawn_timer = 0
        self.game_over = False

        # スクロール用
        self.scroll_speed = 1.8          # 地面の流れる速さ
        self.line_spacing = 20           # 横線の間隔

    def on_update(self):
        if self.game_over:
            if pyxel.btnp(pyxel.KEY_R):
                self.reset()
            return

        # 敵出現
        self.spawn_timer -= 1
        if self.spawn_timer <= 0:
            x = pyxel.rndi(-50, 50)
            self.add_child(Enemy(x))
            self.spawn_timer = SPAWN_INTERVAL

        # 簡易当たり判定（弾 vs 敵）
        bullets = [n for n in self.children if isinstance(n, Bullet)]
        enemies = [n for n in self.children if isinstance(n, Enemy)]

        for bullet in bullets:
            bpos = bullet.transform.pos
            for enemy in enemies:
                epos = enemy.transform.pos
                if (bpos - epos).length() < 12:
                    bullet.destroy()
                    enemy.destroy()
                    self.score += 100
                    pyxel.play(1, 1)
                    break

        # プレイヤー vs 敵
        ppos = self.player.transform.pos
        for enemy in enemies:
            if (ppos - enemy.transform.pos).length() < 16:
                self.game_over = True
                pyxel.play(2, 2)
                break

    def reset(self):
        for child in list(self.children):
            if isinstance(child, (Bullet, Enemy)):
                child.destroy()
        self.player.transform = Mat4.from_translation(Vec3(0, 0, 20))
        self.score = 0
        self.spawn_timer = 0
        self.game_over = False

    def on_draw(self):
        # ===== スクロールする地面 =====
        # 横線を手前に流す
        offset = (pyxel.frame_count * self.scroll_speed) % self.line_spacing

        for i in range(-12, 6):  # 十分な本数を描画
            z = i * self.line_spacing + offset
            # 少し奥の方は暗く、手前は明るくすると遠近感が出る
            color = 5 if z < -40 else 6
            self.line(Vec3(-75, -8, z), Vec3(75, -8, z), color)

        # 両サイドの縦線（固定）
        self.line(Vec3(-75, -8, -220), Vec3(-75, -8, 50), 5)
        self.line(Vec3(75, -8, -220), Vec3(75, -8, 50), 5)

        # 中央の補助線（ゼビウスっぽく少し目立たせる）
        self.line(Vec3(0, -8, -220), Vec3(0, -8, 50), 1)
        


class App:
    def __init__(self):
        pyxel.init(SCREEN_W, SCREEN_H, title="Pyxel Cube Shooter", fps=60)

        # 簡易SE
        pyxel.sounds[0].set("c3", "p", "7", "n", 5)   # 発射
        pyxel.sounds[1].set("e3g3c4", "n", "7654", "f", 8)  # ヒット
        pyxel.sounds[2].set("a2f2d2", "t", "765", "s", 15)  # ゲームオーバー

        self.scene = Scene()
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        self.scene.update()

    def draw(self):
        self.scene.draw(0, 0, pyxel.width, pyxel.height)

        # UI
        pyxel.text(6, 6, f"SCORE {self.scene.score}", 7)
        if self.scene.game_over:
            pyxel.text(SCREEN_W // 2 - 28, SCREEN_H // 2 - 8, "GAME OVER", 8)
            pyxel.text(SCREEN_W // 2 - 40, SCREEN_H // 2 + 4, "PRESS R TO RETRY", 7)
        else:
            pyxel.text(6, SCREEN_H - 12, "←→/AD: Move  SPACE/Z: Shoot  Q: Quit", 13)


App()
