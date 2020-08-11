# must open file through Anaconda Navigator

# %%
# determine state of the board
# state 1 means turn 1 - all cells unknown, 
# state 2 means enough information to reveal one or more cells
# state 3 means there are cells to be flagged
# state 4 means means there are known cells
# state 5 means not enough information to place a flag - must guess
# state 6 means board is complete
# state 7 means you lose
# state 0 means does not meet above criteria (shouldn't happen once code is complete)

def det_state(board):
    state = 0

#   removed since state 1 = state 5   
#     if board.sum() == 0:
#         state = 1   
#         cell = [-1,-1]
        
    if 10 in board:
        state = 7
        cell = [-1,-1]
    
    if 0 not in board:
        state = 6
        cell = [-1,-1]
        
    if state == 0:
        flag_list = det_flag_certain(board)   
        if len(flag_list) > 0:
            state = 3
            cell = flag_list[0]

    if state == 0:
        determined_cells_list = find_determined_cells(board)
        if len(determined_cells_list) > 0:
            state = 2
            cell = determined_cells_list[0]
        
    if state == 0:
        flag_list = det_flag_certain_two(board)
        if len(flag_list) > 0:
            state = 3
            cell = flag_list[0]
        
    if state == 0:
        known_cells_list = det_known_cells(board)
        if len(known_cells_list) > 0:
            state = 4
            cell = known_cells_list[0]
        
    if state == 0:   
        unknown_cells_list = guess_unknown_cell(board)
        state = 5
        cell = unknown_cells_list[0]
        
    action = [state,cell]
    
    return action


# %%
def det_flag_certain(board):
    dim_x = board.shape[0]
    dim_y = board.shape[1]
    flag_list = []
    for i in range(dim_x):
        for j in range(dim_y):
            if 1 <= board[i,j] <= 8:
                unknown_neighbours_list = find_unknown_neighbours(board, i, j)
                flag_neighbours_list = find_flag_neighbours(board, i, j)
                if len(unknown_neighbours_list) == board[i,j] - len(flag_neighbours_list):
                    flag_list.extend(unknown_neighbours_list)
                    
    if len(flag_list) == 0:
        return flag_list
    else:
        flag_certain_list = np.ndarray.tolist(np.unique(flag_list, axis = 0))
        flag_certain_list = [i for i in flag_certain_list if i not in flag_neighbours_list] 
        return flag_certain_list


# %%
def find_neighbours(board, i, j):
    dim_x = board.shape[0]
    dim_y = board.shape[1]
    
    neighbours_list_all = [
        [i-1, j-1],
        [i-1, j],
        [i-1, j+1],
        [i, j-1],
        [i, j+1],
        [i+1, j-1],
        [i+1, j],
        [i+1, j+1]
    ]
    
    neighbours_list = []
    
    for n in range(len(neighbours_list_all)):
        if neighbours_list_all[n][0] >= 0 and neighbours_list_all[n][1] >= 0 and neighbours_list_all[n][0] < dim_x and neighbours_list_all[n][1] < dim_y:
            neighbours_list.append(neighbours_list_all[n])
            
    return neighbours_list


# %%
def find_unknown_neighbours(board, i, j):
    neighbours_list = find_neighbours(board, i, j)
    unknown_neighbours_list = []
    for n in range(len(neighbours_list)):
        if board[neighbours_list[n][0], neighbours_list[n][1]] == 0:
            unknown_neighbours_list.append(neighbours_list[n])
    
    return unknown_neighbours_list


# %%
def find_flag_neighbours(board, i, j):
    neighbours_list = find_neighbours(board, i, j)
    flag_neighbours_list = []
    for n in range(len(neighbours_list)):
        if board[neighbours_list[n][0], neighbours_list[n][1]] == 9:
            flag_neighbours_list.append(neighbours_list[n])
    
    return flag_neighbours_list


