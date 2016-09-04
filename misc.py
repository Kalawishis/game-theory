#module containing the basics which Matrix_Single and Tree_Single need to function


import functools
import itertools
import random
import collections
from sympy import Symbol, solve


ALPHABET = "abcdefghijklmnopqrstuvwxyz"  #problem: only 26 players until an out of bounds error
NUMBERS = "0123456789"  #problem: a player may only have 10 strats before an out of bounds error


#following class represents a (pure) strat
class Strat: 
    
    def __init__(self, name):
        #argument name expected to be a string
        
        self.name = name
        
    def __repr__(self):

        #return value is a string
        return self.name


#represent a mixed strat
class Mixed_Strat:   
    
    def __init__(self, strat_list, prob_list):
        #argument strat_list expected to be a list of Strat
        #argument prob_list expected to be a list of float x, such that 0 <= x <= 1
        
        #following code links each pure strategy in strat_list to a probability in prob_list
        #creating a mixed strategy
        self.strat_prob_list = list(zip(strat_list, prob_list))
        self.mix = {}
        for strat, prob in self.strat_prob_list:
            self.mix[strat] = prob
        #end
        
    def __repr__(self):
        
        #return value is a string form of a dictionary
        return str(self.mix)


#following function takes two different lists of strats and returns their product
#combine([[a,b],[a,b]]) yields aa, ab, ba, bb
#the order is like FOIL - using the distributive property
def combine(strat_lists):
    #argument strat_lists expected to be one list or more
    #lists are expected to be separate, not part of one collection

    #return value is a matrix of Strat
    return list(itertools.product(*strat_lists))


#following function returns strat names sequentially given strat_list 
def show_strats(strat_list, sep = ""):
    #argument strat_list expected to be a list of Strat
    #argument sep expected to be a string
    
    result = ""
    for strat in strat_list:
        result += strat.name + sep
    result = result[:len(result) - len(sep)]

    #return value is a string of Strat self.name
    return result


#following class represents a U sub i(s) 
class Payoff_Dict():
    
    def __init__(self, player_list, payoff_list):
        #argument player_list expected to be the self.player_list of a
        #Tree_Single or a Matrix_Single
        #argument payoff_list expected to be an element of
        #self.payoff_mat of a Tree_Single or a Matrix_Single

        self.check_validity(player_list, payoff_list)
        self.player_list = player_list
        self.payoff_list = payoff_list
        self.payoff_dict = self.make_payoff_dict()
        
    #following function checks if the constructor arguments are comprehensible
    def check_validity(self, player_list, payoff_list):  #FUNCTION DOES NOT THROW EXCEPTIONS YET
        #argument player_list expected to be same as player_list in constructor
        #argument payoff_list expected to be same as payoff_list in constructor
        if len(player_list) != len(payoff_list):
            print("ERROR, PAYOFF_DICT")  #PLACEHOLDER CODE: THROW AN EXCEPTION HERE
            print("ERROR PLAYERS", player_list)
            print("ERROR PAYOFF", payoff_list)
            
    #following function makes a dict that corresponds players to their payoff
    def make_payoff_dict(self):
            
        payoff_dict = {player[1] : self.payoff_list[player[0]] \
                       for player in enumerate(self.player_list)}

        #return value is a dict of form string: float
        return payoff_dict

    #following function, given a player i, returns payoff for i
    def get_payoff(self, player):
        #player expected to string in self.player_list

        #return value is a float
        return self.payoff_dict[player]





