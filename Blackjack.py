import random

def blackjack(deck, starting_bet, bankroll, max_splits, num_plays, 
              trade_counter, max_loss, min_loss, all_losses, 
              max_gain, min_gain, all_gains, vol, alpha, beta):
  num_decks = 8
  
  shoe = deck * num_decks
  random.shuffle(shoe)
  
  running_total = 0
  cards_dealt = 0
  # Decks remaining = ((num_decks * 52) - cards_dealt) % 52
  # True count = running_count / decks_remaining
  # + (running_count / decks_remaining)
  old_bankroll = bankroll
  round = 1

  print("------ ROUND 1 ------")
  for i in range(num_plays):
    if len(shoe) <= 60:
      print("Shuffling decks...")
      shoe = deck * num_decks
      random.shuffle(shoe)
      running_total = 0
      cards_dealt = 0

    round += 1

    # BET SIZING
    # new_bet is the bet used for the round
    old_bankroll = bankroll
    decks_remaining = ((num_decks * 52) - cards_dealt) // 52
    new_bet = starting_bet + (running_total / decks_remaining) * (starting_bet)
    bets = [new_bet]
    bankroll -= new_bet
    p_hands = []
    d_hand = []
    
    number_of_splits = 0
    for i in range(2):
      new_card = shoe.pop(0)
      p_hands.append(new_card)
      running_total += convert(new_card)
      new_card = shoe.pop(0)
      d_hand.append(new_card)
      running_total += convert(new_card)

    p_hands = [p_hands]
    # Splitting cards if necessary
    while True:
      has_duplicate = False
      for hand in p_hands:
        if hand[0] == hand[1]:
          if calculate_first_strategy(hand[0], hand[1], p_hands[0] == 0, d_hand[0]) == "P" and number_of_splits < max_splits:
            number_of_splits += 1
            has_duplicate = True
            p_hands.remove(hand)

            new_card = shoe.pop(0)
            p_hands.append([hand[0], new_card])
            running_total += convert(new_card)

            new_card = shoe.pop(0)
            p_hands.append([hand[1], new_card])
            running_total += convert(new_card)

            bets.append(new_bet)
            bankroll -= new_bet
      if not has_duplicate or number_of_splits == max_splits:
        break

    print("Dealer Upcard:", d_hand[0])
    i = 0
    for hand in p_hands:
      print("Player's Hands:", p_hands)
      strategy = player_action(hand, d_hand[0])
      if strategy == "S":
        print("Hand:", hand, "Strategy:", strategy)
      while strategy != "S":
        print("Hand:", hand, "Strategy:", strategy)
        if strategy == "S":
          break
        elif strategy == "H":
          new_card = shoe.pop(0)
          hand.append(new_card)
          running_total += convert(new_card)
        elif strategy == "D":
          new_card = shoe.pop(0)
          hand.append(new_card)
          running_total += convert(new_card)
          bankroll -= bets[i]
          bets[i] *= 2
        elif strategy == "DH":
          if bankroll > bets[i]:
            new_card = shoe.pop(0)
            hand.append(new_card)
            running_total += convert(new_card)
            bankroll -= bets[i]
            bets[i] *= 2
          else:
            new_card = shoe.pop(0)
            hand.append(new_card)
            running_total += convert(new_card)
        elif strategy == "DS":
          if bankroll > bets[i]:
            new_card = shoe.pop(0)
            hand.append(new_card)
            running_total += convert(new_card)
            bankroll -= bets[i]
            bets[i] *= 2
          else:
            break
        elif strategy == "P":
          if number_of_splits < max_splits:
            number_of_splits += 1
            p_hands.remove(hand)
            new_card = shoe.pop(0)
            p_hands.append([hand[0], new_card])
            running_total += convert(new_card)

            new_card = shoe.pop(0)
            p_hands.append([hand[1], new_card])
            running_total += convert(new_card)
            bets.append(new_bet)
            bankroll -= new_bet
          else:
            break
        elif strategy == "SUH":
            new_card = shoe.pop(0)
            hand.append(new_card)
            running_total += convert(new_card)
        elif strategy == "SUS":
          break
        elif strategy == "SUP":
          if hand in p_hands and number_of_splits < max_splits:
            number_of_splits += 1
            p_hands.remove(hand)
            new_card = shoe.pop(0)
            p_hands.append([hand[0], new_card])
            running_total += convert(new_card)

            new_card = shoe.pop(0)
            p_hands.append([hand[1], new_card])
            running_total += convert(new_card)
            bets.append(new_bet)
            bankroll -= new_bet
          else:
            break
        strategy = player_action(hand, d_hand[0])
      i += 1
    print("Hands after strategy:", p_hands)

      # Calculate profit, dealer's play
    dealer_total = 0
    dealer_num_aces = 0
    for card in d_hand:
      dealer_total += card
      if card == 0:
        dealer_num_aces += 1
    if dealer_num_aces == 2:
      dealer_total = 12
    elif dealer_num_aces == 1:
      if dealer_total + 11 > 21:
        dealer_total += 1
      else:
        dealer_total += 11
    
    while (dealer_total < 17):
      new_card = shoe.pop(0)
      running_total += convert(new_card)
      d_hand.append(new_card)
      if new_card == 0:
        if dealer_total + 11 > 21:
          dealer_total += 1
        else:
          dealer_total += 11
      else:
        dealer_total += new_card

    print("Dealer hand:", d_hand, "Total:", dealer_total)

    for i in range(len(p_hands)):
      hand = p_hands[i]
      total = 0
      num_aces = 0
      for card in hand:
        total += card
        if card == 0:
          num_aces += 1
      for _ in range(num_aces):
        if total + 11 > 21:
          total += 1
        else:
          total += 11
      
      if total > 21 or total < dealer_total:
        bets[i] = 0
        print("Hand:", hand, "lost.")
      elif dealer_total > 21 or total > dealer_total:
        bets[i] *= 2
        print("Hand:", hand, "won.")
    
    print("Bets:", bets)
    new_bankroll = bankroll
    for bet in bets:
      new_bankroll += bet
    
    print("Profit:", new_bankroll - old_bankroll)
    bankroll = new_bankroll
    print("New Balance:", bankroll)

    if bankroll <= 0:
      print("RAN OUT OF MONEY!")
      return bankroll - old_bankroll

    print("------ ROUND", round, " ------")
  return bankroll - old_bankroll
    