# %%
def find_known_neighbours(board, i, j):
    neighbours_list = find_neighbours(board, i, j)
    known_neighbours_list = []
    for n in range(len(neighbours_list)):
        if 1 <= board[neighbours_list[n][0], neighbours_list[n][1]] <= 8:
            known_neighbours_list.append(neighbours_list[n])
    
    return known_neighbours_list


# %%
# determined cells are cells whose flag number is satisfied
# source of improvement:
# if all unknown neighbours of determined cell is also included in unknown neighbours
# of other determined cell delete the first one
def find_determined_cells(board):
    dim_x = board.shape[0]
    dim_y = board.shape[1]
    determined_cells = []
    for i in range(dim_x):
        for j in range(dim_y):
            if 1 <= board[i,j] <= 8:
                unknown_neighbours = find_unknown_neighbours(board, i, j)
                flag_neighbours = find_flag_neighbours(board, i, j)
                if board[i,j] == len(flag_neighbours) and len(unknown_neighbours) > 0:
                    determined_cells.append([i,j])

    return determined_cells


# %%
# code for any variation of [1 2] pattern (4 possible directions)
# place flag 'above' 3rd tile provided there are numbers or white cells 'underneath' the pattern
# make sure all determined cells are expanded before this function is run
def det_flag_certain_two(board):
    dim_x = board.shape[0]
    dim_y = board.shape[1]
    flag_list = []
    for i in range(dim_x):
        for j in range(dim_y):
                # for [1 2] horizontal pattern
                if j < dim_y - 2 and board[i,j] - len(find_flag_neighbours(board,i,j)) == 1 and board[i,j+1] - len(find_flag_neighbours(board,i,j+1)) == 2 and 1 <= board[i,j+2] <= 8:
                    # for flagging above
                    if i == dim_x - 1:
                        if board[i-1,j+2] == 0:
                            flag_list.append([i-1,j+2])
                    elif i != 0:
                        if board[i-1,j+2] == 0 and board[i+1,j+2] != 0:
                            flag_list.append([i-1,j+2])
                    # for flagging below
                    if i == 0:
                        if board[i+1,j+2] == 0:
                            flag_list.append([i+1,j+2])
                    elif i != dim_x - 1:
                        if board[i+1,j+2] == 0 and board[i-1,j+2] != 0:
                            flag_list.append([i+1,j+2])
                # for [2 1] horizontal pattern
                if j < dim_y - 2 and board[i,j+2] - len(find_flag_neighbours(board,i,j+2)) == 1 and board[i,j+1] - len(find_flag_neighbours(board,i,j+1)) == 2 and 1 <= board[i,j] <= 8:
                    # for flagging above
                    if i == dim_x - 1:
                        if board[i-1,j] == 0:
                            flag_list.append([i-1,j])
                    elif i != 0:
                        if board[i-1,j] == 0 and board[i+1,j] != 0:
                            flag_list.append([i-1,j])
                    # for flagging below
                    if i == 0:
                        if board[i+1,j] == 0:
                            flag_list.append([i+1,j])
                    elif i != dim_x - 1:
                        if board[i+1,j] == 0 and board[i-1,j] != 0:
                            flag_list.append([i+1,j])
                # for [1 2] vertical pattern
                if i < dim_x - 2 and board[i,j] - len(find_flag_neighbours(board,i,j)) == 1 and board[i+1,j] - len(find_flag_neighbours(board,i+1,j)) == 2 and 1 <= board[i+2,j] <= 8:   
                    # for flagging to the left
                    if j == dim_y - 1:
                        if board[i+2,j-1] == 0:
                            flag_list.append([i+2,j-1])
                    elif j != 0:
                        if board[i+2,j-1] == 0 and board[i+2,j+1] != 0:
                            flag_list.append([i+2,j-1])
                    # for flagging to the right
                    if j == 0:
                        if board[i+2,j+1] == 0:
                            flag_list.append([i+2,j+1])
                    elif j != dim_y - 1:
                        if board[i+2,j+1] == 0 and board[i+2,j-1] != 0:
                            flag_list.append([i+2,j+1])
                # for [2 1] vertical pattern
                if i < dim_x - 2 and board[i+2,j] - len(find_flag_neighbours(board,i+2,j)) == 1 and board[i+1,j] - len(find_flag_neighbours(board,i+1,j)) == 2 and 1 <= board[i,j] <= 8:   
                    # for flagging to the left
                    if j == dim_y - 1:
                        if board[i,j-1] == 0:
                            flag_list.append([i,j-1])
                    elif j != 0:
                        if board[i,j-1] == 0 and board[i,j+1] != 0:
                            flag_list.append([i,j-1])
                    # for flagging to the right
                    if j == 0:
                        if board[i,j+1] == 0:
                            flag_list.append([i,j+1])
                    elif j != dim_y - 1:
                        if board[i,j+1] == 0 and board[i,j-1] != 0:
                            flag_list.append([i,j+1])
                               
    if len(flag_list) == 0:
        return flag_list
    else:
        return np.ndarray.tolist(np.unique(flag_list, axis = 0))


