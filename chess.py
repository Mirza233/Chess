import pygame,math


board = pygame.image.load("chessboard.png")
initial = {(0,0):"bR",(1,0):"bKn",(2,0):"bB",(3,0):"bQ",(4,0):"bK",(5,0):"bB",(6,0):"bKn",
           (7,0):"bR",(0,7):"wR",(1,7):"wKn",(2,7):"wB",(3,7):"wQ",(4,7):"wK",(5,7):"wB",(6,7):"wKn",(7,7):"wR"
        }
white = ["wR","wKn","wB","wK","wQ","wp"]
black = ["bR","bKn","bB","bK","bQ","bp"]
count = 0
for i in range(8):
    initial[(i,1)] = "bp"
    initial[(i,6)] = "wp"
current = initial.copy()

def showBoard(w,surface):
    global board
    board = pygame.transform.scale(board,(w//4,w//4))
    x,y = 0,0
    for i in range(4):
        for j in range(4):
            surface.blit(board,(x,y))
            x+=w//4
        x = 0
        y+=w//4

def piece(figura):
    pawnW = pygame.image.load("pawnW.png")
    pawnB = pygame.image.load("pawnB2.png")
    rookW = pygame.image.load("rookW.png")
    rookB = pygame.image.load("rookB2.png")
    knightW = pygame.image.load("knightW.png")
    knightB = pygame.image.load("knightB2.png")
    bishopW = pygame.image.load("bishopW.png")
    bishopB = pygame.image.load("bishopB2.png")
    kingW = pygame.image.load("kingW.png")
    kingB = pygame.image.load("kingB2.png")
    queenW = pygame.image.load("queenW.png")
    queenB = pygame.image.load("queenB2.png")

    d = {"bR":rookB,"bKn":knightB,"bB":bishopB,"bQ":queenB,"bK":kingB,"bp":pawnB,"wR":rookW,"wKn":knightW,"wB":bishopW,"wQ":queenW,"wK":kingW,"wp":pawnW}
    return d[figura]


def move(w,win):
    showBoard(w,win)
    showPieces(w,win)
    pygame.display.update()
    global current,count
    a = True
    while a:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                x,y = event.pos[0],event.pos[1]
                x1,y1 = 8*x//w,8*y//w
                if (x1,y1) not in current:
                    return move(w,win)
                showLegal(x1,y1,w,win)
                while a:
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONUP:
                            x,y = event.pos[0],event.pos[1]
                            x2,y2 = 8*x//w,8*y//w
                            a = False
                            
    #print(current)
    if (x1,y1) == (x2,y2) or (x1,y1) not in current:
        return move(w,win)
    elif is_legal(x1,y1,x2,y2):
        if (x2,y2) in current :
            del current[x2,y2]
        current[x2,y2] = current[x1,y1]
        del current[x1,y1]
        count+=1
    else:
        move(w,win)
        
def showLegal(x1,y1,w,win):
    for i in range(8):
        for j in range(8):
            if is_legal(x1,y1,i,j) or (i,j)==(x1,y1):
                s = pygame.Surface((w//8,w//8))
                s.set_alpha(80)
                s.fill((250,50,0))
                win.blit(s,(i*w//8,j*w//8))                
    pygame.display.update()
        
def showPieces(w,win):
    for x in range(8):
        for y in range(8):
            if (x,y) in current:
                win.blit(piece(current[(x,y)]),(x*w/8+w/50,y*w/8+w/50))


def is_legal(x1,y1,x2,y2):
    global count
    if (count%2 == 0 and current[(x1,y1)] in black) or (count%2 == 1 and current[(x1,y1)] in white):
        return False
    if (x2,y2) in current:
        if color(current[x1,y1])==color(current[x2,y2]):
            return False
    d={"bR":Rlegal(x1,y1,x2,y2),"wR":Rlegal(x1,y1,x2,y2),"wKn":Knlegal(x1,y1,x2,y2),"bKn":Knlegal(x1,y1,x2,y2),"wp":plegal(x1,y1,x2,y2),"bp":plegal(x1,y1,x2,y2),"bB":Blegal(x1,y1,x2,y2),"wB":Blegal(x1,y1,x2,y2)
       ,"wQ":Qlegal(x1,y1,x2,y2),"bQ":Qlegal(x1,y1,x2,y2),"wK":Klegal(x1,y1,x2,y2),"bK":Klegal(x1,y1,x2,y2)}
    return d[current[x1,y1]]
    

def color(piece):
    if piece in white:
        return "W"
    elif piece in black:
        return "B"
    else:
        return None

def Rlegal(x1,y1,x2,y2):
    between = True

    for i in range(min(x1,x2),max(x2,x1)):
        if (i,y1) in current:
            if i!=x1 and i!=x2:
                between = False
    for i in range(min(y1,y2),max(y2,y1)):
        if (x1,i) in current:
            if i!= y1 and i!=y2:
                between = False
    return (x1-x2 == 0 or y1-y2 == 0) and between

def Klegal(x1,y1,x2,y2):
    return abs(x1-x2)<=1 and abs(y1-y2)<=1

def Blegal(x1,y1,x2,y2):
    between = True
    x,y = x1,y1
    while x!=x2 and y!=y2:
        if (x,y) in current:
            if x != x1:
                between = False
        x,y = x+(x2-x1)/abs(x1-x2), y+(y2-y1)/abs(y1-y2)
    return abs(x2-x1)== abs(y2-y1) and between

def Knlegal(x1,y1,x2,y2):
    x,y = abs(x1-x2),abs(y1-y2)
    return x+y == 3 and x!=0 and y!=0

def Qlegal(x1,y1,x2,y2):
    return Blegal(x1,y1,x2,y2) or Rlegal(x1,y1,x2,y2)

def plegal(x1,y1,x2,y2):
    if x1 == x2 and (((x2,y2) in current) or (abs(y1-y2)==2 and (x2,(y1+y2)//2) in current)):
        return False
    a = True
    if x1!=x2:
        a = False
    if abs(x1-x2)==1 and abs(y1-y2) == 1 and (x2,y2) in current:
        a = True
    if current[(x1,y1)] in white: 
        if y1-y2>1 or y2>y1:
            a = False
        if abs(y1-y2) == 2 and y1 == 6 and x1==x2:
            a = True
    else:
        if y2-y1>1 or y1>y2:
            a = False
        if abs(y1-y2) == 2 and y1 == 1 and x1 == x2:
            a = True
    return a


def main():
    w = 600 
    win = pygame.display.set_mode((w,w))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                 pygame.quit()
        showBoard(w,win)
        showPieces(w,win)
        pygame.display.update()
        move(w,win)
        pygame.display.update()

main()
