"""AI bidding logic for computer-controlled auction players.

Kept separate from the core game model so the "how does an AI decide to
bid" question lives in one obvious place.
"""

import random

from game import Player, Product


def get_ai_decision(player: Player, product: Product) -> bool:
    """Return True if the AI player chooses to buy the product at its current price."""
    if not product:
        return False

    can_afford = player.balance >= product.current_price
    good_price = product.current_price <= product.start_price * 0.7

    likes_product = player.wants.lower() in product.name.lower()
    dislikes_product = player.dislikes.lower() in product.name.lower()
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
