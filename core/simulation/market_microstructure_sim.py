"""
JobGuard Core Simulation - Financial Market Microstructure & Limit Order Book (LOB)
Simulates Continuous Double Auction (CDA), Price-Time Priority matching,
market orders, limit orders, and market maker liquidity provisioning.
"""

import heapq
import time
from typing import List, Tuple, Dict, Optional, Any
from dataclasses import dataclass, field


@dataclass(order=True)
class Order:
    price: float
    timestamp: float
    order_id: str = field(compare=False)
    trader_id: str = field(compare=False)
    side: str = field(compare=False)  # "BUY" or "SELL"
    quantity: int = field(compare=False)


@dataclass
class Trade:
    buy_order_id: str
    sell_order_id: str
    price: float
    quantity: int
    timestamp: float


class LimitOrderBook:
    """Price-Time Priority Continuous Double Auction (CDA) matching engine."""

    def __init__(self):
        # Bids: max-heap (negate price)
        self.bids: List[Tuple[float, float, Order]] = []
        # Asks: min-heap
        self.asks: List[Tuple[float, float, Order]] = []
        self.trade_history: List[Trade] = []
        self._order_counter = 0

    def submit_limit_order(self, trader_id: str, side: str, price: float, quantity: int) -> List[Trade]:
        """Submit a limit order and execute matching trades against resting orders."""
        self._order_counter += 1
        now = time.monotonic()
        order = Order(
            price=price,
            timestamp=now,
            order_id=f"ORD_{self._order_counter:07d}",
            trader_id=trader_id,
            side=side.upper(),
            quantity=quantity
        )

        executed_trades: List[Trade] = []

        if side.upper() == "BUY":
            # Match against asks (sellers)
            while self.asks and order.quantity > 0:
                best_ask_price, _, best_ask = self.asks[0]
                if price >= best_ask_price:
                    # Match
                    trade_qty = min(order.quantity, best_ask.quantity)
                    trade = Trade(
                        buy_order_id=order.order_id,
                        sell_order_id=best_ask.order_id,
                        price=best_ask_price,
                        quantity=trade_qty,
                        timestamp=now
                    )
                    executed_trades.append(trade)
                    self.trade_history.append(trade)

                    order.quantity -= trade_qty
                    best_ask.quantity -= trade_qty

                    if best_ask.quantity == 0:
                        heapq.heappop(self.asks)
                else:
                    break

            # If leftover quantity, rest on bids book
            if order.quantity > 0:
                heapq.heappush(self.bids, (-order.price, order.timestamp, order))

        else:
            # Match against bids (buyers)
            while self.bids and order.quantity > 0:
                neg_best_bid_price, _, best_bid = self.bids[0]
                best_bid_price = -neg_best_bid_price
                if price <= best_bid_price:
                    trade_qty = min(order.quantity, best_bid.quantity)
                    trade = Trade(
                        buy_order_id=best_bid.order_id,
                        sell_order_id=order.order_id,
                        price=best_bid_price,
                        quantity=trade_qty,
                        timestamp=now
                    )
                    executed_trades.append(trade)
                    self.trade_history.append(trade)

                    order.quantity -= trade_qty
                    best_bid.quantity -= trade_qty

                    if best_bid.quantity == 0:
                        heapq.heappop(self.bids)
                else:
                    break

            if order.quantity > 0:
                heapq.heappush(self.asks, (order.price, order.timestamp, order))

        return executed_trades

    def get_best_bid_ask(self) -> Tuple[Optional[float], Optional[float]]:
        best_bid = -self.bids[0][0] if self.bids else None
        best_ask = self.asks[0][0] if self.asks else None
        return best_bid, best_ask
