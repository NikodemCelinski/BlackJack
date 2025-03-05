#!/usr/bin/env python
# -*- coding: utf-8 -*-

#BlackJack Game : CLASSES
#By Nikodem Celiński 

#file created : 14:00 | 18.09.18 


import random
from bj_exceptions import MovementFail 
from subprocess import call
from other_func import convert_to_int

class Deck():

	def __init__(self):
		self.possible_figures = [2,3,4,5,6,7,8,9,10,'J','D','K','A']
		self.cards = self.possible_figures*4

	def shuffle(self):
		random.shuffle(self.cards)

	def pop_top_card(self):
		"""
		INPUT: none
		OUTPUT: first card in deck

		Function deletes returned card from deck.
		"""

		#print(str(self.cards) + "\n KARTY \n")

		top_card = self.cards[0]
		#print("NEW CARD : " + str(top_card))
		self.cards.pop(0)
		return top_card

	def new_shuffled_deck(self):
		self.cards = self.possible_figures*4
		self.shuffle()

class Hand():
	"""
	Class represents a participant's hand. 

	hand - a list of cards
	
	"""

	def __init__(self):
		self.cards = []

		self.points_hi = 0
		self.points_lo = 0
		self.preferable_points = 0
		self.is_busted = False
		self.hi_busted = False
		self.bet = 0
		self.hit_limit_on = False

	def __str__(self):

		cards_str = str(self.cards)
		pointsHi_str = str(self.points_hi)
		pointsLo_str = str(self.points_lo)
		is_busted_str = str(self.is_busted)
		bet_str = str(self.bet)
		hit_limit_str = str(self.hit_limit_on)

		print("CARDS : " + cards_str)
		print("POINTS (high/low) : " + pointsHi_str +'/'+ pointsLo_str)
		print("IS_BUSTED :" + is_busted_str)
		print("BET : " + bet_str)
		print("HIT_LIMIT : " + hit_limit_str)

		return ''

	def update_points_stats(self):
		points_sum_hi = 0
		points_sum_lo = 0
		for card in self.cards : 
			if isinstance(card, int):
				points_sum_hi += card 
				points_sum_lo += card 
			elif card == 'A' :
				points_sum_lo += 1
				points_sum_hi += 11
			else : 
				points_sum_hi += 10
				points_sum_lo += 10

		self.points_hi = points_sum_hi
		self.points_lo = points_sum_lo

		if points_sum_hi > 21 :
			self.hi_busted = True
			self.preferable_points = points_sum_lo
		else:
			self.preferable_points = points_sum_hi

		if points_sum_lo > 21 : # Change to new class
			self.is_busted = True

		return (self.points_hi, self.points_lo, self.preferable_points)



	



class Participant():

	"""
	Class that models every participant of Black Jack game. 

	Participant is a class modeling every human being involved in playing Black Jack. In this case : Players and Croupier

	hand - This is a class containing info about hand status, points and 

	Every game participant is able to perform :
	Hit - participant draw a card (can drow up to bust or otherwise, if explicitely written)
	Stay - participant don't draw a card

	"""

	def __init__(self):

		self.is_busted = False
		self.list_of_hands = []
	

	def show_stats(self):
		hand = self.list_of_hands[0]
		print("Croupier : ")
		print("Cards : " + str(hand.cards))
		print('\n')

	def stand(self):
		pass

	def hit(self, hand, deck):
		if hand.hit_limit_on and len(hand.cards) > 2 : 
			raise MovementFail('You could hit only once !!') 
			return False

		hand.cards.append(deck.pop_top_card())
		hand.update_points_stats()
		return True

	def get_initial_hand(self,deck): 
		self.list_of_hands.append(Hand())
		initial_hand = self.list_of_hands[0]
		self.hit(initial_hand,deck)
		self.hit(initial_hand,deck)

	def make_move(self, deck, hand):
		while hand.points_lo < 17 :
			self.hit(hand,deck)
			if hand.points_lo > 21 :
				self.is_busted = True
				self.show_stats()
				return False

		self.show_stats()
		self.stand()
		return True