# %%
# code for any variation of the [1 1] pattern
# known cells are cells which cannot contain a mine
def det_known_cells(board):
    dim_x = board.shape[0]
    dim_y = board.shape[1]
    known_cells_list = []
    for i in range(dim_x):
        for j in range(dim_y):
            # for uncovered cell on right side
            if j < dim_y - 2 and board[i,j] - len(find_flag_neighbours(board,i,j)) == 1 and board[i,j+1] - len(find_flag_neighbours(board,i,j+1)) == 1 and board[i,j+2] != 0:        
                # for cell above
                if i != 0 and (board[i-1,j] + board[i-1,j+1] + board[i-1,j+2]) == 0:
                    if i == dim_x - 1:
                        if j == 0:
                            known_cells_list.append([i-1,j+2])
                        elif 0 not in {board[i,j-1],board[i-1,j-1]}:
                            known_cells_list.append([i-1,j+2])
                    else:
                        if j == 0 and 0 not in {board[i+1,j],board[i+1,j+1],board[i+1,j+2]}:
                            known_cells_list.append([i-1,j+2])
                        elif 0 not in {board[i-1,j-1],board[i,j-1],board[i+1,j-1],board[i+1,j],board[i+1,j+1],board[i+1,j+2]}:
                            known_cells_list.append([i-1,j+2])
                # for cell below
                if i != dim_x - 1 and (board[i+1,j] + board[i+1,j+1] + board[i+1,j+2]) == 0:
                    if i == 0:
                        if j == 0:
                            known_cells_list.append([i+1,j+2])
                        elif 0 not in {board[i,j-1],board[i+1,j-1]}:
                            known_cells_list.append([i+1,j+2])
                    else:
                        if j == 0 and 0 not in {board[i-1,j],board[i-1,j+1],board[i-1,j+2]}:
                            known_cells_list.append([i+1,j+2])
                        elif 0 not in {board[i+1,j-1],board[i,j-1],board[i-1,j-1],board[i-1,j],board[i-1,j+1],board[i-1,j+2]}:
                            known_cells_list.append([i+1,j+2])
            # for uncovered cell on left side
            if j > 1 and board[i,j] - len(find_flag_neighbours(board,i,j)) == 1 and board[i,j-1] - len(find_flag_neighbours(board,i,j-1)) == 1 and board[i,j-2] != 0:                 
                # for cell above
                if i != 0 and (board[i-1,j-2] + board[i-1,j-1] + board[i-1,j]) == 0:
                    if i == dim_x - 1:
                        if j == dim_y - 1:
                            known_cells_list.append([i-1,j-2])
                        elif 0 not in {board[i-1,j+1],board[i,j+1]}:
                            known_cells_list.append([i-1,j-2])
                    else:
                        if j == dim_y - 1 and 0 not in {board[i+1,j-2],board[i+1,j-1],board[i+1,j]}:
                            known_cells_list.append([i-1,j-2])
                        elif 0 not in {board[i+1,j-2],board[i+1,j-1],board[i+1,j],board[i+1,j+1],board[i,j+1],board[i-1,j+1]}:
                            known_cells_list.append([i-1,j-2])   
                # for cell below
                if i != dim_x - 1 and (board[i+1,j-2] + board[i+1,j-1] + board[i+1,j]) == 0:
                    if i == 0:
                        if j == dim_y - 1:
                            known_cells_list.append([i+1,j-2])
                        elif 0 not in {board[i,j+1],board[i+1,j+1]}:
                            known_cells_list.append([i+1,j-2])
                    else:
                        if j == dim_y - 1 and 0 not in {board[i-1,j-2],board[i-1,j-1],board[i-1,j]}:
                            known_cells_list.append([i+1,j-2])
                        elif 0 not in {board[i-1,j-2],board[i-1,j-1],board[i-1,j],board[i-1,j+1],board[i,j+1],board[i+1,j+1]}:
                            known_cells_list.append([i+1,j-2])
            # for uncovered cell above
            if i > 1 and board[i,j] - len(find_flag_neighbours(board,i,j)) == 1 and board[i-1,j] - len(find_flag_neighbours(board,i-1,j)) == 1 and board[i-2,j] != 0:                 
                # for cell on right side
                if j != dim_y - 1 and (board[i-2,j+1] + board[i-1,j+1] + board[i,j+1]) == 0:
                    if i == dim_x - 1:
                        if j == 0:
                            known_cells_list.append([i-2,j+1])
                        elif 0 not in {board[i-2,j-1],board[i-1,j-1],board[i,j-1]}:
                            known_cells_list.append([i-2,j+1])
                    else:
                        if j == 0 and 0 not in {board[i+1,j],board[i+1,j+1]}:
                            known_cells_list.append([i-2,j+1])
                        elif 0 not in {board[i-2,j-1],board[i-1,j-1],board[i,j-1],board[i+1,j-1],board[i+1,j],board[i+1,j+1]}:
                            known_cells_list.append([i-2,j+1])
                # for cell on left side
                if j != 0 and (board[i-2,j-1] + board[i-1,j-1] + board[i,j-1]) == 0:
                    if i == dim_x - 1:
                        if j == dim_y - 1:
                            known_cells_list.append([i-2,j-1])
                        elif 0 not in {board[i-2,j+1],board[i-1,j+1],board[i,j+1]}:
                            known_cells_list.append([i-2,j-1])
                    else:
                        if j == dim_y - 1 and 0 not in {board[i+1,j-1],board[i+1,j]}:
                            known_cells_list.append([i-2,j-1])
                        elif 0 not in {board[i+1,j-1],board[i+1,j],board[i+1,j+1],board[i,j+1],board[i-1,j+1],board[i-2,j+1]}:
                            known_cells_list.append([i-2,j-1])
            # for uncovered cell below
            if i < dim_x - 2 and board[i,j] - len(find_flag_neighbours(board,i,j)) == 1 and board[i+1,j] - len(find_flag_neighbours(board,i+1,j)) == 1 and board[i+2,j] != 0:                 
                # for cell on right side   
                if j != dim_y - 1 and (board[i,j+1] + board[i+1,j+1] + board[i+2,j+1]) == 0:
                    if i == 0:
                        if j == 0:
                            known_cells_list.append([i+2,j+1])
                        elif 0 not in {board[i,j-1],board[i+1,j-1],board[i+2,j-1]}:
                            known_cells_list.append([i+2,j+1])
                    else:
                        if j == 0 and 0 not in {board[i-1,j],board[i-1,j+1]}:
                            known_cells_list.append([i+2,j+1])
                        elif 0 not in {board[i+2,j-1],board[i+1,j-1],board[i,j-1],board[i-1,j-1],board[i-1,j],board[i-1,j+1]}:
                            known_cells_list.append([i+2,j+1])
                # for cell on left side
                if j != 0 and (board[i,j-1] + board[i+1,j-1] + board[i+2,j-1]) == 0:
                    if i == 0:
                        if j == dim_y - 1:
                            known_cells_list.append([i+2,j-1])
                        elif 0 not in {board[i,j+1],board[i+1,j+1],board[i+2,j+1]}:
                            known_cells_list.append([i+2,j-1])
                    else:
                        if j == dim_y - 1 and 0 not in {board[i-1,j-1],board[i-1,j]}:
                            known_cells_list.append([i+2,j-1])
                        elif 0 not in {board[i-1,j-1],board[i-1,j],board[i-1,j+1],board[i,j+1],board[i+1,j+1],board[i+2,j+1]}:
                            known_cells_list.append([i+2,j-1])
                            
    if len(known_cells_list) == 0:
        return known_cells_list
    else:
        return np.ndarray.tolist(np.unique(known_cells_list, axis = 0))


