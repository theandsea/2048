from __future__ import absolute_import, division, print_function
import copy, random
from filecmp import cmp

import numpy as np

from game import Game

MOVES = {0: 'up', 1: 'left', 2: 'down', 3: 'right'}
MAX_PLAYER, CHANCE_PLAYER = 0, 1


# Tree node. To be used to construct a game tree.
class Node:
    # Recommended: do not modify this __init__ function
    def __init__(self, state, player_type):
        self.state = (copy.deepcopy(state[0]), state[1])

        # to store a list of (direction, node) tuples
        self.children = []

        self.player_type = player_type

    # returns whether this is a terminal state (i.e., no children)
    def is_terminal(self):
        # TODO: complete this
        if len(self.children) == 0:
            return True
        pass


# AI agent. To be used do determine a promising next move.
class AI:
    # Recommended: do not modify this __init__ function
    def __init__(self, root_state, search_depth=3):
        self.root = Node(root_state, MAX_PLAYER)
        self.search_depth = search_depth
        self.simulator = Game(*root_state)

    # recursive function to build a game tree
    def build_tree(self, node=None, depth=0, ec=False):
        if node == None:
            node = self.root

        node.deepth=depth
        if depth == self.search_depth:
            return

        if node.player_type == MAX_PLAYER:
            # TODO: find all children resulting from
            # all possible moves (ignore "no-op" moves)
            # NOTE: the following calls may be useful:
            # self.simulator.reset(*(node.state))
            # self.simulator.get_state()
            # self.simulator.move(direction)

            # 4 direction
            game = Game(node.state[0], node.state[1])
            node.children.clear()
            for i in range(4):
                game.move(i)
                child = Node(copy.deepcopy(game.get_state()), CHANCE_PLAYER)
                node.children.append(child)
                game.undo()
            #print("len",len(node.children))
            pass

        elif node.player_type == CHANCE_PLAYER:
            # TODO: find all children resulting from
            # all possible placements of '2's
            # NOTE: the following calls may be useful
            # (in addition to those mentioned above):
            # self.simulator.get_open_tiles():
            board = node.state[0]
            node.children.clear()
            for i in range(len(board)):
                for j in range(len(board[i])):
                    if board[i][j] == 0:
                        child_state = copy.deepcopy(node.state)
                        child_state[0][i][j] = 2
                        node.children.append(Node(child_state, MAX_PLAYER))
            pass

        # print("summary___", node.player_type, "___", depth)
        # for child in node.children:
        #   print(child.state)

        # TODO: build a tree for each child of this node
        if depth < self.search_depth:
            for child in node.children:
                self.build_tree(child, depth + 1)

    # expectimax implementation;
    # returns a (best direction, best value) tuple if node is a MAX_PLAYER
    # and a (None, expected best value) tuple if node is a CHANCE_PLAYER
    def expectimax(self, node=None):
        # TODO: delete this random choice but make sure the return type of the function is the same
        #return random.randint(0, 3), 0

        #print("This is for Node deepth of   ", node.deepth)
        #print("Node player",node.player_type)
        #print("children number",len(node.children))
        #print(node.state)

        if node == None:
            node = self.root

        if node.is_terminal():
            # TODO: base case
            return 1, node.state[1]
            pass

        elif node.player_type == MAX_PLAYER:
            # TODO: MAX_PLAYER logic
            max = 0
            direct = None
            for i in range(len(node.children)): # why it go more than once ???
                #print("-----direction",i," ----deepth",node.children[i].deepth)
                #print("New child")
                #print(k)
                child = node.children[i]
                _, child_score = self.expectimax(child);
                #if len(child.children)!=0:
                    # print(len(child.children),i,child_score)
                # try to find whether they are the same
                #print(i)
                same=True
                a_arr=node.state[0]
                b_arr=child.state[0]
                for x in range(len(a_arr)):
                    for y in range(len(a_arr[x])):
                        if a_arr[x][y]!=b_arr[x][y]:
                            same=False
                #print(i)
                #print("This is for Node deepth of   ", node.deepth)
                #print("Maxplayer!!!!!")
                #print(a_arr,)
                #print(b_arr,child_score)
                #print(same)

                if  (not same) and max < child_score:
                    max = child_score
                    direct = copy.deepcopy(i)
                # print(self.expectimax(child))
                #print("after",i)
                #k +=1
            return direct,max
            pass

        elif node.player_type == CHANCE_PLAYER:
            # TODO: CHANCE_PLAYER logic
            sum = 0.0
            for child in node.children:
                sum += self.expectimax(child)[1]
            sum /= (len(node.children)+0.0)
            # sub step cannot move
            if sum==0:
                sum=node.state[1]
            return 1, sum
            pass

    # Do not modify this function
    def compute_decision(self):
        self.build_tree()
        #print("======================",len(self.root.children),"====================")
        #print("Now", self.root.state)
        direction, _ = self.expectimax(self.root)
        #print("take action",direction, self.root.state)
        return direction

    # Implement expectimax with customized evaluation function here
    def compute_decision_ec(self):
        # TODO delete this
        self.build_tree()
        # direction, _ = self.expectimax(self.root)

        max = 0
        direct = None
        node=self.root
        for i in range(len(node.children)):
            child = node.children[i]
            _, child_score = self.expectimax(child);

            same = True
            a_arr = node.state[0]
            b_arr = child.state[0]
            for x in range(len(a_arr)):
                for y in range(len(a_arr[x])):
                    if a_arr[x][y] != b_arr[x][y]:
                        same = False

            heuristic=0
            pre=0
            rear=0
            for x in range(len(b_arr)):
                for y in range(1,len(b_arr[x])):
                    res=b_arr[x][y]-b_arr[x][y-1]
                    if res>0:
                        rear +=res
                    else:
                        pre -=res
            #print(pre,rear)
            heuristic += np.absolute(pre-rear)

            pre = 0
            rear = 0
            for x in range(1,len(b_arr)):
                for y in range(0, len(b_arr[x])):
                    res = b_arr[x][y] - b_arr[x- 1][y]
                    if res > 0:
                        rear += res
                    else:
                        pre -= res
            heuristic += np.absolute(pre-rear)

            #print(pre,rear)
            #print(heuristic)

            max_num=0;
            null_num=0;
            for x in range(0,len(b_arr)):
                for y in range(0, len(b_arr[x])):
                    if b_arr[x][y]==0:
                        null_num +=1
                    if max_num < b_arr[x][y]:
                        max_num = b_arr[x][y]
            #print(16-null_num)
            heuristic += max_num*null_num/4

            total=child_score+heuristic
            if (not same) and max < total:
                max = total
                direct = copy.deepcopy(i)

        return direct




        #return random.randint(0, 3)


