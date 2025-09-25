import random
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Klasse für eine Karte
class Card:
    def __init__(self, farbe, name):
        self.farbe = farbe  # Farbe der Karte (Herz, Pik, Kreuz, Karo)
        self.name = name    # Name der Karte (2-10, J, Q, K, A)

    def __str__(self):
        return f'{self.name} {self.farbe}'

    # Gibt den Pfad zum Bild der Karte zurück
    def get_image_path(self):
        return f'cards/{self.name}{self.farbe}.png'

# Klasse für das Deck
class Deck:
    farbes = ['Herz', 'Pik', 'Kreuz', 'Karo']
    names = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

    def __init__(self):
        # Erzeugt alle Kartenkombinationen und mischt das Deck
        self.cards = [Card(farbe, name) for farbe in self.farbes for name in self.names]
        random.shuffle(self.cards)

    # Gibt die oberste Karte zurück und entfernt sie aus dem Deck
    def deal(self):
        return self.cards.pop()

# Klasse für einen Spieler
class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []       # Handkarten des Spielers
        self.balance = 400   # Startguthaben
        self.bet = 0         # Aktueller Einsatz

    # Fügt eine Karte zur Hand hinzu
    def add_card(self, card):
        self.hand.append(card)

    # Berechnet die Punktzahl der Hand
    def calculate_score(self):
        score = 0
        ace_found = False  # Flagge für das erste Ass

        for card in self.hand:
            if card.name.isdigit():          # Zahlenkarten
                score += int(card.name)
            elif card.name in ['J', 'Q', 'K']:  # Bildkarten
                score += 10
            elif card.name == 'A':           # Ass
                if not ace_found:
                    score += 11
                    ace_found = True
                else:
                    score += 11  # Wird ggf. später auf 1 reduziert

        # Wenn Punktzahl > 21 und ein Ass vorhanden ist, Ass als 1 zählen
        if score > 21 and ace_found:
            score -= 10
        return score

