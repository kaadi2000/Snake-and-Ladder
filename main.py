import numpy
import random
import threading

level_list_snakes={'easy': 5, 'medium': 6, 'hard':7}
level_list_ladder={'easy': 7, 'medium': 6, 'hard':5}

def check_tail_foot(y_axis):
    return (9-y_axis)*10

class score:
    def __init__(self):
        self.score = 0

    @property
    def check_score(self):
        return self.score

    def change_score(self,value):
        self.score=value


def create_snake(level):
    global snakes_mouth, snakes_tail
    snakes_mouth = []
    snakes_tail = []
    for i in range(0,level_list_snakes[level]):
        y_axis=random.randint(0,7)
        x_axis=random.randint(0,9)
        snakes_mouth.append((y_axis,x_axis))
        temp = random.randint(1,check_tail_foot(y_axis))
        board[y_axis][x_axis] += 0.01*((i+1)*10)
        indexes=numpy.where(board_original == temp)
        snakes_tail.append((indexes[0][0],indexes[1][0]))
        board[indexes[0][0]][indexes[1][0]] += 0.01*((i+1)*10+1)

def create_ladder(level):
    global ladder_top, ladder_foot
    ladder_top = []
    ladder_foot = []
    n=0
    while(n<level_list_ladder[level]):
        y_axis=random.randint(0,7)
        x_axis=random.randint(0,9)
        if (y_axis,x_axis) in snakes_mouth:
            n -= 1
        else:
            ladder_top.append((y_axis,x_axis))
            board[y_axis][x_axis] += 0.001*((n+1)*10)
            temp = random.randint(1,check_tail_foot(y_axis))
            indexes=numpy.where(board_original == temp)
            if ((indexes[0][0],indexes[1][0]) in snakes_mouth) or((indexes[0][0],indexes[1][0]) in snakes_tail):
                del ladder_top[-1]
                n -= 1
            else:
                ladder_foot.append((indexes[0][0],indexes[1][0]))
                board[indexes[0][0]][indexes[1][0]] += 0.001*((n+1)*10+1)
        n=n+1


def new_game(level):
    global board_original
    global board
    board = numpy.zeros((10,10))
    for i in range(0,10):
        for j in range(0,10):
            if i % 2 == 0:
                board[i][j]=(10-i)*10+(10-j)-10
            else:
                board[i][j]=(9-i)*10 + j + 1
    board_original = board
    board_original = board_original.astype('int32')
    x=threading.Thread(target = create_snake, args = (level,))
    x.start()
    y=threading.Thread(target = create_ladder, args = (level,))
    y.start()

def game_prerequisite():
    global player_list,object_list
    player_list=[]
    try:
        n=int(input("\nEnter Number of players:"))
    except ValueError:
        print("Please enter an integer Value!!")
        game_prerequisite()
    else:
        if n<2:
            print("Atleast 2 players required!!")
            play()
        else:
            level=input("\nEnter Level\nEasy,Medium,Hard\nEnter your response:").lower()
            if level not in level_list_snakes:
                print("Invalid level selection!!")
                game_prerequisite()
            else:
                new_game(level)
                for i in range(1,n+1):
                    print("Enter player",i,"name:", end =""),
                    name=str(input()).upper()
                    player_list.append(name)
                object_list=[score() for i in player_list]
                play(n)

def check(i):
    indexes=numpy.where(board_original == object_list[i].check_score)
    if (indexes[0][0],indexes[1][0]) in snakes_mouth:
        location = snakes_mouth.index((indexes[0][0],indexes[1][0]))
        temp=snakes_tail[location]
        object_list[i].change_score(board_original[temp[0]][temp[1]])
        print("\nSnake Bites !!")
        input("\nPress Enter to continue:")
    if (indexes[0][0],indexes[1][0]) in ladder_foot:
        location = ladder_foot.index((indexes[0][0],indexes[1][0]))
        temp=ladder_top[location]
        object_list[i].change_score(board_original[temp[0]][temp[1]])
        print("\nLadder Climbed !!")
        input("\nPress Enter to contunue:")


def update(dice,i):
    while True:
        if object_list[i].check_score == 0:
            if dice == 6:
                object_list[i].change_score(1)
        elif object_list[i].check_score == 100:
            break
        else:
            score=object_list[i].check_score + dice
            if score <= 100:
                object_list[i].change_score(score)
                check(i)
        if(dice == 6):
            input("\nPress enter to roll dice:")
            dice = random.randint(1,6)
            print("Dice:",dice,"\n")
        else:
            break

def end_game():
    print("\n1.Play Again\n2.Exit\n\nEnter Your Response:",end="")
    try:
        choice = int(input())
    except:
        print("Invalid Choice!!")
        end_game()
    else:
        if choice == 1:
            game_prerequisite()
        elif choice == 2:
            exit()
        else:
            print("\nInvalid Choice!!\n")
            end_game()

def play(n):
    while(1):
        for i in range(0,n):
            print("\nPlayer",i+1,":",player_list[i])
            input("\nPress enter to roll dice:")
            dice = random.randint(1,6)
            print("Dice:",dice,"\n")
            update(dice,i)
        for i in range(0,n):
            print(player_list[i],":",object_list[i].check_score)
        print("\n\n",board,"\n\n")
        input("\nPress enter to roll dice:")
        if all(object_list[i].check_score == 100 for i in range(0,n)):
            print("\nGame Over!!")
            end_game()

game_prerequisite()
