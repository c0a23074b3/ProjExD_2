import os
import sys
import time
import random
import pygame as pg


WIDTH, HEIGHT = 1600, 900
DELTA = {
    pg.K_UP: (0,-5),
    pg.K_DOWN: (0,+5),
    pg.K_LEFT: (-5,0),
    pg.K_RIGHT: (+5,0)
}  # 練習問題１ 移動量辞書、押下キーに対応
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRectかばくだんRect
    戻り値：タプル（横方向判定結果、縦方向判定結果）
    画面内ならtrue,画面外ならfalse
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate

def kk_dict():
    roto_face = {

    }  # rotozoomしたSurfaceを値とした辞書を作成
    kk_img = pg.image.load("")


#  課題２　時間とともに爆弾が拡大、加速
def big_fast():
    accs = [a for a in range(1, 11)]
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.drawcircle(bb_img, (255,0,0),(10*r, 10*r), 10*r)


#  課題３　ゲームオーバー画面
def game_over(screen: pg.display) -> None:
    """
    引数：displayのみ
    戻り値：なし
    """
    img = pg.Surface((1600, 900))
    fonto = pg.font.Font(None, 80)
    go_img = img.get_rect()  # gameoverの黒画面の四角形を生成する
    go_img.center = 0, 0
    kk_sad_img = pg.image.load("fig/8.png")  # 泣いているこうかとんの画像を挿入
    kk_sad_img = pg.transform.rotozoom(kk_sad_img, 0, 3)
    txt = fonto.render("Game Over", True, (255, 255, 255))  # gameoverの文字を入力
    img.set_alpha(150)
    screen.blit(img, go_img.center)
    screen.blit(kk_sad_img, [400, 450])
    screen.blit(kk_sad_img, [1200,450])
    screen.blit(txt, [650, 450])
    pg.display.update()



def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    # ここからこうかとんの設定
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    # ここから爆弾の設定 
    bm_img = pg.Surface((20,20))
    bm_img.set_colorkey((0,0,0))
    pg.draw.circle(bm_img, (255,0,0), (10,10), 10)
    bm_rct = bm_img.get_rect()
    bm_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx, vy = +5, +5  # 横方向速度、縦方向速度

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bm_rct):  # こうかとんが爆弾とぶつかったら
            print("gameover")
            game_over(screen)
            time.sleep(5)
            return
        screen.blit(bg_img, [0, 0]) 

        # こうかとんと移動の表示
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, v in DELTA.items():  # 練習１
            if key_lst[k]:  # 押されたキーがTrueなら
                sum_mv[0] += v[0]
                sum_mv[1] += v[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        # 爆弾移動と表示
        bm_rct.move_ip(vx, vy)
        screen.blit(bm_img, bm_rct)
        yoko, tate = check_bound(bm_rct)
        if not yoko:  # 横方向にはみ出たら
            vx *= -1
        if not tate:  # 縦方向にはみ出たら
            vy *= -1
    
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
