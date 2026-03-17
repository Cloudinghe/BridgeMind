"""
核心数据模型
Core Data Models

定义桥牌相关的核心数据结构
"""

from enum import Enum
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime


class Suit(Enum):
    """
    花色枚举
    
    桥牌的四种花色：黑桃(Spade)、红心(Heart)、方块(Diamond)、梅花(Club)
    """
    CLUBS = "C"      # 梅花
    DIAMONDS = "D"   # 方块
    HEARTS = "H"     # 红心
    SPADES = "S"     # 黑桃
    
    def __str__(self):
        """花色的字符串表示"""
        symbols = {
            self.CLUBS: "♣",
            self.DIAMONDS: "♦",
            self.HEARTS: "♥",
            self.SPADES: "♠"
        }
        return symbols[self]
    
    def __lt__(self, other):
        """花色大小比较（按C-D-H-S顺序）"""
        order = [self.CLUBS, self.DIAMONDS, self.HEARTS, self.SPADES]
        return order.index(self) < order.index(other)


class Rank(Enum):
    """
    点数枚举
    
    桥牌的13个点数：A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, 2
    """
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14
    
    def __str__(self):
        """点数的字符串表示"""
        symbols = {
            self.TWO: "2",
            self.THREE: "3",
            self.FOUR: "4",
            self.FIVE: "5",
            self.SIX: "6",
            self.SEVEN: "7",
            self.EIGHT: "8",
            self.NINE: "9",
            self.TEN: "T",
            self.JACK: "J",
            self.QUEEN: "Q",
            self.KING: "K",
            self.ACE: "A"
        }
        return symbols[self]
    
    def __lt__(self, other):
        """点数大小比较"""
        return self.value < other.value


class Position(Enum):
    """
    方位枚举
    
    桥牌的四个方位：北(North)、东(East)、南(South)、西(West)
    """
    NORTH = "N"
    EAST = "E"
    SOUTH = "S"
    WEST = "W"
    
    def __str__(self):
        """方位的字符串表示"""
        return self.value
    
    def get_partner(self) -> 'Position':
        """
        获取搭档的方位
        
        Returns:
            搭档的方位
        """
        partner_map = {
            self.NORTH: self.SOUTH,
            self.SOUTH: self.NORTH,
            self.EAST: self.WEST,
            self.WEST: self.EAST
        }
        return partner_map[self]
    
    def get_left_opponent(self) -> 'Position':
        """
        获取左手的对手（顺时针下一个）
        
        Returns:
            左手对手的方位
        """
        order = [self.NORTH, self.EAST, self.SOUTH, self.WEST]
        idx = order.index(self)
        return order[(idx + 1) % 4]
    
    def get_right_opponent(self) -> 'Position':
        """
        获取右手的对手（逆时针下一个）
        
        Returns:
            右手对手的方位
        """
        order = [self.NORTH, self.WEST, self.SOUTH, self.EAST]
        idx = order.index(self)
        return order[(idx + 1) % 4]


class Strain(Enum):
    """
    定约花色枚举
    """
    CLUBS = "C"
    DIAMONDS = "D"
    HEARTS = "H"
    SPADES = "S"
    NOTRUMP = "NT"
    
    def __str__(self):
        """定约花色的字符串表示"""
        if self == self.NOTRUMP:
            return "NT"
        return self.value
    
    def is_major(self) -> bool:
        """
        是否为高花（红心或黑桃）
        
        Returns:
            是否为高花
        """
        return self in [self.HEARTS, self.SPADES]
    
    def is_minor(self) -> bool:
        """
        是否为低花（方块或梅花）
        
        Returns:
            是否为低花
        """
        return self in [self.CLUBS, self.DIAMONDS]


