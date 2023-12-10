import pygame
import random
import time

t0 = time.time()
width = 800 
height = 600 
doguinho_walk = [] 
doguinho_anim_frame = 1
doguinho_pos_x = 100
doguinho_pos_y = 400
doguinho_anim_time = 0 # variavel para controle do tempo da animação
invert = True
mapa =[]
tile_quads =[]
BLACK = [0,0,0]
ranking = []
presente_misterioso_anim_time = 0
presente_misterioso_anim_frame = 0

bomba_anim_time = 0
bomba_anim_frame = 0
bomba = []

doguinho_pulando = []

presente_misterioso = []

doguinho_idle = []
altura_pulo = 20
velocidade_pulo = altura_pulo

dificuldade = 0.2

vidas = 20
lista_tempo = []

gravidade = 1

pulando = False
walk = False
up = False
down = False

placar_atual = 0

recorde = 0

def load_mapa(filename): #Lê o conteúdo do arquivo para a matriz
    global mapa
    file = open(filename,"r")
    i = 0 
    for line in file.readlines():
        
        mapa.append([])
        for j in line.strip():
            mapa[i].append(j)
        i = i + 1

    
    file.close()

def load_ranking():
    try:
        with open("ranking.txt", "r") as file:
            ranking_data = file.readlines()
            ranking = [float(time.strip()) for time in ranking_data]
            return ranking
    except FileNotFoundError:
        return []

def save_ranking(ranking):
    with open("ranking", "w") as file:
        for time in ranking:
            file.write(f"{time:.2f}\n")

def update_ranking(placar_atual, ranking):
    ranking.append(placar_atual)
    ranking.sort()
    save_ranking(ranking_list)


def game_over_screen(screen, placar_atual, ranking_list):
    global clock

    font = pygame.font.Font(pygame.font.get_default_font(), 50)
    update_ranking(placar_atual,ranking_list)
    running = True
    while running:
        screen.fill((190, 200, 220))

        t1 = font.render("FALECEU", False, BLACK)
        t2 = font.render(f"Seu tempo: {placar_atual:.2f}", False, BLACK)
        t3 = font.render("FAÇA MELHOR na proxima", False, BLACK)
        t4 = font.render("É facin :)", False, BLACK)
        t5 = font.render("Pressione enter para recomeçar", False, BLACK)

        screen.blit(t1, (300, 90))
        screen.blit(t2, (200, 170))
        screen.blit(t3, (100, 240))
        screen.blit(t4, (300, 330))
        screen.blit(t5, (10, 440))


        pygame.display.update()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    return True
                elif e.key == pygame.K_ESCAPE:
                    running = False

        clock.tick(5)  

    return False

def load_tiles():
    global  tile_quads
    cenario = pygame.image.load('cenario_1.png')
    cenario=pygame.transform.scale(cenario, (cenario.get_width()-200,cenario.get_height()-160))
    tile_quads.append((cenario))    
    for i in range(2,4):
        cenario = pygame.image.load('cenario_'+ str(i)+'.png')
        cenario=pygame.transform.scale(cenario, (cenario.get_width()-80,cenario.get_height()-80))
        tile_quads.append((cenario))  



