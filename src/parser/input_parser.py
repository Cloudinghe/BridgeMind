"""
桥牌输入解析器
Bridge Input Parser

解析桥牌游戏输入数据
"""

import json
from typing import Dict, Any, Optional, List
from .models import (
    Suit, Rank, Position, Strain, Card, Contract, Hand, GameState
)


class BridgeInputParser:
    """桥牌输入解析器"""
    
    def __init__(self):
        """初始化解析器"""
        pass
    
    def parse(self, input_data: str, format_type: str = 'json') -> Dict[str, Any]:
        """
        解析输入数据
        
        Args:
            input_data: 输入数据字符串
            format_type: 输入格式 ('json')
            
        Returns:
            解析后的数据字典
            
        Raises:
            ValueError: 不支持的格式或解析失败
        """
        if format_type == 'json':
            return self._parse_json(input_data)
        else:
            raise ValueError(f"Unsupported format: {format_type}")
    
    def _parse_json(self, json_str: str) -> Dict[str, Any]:
        """
        解析JSON格式输入
        
        Args:
            json_str: JSON字符串
            
        Returns:
            解析后的数据字典
            
        Raises:
            ValueError: JSON格式错误或数据无效
        """
        try:
            data = json.loads(json_str)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format: {e}")
        
        # 验证必要字段
        required_fields = ['hands', 'dealer']
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")
        
        # 解析手牌
        hands = self._parse_hands(data['hands'])
        
        # 解析定约（可选）
        contract = None
        if 'contract' in data:
            contract = self._parse_contract(data['contract'])
        
        # 解析庄家和明手（可选）
        declarer = None
        dummy = None
        if 'declarer' in data:
            declarer = Position(data['declarer'])
        if 'dummy' in data:
            dummy = Position(data['dummy'])
        
        # 解析叫牌记录（可选）
        bidding = []
        if 'bidding' in data:
            bidding = self._parse_bidding(data['bidding'])
        
        # 解析打牌记录（可选）
        plays = []
        if 'plays' in data:
            plays = self._parse_plays(data['plays'])
        
        return {
            'hands': hands,
            'dealer': Position(data['dealer']),
            'contract': contract,
            'declarer': declarer,
            'dummy': dummy,
            'vul': data.get('vul', 'None'),
            'bidding': bidding,
            'plays': plays
        }
    
    def _parse_hands(self, hands_data: Dict[str, List[str]]) -> Dict[Position, List[Card]]:
        """
        解析手牌数据
        
        Args:
            hands_data: 手牌数据字典，键为方位，值为牌张列表
            
        Returns:
            方位到牌张列表的映射
            
        Raises:
            ValueError: 手牌数据无效
        """
        hands = {}
        
        for position_str, cards_str in hands_data.items():
            position = Position(position_str)
            cards = []
            
            for card_str in cards_str:
                try:
                    card = Card.from_string(card_str)
                    cards.append(card)
                except ValueError as e:
                    raise ValueError(f"Invalid card '{card_str}' for position {position}: {e}")
            
            # 验证手牌长度
            if len(cards) != 13:
                raise ValueError(f"Hand for {position} must have exactly 13 cards, got {len(cards)}")
            
            hands[position] = cards
        
        return hands
    
    def _parse_contract(self, contract_data: Dict[str, Any]) -> Contract:
        """
        解析定约数据
        
        Args:
            contract_data: 定约数据字典
            
        Returns:
            定约对象
            
        Raises:
            ValueError: 定约数据无效
        """
        level = contract_data.get('level')
        strain_str = contract_data.get('strain')
        doubled = contract_data.get('doubled', False)
        redoubled = contract_data.get('redoubled', False)
        
        if level is None or strain_str is None:
            raise ValueError("Contract must include 'level' and 'strain'")
        
        strain = Strain(strain_str)
        
        return Contract(level, strain, doubled, redoubled)
    
    def _parse_bidding(self, bidding_data: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        解析叫牌记录
        
        Args:
            bidding_data: 叫牌数据列表
            
        Returns:
            叫牌记录列表
        """
        bidding = []
        
        for bid_record in bidding_data:
            player = bid_record.get('player')
            bid = bid_record.get('bid')
            
            if player is None or bid is None:
                raise ValueError("Each bidding record must include 'player' and 'bid'")
            
            bidding.append({
                'player': player,
                'bid': bid
            })
        
        return bidding
    
    def _parse_plays(self, plays_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        解析打牌记录
        
        Args:
            plays_data: 打牌数据列表
            
        Returns:
            打牌记录列表
        """
        plays = []
        
        for play_record in plays_data:
            trick_number = play_record.get('trick_number')
            player = play_record.get('player')
            card = play_record.get('card')
            
            if trick_number is None or player is None or card is None:
                raise ValueError("Each play record must include 'trick_number', 'player', and 'card'")
            
            plays.append({
                'trick_number': trick_number,
                'player': player,
                'card': card
            })
        
        return plays
    
    def create_game_state(self, parsed_data: Dict[str, Any]) -> GameState:
        """
        从解析数据创建游戏状态对象
        
        Args:
            parsed_data: 解析后的数据字典
            
        Returns:
            游戏状态对象
        """
        return GameState(
            hands=parsed_data['hands'],
            dealer=parsed_data['dealer'],
            contract=parsed_data['contract'],
            declarer=parsed_data['declarer'],
            dummy=parsed_data['dummy'],
            vulnerable=parsed_data['vul']
        )
