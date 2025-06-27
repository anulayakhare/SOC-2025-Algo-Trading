from src.backtester import Order, OrderBook
from typing import List

class Trader:
    def run(self, state, current_position):
        result = {}
        orders: List[Order] = []
        order_depth: OrderBook = state.order_depth

        sorted_sell_orders = sorted(order_depth.sell_orders.items(), key=lambda x: x[0])
        sorted_buy_orders = sorted(order_depth.buy_orders.items(), key=lambda x: -x[0])

        best_ask, best_ask_amount = sorted_sell_orders[0]
        best_bid, best_bid_amount = sorted_buy_orders[0]

        mid_price = (best_bid + best_ask) / 2
        spread = best_ask - best_bid
        buy_price = 0
        sell_price = 0
        if spread > 0.5:
            buy_price = mid_price - spread/2
            sell_price = mid_price + spread/2
        
        orders.append(Order("PRODUCT", buy_price, 50-current_position))
        orders.append(Order("PRODUCT", sell_price, -(50+current_position)))

        result["PRODUCT"] = orders
        return result