def load():
    global clock,som, doguinho_walk, doguinho_idle, doguinho_pulando, presente_misterioso, presente_misterioso_x, presente_misterioso_y, sys_font, bomba, bomba_x, bomba_y, recorde, arq, arq_saida
    clock = pygame.time.Clock() 
    musica = pygame.mixer.music.load('music_bg.mp3')
    som = pygame.mixer.Sound('dano.mp3')
    presente_misterioso_anim_frame = 0
    bomba_anim_frame = 0
    load_mapa("mapa.txt")
    load_tiles()
    for i in range(6):
        doguinho_walk.append(pygame.image.load("gato_" + str(i) + ".png"))

    doguinho_idle.append(pygame.image.load("gato_2.png"))

    bomba = [pygame.image.load("bomba_" + str(i) + ".png") for i in range(2)]
    bomba[0] = pygame.transform.scale(bomba[0], (bomba[0].get_width() // 4, bomba[0].get_height() // 4))
    bomba[1] = pygame.transform.scale(bomba[1], (bomba[1].get_width() // 4, bomba[1].get_height() // 4))

    presente_misterioso = [pygame.image.load("presente_misterioso_" + str(i) + ".png") for i in range(2)]
    presente_misterioso[0] = pygame.transform.scale(presente_misterioso[0], (presente_misterioso[0].get_width() // 5, presente_misterioso[0].get_height() // 5))
    presente_misterioso[1] = pygame.transform.scale(presente_misterioso[1], (presente_misterioso[1].get_width() // 5, presente_misterioso[1].get_height() // 5))
    
    doguinho_pulando.append(pygame.image.load("gato_0.png"))



    presente_misterioso_x = random.randint(0, width - presente_misterioso[presente_misterioso_anim_frame].get_width())
    presente_misterioso_y = -presente_misterioso[presente_misterioso_anim_frame].get_height()


    sys_font = pygame.font.Font(pygame.font.get_default_font(), 35)


    arq = open("ranking", 'r') 
    for linha in arq : 
        linha = linha.strip()
        if float(linha) > recorde :
            recorde = float(linha)
    
    arq.close()    

    

    bomba_x = random.randint(0, width - bomba[bomba_anim_frame].get_width())
    bomba_y = -bomba[bomba_anim_frame].get_height()
    
def mouse_click_down(px_mouse, py_mouse, mouse_buttons):
    if mouse_buttons[0]: # left
        if px_mouse>=35 and px_mouse<=85 and py_mouse>=80 and py_mouse<=130:
            pygame.mixer.music.play()
        if px_mouse>=100 and px_mouse<=150 and py_mouse>=80 and py_mouse<=130:
            pygame.mixer.music.pause()
        
            
def update(dt):
    global doguinho_walk,contador_placar, doguinho_anim_frame, doguinho_pos_x, doguinho_anim_time, invert, doguinho_pos_y, walk, up, down, pulando, velocidade_pulo, altura_pulo, gravidade_velocide, presente_misterioso_y, presente_misterioso_x, presente_misterioso_anim_frame, presente_misterioso_anim_time, dificuldade, lista_tempo, bomba, bomba_x, bomba_y, bomba_anim_frame, bomba_anim_time, vidas, t1, t0, tempo_passado

    keys = pygame.key.get_pressed()

    t1 = time.time()

    tempo_passado = t1 - t0

    contador_int = pygame.time.get_ticks()//1000
    
   
        
    if contador_int not in lista_tempo :
        lista_tempo.append(contador_int)
    
   


    bomba_y += dificuldade * dt
    presente_misterioso_y += dificuldade * dt

    if (
        doguinho_pos_x < bomba_x + bomba[bomba_anim_frame].get_width()
        and doguinho_pos_x + doguinho_walk[doguinho_anim_frame].get_width() > bomba_x
        and doguinho_pos_y < bomba_y + bomba[bomba_anim_frame].get_height()
        and doguinho_pos_y + doguinho_walk[doguinho_anim_frame].get_height() > bomba_y
    ):
        som.play()
        vidas -= 1
        bomba_y = -bomba[bomba_anim_frame].get_height()
        bomba_x = random.randint(0, width - bomba[bomba_anim_frame].get_width())

    if (
        doguinho_pos_x < presente_misterioso_x + presente_misterioso[presente_misterioso_anim_frame].get_width()
        and doguinho_pos_x + doguinho_walk[doguinho_anim_frame].get_width() > presente_misterioso_x
        and doguinho_pos_y < presente_misterioso_y + presente_misterioso[presente_misterioso_anim_frame].get_height()
        and doguinho_pos_y + doguinho_walk[doguinho_anim_frame].get_height() > presente_misterioso_y
    ):
        som.play()
        vidas -= 2
        presente_misterioso_y = -presente_misterioso[presente_misterioso_anim_frame].get_height()
        presente_misterioso_x = random.randint(0, width - presente_misterioso[presente_misterioso_anim_frame].get_width())
    
    
    if presente_misterioso_y > height:
        presente_misterioso_y = -presente_misterioso[presente_misterioso_anim_frame].get_height()
        presente_misterioso_x = random.randint(0, width - presente_misterioso[presente_misterioso_anim_frame].get_width())

    presente_misterioso_anim_time = presente_misterioso_anim_time + dt #incrementa o tempo usando dt
    if presente_misterioso_anim_time > 100: #quando acumular mais de 100 ms
            presente_misterioso_anim_frame = presente_misterioso_anim_frame + 1 # avança para proximo frame
            if presente_misterioso_anim_frame > 1: # loop da animação
                presente_misterioso_anim_frame = 0
            presente_misterioso_anim_time = 0 #reinicializa a contagem do tempo

    if bomba_y > height:
        bomba_y = -bomba[bomba_anim_frame].get_height()
        bomba_x = random.randint(0, width - bomba[bomba_anim_frame].get_width())

    bomba_anim_time = bomba_anim_time + dt #incrementa o tempo usando dt
    if bomba_anim_time > 100: #quando acumular mais de 100 ms
            bomba_anim_frame = bomba_anim_frame + 1 # avança para proximo frame
            if bomba_anim_frame > 1: # loop da animação
                bomba_anim_frame = 0
            bomba_anim_time = 0 #reinicializa a contagem do tempo

    if keys[pygame.K_RIGHT]:
        invert = True
        up = False
        down = False
        walk = True
        doguinho_pos_x = doguinho_pos_x + (0.4 * dt) 
        doguinho_anim_time = doguinho_anim_time + dt #incrementa o tempo usando dt
        if doguinho_anim_time > 100: #quando acumular mais de 100 ms
            doguinho_anim_frame = doguinho_anim_frame + 1 # avança para proximo frame
            if doguinho_anim_frame > 3: # loop da animação
                doguinho_anim_frame = 0
            doguinho_anim_time = 0 #reinicializa a contagem do tempo

    if keys[pygame.K_LEFT]:
        invert = False
        up = False
        down = False
        walk = True
        doguinho_pos_x = doguinho_pos_x - (0.4 * dt) 
        doguinho_anim_time = doguinho_anim_time + dt #incrementa o tempo usando dt
        if doguinho_anim_time > 100: #quando acumular mais de 100 ms
            doguinho_anim_frame = doguinho_anim_frame + 1 # avança para proximo frame
            if doguinho_anim_frame > 3: # loop da animação
                doguinho_anim_frame = 0
            doguinho_anim_time = 0 #reinicializa a contagem do tempo


            
    if keys[pygame.K_UP]:
        pulando = True
    

    if pulando :
        doguinho_pos_y -= velocidade_pulo
        velocidade_pulo -= gravidade

        if velocidade_pulo < -altura_pulo :
            pulando = False
            velocidade_pulo = altura_pulo

    elif not keys[pygame.K_UP] and not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT] :
        walk = False

    if lista_tempo[-1] % 4 == 0:
        dificuldade += 0.001    

    t = sys_font.render(f"Tempo: {tempo_passado:.2f}", False, BLACK)
    screen.blit(t, (33,34))

    
    

def draw_screen(screen):
    screen.fill((190,200,220))
    global tile_quads,placar_atual, presente_misterioso_anim_frame, presente_misterioso, vidas, presente_misterioso_x, presente_misterioso_anim_time, presente_misterioso_anim_frame_time, presente_misterioso, contador, bomba_anim_frame_time, bomba, bomba_anim_frame, bomba_x, bomba_y, ranking, tempo_passado, recorde
    pygame.draw.rect(screen, (240, 240, 240), (35, 80, 50, 50),0,2)
    pygame.draw.polygon(screen,(0, 0, 0), [(45, 85), (45, 125), (75, 105)],3)
    pygame.draw.rect(screen, (0, 0, 0), (35, 80, 50, 50),2,4)
    pygame.draw.rect(screen, (240, 240, 240), (100, 80, 50, 50),0,2)
    pygame.draw.rect(screen, (0, 0, 0), (100, 80, 50, 50),2,4)
    pygame.draw.rect(screen, (0, 0, 0), (110, 85, 10, 40),2,3)
    pygame.draw.rect(screen, (0, 0, 0), (130, 85, 10, 40),2,3)
    
    
        
    for i in range(8): #Percorre a matriz e desenha quadrados coloridos 
        for j in range(17):
            
            if mapa[i][j] == "T":
                screen.blit(tile_quads[0], ((j * 50), (i * 32)))
            elif mapa[i][j] == "V": 
                pygame.draw.rect(screen, (140,169,70), (j*80,i*76, 100, 100))
            elif mapa[i][j] == "G": 
                screen.blit(tile_quads[2], ((j * 110), (i * 83)))
    #desenha o personagem usando o indice da animação
    if invert and walk:
        imagem_invertida =  pygame.transform.flip(doguinho_walk[doguinho_anim_frame], True, False)
        screen.blit(imagem_invertida, (doguinho_pos_x, doguinho_pos_y))

    elif invert and pulando :
        imagem_invertida =  pygame.transform.flip(doguinho_pulando[0], True, False)
        screen.blit(imagem_invertida, (doguinho_pos_x, doguinho_pos_y))
    elif pulando :
        screen.blit(doguinho_pulando[0], (doguinho_pos_x, doguinho_pos_y))

        
    elif walk :
        screen.blit(doguinho_walk[doguinho_anim_frame], (doguinho_pos_x, doguinho_pos_y))
    
    elif invert and not walk : 
        imagem_invertida =  pygame.transform.flip(doguinho_idle[0], True, False)
        screen.blit(imagem_invertida, (doguinho_pos_x, doguinho_pos_y))
    elif not walk :
        screen.blit(doguinho_idle[0], (doguinho_pos_x, doguinho_pos_y))
    
    screen.blit(presente_misterioso[presente_misterioso_anim_frame], (presente_misterioso_x ,presente_misterioso_y))
    screen.blit(bomba[bomba_anim_frame], (bomba_x ,bomba_y))

    
    
    
    t = sys_font.render(f"Vidas: {vidas}", False, BLACK)
    screen.blit(t, (620,34))

    
    t = sys_font.render(f"Maior Recorde: {recorde}", False, BLACK)
    screen.blit(t, (20,150))


def main_loop(screen, ranking_list):  
    global clock, vidas, parado, tempo_passado, t0, dificuldade,arq
    running = True
    while running and vidas > 0:
        for e in pygame.event.get(): 
            if e.type == pygame.QUIT:
                running = False
                break
            elif e.type == pygame.MOUSEBUTTONDOWN: #detecta o inicio do clique do mouse
                mouse_buttons = pygame.mouse.get_pressed()
                px_mouse, py_mouse = pygame.mouse.get_pos()
                mouse_click_down(px_mouse, py_mouse, mouse_buttons)

            

        
            
        # Define FPS máximo
        clock.tick(60)        
        # Calcula tempo transcorrido desde a última atualização 
        dt = clock.get_time()
        # Desenha objetos na tela 
        draw_screen(screen)
        # Atualiza posição dos objetos da tela
        update(dt)
        # Pygame atualiza o seu estado
        pygame.display.update()
        

    restart = game_over_screen(screen, tempo_passado, ranking_list)

    if restart:
        load()

        vidas = 20
        tempo_passado = 0
        t0 = time.time()
        dificuldade = 0.2
        contador_int = 0
        presente_misterioso_anim_frame = 1
        presente_misterioso_anim_time = 0
        bomba_anim_frame = 1
        bomba_anim_time = 0

        main_loop(screen,ranking_list)

ranking_list = load_ranking()

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ta chovendo doguinho")
load()
main_loop(screen,ranking_list)
pygame.quit()

