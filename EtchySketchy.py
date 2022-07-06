"""Simple drawing program, sort of like an Etch a Sketch."""

import shutil
import sys

#Constants for drawing lines
UP_DOWN         = chr(9474)  # 9474 is |
LEFT_RIGHT      = chr(9472)  # 9472 is ─
DOWN_RIGHT      = chr(9484)  # 9484 is ┌
DOWN_LEFT       = chr(9488)  # 9488 is ┐
UP_RIGHT        = chr(9492)  # 9492 is └
UP_LEFT         = chr(9496)  # 9496 is ┘
UP_DOWN_RIGHT   = chr(9500)  # 9500 is ├
UP_DOWN_LEFT    = chr(9508)  # 9508 is ┤
DOWN_LEFT_RIGHT = chr(9516)  # 9516 is ┬
UP_LEFT_RIGHT  = chr(9524)   # 9524 is ┴
CROSS         = chr(9532)    # 9532 is ┼

CANVAS_WIDTH, CANVAS_HEIGHT = shutil.get_terminal_size()
CANVAS_HEIGHT -= 5 #Margins so we can see
CANVAS_WIDTH -= 2

#The keys for the canvas dictionary will be integer tuples for the coordinates. The values will be WASD (for line type)

canvas = {}
cursorX = 0
cursorY = 0

def getCanvasString(canvasData,cx,cy):
    # Get a multiline string of the line already drawn
    canvasStr = ''

    for rowNum in range(CANVAS_HEIGHT):
        for columnNum in range (CANVAS_WIDTH):
            if columnNum == cx and rowNum == cy:
                canvasStr += '#'
                continue

            # Add the line character for the current coordinate
            cell = canvasData.get((columnNum,rowNum))
            if cell in (set(['W', 'S']), set(['W']), set(['S'])):
                canvasStr += UP_DOWN
            elif cell in (set(['A', 'D']), set(['A']), set(['D'])):
                canvasStr += LEFT_RIGHT
            elif cell == set(['S', 'D']):
                canvasStr += DOWN_RIGHT
            elif cell == set(['S', 'A']):
                canvasStr += DOWN_LEFT
            elif cell == set(['W', 'D']):
                canvasStr += UP_RIGHT
            elif cell == set(['W', 'A']):
                canvasStr += UP_LEFT
            elif cell == set(['W', 'S', 'D']):
                canvasStr += UP_DOWN_RIGHT
            elif cell == set(['W', 'S', 'A']):
                canvasStr += UP_DOWN_LEFT
            elif cell == set(['A', 'S', 'D']):
                canvasStr += DOWN_LEFT_RIGHT
            elif cell == set(['A', 'W', 'D']):
                canvasStr += UP_LEFT_RIGHT
            elif cell == set(['W', 'A', 'S', 'D']):
                canvasStr += CROSS
            elif cell == None:
                canvasStr += ' '
        canvasStr += '\n' # New line after the row
    return canvasStr

moves = []
while True: #Program loop
    #Draw the lines based on canvas
    print(getCanvasString(canvas,cursorX, cursorY))
    print('Use "WASD" to move, "C" to clear the screen, or "H" for help! ' 
    + 'F to save, or QUIT!')
    response = input ('> ').upper()

    if response == 'QUIT':
        print('Thanks for sketchin!')
        sys.exit()
    elif response == 'H':
        print('Use W,A,S,D to move the cursor to draw a line! \n')
        print('You can save your drawing to a text file by entering F')
        input('Press enter to return to the program')
        continue
    elif response == 'C':
        canvas = {} #Clear canvas
        moves.append('C') # Record clear in moves
    elif response == 'F':
        # Save the canvas
        try:
            print('Please enter the filename to save to')
            filename = input('> ')
            if not filename.endswith('.txt'):
                filename+= '.txt'
            with open (filename,'w', encoding='utf-8') as file:
                file.write(''.join(moves) + '\n')
                file.write(getCanvasString(canvas, None, None))
        except:
                print("ERROR - could not save file!")

    for command in response:
        if command not in ('W','A','S','D'):
            continue #Ignore random inputs
        moves.append(command)

        if canvas == {}:
            if command in ('W','S'):
                # Make the first line a horizontal one
                canvas[(cursorX,cursorY)] = set (['W', 'S'])

            elif command in ('A', 'D'):
                # First line vertical
                canvas[(cursorX,cursorY)] = set(['A', 'D'])
        
        #Update x & y

        if command == 'W' and cursorY > 0:
            canvas[(cursorX, cursorY)].add(command)
            cursorY = cursorY - 1
        elif command == 'S' and cursorY < CANVAS_HEIGHT - 1:
            canvas[(cursorX, cursorY)].add(command)
            cursorY = cursorY + 1
        elif command == 'A' and cursorX > 0:
            canvas[(cursorX, cursorY)].add(command)
            cursorX = cursorX - 1
        elif command == 'D' and cursorX < CANVAS_WIDTH - 1:
            canvas[(cursorX, cursorY)].add(command)
            cursorX = cursorX + 1
        else:
            continue #Cursor won't move if it's off edge of canvas

        #Add empty set, if there's no set for cursorX, cursorY
        if (cursorX, cursorY) not in canvas:
            canvas[(cursorX, cursorY)] = set()
        
        #Add direction string to the XY set
        if command == 'W':
            canvas[(cursorX, cursorY)].add('S')
        elif command =='S':
            canvas[(cursorX, cursorY)].add('W')
        elif command == 'A':
            canvas[(cursorX, cursorY)].add('D')
        elif command == 'D':
            canvas[(cursorX, cursorY)].add('A')

        

