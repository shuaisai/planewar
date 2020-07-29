import random
import pygame

# 屏幕大小的常量
SCREEN_RECT = pygame.Rect(0, 0, 480, 700)
# 刷新率常量
FRAME_PER_SEC = 60
# 创建敌机的定时器常量
CREATE_ENEMY_EVENT = pygame.USEREVENT
# 英雄发射子弹事件定时器常量
HERO_FIRE_EVENT = pygame.USEREVENT + 1

# 定义一个精灵类
class GameSprites(pygame.sprite.Sprite):
    """飞机大战游戏精灵类"""

    def __init__(self, image_name, speed=1):

        # 调用父类的初始化方法
        super().__init__()

        self.image = pygame.image.load(image_name)
        # get_rect() 会取到 <rect(0, 0, 480, 700)>
        self.rect = self.image.get_rect()
        self.speed = speed

    def update(self):

        self.rect.y += self.speed


class Background(GameSprites):
    """游戏背景精灵"""

    def __init__(self, is_alt=False):
        # 调用父类方法完成精灵的创建 (image/rect/speed)
        super().__init__("./images/background.png")
        # 判断是否是交替图像，如果是，需要设置初始位置
        if is_alt:
            self.rect.y = -self.rect.height

    def update(self):

        # 调用父类的垂直移动
        super().update()
        # 判断是否移出屏幕，如果移出，将图像设置到屏幕上方
        if self.rect.y >= SCREEN_RECT.height:
            self.rect.y = -self.rect.height


class Enemy(GameSprites):
    """敌机精灵类"""
    def __init__(self):
        # 调用父类方法，创建敌机精灵
        self.enemy_lsit = ["./images/enemy1.png", "./images/enemy2.png", "./images/enemy3_n1.png",
                           "./images/enemy3_n2.png"]
        super().__init__(random.choice(self.enemy_lsit))
        # 指定敌机随机速度
        self.speed = random.randint(1, 3)
        print(self.speed)
        # 指定敌机随机位置
        # self.rect.y = -self.rect.y
        self.rect.bottom = 0
        max_x = SCREEN_RECT.width - self.rect.width
        self.rect.x = random.randint(0, max_x)

    def update(self):
        # 调用父类方法，保持垂直飞行
        super().update()
        # 判断是否飞出屏幕， 飞出则删除
        if self.rect.y >= SCREEN_RECT.height:
        # kill方法可以将精灵从所有精灵组中移除，精灵会被自动销毁
            self.kill()

    def __del__(self):
        # print("enmey is dead %s" % self.rect)
        pass


class Hero(GameSprites):
    """英雄飞机精灵类"""
    def __init__(self):
        # 调用父类方法，创建英雄精灵，指定英雄飞机速度
        super().__init__("./images/me1.png", 0)
        # 指定英雄初始位置
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.bottom - 120
        # 创建子弹精灵组
        self.bullets = pygame.sprite.Group()
        # 创建得分
        self.score = 0

    def update(self):
        # 通过self.speed 判断是水平方向移动还是竖直方向移动
        if self.speed == 3:
            self.rect.y += self.speed - 1
        elif self.speed == -3:
            self.rect.y += self.speed + 1
        else:
            self.rect.x += self.speed

        # 边界判断
        if self.rect.x <= 0:
            self.rect.x = 0
        elif self.rect.right >= SCREEN_RECT.width:
            self.rect.right = SCREEN_RECT.width
        elif self.rect.y <= 0:
            self.rect.top = SCREEN_RECT.top
        elif self.rect.bottom >= SCREEN_RECT.bottom:
            self.rect.bottom = SCREEN_RECT.bottom

    def fire(self):
        for i in (0, 1, 2):
            # 创建子弹精灵
            bullet = Bullet()
            # 设置子弹位置
            bullet.rect.bottom = self.rect.y - i * 20
            bullet.rect.centerx = self.rect.centerx
            # 加入子弹精灵组
            self.bullets.add(bullet)

    def bomb(self):
            # 创建炸弹精灵
            bomb = Bomb()
            # 设置炸弹位置
            x_bomb = ['1', '-1']
            bomb.rect.bottom = self.rect.y
            bomb.rect.centerx = self.rect.centerx + int(random.choice(x_bomb)) * 60
            # 加入子弹精灵组
            self.bullets.add(bomb)



class Bullet(GameSprites):
    """子弹精灵类"""
    def __init__(self):
        # 调用父类方法，创建敌机精灵, 指定子弹速度
        super().__init__("./images/bullet1.png", -2)

    def update(self):
        # 调用父类方法，保持垂直飞行
        super().update()
        # 判断是否飞出屏幕， 飞出则删除
        if self.rect.bottom < 0:
            # kill方法可以将精灵从所有精灵组中移除，精灵会被自动销毁
            self.kill()


class Bomb(GameSprites):
    """子弹精灵类"""
    def __init__(self):
        # 调用父类方法，创建敌机精灵, 指定子弹速度
        super().__init__("./images/bomb.png", -1)

    def update(self):
        x_speed = ['1', '-1']
        self.rect.y += self.speed
        self.rect.x += int(random.choice(x_speed))

        if self.rect.bottom < 0:
            # kill方法可以将精灵从所有精灵组中移除，精灵会被自动销毁
            self.kill()










