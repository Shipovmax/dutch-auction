"""Console Dutch auction game — CLI entry point and display/render loop.

The auction/pricing rules live in game.py and the AI bidding logic lives in
ai.py; this module is only responsible for drawing the screen and reading
player input.
"""

import os
import time

from ai import get_ai_decision
from game import DutchAuctionGame


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


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def print_header():
    print(f"{Colors.BOLD}{Colors.PURPLE}")
    print("=" * 60)
    print("🔥 GOLAN DUTCH AUCTION - CONSOLE EDITION 🔥")
    print("=" * 60)
    print(f"{Colors.END}")


def print_player_info(game: DutchAuctionGame, player):
    print(f"{Colors.CYAN}👤 {player.name}{Colors.END}")
    print(
        f"   💰 Balance: {Colors.GREEN}{game.format_money(player.balance)}{Colors.END}"
    )
    print(
        f"   📈 Profit: {Colors.BLUE}{game.format_money(player.total_profit)}{Colors.END}"
    )
    print(f"   🛒 Purchases: {Colors.YELLOW}{player.purchases}{Colors.END}")
    print(f"   ❤️  Likes: {Colors.RED}{player.wants}{Colors.END}")
    print(f"   💔 Dislikes: {Colors.RED}{player.dislikes}{Colors.END}")
    print()


def print_product_info(game: DutchAuctionGame):
    product = game.current_product
    if not product:
        return

    print(f"{Colors.BOLD}{Colors.YELLOW}💎 CURRENT LOT{Colors.END}")
    print(f"   🌸 Product: {Colors.BOLD}{product.name}{Colors.END}")
    print(f"   📦 Quantity: {Colors.CYAN}{product.quantity} pcs.{Colors.END}")
    print(
        f"   💰 Current price: {Colors.GREEN}{game.format_money(product.current_price)}{Colors.END}"
    )
    print(
        f"   💸 Cost basis: {Colors.RED}{game.format_money(product.cost)}{Colors.END}"
    )
    potential_profit = product.cost - product.current_price
    profit_color = Colors.GREEN if potential_profit >= 0 else Colors.RED
    profit_sign = "+" if potential_profit >= 0 else ""
    print(
        f"   📈 Potential profit: {profit_color}{profit_sign}{game.format_money(potential_profit)}{Colors.END}"
    )
    print(f"   💡 Profit = Purchase price × 1.3 (130%)")
    print(f"   📝 Description: {product.description}")
    print()


def print_leaderboard(game: DutchAuctionGame):
    sorted_players = sorted(
        game.players + ([game.user_player] if game.user_player else []),
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
            f"{medal} {player.name}: {profit_color}{profit_sign}{game.format_money(player.total_profit)}{Colors.END}"
        )
    print()


def run_game():
    game = DutchAuctionGame()

    clear_screen()
    print_header()

    print(f"{Colors.CYAN}Welcome to the Dutch Auction!{Colors.END}")
    user_name = input(f"{Colors.YELLOW}Enter your name: {Colors.END}").strip()
    if not user_name:
        user_name = "Player"

    game.create_user_player(user_name)

    print(
        f"\n{Colors.GREEN}Hello, {user_name}! You have {game.format_money(game.user_player.balance)}{Colors.END}"
    )
    input(f"{Colors.YELLOW}Press Enter to start the game...{Colors.END}")

    round_count = 0
    max_rounds = 10

    while round_count < max_rounds and game.products:
        clear_screen()
        print_header()

        if not game.start_new_round():
            break

        round_count += 1
        print(f"{Colors.BOLD}Round {round_count}/{max_rounds}{Colors.END}\n")

        print_product_info(game)

        print(f"{Colors.BOLD}YOUR PROFILE{Colors.END}")
        print_player_info(game, game.user_player)

        auction_active = True
        price_decrease_count = 0

        while auction_active and game.current_product:
            print(
                f"{Colors.BOLD}💰 Current price: {Colors.GREEN}{game.format_money(game.current_product.current_price)}{Colors.END}"
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
                if game.buy_product(game.user_player):
                    print(
                        f"\n{Colors.GREEN}🎉 Congratulations! You bought {game.current_product.name} for {game.format_money(game.current_product.current_price)}!{Colors.END}"
                    )
                    profit = (
                        game.current_product.cost - game.current_product.current_price
                    )
                    print(
                        f"{Colors.BLUE}💰 Your profit: {game.format_money(profit)}{Colors.END}"
                    )
                    auction_active = False
                else:
                    print(f"\n{Colors.RED}❌ Insufficient funds!{Colors.END}")

            elif choice == "2":
                if game.decrease_price():
                    print(f"\n{Colors.YELLOW}⏳ The price is dropping...{Colors.END}")
                    price_decrease_count += 1

                    for player in game.players:
                        if get_ai_decision(
                            player, game.current_product
                        ) and game.buy_product(player):
                            print(
                                f"{Colors.CYAN}🤖 {player.name} bought the product!{Colors.END}"
                            )
                            auction_active = False
                            break
                else:
                    print(
                        f"\n{Colors.RED}❌ The price reached its minimum!{Colors.END}"
                    )
                    auction_active = False

            elif choice == "3":
                print_leaderboard(game)
                input(f"{Colors.YELLOW}Press Enter to continue...{Colors.END}")

            elif choice == "4":
                print(f"\n{Colors.YELLOW}⏭️ Round skipped{Colors.END}")
                auction_active = False

            else:
                print(f"\n{Colors.RED}❌ Invalid choice!{Colors.END}")

            if auction_active:
                time.sleep(0.5)

        if not auction_active:
            print(f"\n{Colors.BOLD}📊 Round result:{Colors.END}")
            print_leaderboard(game)

            if round_count < max_rounds and game.products:
                input(f"{Colors.YELLOW}Press Enter for the next round...{Colors.END}")

    clear_screen()
    print_header()
    print(f"{Colors.BOLD}{Colors.GREEN}🎉 GAME OVER! 🎉{Colors.END}\n")

    print(f"{Colors.BOLD}📊 FINAL RESULTS:{Colors.END}")
    print_leaderboard(game)

    print(f"{Colors.BOLD}👤 YOUR RESULTS:{Colors.END}")
    print_player_info(game, game.user_player)

    print(f"{Colors.CYAN}Thanks for playing! Goodbye! 👋{Colors.END}")


def main():
    try:
        run_game()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.RED}The game was interrupted by the user{Colors.END}")
    except Exception as e:
        print(f"\n\n{Colors.RED}Error: {e}{Colors.END}")


if __name__ == "__main__":
    main()