def convert(card):
  if 2 <= card <= 6:
    return 1
  if 7 <= card <= 9:
    return 0
  return -1

def player_action(hand, upcard):
  total = 0
  num_aces = 0
  for card in hand:
    if (card == 0): # Card is ace
      num_aces += 1
    total += card



  if len(hand) == 2:
    # print("Hand:", hand[0], hand[1])

    strategy = calculate_first_strategy(hand[0], hand[1], num_aces, upcard)
  elif len(hand) > 2:
    strategy = calculate_strategy(total, num_aces, upcard)


  return strategy

  
def calculate_first_strategy(first, second, num_aces, upcard):
  if (first == 2 and second == 2) or (first == 3 and second == 3):
    if 2 <= upcard <= 7:
      return "P"
    else:
      return "H"
  if first == 4 and second == 4:
    if 5 <= upcard <= 6:
      return "P"
    else:
      return "H"
  if first == 5 and second == 5:
    if 2 <= upcard <= 9:
      return "DH"
    else:
      return "H"
  if first == 6 and second == 6:
    if 2 <= upcard <= 6:
      return "P"
    else:
      return "H"
  if first == 7 and second == 7:
    if 2 <= upcard <= 7:
      return "P"
    else:
      return "H"
  if first == 8 and second == 8:
    if upcard == 0:
      return "SUP"
    else:
      return "P"
  if first == 9 and second == 9:
    if upcard == 7 or upcard == 10 or upcard == 0:
      return "S"
    else:
      return "P"
  if first == 10 and second == 10:
    return "S"
  if first == 0 and second == 0:
    return "P"
  
  total = first + second
  return calculate_strategy(total, num_aces, upcard)
  

def calculate_strategy(total, num_aces, upcard):
  if num_aces == 0:
    if 5 <= total <= 8:
      return "H"
    if total == 9:
      if upcard == 2 or 7 <= upcard <= 10 or upcard == 0:
        return "H"
      else:
        return "DH"
    if total == 10:
      if 2 <= upcard <= 9:
        return "DH"
      else:
        return "H"
    if total == 11:
      return "DH"
    if total == 12:
      if 4 <= upcard <= 6:
        return "S"
      else:
        return "H"
    if 13 <= total <= 14:
      if 2 <= upcard <= 6:
        return "S"
      else:
        return "H"
    if total == 15:
      if 2 <= upcard <= 6:
        return "S"
      if 7 <= upcard <= 9:
        return "H"
      else:
        return "SUH"
    if total == 16:
      if 2 <= upcard <= 6:
        return "S"
      if 7 <= upcard <= 8:
        return "H"
      else:
        return "SUH"
    if total == 17:
      if 2 <= upcard <= 10:
        return "S"
      else:
        return "SUS"
  else:
    if 2 <= total <= 3:
      if 5 <= upcard <= 6:
        return "DH"
      else:
        return "H"
    if 4 <= total <= 5:
      if 4 <= upcard <= 6:
        return "DH"
      else:
        return "H"
    if total == 6:
      if 3 <= upcard <= 6:
        return "DH"
      else:
        return "H"
    if total == 7:
      if 2 <= upcard <= 6:
        return "DS"
      if 7 <= upcard <= 8:
        return "S"
      else:
        return "H"
    if total == 8:
      if upcard == 6:
        return "DS"
      else:
        return "S"
    if total == 9:
      return "S"

  return "S"

def card_count(count, p_card, d_card):
  return count

ranks = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
suits = ["S", "D", "H", "C"]
deck = []
for suit in suits:
  for rank in ranks:
    deck.append(rank)


'''
deck, starting_bet, bankroll, max_splits, num_plays, 
              trade_counter, max_loss, min_loss, all_losses, 
              max_gain, min_gain, all_gains, vol, alpha, beta
'''
total = 0
for _ in range(100):
    total += blackjack(deck, 1, 1000, 3, 10000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
print(total / 100)
