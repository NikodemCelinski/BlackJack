#!/usr/bin/env python
# -*- coding: utf-8 -*-


# BlackJack Game 
# By Nikodem Celiński 

# file created : 12:50 | 18.09.18 

import black_jack_classes

"""
This code represents logic of the Game.

"""

Game = black_jack_classes.Game()


Game.init()
# HERE GAME LOOP 

while not Game.game_end:
	for player in Game.all_players :
		player.get_initial_hand(Game.deck)
		player.make_bet( Game.all_players.index(player))
	Game.croupier.get_initial_hand(Game.deck)

	# players ought to see first card in croupiers hand before their move

	# players make move
	#Game.show_table(Game.all_players[0],Game.all_players[0].list_of_hands[0])

	for player in Game.all_players : 
		for hand in player.list_of_hands :
			Game.show_table(player,hand)
			player.make_move(Game.deck,hand, Game)
			#player.show_stats()

	#print ("THESE WERE PLAYERSSS ------------------------")
	Game.croupier.make_move(Game.deck, Game.croupier.list_of_hands[0])
	#print("THIS WAS CROUPIER **************************************")

	Game.manage_bets_after_deal()
	Game.clear_hands()
	print("TABLE CLEARED !")
	Game.kick_bancrupt_players()


	if len(Game.deck.cards) < 25:
		Game.deck.new_shuffled_deck()
		print("\n Hey, That's a new DECK ! \n")

	

if not Game.all_players :
	print("ALL PLAYERS ARE BANCRUPT ! \n GAME OVER ! ")

else : 
	print("The Game has ended")



# NEED TO BE DONE : 

	#1. Make UI somewhat clear and readable 



	

