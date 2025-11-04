# lightweight event types used by the engine
from dataclasses import dataclass

@dataclass
class MarketEvent:
    timestamp: int
    bars: dict

@dataclass
class SignalEvent:
    timestamp: int
    symbol: str
    side: str
    qty: float

@dataclass
class OrderEvent:
    timestamp: int
    symbol: str
    side: str
    qty: float

@dataclass
class FillEvent:
    timestamp: int
    symbol: str
    side: str
    qty: float
    price: float
