"""
桥牌数据校验器
Bridge Data Validator

校验桥牌游戏数据的有效性
"""

from typing import Dict, Any, List, Optional
from .models import Position, Suit, Rank, Card


class BridgeDataValidator:
    """桥牌数据校验器"""
    
    def __init__(self):
        """初始化校验器"""
        self.errors = []
        self.warnings = []
    
    def validate_parsed_data(self, data: Dict[str, Any]) -> bool:
        """
        校验解析后的数据
        
        Args:
            data: 解析后的数据字典
            
        Returns:
            是否校验通过
        """
        self.errors = []
        self.warnings = []
        
        # 校验手牌
        self._validate_hands(data.get('hands', {}))
        
        # 校验发牌人
        self._validate_dealer(data.get('dealer'))
        
        # 校验定约
        self._validate_contract(data.get('contract'))
        
        # 校验庄家和明手
        self._validate_declarer_and_dummy(
            data.get('declarer'),
            data.get('dummy'),
            data.get('contract')
        )
        
        # 校验叫牌记录
        self._validate_bidding(data.get('bidding', []))
        
        # 校验打牌记录
        self._validate_plays(data.get('plays', []), data.get('hands', {}))
        
        return len(self.errors) == 0
    
    def _validate_hands(self, hands: Dict[Position, List[Card]]):
        """
        校验手牌
        
        Args:
            hands: 手牌数据
        """
        if not hands:
            self.errors.append("Hands data is empty")
            return
        
        # 检查是否有四个方位
        for position in Position:
            if position not in hands:
                self.errors.append(f"Missing hand for position: {position}")
        
        # 检查每个手牌是否有13张牌
        for position, cards in hands.items():
            if len(cards) != 13:
                self.errors.append(
                    f"Hand for {position} must have exactly 13 cards, got {len(cards)}"
                )
        
        # 检查是否有重复的牌
        all_cards = []
        for position, cards in hands.items():
            all_cards.extend(cards)
        
        unique_cards = set(all_cards)
        if len(all_cards) != len(unique_cards):
            self.errors.append("Duplicate cards found across all hands")
        
        # 检查是否有52张牌
        if len(all_cards) != 52:
            self.errors.append(f"Expected 52 cards total, got {len(all_cards)}")
    
    def _validate_dealer(self, dealer: Optional[Position]):
        """
        校验发牌人
        
        Args:
            dealer: 发牌人
        """
        if dealer is None:
            self.errors.append("Dealer is required")
        elif not isinstance(dealer, Position):
            self.errors.append(f"Invalid dealer: {dealer}")
    
    def _validate_contract(self, contract: Optional[object]):
        """
        校验定约
        
        Args:
            contract: 定约对象
        """
        if contract is None:
            self.warnings.append("No contract specified")
            return
        
        # 这里假设contract已经是Contract对象，具体验证在Contract.__post_init__中完成
        if not hasattr(contract, 'level') or not hasattr(contract, 'strain'):
            self.errors.append(f"Invalid contract object: {contract}")
    
    def _validate_declarer_and_dummy(self, declarer: Optional[Position], 
                                      dummy: Optional[Position],
                                      contract: Optional[object]):
        """
        校验庄家和明手
        
        Args:
            declarer: 庄家
            dummy: 明手
            contract: 定约
        """
        if contract is None:
            return
        
        if declarer is None:
            self.warnings.append("No declarer specified")
        
        if dummy is None:
            self.warnings.append("No dummy specified")
        
        # 庄家和明手应该是搭档
        if declarer is not None and dummy is not None:
            if declarer.get_partner() != dummy:
                self.warnings.append(
                    f"Declarer {declarer} and dummy {dummy} should be partners"
                )
    
    def _validate_bidding(self, bidding: List[Dict[str, str]]):
        """
        校验叫牌记录
        
        Args:
            bidding: 叫牌记录列表
        """
        if not bidding:
            self.warnings.append("No bidding records")
            return
        
        # 检查每个叫牌记录的格式
        for i, bid_record in enumerate(bidding):
            if 'player' not in bid_record:
                self.errors.append(f"Bidding record {i}: missing 'player'")
            
            if 'bid' not in bid_record:
                self.errors.append(f"Bidding record {i}: missing 'bid'")
    
    def _validate_plays(self, plays: List[Dict[str, Any]], 
                       hands: Dict[Position, List[Card]]):
        """
        校验打牌记录
        
        Args:
            plays: 打牌记录列表
            hands: 手牌数据
        """
        if not plays:
            self.warnings.append("No play records")
            return
        
        # 检查每个打牌记录的格式
        for i, play_record in enumerate(plays):
            if 'trick_number' not in play_record:
                self.errors.append(f"Play record {i}: missing 'trick_number'")
            
            if 'player' not in play_record:
                self.errors.append(f"Play record {i}: missing 'player'")
            
            if 'card' not in play_record:
                self.errors.append(f"Play record {i}: missing 'card'")
    
    def get_errors(self) -> List[str]:
        """
        获取所有错误
        
        Returns:
            错误列表
        """
        return self.errors
    
    def get_warnings(self) -> List[str]:
        """
        获取所有警告
        
        Returns:
            警告列表
        """
        return self.warnings
    
    def has_errors(self) -> bool:
        """
        是否有错误
        
        Returns:
            是否有错误
        """
        return len(self.errors) > 0
    
    def has_warnings(self) -> bool:
        """
        是否有警告
        
        Returns:
            是否有警告
        """
        return len(self.warnings) > 0
