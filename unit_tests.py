##BlackJack Game : Unit Tests
# By Nikodem Celiński 

# file created : 13:38 | 21.09.18 

import unittest
import black_jack_classes
import func_for_unittest 


def check_if_shuffled(deck):
	model_deck = black_jack_classes.Deck()
	i = 0
	is_different = False
	for card in deck.cards:
		if model_deck.cards[i] != card :
			is_different = True
			break
		i+=1

	if i<26 :
		print("probably shuffled ! ")
		return True

	else : 
		print("Probably not shuffled. Check again ! ")
		return False



class DeckTest(unittest.TestCase):

	def test_cards_range(self):
		deck = black_jack_classes.Deck()
		func_output = len(deck.cards)

		print ("LENGTH OF CARDS : {} \n".format(func_output) )

		self. assertEqual(func_output, 52 )

	def test_poping_deck(self):
		deck = black_jack_classes.Deck()
		card_popped = deck.cards[0]
		func_output = deck.pop_top_card()

		self.assertEqual(func_output, card_popped)


	def test_shuffle(self):
		deck = black_jack_classes.Deck()
		deck.shuffle()
		check_if_shuffled(deck)
		self.assertEqual(check_if_shuffled(deck), True)


class HandTest(unittest.TestCase):
	def test_update(self):
		print("#"*30 + "\n" + "update_testing ..... ")

		hand = black_jack_classes.Hand()
		hand.cards = [8, 8]
		func_output = hand.update_points_stats()
		print(hand)

		self.assertEqual(hand.points_hi, 16)
		self.assertEqual(hand.points_lo, 16)
		self.assertEqual(hand.is_busted, False)

		hand.cards = ['A','A',5]
		func_output = hand.update_points_stats()

		print(hand)

		self.assertEqual(hand.points_hi, 27)
		self.assertEqual(hand.points_lo, 7)
		self.assertEqual(hand.is_busted, False)

		hand.cards = ['K','K',5]
		func_output = hand.update_points_stats()

		print(hand)

		self.assertEqual(hand.points_hi, 25)
		self.assertEqual(hand.points_lo, 25)
		self.assertEqual(hand.is_busted, True)

		print("#"*30 + "\n")

class PlayerTest(unittest.TestCase):

	def test_double_down(self):
		player = black_jack_classes.Player()
		player.list_of_hands.append(black_jack_classes.Hand())
		current_hand = player.list_of_hands[0]

		current_hand.cards.append(10)
		current_hand.cards.append(9)

		player.money = 5000
		
		current_hand.bet = 500
		first_bet=500
		new_bet_on_hand = player.double_down(current_hand)

		self.assertEqual(new_bet_on_hand,first_bet*2)
		self.assertEqual(player.money, 4000)


	def test_split(self):
		player2 = black_jack_classes.Player()
		player2.money = 3000

		player2.list_of_hands.append(black_jack_classes.Hand())
		old_hand = player2.list_of_hands[0]
		old_hand.cards = [8,8]
		old_hand.bet = 500
		new_hands_touple = {8,8}

		func_output = player2.split(old_hand)

		self.assertEqual(func_output, new_hands_touple)
		self.assertEqual(len(player2.list_of_hands), 2)

	def test_make_move(self):

		game = black_jack_classes.Game()
		player = black_jack_classes.Player()
		player.list_of_hands.append(black_jack_classes.Hand())
		

		game.all_players.append(player)
		hand = game.all_players[0].list_of_hands[0]
		game.croupier = func_for_unittest.croupier_init(game, ['D',9])
		
		hand.cards = [8,8]

		print ("LENGTH OF CARDS : {} \n".format(len(game.deck.cards)) )


		print(hand)

		print("TEST MAKE MOVE ")
		func_output = player.make_move(game.deck, hand, game, test_move_str_override="stand")


		print("="*50)
		print("\n")
		print("END RESULT OF MOVES : \n")
		print("\n")


		for hand in player.list_of_hands :
			print("\n")
			print(hand)
			print("\n")

		print('='*50)

	def test_croupier_make_move(self):
		print("%"*30 + " CROUPIER_MOVES !")


		croupier = black_jack_classes.Participant()
		deck = black_jack_classes.Deck()
		deck.shuffle()
		croupier.get_initial_hand(deck)
		hand = croupier.list_of_hands[0]
		func_output = croupier.make_move(deck,hand)

		print(hand)

		self.assertEqual(not hand.is_busted, func_output)

		print("%"*30)

class GameTest(unittest.TestCase): 
	def test_prize_for(self):
		player_initial_money = 1000
		player_bet = 500
		game = black_jack_classes.Game()
		player = func_for_unittest.player_init( player_initial_money, [ func_for_unittest.hand_init(['A',8],player_bet) ] )
		
		output = game.prize_for(player,player.list_of_hands[0])

		self.assertEqual(player_bet*2 + player_initial_money, output)

 
	def test_show_table(self):  
		game = black_jack_classes.Game()
		deck = black_jack_classes.Deck()
		hand_p8 = func_for_unittest.hand_init([8,8],0)
		hand_p9 = func_for_unittest.hand_init([9,9],0)
		


		croupier = func_for_unittest.croupier_init(game,['D',10])
		player_9 = func_for_unittest.player_init(300,[hand_p9])
		player_8 = func_for_unittest.player_init(300,[hand_p8])

		game.all_players.append(player_8)
		game.all_players.append(player_9)

		player_8.make_move(deck, player_8.list_of_hands[0], game, test_move_str_override="stand")

		game.show_table(game.all_players[0], game.all_players[0].list_of_hands[0]) # Are those args different objects ? 


if __name__ == '__main__':
	unittest.main()