# %%
def find_known_cell_two(board):
    dim_x = board.shape[0]
    dim_y = board.shape[1]
    known_cells_list = []
    for i in range(dim_x):
        for j in range(dim_y):
            if 1 <= board[i,j] <= 8:
                unknown_neighbours_list = find_unknown_neighbours(board, i, j)
                for n in range(len(unknown_neighbours_list)):
                    # need to find the co-ordinate that appears in every known_neighbours_list for each unknown cell
                    # (excluding the first cell) - known_neighbours_list.remove([i,j])
                    known_neighbours_list[n] = find_known_neighbours(unknown_neighbours_list[n])

            
            
#     algorithm 1:
#     find unknown neighbours of first cell
#     if those unknown neighbours are all also neighbours of another cell whose value = value of first cell then 
#     all neighbours of the second cell excluding the intersecting cells cannot be mines
    
#     algorithm 2:
#     find unknown neighbours of first cell
#     if the number of non intersecting cells (number of neighbouring cells of second cell - intersecting cells) 
#             = value of second cell - value of first cell then flag all non intersecting cells


# %%
def guess_unknown_cell(board):
    dim_x = board.shape[0]
    dim_y = board.shape[1]
    unknown_cells_list = []
    for i in range(dim_x):
        for j in range(dim_y):
            if 1 <= board[i,j] <= 8:
                unknown_neighbours = find_unknown_neighbours(board, i, j)
                unknown_cells_list.extend(unknown_neighbours)
                
    if len(unknown_cells_list) == 0:
        for i in range(dim_x):
            for j in range(dim_y):
                if board[i,j] == 0:
                    unknown_cells_list.append([i,j])
                    
    if len(unknown_cells_list) > 0:
        return np.ndarray.tolist(np.unique(unknown_cells_list, axis = 0))
    else:
        return unknown_cells_list
    


