#module for Tree_Single


from misc import *


#following class simulates a single-stage tree game
class Tree_Single:
    
    def __init__(self, player_list, strat_list, payoff_mat, acting_player = None):
        #argument players expected to be a list of string
        #argument strat_list expected to be a list of Strategy
        #argument payoff_mat expected to be a mat of float with its
        #elements having 1 to 1 correspondence to elements of strat_list
        #argument acting_player expected to be a string in player_list
        
        self.check_validity(player_list, strat_list, payoff_mat, acting_player)
        self.player_list = list(player_list)
        self.strat_list = list(strat_list)
        self.payoff_mat = list(payoff_mat)
        self.tree_dict = self.make_tree_dict()
        if acting_player:
            self.acting_player = acting_player
        else:
            self.acting_player = self.player_list[0]
        self.br_list = self.make_br_list()
        self.ne_list = self.make_ne_list()
        self.logical_payoff_mat = self.make_logical_payoff_mat()

    #following function checks if the constructor arguments are comprehensible
    def check_validity(self, player_list, strat_list, payoff_mat, acting_player):  #FUNCTION DOES NOT THROW EXCEPTIONS YET
        #arguments here expected to be the same as their counterparts in __init__
        
        if len(player_list) < 1 or len(strat_list) < 1 or len(payoff_mat) < 1:
            print("Error, no players, no strats, or no payoff.")  #PLACEHOLDER CODE: THROW AN EXCEPTION HERE
        if acting_player not in player_list and acting_player != None:
            print("Error, the acting player isn't a player.")  #PLACEHOLDER CODE: THROW AN EXCEPTION HERE

    #following function maps strats to payoffs
    def make_tree_dict(self):
        
        tree_dict = {strat[1] : Payoff_Dict(self.player_list, self.payoff_mat[strat[0]]) \
                     for strat in enumerate(self.strat_list)}

        #return value is a dict of the form Strategy: list of float
        return tree_dict

    #following function finds best strats for the player to choose
    def make_br_list(self):
        
        br_list = []
        br_payoff = None

        #following code goes through all of the acting player i's strategies s sub i,
        #finds the one with the highest U(s' sub i), which is the BR sub i, then goes
        #through the list again to find all U(s sub i) == U(s' sub i)
        for strat in self.strat_list:
            if br_payoff == None or \
               br_payoff < self.tree_dict[strat].get_payoff(self.acting_player):
                br_payoff = self.tree_dict[strat].get_payoff(self.acting_player)
        for strat in self.strat_list:
            if br_payoff == self.tree_dict[strat].get_payoff(self.acting_player):
                br_list.append(strat)
        #end

        #return value is a list of Strategy
        return br_list

    #following function finds the NE of the tree subgame
    #since this class is a single-stage tree subgame, it's trivial
    def make_ne_list(self):

        #return value is a list of Strategy
        return self.br_list

    #following function returns the payoffs that would be given to each player
    #assuming all players play this game logically
    def make_logical_payoff_mat(self):
        
        logical_payoff_mat = []

        #following code goes through each ne (NE are BR in this case)
        #and appends the payoffs of that NE to logical_payoff_mat
        for ne in self.ne_list:
            payoff_list = []
            payoff_dict = self.tree_dict[ne]
            for player in self.player_list:
                payoff_list.append(payoff_dict.get_payoff(player))
            logical_payoff_mat.append(payoff_list)
        #end

        #return value is a mat of float
        return logical_payoff_mat

    #following function returns the payoffs of the tree single, played logically.
    #that is, the payoffs if the acting player plays a BR
    def get_logical_payoff_mat(self):

        #return value is a mat of float
        return self.logical_payoff_mat

    #following function gives relevant information
    def print_state(self):
        print("The players are", self.player_list)
        print("The acting player is", self.acting_player)
        print("The acting player's strat(ies):", self.strat_list)

        #following code goes through all s sub i, where i is the acting player
        #and gives the U sub j(s sub i) for each player j, in the form:
        #"s sub i yields U sub j(s sub i) for j"
        print("Here are the payoff for each strat choice by the acting player:")
        for strat in self.strat_list:
            print(strat.name, "yields", end = " ")
            for player in self.tree_dict[strat].player_list:
                print(self.tree_dict[strat].get_payoff(player),
                      "for", player, end = ", ")
            print()
        #end

        #following code gives the BR for the acting player, which is the NE
        print("Best response(s) for acting player", self.acting_player + ":", end = " ")
        for br in self.br_list:
            print(br, end = ", ")
        print()
        #end
        
        print("(the nash equilibrium(a) is the best response in this case)\n")
