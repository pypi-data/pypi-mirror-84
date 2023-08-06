# 使用turtle模块画出星空
from random import randint,choice
from turtle import *
from time import sleep, perf_counter

__email__="3416445406@qq.com"
__author__="七分诚意 qq:3076711200 邮箱:%s"%__email__
__version__="1.0"

class Star(Turtle):
    def __init__(self):
        super().__init__()
        self.setundobuffer(None)
        self.setheading(randint(0,360))
        self.dt=randint(5,16)
        self.penup()
        self.shape("circle")
        self.shapesize(0.1)
        self.forward(self.dt*12)
        

        self._color=100
        self.color((self._color,)*3)
    def move(self):
        # 移动星星
        self.forward(self.dt)
        self.dt*=1.02
        # 使星的颜色变亮
        self._color=min(self._color+4,255)
        self.color((self._color,)*3)
        self.shapesize(self.shapesize()[0]*1.01)
def main():
    num=20 # 星星个数
    scr=Screen()
    colormode(255)
    bgcolor("black")
    tracer(False)
    stars=[]
    for i in range(num):
        stars.append(Star())

    while True:
        start=perf_counter()
        for star in stars:
            star.move()
            # 移除屏幕外的星
            if abs(star.xcor())>window_width()/2 \
               or abs(star.ycor())>window_height()/2:
                star.hideturtle()
                #turtles().remove(star)
                stars.remove(star)
        update()
        sleep(max(0.04-(perf_counter()-start),0))
        if len(stars)<num:
            for i in range(num-len(stars)):
                stars.append(Star())

if __name__=="__main__":main()