class Player(Participant):

	def __init__(self):
		self.money = 10000 
		#self.is_busted = False
		self.list_of_hands = []
		self.lost = False

	def show_stats(self):
		for hand in self.list_of_hands:
			print("Hand " + str(self.list_of_hands.index(hand)) + " :")
			print("cards : " + str(hand.cards))
			print("bet : " + str(hand.bet))
			print("busted ? : " + str(hand.is_busted))

		print("money : " + str(self.money))
		print("\n")
	

	def make_bet(self, player_index):
		while(True):

			bet = convert_to_int(input("player {} How much do you want to bet ? \n".format(player_index)))

			if self.money < bet:
				print ( " ERROR : You don't have this much money ! \n")
				continue
			elif bet <= 0:
				print("You can't bet nothing !")
				continue
			else:
				self.money -= bet
				self.list_of_hands[0].bet = bet
				return True

		self.money = self.money - bet

	def double_down(self, hand):
		"""
		 func doubling the bet, after that may take only one hit, Return : bet on doubled hand

		double_down is possible only when len(hand.cards) == 2. 

		INPUT: hand to double
		OUTPUT: Amount of money after double
		"""
		print("DOUBLE_DOWN !!!!!!!!!!!!!\n")
		print(hand)
		if not len(hand.cards) == 2 :
			raise MovementFail("you can't double with more than 2 cards !\n")
			return False #?? Will it run ?

		hand.bet = hand.bet*2
		self.money = self.money - hand.bet
		hand.hit_limit_on = True

		return hand.bet

	def split(self,hand):
		
		"""
		INPUT: hand
		OUTPUT: touple of those cards in separate hands

		split a pair into two hands
		"""

		if not len(hand.cards)  == 2 :

			print("Error, It might be an exception here !\n")
			return False

		if not hand.cards[0] == hand.cards[1]:

			print("Error : You can only split cards if you have pair !\n")
			return False

		if hand.bet > self.money:

			print("You don't have enough money !\n")
			return False

		
		#print(self.list_of_hands[1])


		new_hand = Hand()
		new_hand.cards.append(hand.cards[0])
		new_hand.bet = hand.bet
		self.money = self.money - hand.bet
		hand.cards.pop(0)
		self.list_of_hands.append(new_hand) # LEN list of hands

		hand.update_points_stats()
		new_hand.update_points_stats()

		return {self.list_of_hands[0].cards[0], self.list_of_hands[1].cards[0]}

	def execute_move(self, choosen_move, hand, deck ):
		if choosen_move == "hit":
			self.hit(hand, deck)
			return True
		if choosen_move == "double down" :
			self.double_down(hand)
			return True
		if choosen_move == "split" :
			self.split(hand)
			return True
		if choosen_move == "status" :
			self.show_stats()
			return True

		return False

	def make_move(self, deck, hand, game, test_move_str_override=''): 
		move_str = '' # move place_holder (choosing)

		while not ((move_str == 'stand') or (hand.is_busted)):
			while True :
				if (test_move_str_override != ''):
					move_str = test_move_str_override
				else:
					move_str = input("Your move ? \n")

				try:
					self.execute_move(move_str,hand, deck)
					call(['clear'])
					print("\n")
					game.show_table(self, hand)
					
					break

				except MovementFail:
					print("There is something wrong ! Try again... \n") 
					continue

		if hand.is_busted:
			print("BUSTED !")

		if (test_move_str_override == ''):
			game.press_enter()
		
		call(['clear'])


