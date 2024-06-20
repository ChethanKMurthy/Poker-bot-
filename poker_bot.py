import random
from itertools import combinations

# Define constants for suits and ranks
SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

# Function to create a deck of cards
def create_deck():
    """
    Creates a standard deck of 52 cards.
    
    Returns:
        list: List of tuples representing each card in the deck (suit, rank).
    """
    return [(suit, rank) for suit in SUITS for rank in RANKS]

# Function to evaluate the strength of a hand (placeholder function)
def evaluate_hand(hand):
    """
    Placeholder function to evaluate the strength of a poker hand.
    Actual implementation depends on specific hand evaluation logic.

    Args:
        hand (list): List of tuples representing cards in the hand.

    Returns:
        tuple: A tuple containing the name of the hand (e.g., "Pair") and a score (float) representing hand strength.
    """
    return "High card", 0.0  # Placeholder return values

# Function to calculate win probability based on current game state
def calculate_win_probability(your_cards, community_cards, num_simulations=1000):
    """
    Calculates the estimated win probability of a player's hand against random opponent hands
    using Monte Carlo simulation.

    Args:
        your_cards (list): List of tuples representing player's hole cards.
        community_cards (list): List of tuples representing community cards.
        num_simulations (int): Number of Monte Carlo simulations to run.

    Returns:
        float: Estimated win probability as a decimal between 0 and 1.
    """
    deck = create_deck()
    
    # Remove known cards (player's and community's) from the deck
    for card in your_cards + community_cards:
        deck.remove(card)

    your_hand = your_cards + community_cards
    opponent_hands = list(combinations(deck, 2))
    wins = 0

    # Run simulations
    for _ in range(num_simulations):
        random.shuffle(deck)
        remaining_community_cards = deck[:5 - len(community_cards)]
        
        # Compare player's hand against each opponent hand
        for opponent_hand in opponent_hands:
            opponent_full_hand = list(opponent_hand) + remaining_community_cards
            _, your_score = evaluate_hand(your_hand + remaining_community_cards)
            _, opponent_score = evaluate_hand(opponent_full_hand)
            
            # If player's hand is stronger, count it as a win
            if your_score > opponent_score:
                wins += 1
                break  # No need to check further if player already wins this simulation

    win_probability = wins / num_simulations
    return win_probability

# Function to get user input for cards
def get_user_cards():
    """
    Prompts the user to input their hole cards.

    Returns:
        list: List of tuples representing player's hole cards.
    """
    your_cards = []
    print("Enter your hole cards (e.g., 'Ah' for Ace of Hearts):")
    for _ in range(2):
        while True:
            card_str = input(f"Card {_ + 1}: ").strip().upper()
            
            # Validate input format
            if len(card_str) != 2:
                print("Invalid input. Please enter in format like 'Ah' for Ace of Hearts.")
                continue
            
            suit = card_str[1]
            rank = card_str[0]
            
            # Validate card values
            if suit not in ['H', 'D', 'C', 'S'] or rank not in RANKS:
                print("Invalid input. Please enter valid card values.")
                continue
            
            # Convert suit abbreviation to full name
            suit_name = {'H': 'Hearts', 'D': 'Diamonds', 'C': 'Clubs', 'S': 'Spades'}[suit]
            your_cards.append((suit_name, rank))
            break
    
    return your_cards

# Function to get user input for community cards
def get_community_cards():
    """
    Prompts the user to input community cards.

    Returns:
        list: List of tuples representing community cards.
    """
    community_cards = []
    print("\nEnter community cards (press enter for each card):")
    
    # Assuming up to 5 community cards can be entered
    for i in range(5):  # Adjust this loop for more community cards if needed
        while True:
            card_str = input(f"Community Card {i + 1}: ").strip().upper()
            
            # If user presses enter without entering a card, break loop
            if card_str == "":
                break
            
            # Validate input format
            if len(card_str) != 2:
                print("Invalid input. Please enter in format like 'Ah' for Ace of Hearts.")
                continue
            
            suit = card_str[1]
            rank = card_str[0]
            
            # Validate card values
            if suit not in ['H', 'D', 'C', 'S'] or rank not in RANKS:
                print("Invalid input. Please enter valid card values.")
                continue
            
            # Convert suit abbreviation to full name
            suit_name = {'H': 'Hearts', 'D': 'Diamonds', 'C': 'Clubs', 'S': 'Spades'}[suit]
            community_cards.append((suit_name, rank))
            break
    
    return community_cards

# Main function to run the poker bot
def main():
    """
    Main function to execute the Texas Hold'em Poker Bot.
    """
    print("Welcome to the Texas Hold'em Poker Bot!")
    
    # Get user's hole cards and community cards
    your_cards = get_user_cards()
    community_cards = get_community_cards()

    # Display user's and community cards
    print("\nYour hole cards:", your_cards)
    print("Community cards:", community_cards)

    # Calculate and display win probability
    win_prob = calculate_win_probability(your_cards, community_cards)
    print(f"\nEstimated win probability: {win_prob:.2%}")

# Entry point of the script
if __name__ == "__main__":
    main()
