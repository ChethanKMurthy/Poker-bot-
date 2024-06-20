import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
import random
from itertools import combinations

# Define constants for suits and ranks
SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

# Function to create a deck of cards
def create_deck():
    return [(suit, rank) for suit in SUITS for rank in RANKS]

# Function to evaluate the strength of a hand (placeholder function)
def evaluate_hand(hand):
    return "High card", 0.0  # Placeholder return values

# Function to calculate win probability based on current game state
def calculate_win_probability(your_cards, community_cards, num_simulations=1000):
    deck = create_deck()
    for card in your_cards + community_cards:
        deck.remove(card)  # Remove known cards from the deck

    your_hand = your_cards + community_cards
    opponent_hands = list(combinations(deck, 2))
    wins = 0

    for _ in range(num_simulations):
        random.shuffle(deck)
        remaining_community_cards = deck[:5 - len(community_cards)]
        for opponent_hand in opponent_hands:
            opponent_full_hand = list(opponent_hand) + remaining_community_cards
            _, your_score = evaluate_hand(your_hand + remaining_community_cards)
            _, opponent_score = evaluate_hand(opponent_full_hand)
            if your_score > opponent_score:
                wins += 1
                break  # No need to check further if you already win this simulation

    win_probability = wins / num_simulations
    return win_probability

# GUI setup
class PokerBotGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Texas Hold'em Poker Bot")
        
        self.your_cards = []
        self.community_cards = []
        
        # Label and Entry for hole cards
        self.label_hole_cards = tk.Label(master, text="Enter your hole cards (e.g., 'Ah' for Ace of Hearts):")
        self.label_hole_cards.pack()
        
        self.entry_hole_card1 = tk.Entry(master, width=5)
        self.entry_hole_card1.pack()
        
        self.entry_hole_card2 = tk.Entry(master, width=5)
        self.entry_hole_card2.pack()
        
        # Button to submit hole cards
        self.submit_hole_cards_button = tk.Button(master, text="Submit Hole Cards", command=self.submit_hole_cards)
        self.submit_hole_cards_button.pack()
        
        # Label and Entry for community cards
        self.label_community_cards = tk.Label(master, text="Enter community cards (press enter for each card):")
        self.label_community_cards.pack()
        
        self.scrolled_text = scrolledtext.ScrolledText(master, width=40, height=5)
        self.scrolled_text.pack()
        
        # Button to submit community cards
        self.submit_community_cards_button = tk.Button(master, text="Submit Community Cards", command=self.submit_community_cards)
        self.submit_community_cards_button.pack()
        
        # Text area to display result
        self.result_text = tk.Text(master, width=40, height=2, state='disabled')
        self.result_text.pack()
        
        # Button to calculate win probability
        self.calculate_button = tk.Button(master, text="Calculate Win Probability", command=self.calculate_win_probability)
        self.calculate_button.pack()

    def submit_hole_cards(self):
        card1 = self.entry_hole_card1.get().strip().upper()
        card2 = self.entry_hole_card2.get().strip().upper()
        
        if len(card1) != 2 or len(card2) != 2 or card1[1] not in ['H', 'D', 'C', 'S'] or card2[1] not in ['H', 'D', 'C', 'S'] or card1[0] not in RANKS or card2[0] not in RANKS:
            messagebox.showerror("Error", "Invalid input. Please enter in format like 'Ah' for Ace of Hearts.")
            return
        
        self.your_cards = [(self.get_suit_name(card1[1]), card1[0]), (self.get_suit_name(card2[1]), card2[0])]
        self.result_text.config(state='normal')
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert(tk.END, f"Your hole cards: {self.your_cards}")
        self.result_text.config(state='disabled')
    
    def submit_community_cards(self):
        community_cards_text = self.scrolled_text.get('1.0', tk.END).strip()
        community_cards_input = community_cards_text.split('\n')
        self.community_cards = []
        
        for card in community_cards_input:
            if card.strip() == '':
                continue
            self.community_cards.append((self.get_suit_name(card[1]), card[0]))
        
        self.result_text.config(state='normal')
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert(tk.END, f"Community cards: {self.community_cards}")
        self.result_text.config(state='disabled')
    
    def calculate_win_probability(self):
        if not self.your_cards or not self.community_cards:
            messagebox.showerror("Error", "Please enter your hole cards and community cards first.")
            return
        
        win_prob = calculate_win_probability(self.your_cards, self.community_cards)
        self.result_text.config(state='normal')
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert(tk.END, f"Estimated win probability: {win_prob:.2%}")
        self.result_text.config(state='disabled')
    
    def get_suit_name(self, suit_initial):
        return {'H': 'Hearts', 'D': 'Diamonds', 'C': 'Clubs', 'S': 'Spades'}[suit_initial]

# Main function to run the GUI
def main():
    root = tk.Tk()
    poker_bot_gui = PokerBotGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