class Game():

	def __init__(self):
		self.game_end = False
		self.players_number = 0 #should be "Quantity"
		self.all_players = []
		self.croupier = Participant()
		self.deck = Deck()

	def init(self):
		self.players_number = int(input("How many players will play ? \n"))
		for player in range(self.players_number): 
			self.all_players.append(Player()) # create players
			self.deck.shuffle()

	def kick_bancrupt_players(self):
		self.all_players = [x for x in self.all_players if x.lost == False] # It  take all players that didn't lose.
		if not self.all_players : 
			self.game_end = True

			return self.all_players


	def prize_for(self,player,hand):
		player.money += 2*hand.bet 
		hand.bet = 0

		return player.money

	def remove_bet(self,player,hand):
		hand.bet = 0
		if player.money == 0:
			player.lost = True

	def manage_bets_after_deal(self): # need to iterate through hand  | check who wins >> Give them prize stack, remove bet stack from all players
		if self.croupier.is_busted: # IF Croupier busted >> prize all not-busted hands.
			for player in self.all_players:	
				for hand in player.list_of_hands:
					if  not hand.is_busted:
						self.prize_for(player,hand)
						print("player " + str(self.all_players.index(player)) + " WON")



		for player in self.all_players:
			for hand in player.list_of_hands:
				if not hand.is_busted and hand.preferable_points > self.croupier.list_of_hands[0].preferable_points:
					self.prize_for(player,hand)
					print("player " + str(self.all_players.index(player)) + " WON")

		for player in self.all_players: # Can be optimalised by rewriting in Hand Class
			for hand in player.list_of_hands:
				self.remove_bet(player,hand)

	def show_table(self,active_player ,active_hand ): # make those last two fairly optional
		def player_labels(): #constructing the output line by line
			spacingg = 50

			active_player_index = self.all_players.index(active_player)
			active_hand_index = active_player.list_of_hands.index(active_hand)

			player_labels = ''
			money_string = ''
			hands_cards_string = ''
			indicator = '>>' #indicator

			count_of_hands = [] # how many hands have each  player ? 
			
			for player in self.all_players: 
				index = self.all_players.index(player)

				
				if active_player_index == index :
					current_string_players = indicator + "player " + str(index) + ' :'
				else:
					current_string_players = "player " + str(index) + ' :'

				player_labels += '{:<{spacing}}'.format(current_string_players, spacing = spacingg)
				current_string_money = "money : " + str(player.money)
				money_string += '{:<{spacing}}'.format(current_string_money, spacing = spacingg)

				player_labels = '{:<{spacing}}'.format(player_labels, spacing = spacingg)
				money_string = '{:<{spacing}}'.format(money_string, spacing = spacingg)

				
				count_of_hands.append(len(player.list_of_hands))
				max_number_of_hands = max(count_of_hands)

				print(max_number_of_hands) # DEBUUUUUGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG 

			for hand_index in range(max_number_of_hands):	
				for player in self.all_players: 

					player_index = self.all_players.index(player)

					if active_hand_index == hand_index and active_player_index == player_index :
						current_string_hands = indicator + "hand " + str(hand_index) +' : ' + str(player.list_of_hands[hand_index].cards) + ' | ' + str(player.list_of_hands[hand_index].bet)
					else:# len(player.list_of_hands) >= hand_index:
						
						current_string_hands = "hand " + str(hand_index) +' : ' + str(player.list_of_hands[hand_index].cards) + ' | ' + str(player.list_of_hands[hand_index].bet)


					
					hands_cards_string += '{:<{spacing}}'.format(current_string_hands, spacing = spacingg) # generator needed ?  
					hands_cards_string = '{:<{spacing}}'.format(hands_cards_string, spacing = spacingg)

				hands_cards_string += '\n'
			
			lines_dict = {'players':player_labels, 'money':money_string, 'hands':hands_cards_string }

			return lines_dict

		print('\n' + 20*'*')
		print("{:^20}".format('TABLE'))
		print(" Croupier : ")
		print("Cards : " + str(self.croupier.list_of_hands[0].cards))
		print('\n\n')


		print(player_labels()['players'])
		print(player_labels()['money']) 
		print(player_labels()['hands'])

		print('\n\n')

	def press_enter(self):
		any_input = input("{:^60}".format('========  PRESS ENTER  ========='))

	def clear_hands(self):
		for player in self.all_players:
			player.list_of_hands = []

		self.croupier.list_of_hands = []


		# NEW CLASS -->  "Game" with general rules functions
		# test new functions !! (GAME CLASS)



