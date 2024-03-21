import pygame , sys , random
# tạo hàm cho game

def draw_floor():
    screen.blit(floor,(floor_x_pos,650))
    screen.blit(floor,(floor_x_pos+432,650))

        
def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (500 , random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midtop = (500 , random_pipe_pos - 650))

    return bottom_pipe , top_pipe

def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 600 :
            screen.blit(pipe_surface , pipe)
        else:
            # biến lật ngược ống lại 
            # False True ở đây là trục x y tọa độ
            # Muốn lật theo trục dọc thì Set f t 
            flip_pipe = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe , pipe)
# xử lý va chạm
# nếu va chạm ống với sàn với trên nóc thì trả về game_activite = False 
# còn không thì trả về True 
def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            return False
    if bird_rect.top <= -75 or bird_rect.bottom >= 650:
        return False
    return True
# hàm xoay chim 
def rotate_bird(bird1):
    # rotozoom() là phương thức của class pygame.transform
    # có ba thằng tham số trong phương thức này 
    # cái đầu tiên là thằng đối tượng
    # cái thứ hai là thằng chiều xoay biến này được tạo trong thăng if game_activite 
    # cái thứ ba là độ scale của hình ảnh con chim thì để là 1 thôi 
    new_bird = pygame.transform.rotozoom(bird1 , -bird_movement*3 , 1)
    return new_bird
# biến screen lưu màn hình
# tạo màn hình lưu chiều cao với chiều rộng

# hàm tạo hiệu hoạt cảnh cho cánh chim 
def bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_rect  = new_bird.get_rect(center = (100 , bird_rect.center))
    return new_bird , new_bird_rect
# hàm hiển thị điểm 
def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)) , True , (255, 255 ,255))
        score_rect = score_surface.get_rect(center = (214, 100))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}' , True , (255, 255 ,255))
        score_rect = score_surface.get_rect(center = (214, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High Score: {int(score)}', True , (255, 255 ,255))
        high_score_rect = high_score_surface.get_rect(center = (214, 610))
        screen.blit(high_score_surface, high_score_rect)     
def update_score(score , high_score):
    if score > high_score:
        high_score = score
    return high_score
pygame.mixer.pre_init(frequency= 44110 , size=-16, channels= 2, buffer= 512)
screen = pygame.display.set_mode((432, 760))
pygame.init()
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf' , 40)
# thiết lập trọng lực và chuyển động của chim
gravity = 0.25
bird_movement = 0       
game_activite = True
score = 0
high_score = 0
# background
bg = pygame.image.load('assets/background-night.png').convert()
bg = pygame.transform.scale2x(bg)
# floor 
floor = pygame.image.load('assets/floor.png').convert()
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0 
# bird 
# bird = pygame.image.load('assets/yellowbird-midflap.png').convert_alpha()        
# bird = pygame.transform.scale2x(bird)

bird_up = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-upflap.png')).convert_alpha()
bird_down = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-downflap.png')).convert_alpha()
bird_mid = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-midflap.png')).convert_alpha()
bird_list = [bird_down , bird_mid , bird_up]
bird_index = 2
bird = bird_list[bird_index]
bird_rect = bird.get_rect(center = (100, 384))         


# tạo timer cho bird 
bird_flap = pygame.USEREVENT + 1
pygame.time.set_timer(bird_flap, 200)   




# pipe 
pipe_surface = pygame.image.load('assets/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
# thiết lập timer 
sqawnpipe = pygame.USEREVENT
# thiết lập là sau 1,2 giây thì tạo ra ống mới
pygame.time.set_timer(sqawnpipe , 2000)

# thiết lập chiều cao cho ống
pipe_height = [200 , 300 , 400 ]



# tạo màn hình kết thúc khi chơi game
game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png')).convert_alpha()
game_over_rect = game_over_surface.get_rect(center=(216,384))

# chèn âm thanh 
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
hit_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_countdown = 100

# vòng lặp cho game    
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_activite:
                bird_movement = 0
                bird_movement = -11
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_activite == False:
                game_activite = True
                pipe_list.clear()
                bird_rect.center = (100 , 384)
                bird_movement = 0      
                score = 0 
        if event.type == sqawnpipe:
            pipe_list.extend(create_pipe())
        if event.type == bird_flap:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0 
                # bird , bird_rect = bird_animation()

        
    # chèn background8
    screen.blit(bg,(0,0))
    if game_activite:
    # chim 
        bird_movement += gravity
        rotated_bird = rotate_bird(bird)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird,bird_rect)
        # set game_activite bằng cái hàm check va chạm này
        game_activite = check_collision(pipe_list) 
        # ống 
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)
        score += 0.01
        score_display('main_game')   
        score_sound_countdown = -1
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = 100       
    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score , high_score)
        score_display('game_over')
    
    # chèn sàn
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -432:
        floor_x_pos = 0
    pygame.display.update()
    clock.tick(120) 