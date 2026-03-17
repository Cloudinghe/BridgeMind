"""
桥牌数据标准化器
Bridge Data Normalizer

标准化桥牌游戏数据格式
"""

from typing import Dict, Any, List
from .models import Position, Card


class BridgeDataNormalizer:
    """桥牌数据标准化器"""
    
    def __init__(self):
        """初始化标准化器"""
        pass
    
    def normalize(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        标准化数据
        
        Args:
            data: 输入数据字典
            
        Returns:
            标准化后的数据字典
        """
        normalized = data.copy()
        
        # 标准化方位
        normalized = self._normalize_positions(normalized)
        
        # 标准化手牌
        normalized = self._normalize_hands(normalized)
        
        # 标准化定约
        normalized = self._normalize_contract(normalized)
        
        # 标准化叫牌记录
        normalized = self._normalize_bidding(normalized)
        
        # 标准化打牌记录
        normalized = self._normalize_plays(normalized)
        
        return normalized
    
    def _normalize_positions(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        标准化方位
        
        Args:
            data: 数据字典
            
        Returns:
            标准化后的数据字典
        """
        # 确保发牌人是Position枚举
        if 'dealer' in data and isinstance(data['dealer'], str):
            data['dealer'] = Position(data['dealer'].upper())
        
        # 确保庄家和明手是Position枚举
        if 'declarer' in data and isinstance(data['declarer'], str):
            data['declarer'] = Position(data['declarer'].upper())
        
        if 'dummy' in data and isinstance(data['dummy'], str):
            data['dummy'] = Position(data['dummy'].upper())
        
        # 标准化叫牌记录中的方位
        if 'bidding' in data:
            for bid_record in data['bidding']:
                if 'player' in bid_record and isinstance(bid_record['player'], str):
                    bid_record['player'] = bid_record['player'].upper()
        
        # 标准化打牌记录中的方位
        if 'plays' in data:
            for play_record in data['plays']:
                if 'player' in play_record and isinstance(play_record['player'], str):
                    play_record['player'] = play_record['player'].upper()
        
        return data
    
    def _normalize_hands(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        标准化手牌
        
        Args:
            data: 数据字典
            
        Returns:
            标准化后的数据字典
        """
        if 'hands' not in data:
            return data
        
        # 确保手牌按花色和点数排序
        for position in data['hands']:
            cards = data['hands'][position]
            # 按花色排序：S, H, D, C
            cards_sorted = sorted(cards, key=lambda x: (
                ['S', 'H', 'D', 'C'].index(str(x.suit.value)),
                -x.rank.value
            ))
            data['hands'][position] = cards_sorted
        
        return data
    
    def _normalize_contract(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        标准化定约
        
        Args:
            data: 数据字典
            
        Returns:
            标准化后的数据字典
        """
        if 'contract' not in data or data['contract'] is None:
            return data
        
        contract = data['contract']
        
        # 如果contract是字符串，尝试解析
        if isinstance(contract, str):
            # 格式如 "4H", "3NT", "4HX", "4HXX"
            contract_str = contract.upper()
            
            # 解析加倍/再加倍
            doubled = 'XX' in contract_str
            redoubled = False
            if doubled:
                contract_str = contract_str.replace('XX', '')
                redoubled = True
            elif 'X' in contract_str:
                contract_str = contract_str.replace('X', '')
                doubled = True
            
            # 解析阶数和花色
            if len(contract_str) >= 2:
                level = int(contract_str[0])
                strain_str = contract_str[1:]
                
                data['contract'] = {
                    'level': level,
                    'strain': strain_str,
                    'doubled': doubled,
                    'redoubled': redoubled
                }
        
        return data
    
    def _normalize_bidding(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        标准化叫牌记录
        
        Args:
            data: 数据字典
            
        Returns:
            标准化后的数据字典
        """
        if 'bidding' not in data:
            return data
        
        # 标准化叫牌内容
        for bid_record in data['bidding']:
            if 'bid' in bid_record:
                bid = bid_record['bid'].upper()
                # 标准化PASS
                if bid in ['PASS', 'P', '']:
                    bid = 'PASS'
                # 标准化加倍
                elif bid in ['DBL', 'DOUBLE', 'X']:
                    bid = 'DBL'
                # 标准化再加倍
                elif bid in ['RDBL', 'REDOUBLE', 'XX']:
                    bid = 'RDBL'
                
                bid_record['bid'] = bid
        
        return data
    
    def _normalize_plays(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        标准化打牌记录
        
        Args:
            data: 数据字典
            
        Returns:
            标准化后的数据字典
        """
        if 'plays' not in data:
            return data
        
        # 标准化牌张表示
        for play_record in data['plays']:
            if 'card' in play_record:
                card = play_record['card'].upper()
                # 标准化10的表示
                if '10' in card:
                    card = card.replace('10', 'T')
                play_record['card'] = card
        
        return data
