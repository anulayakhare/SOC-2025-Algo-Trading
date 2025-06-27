from src.backtester import Order, OrderBook
from typing import List

import numpy as np

ask_h = []
bid_h = []
mid_h = []
spread_h = []
class Trader:
    def run(self, state, current_position):
        result = {}
        orders: List[Order] = []
        order_depth: OrderBook = state.order_depth

        sorted_sell_orders = sorted(order_depth.sell_orders.items(), key=lambda x: x[0])
        sorted_buy_orders = sorted(order_depth.buy_orders.items(), key=lambda x: -x[0])

        best_ask, best_ask_amount = sorted_sell_orders[0]
        best_bid, best_bid_amount = sorted_buy_orders[0]

        ask_h.append(best_ask)
        bid_h.append(best_bid)

        mid_price = (best_bid + best_ask) / 2
        mid_h.append(mid_price)
        spread = best_ask - best_bid
        spread_h.append(spread)
        spread_std = np.std(spread_h)
        buy_price = min(np.mean(mid_h) - spread_std, best_ask)
        sell_price = max(np.mean(mid_h) + spread_std, best_bid)
        
        orders.append(Order("PRODUCT", buy_price + 1, 50-current_position))
        orders.append(Order("PRODUCT", sell_price - 1, -(50+current_position)))

        result["PRODUCT"] = orders
        return result
