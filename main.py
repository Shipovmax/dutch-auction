import random
import time
import os
import sys
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime


class Colors:
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"


@dataclass
class Product:
    id: int
    name: str
    quantity: int
    start_price: int
    current_price: int
    cost: int
    description: str


@dataclass
class Player:
    name: str
    balance: int
    total_profit: int
    purchases: int
    wants: str
    dislikes: str


class DutchAuctionGame:

    def __init__(self):
        self.products = self._create_products()
        self.players = self._create_players()
        self.current_round = 0
        self.current_product = None
        self.game_active = False
        self.user_player = None

    def _create_products(self) -> List[Product]:
        products = [
            Product(
                1, "🌹 Roses", 50, 15000, 15000, 8000, "Red roses, a symbol of love"
            ),
            Product(2, "🌻 Sunflowers", 30, 8000, 8000, 4000, "Bright sunflowers"),
            Product(3, "🌺 Orchids", 20, 25000, 25000, 12000, "Exotic orchids"),
            Product(4, "🌷 Tulips", 40, 12000, 12000, 6000, "Spring tulips"),
            Product(5, "🌸 Sakura", 15, 30000, 30000, 15000, "Blooming sakura"),
            Product(6, "🌼 Daisies", 60, 5000, 5000, 2500, "Simple daisies"),
            Product(7, "🌿 Lavender", 35, 10000, 10000, 5000, "Fragrant lavender"),
            Product(8, "🌺 Peonies", 25, 18000, 18000, 9000, "Lush peonies"),
            Product(9, "🌻 Dahlias", 30, 14000, 14000, 7000, "Large dahlias"),
            Product(10, "🌷 Irises", 40, 11000, 11000, 5500, "Elegant irises"),
            Product(11, "🌹 Carnations", 45, 9000, 9000, 4500, "Classic carnations"),
            Product(12, "🌺 Lilies", 20, 20000, 20000, 10000, "White lilies"),
        ]
        return products

    def _create_players(self) -> List[Player]:
        players = [
            Player("Ivan", 150000, 0, 0, "Peonies", "Roses"),
            Player("Anastasia", 280000, 0, 0, "Roses", "Peonies"),
            Player("Igor", 200000, 0, 0, "Orchids", "Daisies"),
            Player("Marina", 120000, 0, 0, "Tulips", "Dahlias"),
            Player("Dmitry", 300000, 0, 0, "Lavender", "Lilies"),
            Player("Svetlana", 175000, 0, 0, "Irises", "Carnations"),
        ]
        return players

    def create_user_player(self, name: str) -> Player:
        self.user_player = Player(name, 200000, 0, 0, "Roses", "Orchids")
        return self.user_player

    def start_new_round(self) -> bool:
        if not self.products:
            return False

        self.current_round += 1

        self.current_product = random.choice(self.products)
        self.current_product.current_price = self.current_product.start_price
        self.game_active = True

        return True

    def decrease_price(self, amount: int = 1000) -> bool:
        if not self.current_product or not self.game_active:
            return False

        self.current_product.current_price -= amount

        if self.current_product.current_price <= self.current_product.cost:
            self.current_product.current_price = self.current_product.cost
            return False

        return True

    def buy_product(self, player: Player) -> bool:
        if not self.current_product or not self.game_active:
            return False

        if player.balance < self.current_product.current_price:
            return False

        player.balance -= self.current_product.current_price
        profit_multiplier = 1.3
        profit = self.current_product.current_price * profit_multiplier
        player.total_profit += profit
        player.purchases += 1

        self.current_product.quantity -= 1

        if self.current_product.quantity <= 0:
            self.products.remove(self.current_product)

        self.game_active = False
        return True

    def get_ai_decision(self, player: Player) -> bool:
        if not self.current_product:
            return False

        can_afford = player.balance >= self.current_product.current_price
        good_price = (
            self.current_product.current_price <= self.current_product.start_price * 0.7
        )

        likes_product = player.wants.lower() in self.current_product.name.lower()
        dislikes_product = player.dislikes.lower() in self.current_product.name.lower()
        buy_probability = 0.1

        if can_afford:
            buy_probability += 0.3
        if good_price:
            buy_probability += 0.2
        if likes_product:
            buy_probability += 0.3
        if dislikes_product:
            buy_probability -= 0.2

        return random.random() < buy_probability

    def format_money(self, amount: int) -> str:
        return f"{amount:,} ₽"

    def clear_screen(self):
        os.system("cls" if os.name == "nt" else "clear")

    def print_header(self):
        print(f"{Colors.BOLD}{Colors.PURPLE}")
        print("=" * 60)
        print("🔥 GOLAN DUTCH AUCTION - CONSOLE EDITION 🔥")
        print("=" * 60)
        print(f"{Colors.END}")

    def print_player_info(self, player: Player):
        print(f"{Colors.CYAN}👤 {player.name}{Colors.END}")
        print(
            f"   💰 Balance: {Colors.GREEN}{self.format_money(player.balance)}{Colors.END}"
        )
        print(
            f"   📈 Profit: {Colors.BLUE}{self.format_money(player.total_profit)}{Colors.END}"
        )
        print(f"   🛒 Purchases: {Colors.YELLOW}{player.purchases}{Colors.END}")
        print(f"   ❤️  Likes: {Colors.RED}{player.wants}{Colors.END}")
        print(f"   💔 Dislikes: {Colors.RED}{player.dislikes}{Colors.END}")
        print()

    def print_product_info(self):
        if not self.current_product:
            return

        print(f"{Colors.BOLD}{Colors.YELLOW}💎 CURRENT LOT{Colors.END}")
        print(f"   🌸 Product: {Colors.BOLD}{self.current_product.name}{Colors.END}")
        print(
            f"   📦 Quantity: {Colors.CYAN}{self.current_product.quantity} pcs.{Colors.END}"
        )
        print(
            f"   💰 Current price: {Colors.GREEN}{self.format_money(self.current_product.current_price)}{Colors.END}"
        )
        print(
            f"   💸 Cost basis: {Colors.RED}{self.format_money(self.current_product.cost)}{Colors.END}"
        )
        potential_profit = (
            self.current_product.cost - self.current_product.current_price
        )
        profit_color = Colors.GREEN if potential_profit >= 0 else Colors.RED
        profit_sign = "+" if potential_profit >= 0 else ""
        print(
            f"   📈 Potential profit: {profit_color}{profit_sign}{self.format_money(potential_profit)}{Colors.END}"
        )
        print(f"   💡 Profit = Purchase price × 1.3 (130%)")
        print(f"   📝 Description: {self.current_product.description}")
        print()

    def print_leaderboard(self):
        sorted_players = sorted(
            self.players + ([self.user_player] if self.user_player else []),
            key=lambda p: p.total_profit,
            reverse=True,
        )

        print(f"{Colors.BOLD}{Colors.PURPLE}🏆 LEADERBOARD{Colors.END}")
        print("-" * 50)
        for i, player in enumerate(sorted_players, 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            profit_color = Colors.GREEN if player.total_profit >= 0 else Colors.RED
            profit_sign = "+" if player.total_profit >= 0 else ""
            print(
                f"{medal} {player.name}: {profit_color}{profit_sign}{self.format_money(player.total_profit)}{Colors.END}"
            )
        print()

    def run_game(self):
        self.clear_screen()
        self.print_header()

        print(f"{Colors.CYAN}Welcome to the Dutch Auction!{Colors.END}")
        user_name = input(f"{Colors.YELLOW}Enter your name: {Colors.END}").strip()
        if not user_name:
            user_name = "Player"

        self.create_user_player(user_name)

        print(
            f"\n{Colors.GREEN}Hello, {user_name}! You have {self.format_money(self.user_player.balance)}{Colors.END}"
        )
        input(f"{Colors.YELLOW}Press Enter to start the game...{Colors.END}")

        round_count = 0
        max_rounds = 10

        while round_count < max_rounds and self.products:
            self.clear_screen()
            self.print_header()

            if not self.start_new_round():
                break

            round_count += 1
            print(f"{Colors.BOLD}Round {round_count}/{max_rounds}{Colors.END}\n")

            self.print_product_info()

            print(f"{Colors.BOLD}YOUR PROFILE{Colors.END}")
            self.print_player_info(self.user_player)

            auction_active = True
            price_decrease_count = 0

            while auction_active and self.current_product:
                print(
                    f"{Colors.BOLD}💰 Current price: {Colors.GREEN}{self.format_money(self.current_product.current_price)}{Colors.END}"
                )

                print(f"\n{Colors.YELLOW}Your actions:{Colors.END}")
                print("1. 🛒 Buy the product")
                print("2. ⏳ Wait for a price drop")
                print("3. 📊 Show the leaderboard")
                print("4. ❌ Skip the round")

                choice = input(
                    f"\n{Colors.CYAN}Choose an action (1-4): {Colors.END}"
                ).strip()

                if choice == "1":
                    if self.buy_product(self.user_player):
                        print(
                            f"\n{Colors.GREEN}🎉 Congratulations! You bought {self.current_product.name} for {self.format_money(self.current_product.current_price)}!{Colors.END}"
                        )
                        profit = (
                            self.current_product.cost
                            - self.current_product.current_price
                        )
                        print(
                            f"{Colors.BLUE}💰 Your profit: {self.format_money(profit)}{Colors.END}"
                        )
                        auction_active = False
                    else:
                        print(f"\n{Colors.RED}❌ Insufficient funds!{Colors.END}")

                elif choice == "2":
                    if self.decrease_price():
                        print(f"\n{Colors.YELLOW}⏳ The price is dropping...{Colors.END}")
                        price_decrease_count += 1

                        for player in self.players:
                            if self.get_ai_decision(player) and self.buy_product(
                                player
                            ):
                                print(
                                    f"{Colors.CYAN}🤖 {player.name} bought the product!{Colors.END}"
                                )
                                auction_active = False
                                break
                    else:
                        print(f"\n{Colors.RED}❌ The price reached its minimum!{Colors.END}")
                        auction_active = False

                elif choice == "3":
                    self.print_leaderboard()
                    input(
                        f"{Colors.YELLOW}Press Enter to continue...{Colors.END}"
                    )

                elif choice == "4":
                    print(f"\n{Colors.YELLOW}⏭️ Round skipped{Colors.END}")
                    auction_active = False

                else:
                    print(f"\n{Colors.RED}❌ Invalid choice!{Colors.END}")

                if auction_active:
                    time.sleep(0.5)

            if not auction_active:
                print(f"\n{Colors.BOLD}📊 Round result:{Colors.END}")
                self.print_leaderboard()

                if round_count < max_rounds and self.products:
                    input(
                        f"{Colors.YELLOW}Press Enter for the next round...{Colors.END}"
                    )

        self.clear_screen()
        self.print_header()
        print(f"{Colors.BOLD}{Colors.GREEN}🎉 GAME OVER! 🎉{Colors.END}\n")

        print(f"{Colors.BOLD}📊 FINAL RESULTS:{Colors.END}")
        self.print_leaderboard()

        print(f"{Colors.BOLD}👤 YOUR RESULTS:{Colors.END}")
        self.print_player_info(self.user_player)

        print(f"{Colors.CYAN}Thanks for playing! Goodbye! 👋{Colors.END}")


def main():
    try:
        game = DutchAuctionGame()
        game.run_game()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.RED}The game was interrupted by the user{Colors.END}")
    except Exception as e:
        print(f"\n\n{Colors.RED}Error: {e}{Colors.END}")


if __name__ == "__main__":
    main()