@dataclass
class Card:
    """
    牌张类
    
    表示一张桥牌，包含花色和点数
    """
    suit: Suit      # 花色
    rank: Rank       # 点数
    
    def __post_init__(self):
        """初始化后的验证"""
        if not isinstance(self.suit, Suit):
            raise ValueError(f"Invalid suit: {self.suit}")
        if not isinstance(self.rank, Rank):
            raise ValueError(f"Invalid rank: {self.rank}")
    
    def __str__(self):
        """牌张的字符串表示"""
        return f"{self.suit}{self.rank}"
    
    def __repr__(self):
        """牌张的正式表示"""
        return f"Card({self.suit}, {self.rank})"
    
    def __eq__(self, other):
        """相等比较"""
        if not isinstance(other, Card):
            return False
        return self.suit == other.suit and self.rank == other.rank
    
    def __hash__(self):
        """哈希值（用于集合和字典）"""
        return hash((self.suit, self.rank))
    
    def __lt__(self, other):
        """大小比较（先比花色，再比点数）"""
        if self.suit != other.suit:
            return self.suit < other.suit
        return self.rank < other.rank
    
    @property
    def hcp(self) -> int:
        """
        高牌点(HCP)值
        
        A=4, K=3, Q=2, J=1, 其他=0
        
        Returns:
            高牌点数
        """
        hcp_map = {
            Rank.ACE: 4,
            Rank.KING: 3,
            Rank.QUEEN: 2,
            Rank.JACK: 1
        }
        return hcp_map.get(self.rank, 0)
    
    def to_index(self) -> int:
        """
        将牌张转换为索引（0-51）
        
        用于强化学习等场景
        
        Returns:
            牌张索引
        """
        # 花色顺序：C-D-H-S
        suit_idx = {
            Suit.CLUBS: 0,
            Suit.DIAMONDS: 1,
            Suit.HEARTS: 2,
            Suit.SPADES: 3
        }[self.suit]
        
        # 点数顺序：2-A
        rank_idx = self.rank.value - 2
        
        return suit_idx * 13 + rank_idx
    
    @classmethod
    def from_index(cls, index: int) -> 'Card':
        """
        从索引创建牌张
        
        Args:
            index: 牌张索引（0-51）
            
        Returns:
            牌张对象
        """
        suit_idx = index // 13
        rank_idx = index % 13 + 2
        
        suit = [Suit.CLUBS, Suit.DIAMONDS, Suit.HEARTS, Suit.SPADES][suit_idx]
        rank = Rank(rank_idx)
        
        return cls(suit, rank)
    
    @classmethod
    def from_string(cls, card_str: str) -> 'Card':
        """
        从字符串创建牌张
        
        Args:
            card_str: 牌张字符串，如 "SA", "HK", "D2"
            
        Returns:
            牌张对象
        """
        if len(card_str) != 2:
            raise ValueError(f"Invalid card string: {card_str}")
        
        suit_char = card_str[0].upper()
        rank_char = card_str[1].upper()
        
        suit_map = {
            'C': Suit.CLUBS,
            'D': Suit.DIAMONDS,
            'H': Suit.HEARTS,
            'S': Suit.SPADES
        }
        
        if suit_char not in suit_map:
            raise ValueError(f"Invalid suit character: {suit_char}")
        
        suit = suit_map[suit_char]
        
        rank_map = {
            'A': Rank.ACE,
            'K': Rank.KING,
            'Q': Rank.QUEEN,
            'J': Rank.JACK,
            'T': Rank.TEN,
            '9': Rank.NINE,
            '8': Rank.EIGHT,
            '7': Rank.SEVEN,
            '6': Rank.SIX,
            '5': Rank.FIVE,
            '4': Rank.FOUR,
            '3': Rank.THREE,
            '2': Rank.TWO
        }
        
        if rank_char not in rank_map:
            raise ValueError(f"Invalid rank character: {rank_char}")
        
        rank = rank_map[rank_char]
        
        return cls(suit, rank)


@dataclass
class Contract:
    """
    定约类
    
    表示桥牌的定约，包括阶数和花色
    """
    level: int          # 阶数（1-7）
    strain: Strain       # 花色
    doubled: bool = False    # 是否加倍
    redoubled: bool = False  # 是否再加倍
    
    def __post_init__(self):
        """初始化后的验证"""
        if not 1 <= self.level <= 7:
            raise ValueError(f"Invalid contract level: {self.level} (must be 1-7)")
        if not isinstance(self.strain, Strain):
            raise ValueError(f"Invalid strain: {self.strain}")
        if self.redoubled and not self.doubled:
            raise ValueError("Redoubled contract must be doubled first")
    
    def __str__(self):
        """定约的字符串表示"""
        # 花色符号映射
        strain_symbols = {
            Strain.CLUBS: "♣",
            Strain.DIAMONDS: "♦",
            Strain.HEARTS: "♥",
            Strain.SPADES: "♠",
            Strain.NOTRUMP: "NT"
        }
        
        result = f"{self.level}{strain_symbols[self.strain]}"
        if self.redoubled:
            result += "XX"
        elif self.doubled:
            result += "X"
        return result
    
    def __repr__(self):
        """定约的正式表示"""
        return f"Contract({self.level}, {self.strain}, doubled={self.doubled}, redoubled={self.redoubled})"
    
    def get_required_tricks(self) -> int:
        """
        获取完成定约需要的墩数
        
        Args:
            无
            
        Returns:
            需要的墩数（阶数 + 6）
        """
        return self.level + 6
    
    def get_bonus(self, vulnerable: bool) -> int:
        """
        计算定约完成的基本分数
        
        Args:
            vulnerable: 是否有局
            
        Returns:
            基本分数
        """
        # 每墩分数
        if self.strain in [Strain.CLUBS, Strain.DIAMONDS]:
            trick_points = 20  # 低花每墩20分
        elif self.strain == Strain.NOTRUMP:
            trick_points = 40  # 无将第一墩40分
        else:
            trick_points = 30  # 高花每墩30分
        
        # 计算墩分
        if self.strain == Strain.NOTRUMP:
            base_score = trick_points + (self.level - 1) * 30
        else:
            base_score = self.level * trick_points
        
        # 加倍/再加倍
        if self.doubled:
            base_score *= 2
        if self.redoubled:
            base_score *= 2
        
        return base_score