# %%
import numpy as np
from selenium import webdriver 
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
import time 
import datetime

# 'beginner', 'intermediate' or 'expert'
input_difficulty = input('please enter the difficulty: ')
automatic_reset = input('automatically reset if program loses? please enter True or False: ')
if automatic_reset == 'True':
    automatic_reset = True
else:
    automatic_reset = False 
print('difficulty: ' + input_difficulty)

# path changes depending on device
browser = webdriver.Chrome(executable_path = 'C:/Projects/Minesweeper/chromedriver')
browser.get('http://www.freeminesweeper.org/minecore.html') 

# switch to new window
new_window = browser.window_handles[0]
browser.switch_to.window(new_window)

if input_difficulty == 'intermediate':
    action = webdriver.common.action_chains.ActionChains(browser)
    element = browser.find_element_by_name("cellIm0_0")
    action.move_to_element_with_offset(element, 0, -65)
    action.click()
    action.perform()
    difficulty_choice = browser.find_element_by_xpath('//*[@id="divMenuGame"]/table/tbody/tr/td/a[3]')
    difficulty_choice.click()
elif input_difficulty == 'expert':
    action = webdriver.common.action_chains.ActionChains(browser)
    element = browser.find_element_by_name("cellIm0_0")
    action.move_to_element_with_offset(element, 0, -65)
    action.click()
    action.perform()
    difficulty_choice = browser.find_element_by_xpath('//*[@id="divMenuGame"]/table/tbody/tr/td/a[4]')
    difficulty_choice.click()
    
