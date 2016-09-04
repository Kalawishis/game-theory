#module to implement sequential games


from matrix_single import *
from tree_single import *


#following function retrieves the payoffs from a game played in its logical form
#if something that isn't a game is passed in, it just returns it
def get_logical_payoff(payoff):
    #argument payoff expected to be Tree_Single, Matrix_Single, or list of float

    try:
        
        #return value is a mat of payoff
        return payoff.get_logical_payoff_mat()
     
    except AttributeError:
        #return value is a mat of payoff
        return [payoff]


#following class exists to be put into a fork_mat: M_I means Matrix Indicator
#represents and yields essential information to create_tree about a Matrix_Single
class M_I:
    
    def __init__(self, fork_num, strat_num_list, included_player_list):
        #argument fork_num expected to be int
        #argument strat_num_list expected to be a list of int
        #arguemnt included_player_list expected to be a list of string 
        #in Game self.player_list
        
        self.fork_num = fork_num
        self.strat_num_list = strat_num_list
        self.included_player_list = included_player_list


#following class exists to be put into a fork_mat: T_I means Tree_Indicator
#represents and yields essential information to create_tree about a Tree_Single
class T_I:
    
    def __init__(self, fork_num, acting_player = None):
        #argument fork_num expected to be int
        #arguemnt acting_player expected to be a string in Game self.player_list
        
        self.fork_num = fork_num
        self.acting_player = acting_player
    

#following class represents an element of a tree
class Node:
    
    def __init__(self, indicator = None, connection_list = None, item_list = None):
        #argument indicator expected to be 0, M_I, or T_I
        #argument connection_list expected to be a list of Node
        #argument item_list expected to be list of float, Matrix_Single, or Tree_Single
        
        self.indicator = indicator
        self.connection_list = connection_list if connection_list else []
        self.item_list = item_list if item_list else []


#following function creates a tree (not a binary one) to organize the
#nodes in order to resemble a sequential game
def create_tree(fork_mat, column):
    #argument fork_mat expected to be a mat of 0, M_I, or Tree Indicator
    #arguement column expected to be an int x, 0 <= x < len(fork_mat)

    current_fork = fork_mat[column][0]

    #following code is base case and run if there are 0 forks
    #creates a payoff node to hold the payoff and be the endnode
    if current_fork == 0:

        #return value is a Node
        return Node(current_fork)
    #end

    #following code creates a Node that holds Matrix_Single or Tree_Single
    #and links to more nodes who's values are calculated by a recursive call
    connection_list = []
    while current_fork.fork_num:
        connection_list.append(create_tree(fork_mat, column + 1))
        fork_mat[column + 1].pop(0)
        current_fork.fork_num -= 1
    #end

    #return value is a Node created by the previous code section
    return Node(current_fork, connection_list)


