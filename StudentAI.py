from random import randint
from BoardClasses import Move
from collections import defaultdict
from BoardClasses import Board
import numpy as np
import random
import time
import math
import copy
#import ZeroDivisionError


#The following part should be completed by students.
#Students can modify anything except the class name and exisiting functions and varibles.
class Node:
    def __init__(self):
        self.parent = None 
        self.children = []
        self.color = None
        self.win_count = 0
        self.visit_count = 0
        self.move = None

    def new_node(self, node, move, play):
        self.childNodes = []
        self.untried = []
        self.move = move
        self.wins = 0
        self.visitCount = 0
        self.color = play
        self.visited = False
        self.parent = node

class StudentAI():
    def __init__(self,col,row,p):
        self.col = col
        self.row = row
        self.p = p
        self.board = Board(col,row,p)
        self.board.initialize_game()
        self.color = ''
        self.opponent = {1:2,2:1}
        self.color = 2
        self.speed = False
        self.step = 0
        self.total_time = 0.0

        #timepassed
    
    def checkBackUp(self, row, col, color):
        score = 0
        if color == 1:
            if row < self.row-1 and col > 0 and col < self.col-1:
                if self.board.board[row+1][col+1].get_color() == 'W':
                    score += 100
                if self.board.board[row+1][col-1].get_color() == 'W':
                    score += 100
        else:
            if row > 0 and col > 0 and col < self.col-1:
                if self.board.board[row-1][col+1].get_color() == 'B':
                    score += 100
                if self.board.board[row-1][col-1].get_color() == 'B':
                    score += 100
        return score
    
    def checkEnemy(self, row, col, color):
        bad_score = 0
        if color == 1:
            if row > 0 and col > 0 and col < self.col-1:
                if self.board.board[row-1][col+1].get_color() == 'B':
                    bad_score += 100
                if self.board.board[row-1][col-1].get_color() == 'B':
                    bad_score += 100

        else:
            if row < self.row-1 and col > 0 and col < self.col-1:
                if self.board.board[row+1][col+1].get_color() == 'W':
                    bad_score += 100
                if self.board.board[row+1][col-1].get_color() == 'W':
                    bad_score += 100
           
        return bad_score

    def heuristic(self, color):
        my_score = 0
        for i in range(self.row):
            for j in range(self.col):
                pawn = self.board.board[i][j]
                pColor = 0
                if pawn.get_color() == 'W':
                    pColor = 1
                elif pawn.get_color() == 'B':
                    pColor = 2
                if color == pColor:
                    if pawn.is_king:
                        my_score += 100
                    else:
                        my_score += 20
                    #my_score -= self.checkEnemy(i,j,pColor)
                elif pColor != 0 and color == self.opponent[pColor]:
                    if pawn.is_king:
                        my_score -= 100
                    else:
                        my_score -= 20
                    #op_score -= self.checkEnemy(i,j,pColor)
        return my_score

    def createTreeNodes(self, node, play):
        moves = self.board.get_all_possible_moves(play)
        for i in range(len(moves)):
            for j in range(len(moves[i])):
                node.untried.append(self.makeNode(node, moves[i][j], play))

    def best_child(self, node):
        max_UCT = -math.inf
        best_node = node.children[0]
        for child in node.children:
            # if child.visit_count == 0:
            #     return child
            # else:
            try:
                UCT = child.win_count / child.visit_count + 2**(1/2) * ((np.log(node.visit_count)/child.visit_count)**(1/2))
                if UCT > max_UCT:
                    max_UCT = UCT
                    best_node = child
            except ZeroDivisionError:
                return child
        return best_node

    def expand(self,node,board):
        moves = board.get_all_possible_moves(node.color)
        if len(moves) == 0:
            return node
        else:
            for pawn in moves:
                for choice in pawn:
                    child = Node()
                    child.color = self.opponent[node.color]
                    child.move = choice
                    child.parent = node
                    node.children.append(child)
        #print(board.show_board())
        next_node = node.children[random.randint(0,len(node.children)-1)]
        #print(next_node.move)
        board.make_move(next_node.move,node.color)
        return next_node
    
    # def simulatePlay(self, board, play):
    #     winner = 0
    #     if board.is_win(play):
    #         winner = board.is_win(play)
    #         board.undo()
    #     else:
    #         moves = board.get_all_possible_moves(self.opponent[play])
    #         i = randint(0, len(moves)-1)
    #         j = randint(0, len(moves[i])-1)
    #         res = moves[i][j]
    #         board.make_move(res, self.opponent[play])
    #         #print("Simulation: ",board.show_board())
    #         winner = self.simulatePlay(board, self.opponent[play])
    #     return winner

    def simulate(self, node, board):
        #counter = 0
        color = node.color
        while True:
            # print("counter is: ---- ", counter)
            # counter += 1
            moves = board.get_all_possible_moves(color)
            if moves is None or len(moves) == 0:
               return self.opponent[color]
            i = random.randint(0, len(moves)-1)
            j =  random.randint(0, len(moves[i])-1)
            move = moves[i][j]
            board.make_move(move, color)
            winner = board.is_win(color)
            if winner != 0:
                return winner
            color = self.opponent[color]

    def back_propogate(self, color, node):
        while node:
            node.visit_count += 1
            if color != node.color:
                node.win_count += 1
            node = node.parent

    def get_move(self,move): 
        if len(move) != 0:
            self.board.make_move(move,self.opponent[self.color])
        else:
            self.color = 1
        board_time = time.time()
        root = Node()
        root.color = self.color
        time_limit = 8.0
        all_possible = self.board.get_all_possible_moves(self.color)
        self.step += 1
        if self.step <= 10:
            time_limit = 3.5
        if self.step >= 11 and self.step <= 30:
            time_limit = 10
        if len(all_possible) == 1 and len(all_possible[0]) == 1:
            #self.speed = True
            time_limit = 0.1
            self.total_time += time_limit
        #elif self.speed:
        #    time_limit = 12
        #    self.speed = False
        else:
            if self.step <= 10:
                time_difference = self.total_time - self.step * 3.5
            elif self.step >= 11 and self.step <= 30:
                time_difference = self.total_time - (self.step * 10 - 35)
            else:
                time_difference = self.total_time - (self.step * time_limit - 235)
            if time_difference < 0:
                time_limit -= time_difference
            if 480 - self.total_time < 15:
                time_limit = 1
            self.total_time += time_limit
        while time.time() - board_time < time_limit:
            board_copy = copy.deepcopy(self.board)
            next_node = root
            while next_node.children:
                next_node = self.best_child(next_node)
                board_copy.make_move(next_node.move, self.opponent[next_node.color])
            if next_node.visit_count != 0:
                child = self.expand(next_node, board_copy)
            else:
                child = next_node
            simulated_color = self.simulate(child, board_copy)
            self.back_propogate(simulated_color,child)

        max_win_rate = -math.inf
        result_node = None
        for child in root.children:
            if child.win_count/child.visit_count > max_win_rate:
                max_win_rate = child.win_count/child.visit_count
                result_node = child

        self.board.make_move(result_node.move,self.color)
        return result_node.move
        
