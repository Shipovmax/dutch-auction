"""Core Dutch auction game logic: products, players, pricing, and purchases.

This module has no knowledge of the console UI or of how AI players decide
to bid — it only models the auction itself (lots, prices, balances).
"""

import random
from dataclasses import dataclass
from typing import List, Optional


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
        self.current_product: Optional[Product] = None
        self.game_active = False
        self.user_player: Optional[Player] = None

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

    def format_money(self, amount: int) -> str:
        return f"{amount:,} ₽"