# initiate with state 0, play game using while loop
state = 0    

while state != 6:

    # determine difficulty of board
    try:
        element = browser.find_element_by_name("cellIm16_15")
        difficulty = 'beginner'
    except NoSuchElementException:
        try:
            element = browser.find_element_by_name("cellIm8_8")
            difficulty = 'intermediate'
        except NoSuchElementException:
            difficulty = 'beginner'

    if difficulty == 'beginner':
        dim_x = 8
        dim_y = 8
    elif difficulty == 'intermediate':
        dim_x = 16
        dim_y = 16
    else:
        dim_x = 16
        dim_y = 30  

    timestamp_1 = datetime.datetime.now()

    # read board state
    board = np.zeros((dim_x,dim_y), dtype=int)
    for i in range(dim_x):
        for j in range(dim_y):
            name = "cellIm" + str(j) + "_" + str(i)
            element = browser.find_element_by_name(name)
            img = element.get_attribute('src')
            if 'open0' in img:
                board[i,j] = -1
            elif '1' in img:
                board[i,j] = 1
            elif '2' in img:
                board[i,j] = 2
            elif '3' in img:
                board[i,j] = 3
            elif '4' in img:
                board[i,j] = 4
            elif '5' in img:
                board[i,j] = 5
            elif '6' in img:
                board[i,j] = 6
            elif '7' in img:
                board[i,j] = 7
            elif '8' in img:
                board[i,j] = 8
            elif 'bombflagged' in img:
                board[i,j] = 9
            elif 'blank' in img:
                board[i,j] = 0
            elif 'bombdeath' in img:
                board[i,j] = 10

    timestamp_2 = datetime.datetime.now()
    #print('time taken to read board: ' + str((timestamp_2 - timestamp_1).total_seconds()) + ' seconds')

    # perform action
    action = det_state(board)
    state = action[0]
    cell = action[1]

    if state == 2:
        actionChains = ActionChains(browser)
        name = "cellIm" + str(cell[1]) + "_" + str(cell[0]) 
        element = browser.find_element_by_name(name)
        actionChains.click(element).perform()

    if state == 3:
        actionChains = ActionChains(browser)
        name = "cellIm" + str(cell[1]) + "_" + str(cell[0]) 
        element = browser.find_element_by_name(name)
        actionChains.context_click(element).perform()

    if state == 4:
        actionChains = ActionChains(browser)
        name = "cellIm" + str(cell[1]) + "_" + str(cell[0]) 
        element = browser.find_element_by_name(name)
        actionChains.click(element).perform()

    if state == 5:
        actionChains = ActionChains(browser)
        name = "cellIm" + str(cell[1]) + "_" + str(cell[0]) 
        element = browser.find_element_by_name(name)
        actionChains.click(element).perform()

    if state == 0:
        print('state = 0, could not determine next move')
        break

    if state == 6:
        print('board complete')
        answer = input('restart the board? enter yes or no: ')
        if answer == 'yes':
            reset = browser.find_element_by_xpath('//*[@id="divBoard"]/table/tbody/tr/td/a[2]/img')
            reset.click()
            state = 1
        else:
            break

    if state == 7:
        if automatic_reset:
            print('guess failed, resetting board')
            reset = browser.find_element_by_xpath('//*[@id="divBoard"]/table/tbody/tr/td/a[2]/img')
            reset.click()
        else:
            print('guess failed, program loses')
            answer = input('restart the board? enter yes or no: ')
            if answer == 'yes':
                reset = browser.find_element_by_xpath('//*[@id="divBoard"]/table/tbody/tr/td/a[2]/img')
                reset.click()
                state = 1
            else:
                break

    timestamp_3 = datetime.datetime.now()
    #print('time taken to determine state: ' + str((timestamp_3 - timestamp_2).total_seconds()) + ' seconds')