@dataclass
class Hand:
    """
    手牌类
    
    表示一个方位的手牌（13张）
    """
    position: Position        # 方位
    cards: List[Card]        # 牌张列表
    
    def __post_init__(self):
        """初始化后的验证"""
        if len(self.cards) != 13:
            raise ValueError(f"Hand must have exactly 13 cards, got {len(self.cards)}")
        if len(set(self.cards)) != 13:
            raise ValueError("Hand contains duplicate cards")
    
    def __str__(self):
        """手牌的字符串表示"""
        return f"{self.position}: {' '.join(str(card) for card in sorted(self.cards))}"
    
    def get_suit(self, suit: Suit) -> List[Card]:
        """
        获取指定花色的牌
        
        Args:
            suit: 花色
            
        Returns:
            该花色的所有牌
        """
        return [card for card in self.cards if card.suit == suit]
    
    def get_suit_length(self, suit: Suit) -> int:
        """
        获取指定花色的长度
        
        Args:
            suit: 花色
            
        Returns:
            该花色的牌数
        """
        return len(self.get_suit(suit))
    
    def get_hcp(self) -> int:
        """
        获取高牌点(HCP)总数
        
        Returns:
            高牌点总数
        """
        return sum(card.hcp for card in self.cards)
    
    def get_distribution(self) -> str:
        """
        获取牌型分布
        
        Returns:
            牌型分布字符串，如 "5-3-3-2"
        """
        lengths = [
            self.get_suit_length(Suit.SPADES),
            self.get_suit_length(Suit.HEARTS),
            self.get_suit_length(Suit.DIAMONDS),
            self.get_suit_length(Suit.CLUBS)
        ]
        return "-".join(map(str, sorted(lengths, reverse=True)))


@dataclass
class GameState:
    """
    游戏状态类
    
    表示桥牌游戏的当前状态
    """
    hands: Dict[Position, List[Card]]  # 四家手牌
    dealer: Position                    # 发牌人
    contract: Optional[Contract] = None # 定约
    declarer: Optional[Position] = None # 庄家
    dummy: Optional[Position] = None    # 明手
    vulnerable: str = "None"            # 局况
    
    def __post_init__(self):
        """初始化后的验证"""
        # 验证四家手牌
        for position in Position:
            if position not in self.hands:
                self.hands[position] = []
        
        # 验证手牌数量
        all_cards = []
        for cards in self.hands.values():
            all_cards.extend(cards)
        
        # 验证没有重复牌
        if len(all_cards) != len(set(all_cards)):
            raise ValueError("Duplicate cards found in hands")
        
        # 验证总牌数为52张
        if len(all_cards) != 52:
            raise ValueError(f"Expected 52 cards, got {len(all_cards)}")
    
    def get_hand(self, position: Position) -> List[Card]:
        """
        获取指定方位的手牌
        
        Args:
            position: 方位
            
        Returns:
            该方位的手牌
        """
        return self.hands.get(position, []).copy()
    
    def get_current_player(self) -> Position:
        """
        获取当前应该出牌的玩家
        
        Returns:
            当前玩家方位
        """
        # TODO: 根据打牌进度确定当前玩家
        # 暂时返回发牌人
        return self.dealer
    
    def is_game_over(self) -> bool:
        """
        判断游戏是否结束
        
        Returns:
            游戏是否结束
        """
        # TODO: 检查所有牌是否已打出
        return False
    
    def get_tricks_played(self) -> int:
        """
        获取已打出的墩数
        
        Returns:
            已打出的墩数
        """
        # TODO: 计算已打出的墩数
        return 0
