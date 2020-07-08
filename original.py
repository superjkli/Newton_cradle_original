from vpython import *
running = True
g = 9.8
size = 0.05
n = 5#擺錘數量(一至五顆)
L = [0.5] * n          #擺線長度
theta = 45 * pi / 180
k = 5000#彈力常數
damp = 200
ball = []
string = []
b = 0
bind = None
#before = None
t = 0
dt = 0.0001
#side = None
pulling = False
#direction = vec(0,0,0)
def run(b):
    global running
    running = not running
    if running: b.text = "Pause"
    else: b.text = "Run"

def down():
    global bind
    global before
    global pulling
    pulling = True
    for i in range(0,n,1):
        if scene.mouse.pos.x <= ball[i].pos.x + size and scene.mouse.pos.x >= ball[i].pos.x - size and scene.mouse.pos.y <= ball[i].pos.y + size and scene.mouse.pos.y >= ball[i].pos.y - size :
            bind = ball[i]
#            before = ball[i]
    if bind == ball[1] or bind == ball[-2]:
        before = bind
def move():
    global bind
#    global before
#    global direction
    global pulling
    global ball
    if bind is not None:
        if bind == ball[0] or bind == ball[-1]:
            bind.pos = vec(scene.mouse.pos.x,scene.mouse.pos.y,0)
#            direction = norm(before.pos - bind.pos)
        elif bind == ball[1] or bind == ball[-2]:
            bind.pos = vec(scene.mouse.pos.x,scene.mouse.pos.y,0)
            
    else:
        pulling = False

    
def up():
    global bind
    global before
#    global direction
    global side
    global pulling
    global ball
    if bind == ball[1] or bind == ball[-2]:
        direction = norm(bind.pos - before.pos)
        amount = mag(bind.pos - before.pos)
    pulling = False
    bind = None
    before = None
#    if side == None:
#        if direction.x < 0:
#            side = "left"
#        elif direction.x > 0:
#            side = "right"
#        else:
#            side = None


def reset():
    delete()
    init()

def kChange(s):
    k = s.value

def dampChange(s):
    damp = s.value

def SpringForce(r,L):
    return -k * (mag(r) - L) * r / mag(r)

def SpringDamp(v, r):  #避震器
    cos_theta = dot(v,r)/(mag(v)*mag(r))                    #用向量內積找v和r夾角的餘弦函數
    r_unit_vector = norm(r)                                 #沿彈簧軸方向的單位向量
    projection_vector = mag(v) * cos_theta * r_unit_vector  #計算v在r方向的分量
    spring_damp = - damp * projection_vector                #沿彈簧軸方向的阻力
    return spring_damp

def collision(v1, v2, r1, r2, m1, m2):
    v1_col = v1 - (2 * m2 /(m1 + m2))*dot((v1 - v2), (r1 - r2)) * (r1 - r2) / mag2(r1 - r2) 
    v2_col = v2 - (2 * m1 /(m1 + m2))*dot((v2 - v1), (r2 - r1)) * (r2 - r1) / mag2(r2 - r1)
    return (v1_col, v2_col)

m = [1] * n                  #擺錘重量

def delete():
    global scene
    global p_button
    global r_button
    global k_slider
    global damp_slider
#    global side
    scene.title = None
    scene.caption = None
    global k_wt
    global damp_wt
    p_button.visible = False
    r_button.visible = False
    
    del p_button
    del r_button
    k_slider.delete()
    damp_slider.delete()
    k_wt.delete()
    damp_wt.delete()
    canvas.delete(scene)
#    side = None

def init():
    global scene
    global p_button
    global r_button
    global k_slider
    global damp_slider
    global k_wt
    global damp_wt
    scene = canvas(width = 1000, height = 500, center = vector(size * n - size, -L[1] / 2, 0), background = vector(0,0,0), range = 1, title = "Newton's cradle simulation")  
    ceiling = box(pos = vector(size * n - size, 0, 0), length = size * 2 * (n + 1), height = 0.001, width = 0.5, color = color.yellow)
    p_button = button(text="Pause", pos=scene.title_anchor, bind=run)
    r_button = button(text="reset", pos=scene.title_anchor, bind=reset)
    scene.caption = "Change the value of the elastic force: \n"
    k_slider = slider(bind=kChange, min=100, max=100000,step = 100, length = 1000)
    k_wt = wtext(text='{:d}'.format(k))
    scene.append_to_caption("\nChange the value of the damp:\n")
    damp_slider = slider(bind = dampChange, min = 100, max = 20000, step = 100, length = 1000)
    damp_wt = wtext(text = '{:d}'.format(damp))
    global ball
    global string
    ball = []
    string = []
    for i in range(0, n, 1):
        ball.append(sphere(pos = vector(i * 2 * size, -L[i], 0), v = vector(0, 0, 0), radius = size, color = color.yellow))
        string.append(cylinder(pos = vector(i * size * 2, 0, 0), length = L[i], radius = 0.003))
    scene.bind("mousedown", down)
    scene.bind("mousemove", move)
    scene.bind("mouseup", up)
    k_slider.value = k
    damp_slider.value = damp
    #ball[0].pos = vector(-L[0] * sin(theta), -L[0] * cos(theta),0)                          
    #ball[1].pos=vector(size*2-L[1]*sin(theta),-L[1]*cos(theta),0)
    #ball[2].pos=vector(size*2*2-L[2]*sin(theta),-L[2]*cos(theta),0)
    #ball[3].pos=vector(size*2*3-L[3]*sin(theta),-L[3]*cos(theta),0)
    #ball[4].pos=vector(size*2*4+L[4]*sin(theta),-L[4]*cos(theta),0)

init()
while True:
    rate(1/dt)

    v = []
    a = []
    if running and not pulling:
        k = k_slider.value
        k_wt.text = '{:d}'.format(k)
        damp = damp_slider.value
        damp_wt.text = '{:d}'.format(damp)
        for i in range(1, n, 1):
            if mag(ball[i].pos - ball[i-1].pos) < 2 * size:
                ball[i-1].v, ball[i].v = collision(ball[i-1].v, ball[i].v, ball[i-1].pos, ball[i].pos, m[i-1], m[i])
        for i in range(0,n,1):
            string[i].axis = ball[i].pos - string[i].pos
            if ball[i].v != vec(0, 0, 0): 
                a.append(vector(0, -g, 0) + SpringForce(string[i].axis, L[i]) + SpringDamp(ball[i].v, string[i].axis)- b * ball[i].v)
            else:
                a.append(vector(0, -g, 0) + SpringForce(string[i].axis, L[i]) - b * ball[i].v)
            ball[i].v += a[i] * dt
            ball[i].pos += ball[i].v * dt

    t=t+dt  