# GUI-Klasse für das Blackjack-Spiel
class BlackjackGameGUI:
    def __init__(self, windows):
        self.windows = windows
        self.windows.title("Black Jack")
        self.windows.minsize(1000, 750)
        self.windows.maxsize(1000, 750)

        # Hintergrundbild laden
        self.bg_image = Image.open('background.jpg').resize((1000, 750))
        self.bg_image = ImageTk.PhotoImage(self.bg_image)
        self.bg_label = tk.Label(self.windows, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Bild für verdeckte Karte
        self.hidden_card_image = Image.open('cards/deck.png').resize((80, 120))
        self.hidden_card_image = ImageTk.PhotoImage(self.hidden_card_image)

        # Initialisierung von Deck und Spielern
        self.deck = Deck()
        self.dealer = Player('Dealer')
        self.player = Player('Player')

        # GUI-Frames für Dealer und Spieler
        self.dealer_frame = tk.Frame(self.windows)
        self.dealer_frame.pack(pady=110)
        self.player_frame = tk.Frame(self.windows)
        self.player_frame.pack()

        # Anzeige der Punkte des Spielers
        self.player_score = tk.Label(self.windows, text="Punkte in der Hand", font=("Cooper Black", 12), bg="darkolivegreen")
        self.player_score.pack(pady=10)

        # Anzeige des Guthabens
        self.balance_label = tk.Label(self.windows, text=f"Balance {self.player.balance}", font=("Cooper Black", 12), bg="darkolivegreen")
        self.balance_label.pack()

        # Anzeige des aktuellen Einsatzes
        self.bet_label = tk.Label(self.windows, text="Ihr Einsatz: 0", font=("Cooper Black", 12), bg="darkolivegreen")
        self.bet_label.pack(pady=10)

        # Frame für Einsatz-Buttons
        self.bet_frame = tk.Frame(self.windows)
        self.bet_frame.pack()

        # Einsatz-Buttons erstellen (anfangs deaktiviert)
        for bet_amount in [5, 10, 25, 50, 100]:
            tk.Button(self.bet_frame, state=tk.DISABLED, text=f"EUR {bet_amount}", bg="gold", font=("Cooper Black", 12),
                      command=lambda amt=bet_amount: self.set_bet(amt)).pack(side=tk.LEFT)

        # Button für neue Runde
        self.round_button = tk.Button(self.windows, text="Spiel", font=("Cooper Black", 12), command=self.new_round)
        self.round_button.pack(pady=10)

        # Frame für Steuerungs-Buttons
        self.controls_frame = tk.Frame(self.windows)
        self.controls_frame.pack(pady=10)

        # Hit-Button (Karte ziehen)
        self.hit_button = tk.Button(self.controls_frame, font=("Cooper Black", 12), text="Karte", command=self.player_hit,
                                    bg="darkolivegreen", state=tk.DISABLED)
        self.hit_button.pack(side=tk.LEFT)

        # Stand-Button (Halten)
        self.stand_button = tk.Button(self.controls_frame, font=("Cooper Black", 12), text="Genug", command=self.player_stand,
                                      bg="darkolivegreen", state=tk.DISABLED)
        self.stand_button.pack(side=tk.LEFT)

        # Beenden-Button
        self.quit_button = tk.Button(self.controls_frame, font=("Cooper Black", 12), text="Ausstieg", command=self.quit_game,
                                     bg="red")
        self.quit_button.pack(side=tk.LEFT)

    # Setzt den Einsatz des Spielers
    def set_bet(self, amount):
        if amount <= self.player.balance:
            self.player.bet += amount
            self.player.balance -= amount
            self.balance_label.config(text=f"Balance {self.player.balance}")
            self.bet_label.config(text=f"Ihr Einsatz: {self.player.bet}")
        else:
            messagebox.showwarning("Fehler", "Nicht genügend Geld für diese Wette!")

    # Startet eine neue Runde
    def new_round(self):
        self.player.hand = []
        self.dealer.hand = []
        self.deck = Deck()
        self.player.bet = 0
        self.round_button.config(state=tk.NORMAL)

        if self.player.balance == 0:
            messagebox.showinfo("Game over", "Sie haben kein Geld mehr! Das Spiel ist vorbei. Versuchen Sie noch einmal zu spielen!")
            self.player.balance = 400
            self.balance_label.config(text=f"Balance: {self.player.balance}")
            self.new_round()
            return

        # Aktivieren der Buttons für die Runde
        self.hit_button.config(state=tk.NORMAL)
        self.stand_button.config(state=tk.NORMAL)
        self.round_button.config(state=tk.DISABLED)

        for widget in self.bet_frame.winfo_children():  # Aktivierung der Einsätze
            widget.config(state=tk.NORMAL)

        # Zwei Karten für Spieler und Dealer
        self.player.add_card(self.deck.deal())
        self.player.add_card(self.deck.deal())
        self.dealer.add_card(self.deck.deal())
        self.dealer.add_card(self.deck.deal())

        # GUI aktualisieren
        self.player_score.config(text=f"Punkte in der Hand: {self.player.calculate_score()}")
        self.update_gui()

    # Aktualisiert die GUI (Handkarten anzeigen)
    def update_gui(self, reveal_dealer_card=False):
        for widget in self.player_frame.winfo_children():
            widget.destroy()
        for widget in self.dealer_frame.winfo_children():
            widget.destroy()

        # Dealer-Karten (erste verdeckt, wenn reveal_dealer_card=False)
        for i, card in enumerate(self.dealer.hand):
            if i == 0 and not reveal_dealer_card:
                card_label = tk.Label(self.dealer_frame, image=self.hidden_card_image)
            else:
                image = Image.open(card.get_image_path()).resize((80, 120))
                card_image = ImageTk.PhotoImage(image)
                card_label = tk.Label(self.dealer_frame, image=card_image)
                card_label.image = card_image
            card_label.pack(side=tk.LEFT)

        # Spieler-Karten
        for card in self.player.hand:
            image = Image.open(card.get_image_path()).resize((80, 120))
            card_image = ImageTk.PhotoImage(image)
            card_label = tk.Label(self.player_frame, image=card_image)
            card_label.image = card_image
            card_label.pack(side=tk.LEFT)

    # Spieler zieht eine Karte
    def player_hit(self):
        self.player.add_card(self.deck.deal())
        self.update_gui()
        self.player_score.config(text=f"Punkte in der Hand {self.player.calculate_score()}")

        if self.player.calculate_score() > 21:
            self.end_game("Spieler ist pleite!! Punkte in der Hand > 21 ")
            self.player.bet = 0
            self.bet_label.config(text=f"Ihr Einsatz: {self.player.bet}")
            self.round_button.config(state=tk.NORMAL)

    # Spieler hält – Dealer zieht Karten
    def player_stand(self):
        while self.dealer.calculate_score() < 17:
            self.dealer.add_card(self.deck.deal())
        self.update_gui()
        self.determine_winner()

    # Ermittelt den Gewinner der Runde
    def determine_winner(self):
        player_score = self.player.calculate_score()
        dealer_score = self.dealer.calculate_score()

        if dealer_score > 21:
            self.end_game(f'Der Händler hat verloren! Ihr Gewinn: {self.player.bet * 2}')
            self.player.balance += self.player.bet * 2
        elif player_score > dealer_score:
            self.end_game(f'Sie haben gewonnen! Ihr Gewinn: {self.player.bet * 2}')
            self.player.balance += self.player.bet * 2
        else:
            self.end_game(f'Der Händler hat gewonnen! Sie haben Ihren Einsatz verloren.')

        # Update GUI Labels nach jeder Runde
        self.balance_label.config(text=f"Balance: {self.player.balance}")
        self.player.bet = 0
        self.bet_label.config(text=f"Ihr Einsatz: {self.player.bet}")
        self.round_button.config(state=tk.NORMAL)

    # Beendet die Runde und zeigt Ergebnis
    def end_game(self, message):
        self.update_gui(reveal_dealer_card=True)
        messagebox.showinfo("Ergebnis", message)
        self.hit_button.config(state=tk.DISABLED)
        self.stand_button.config(state=tk.DISABLED)
        for widget in self.bet_frame.winfo_children():  # Einsätze deaktivieren
            widget.config(state=tk.DISABLED)

    # Beendet das Spiel
    def quit_game(self):
        messagebox.showinfo("Exit", "Danke fürs Mitspielen!")
        self.windows.quit()

# Hauptprogramm starten
windows = tk.Tk()
game = BlackjackGameGUI(windows)
windows.mainloop()