#following function represents a sequential game, a linkage of multiple
#singles to form one complex node web
class Game:
    
    def __init__(self, player_list, game_tree, end_payoff_mat):
        #arguement player_list expected to be a list of string
        #argument game_tree expected to be a Node returned by create_tree
        #argument end_payoff_mat expected to be a mat of float with 1 to 1
        #correspondence with the number of endnodes in game_tree
      
        self.player_list = player_list
        self.game_tree = game_tree
        self.letter_strat_dict = self.make_letter_strat_dict()
        self.game = self.make_game(self.game_tree, end_payoff_mat, 0)
        self.sp_eq_list = self.make_sp_eq_list()

    #following function creates a corresponding strat for every letter
    #utilized for convenience
    def make_letter_strat_dict(self):    
        letter_strat_dict = {}
        for letter in ALPHABET:
            letter_strat_dict[letter] = Strat(letter)

        #return value is a dict of form char: Strategy
        return letter_strat_dict

    #following function gives nodes their game singles, or payoffs if
    #the nodes are endnodes
    def make_game(self, node, end_payoff_mat, column):
        #argument node expected to be Node
        #argument end_payoff_mat expected to be mat of float
        #argument column expect to be int 

        #following code is base case and run if node is an endnode
        #it gives the endnode the first payoff from end_payoff_mat
        #then readies the next end_payoff_mat element to be given
        if not node.indicator:
            node.item_list.append(end_payoff_mat[0])
            end_payoff_mat.pop(0)
        #end

        #following code run if node is a M_I node
        #calculates all the payoffs of the node's forks recursively
        #then creates a Matrix_Single with M_I self.included_player_list,
        #auto-generated strat_mat with strat_mat[x] equalling M_I
        #self.strat_num_list[x], and the found payoffs
        #if multiple logical payoffs are found for a single fork, the
        #code creates multiple matrix singles, one for each logical payoff
        elif type(node.indicator) == M_I:
            strat_mat = [[self.letter_strat_dict[letter] for letter in ALPHABET[:strat_num]] \
                         for strat_num in node.indicator.strat_num_list]
            payoff_mat = []
            for fork in node.connection_list:
                payoff_list = []
                fork.item_list = self.make_game(fork, end_payoff_mat, column + 1)
                for item in fork.item_list:
                    for logical_payoff in get_logical_payoff(item):
                        payoff_list.append(logical_payoff)
                payoff_mat.append(payoff_list)
            payoff_combo_list = list(itertools.product(*payoff_mat))
            for payoff_combo in payoff_combo_list:
                node.item_list.append(Matrix_Single(node.indicator.included_player_list, \
                                                    strat_mat, \
                                                    payoff_combo))
        #end

        #following code run if node is a T_I node
        #calculates all the payoffs of the node's forks recursively
        #then creates a Tree_Single with self.player_list, auto-generated
        #strat_list (len equal to number of forks), the found payoffs, and an
        #acting_player determined by T_I or the sequence of the game
        #if multiple logical payoffs are found for a single fork, the
        #code creates multiple tree singles, one for each logical payoff
        elif type(node.indicator) == T_I:
            strat_list = [self.letter_strat_dict[letter] \
                          for letter in ALPHABET[:len(node.connection_list)]]
            if not node.indicator.acting_player:
                node.indicator.acting_player = self.player_list[column % len(self.player_list)]
            payoff_mat = []
            for fork in node.connection_list:
                payoff_list = []
                fork.item_list = self.make_game(fork, end_payoff_mat, column + 1)
                for item in fork.item_list:
                    for logical_payoff in get_logical_payoff(item):
                        payoff_list.append(logical_payoff)
                payoff_mat.append(payoff_list)
            payoff_combo_list = list(itertools.product(*payoff_mat))
            for payoff_combo in enumerate(payoff_combo_list):
                tree_single = Tree_Single(self.player_list, \
                                          strat_list, \
                                          payoff_combo[1], \
                                          node.indicator.acting_player)
                node.item_list.append(tree_single)
        #end

        #return value is a Node
        return node.item_list

    #following function makes a list of all the subgame perfect equilibira
    #(sp_eq) inside a Game, with sp_eq being defined as a strategy set s that
    #creates a ne within every subgame of the  Game
    def make_sp_eq_list(self):
        sp_eq_pool = []

        #following function makes an sp_eq pool, or a mat of column_ne_lists,
        #which are mats of lists of the ne of different nodes of a single
        #column
        #following function is also nested within make_sp_eq_list
        def make_sp_eq_pool(node, column):
            #argument node expected to be Node
            #argument column expected to be int
            
            ne_list = []

            #following code makes sure there is always a column_ne_list in
            #sp_eq_pool for this function to add ne to
            if column >= len(sp_eq_pool) and \
               (type(node.indicator) == T_I or type(node.indicator) == M_I):
                sp_eq_pool.append([])
            #end

            #following code run if node is a T_I node, adds all the ne of all
            #the tree singles in the node to sp_eq_pool, ignoring duplicates
            if type(node.indicator) == T_I:
                for item in node.item_list:
                    for ne in item.ne_list:
                        ne_list.append(ne)
                sp_eq_pool[column].append(list(set(ne_list)))
            #end

            #following code run if node is a M_I node, adds all the ne (pure and mixed)
            #of all the matrix singles in the node to sp_eq_pool, ignoring duplicates
            elif type(node.indicator) == M_I:
                for item in node.item_list:
                    for pure_ne in item.pure_ne_list:
                        ne_list.append(pure_ne)
                    for mixed_ne in item.mixed_ne_list:
                        ne_list.append(mixed_ne)
                sp_eq_pool[column].append(list(set(ne_list)))
            #end

            #following code finds the sp_eq_pool for all the forks of node
            #in effect adding them to sp_eq_pool
            for fork in node.connection_list:
                make_sp_eq_pool(fork, column + 1)
            #end
                
        #end nested function
        
        make_sp_eq_pool(self.game_tree, 0)

        #following code gets all the possible combinations of each ne at
        #each node to create a list of unique sp_eq
        sp_eq_list = list(itertools.product(*[list(itertools.product(*column_ne_list)) \
                                              for column_ne_list in sp_eq_pool]))
        #end
        
        return sp_eq_list
    
        
    #following function gives relevant information
    def print_state(self, node, column, row_tracker):
        #argument node expected to be Node
        #argument column expected to be int
        #argument row_tracker expected to be a list of only one int

        #following code prints positional information
        print("COLUMN", str(column) + ",", "ROW", row_tracker[column])
        #end

        #following code is base case and run if node has no forks (is endnode)
        #gives positional information and the payoff
        if len(node.connection_list) == 0:
            print("PAYOFF", node.item_list[0], '\n')
            row_tracker[column] += 1
            return
        #end

        #following code run if node holds a Tree_Single or a Matrix_Single
        #goes through all the singles the node holds and calls their self.print_state
        #then calls Game self.print_state for each fork of the node
        print("\nHELD GAMES\n")
        for item in node.item_list:
            item.print_state()
        print("END HELD GAMES\n")
        row_tracker.append(0)
        for node in node.connection_list:
            self.print_state(node, column + 1, row_tracker)
        row_tracker[column] += 1
        #end
