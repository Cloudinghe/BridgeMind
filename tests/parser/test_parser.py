"""
解析器测试
Tests for Parser
"""

import pytest
import json
from src.parser import (
    BridgeInputParser, BridgeDataValidator, BridgeDataNormalizer
)
from src.parser.models import Position, Suit, Strain, Card


class TestBridgeInputParser:
    """测试输入解析器"""
    
    def test_parse_json_basic(self):
        """测试基本JSON解析"""
        parser = BridgeInputParser()
        
        json_str = json.dumps({
            'hands': {
                'N': ['SA', 'SK', 'SQ', 'SJ', 'S10'],
                'E': ['HA', 'HK', 'HQ', 'HJ', 'H10'],
                'S': ['DA', 'DK', 'DQ', 'DJ', 'D10'],
                'W': ['CA', 'CK', 'CQ', 'CJ', 'C10']
            },
            'dealer': 'N'
        }, indent=None)
        
        # 注意：上面的手牌每家只有5张，用于简化测试
        # 实际解析会失败，因为需要13张牌
        with pytest.raises(ValueError):
            parser.parse(json_str)
    
    def test_parse_json_full_hands(self):
        """测试完整手牌JSON解析"""
        parser = BridgeInputParser()
        
        # 创建完整的52张牌
        all_cards = []
        for suit in ['S', 'H', 'D', 'C']:
            for rank in ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']:
                all_cards.append(f'{suit}{rank}')
        
        # 分配给四家
        json_str = json.dumps({
            'hands': {
                'N': all_cards[0:13],
                'E': all_cards[13:26],
                'S': all_cards[26:39],
                'W': all_cards[39:52],
            },
            'dealer': 'N'
        }, indent=None)
        
        data = parser.parse(json_str)
        
        assert 'hands' in data
        assert 'dealer' in data
        assert data['dealer'] == Position.NORTH
        assert len(data['hands']) == 4
        for pos in data['hands']:
            assert len(data['hands'][pos]) == 13
    
    def test_parse_json_with_contract(self):
        """测试带定约的JSON解析"""
        parser = BridgeInputParser()
        
        # 创建完整的52张牌
        all_cards = []
        for suit in ['S', 'H', 'D', 'C']:
            for rank in ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']:
                all_cards.append(f'{suit}{rank}')
        
        json_str = json.dumps({
            'hands': {
                'N': all_cards[0:13],
                'E': all_cards[13:26],
                'S': all_cards[26:39],
                'W': all_cards[39:52],
            },
            'dealer': 'N',
            'contract': {
                'level': 4,
                'strain': 'H',
                'doubled': True
            },
            'declarer': 'S',
            'dummy': 'N'
        }, indent=None)
        
        data = parser.parse(json_str)
        
        assert data['contract'] is not None
        assert data['contract'].level == 4
        assert data['contract'].strain == Strain.HEARTS
        assert data['contract'].doubled is True
        assert data['declarer'] == Position.SOUTH
        assert data['dummy'] == Position.NORTH
    
    def test_parse_json_with_bidding(self):
        """测试带叫牌记录的JSON解析"""
        parser = BridgeInputParser()
        
        all_cards = []
        for suit in ['S', 'H', 'D', 'C']:
            for rank in ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']:
                all_cards.append(f'{suit}{rank}')
        
        json_str = json.dumps({
            'hands': {
                'N': all_cards[0:13],
                'E': all_cards[13:26],
                'S': all_cards[26:39],
                'W': all_cards[39:52],
            },
            'dealer': 'N',
            'bidding': [
                {'player': 'N', 'bid': '1H'},
                {'player': 'E', 'bid': 'PASS'},
                {'player': 'S', 'bid': 'PASS'},
                {'player': 'W', 'bid': 'DBL'}
            ]
        }, indent=None)
        
        data = parser.parse(json_str)
        
        assert len(data['bidding']) == 4
        assert data['bidding'][0]['bid'] == '1H'
        assert data['bidding'][3]['bid'] == 'DBL'
    
    def test_parse_invalid_json(self):
        """测试无效JSON"""
        parser = BridgeInputParser()
        
        with pytest.raises(ValueError):
            parser.parse("not valid json")
    
    def test_parse_missing_required_field(self):
        """测试缺少必要字段"""
        parser = BridgeInputParser()
        
        json_str = json.dumps({'dealer': 'N'})
        
        with pytest.raises(ValueError):
            parser.parse(json_str)


class TestBridgeDataValidator:
    """测试数据校验器"""
    
    def test_valid_data(self):
        """测试有效数据校验"""
        validator = BridgeDataValidator()
        
        all_cards = []
        for suit in ['S', 'H', 'D', 'C']:
            for rank in ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']:
                all_cards.append(f'{suit}{rank}')
        
        data = {
            'hands': {
                Position.NORTH: [Card.from_string(c) for c in all_cards[0:13]],
                Position.EAST: [Card.from_string(c) for c in all_cards[13:26]],
                Position.SOUTH: [Card.from_string(c) for c in all_cards[26:39]],
                Position.WEST: [Card.from_string(c) for c in all_cards[39:52]],
            },
            'dealer': Position.NORTH
        }
        
        assert validator.validate_parsed_data(data) is True
        assert len(validator.get_errors()) == 0
    
    def test_invalid_hand_length(self):
        """测试无效手牌长度"""
        validator = BridgeDataValidator()
        
        data = {
            'hands': {
                Position.NORTH: [],
                Position.EAST: [],
                Position.SOUTH: [],
                Position.WEST: [],
            },
            'dealer': Position.NORTH
        }
        
        assert validator.validate_parsed_data(data) is False
        assert len(validator.get_errors()) > 0
    
    def test_missing_dealer(self):
        """测试缺少发牌人"""
        validator = BridgeDataValidator()
        
        data = {
            'hands': {},
            'dealer': None
        }
        
        assert validator.validate_parsed_data(data) is False
        assert len(validator.get_errors()) > 0
    
    def test_warnings(self):
        """测试警告信息"""
        validator = BridgeDataValidator()
        
        all_cards = []
        for suit in ['S', 'H', 'D', 'C']:
            for rank in ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']:
                all_cards.append(f'{suit}{rank}')
        
        data = {
            'hands': {
                Position.NORTH: [Card.from_string(c) for c in all_cards[0:13]],
                Position.EAST: [Card.from_string(c) for c in all_cards[13:26]],
                Position.SOUTH: [Card.from_string(c) for c in all_cards[26:39]],
                Position.WEST: [Card.from_string(c) for c in all_cards[39:52]],
            },
            'dealer': Position.NORTH,
            'bidding': [],
            'plays': []
        }
        
        assert validator.validate_parsed_data(data) is True
        assert len(validator.get_warnings()) > 0  # 应该有警告，因为没有叫牌和打牌记录


class TestBridgeDataNormalizer:
    """测试数据标准化器"""
    
    def test_normalize_positions(self):
        """测试方位标准化"""
        normalizer = BridgeDataNormalizer()
        
        data = {
            'dealer': 'n',
            'declarer': 's',
            'dummy': 'w'
        }
        
        normalized = normalizer.normalize(data)
        
        assert normalized['dealer'] == Position.NORTH
        assert normalized['declarer'] == Position.SOUTH
        assert normalized['dummy'] == Position.WEST
    
    def test_normalize_bidding(self):
        """测试叫牌标准化"""
        normalizer = BridgeDataNormalizer()
        
        data = {
            'bidding': [
                {'player': 'n', 'bid': '1h'},
                {'player': 'e', 'bid': 'pass'},
                {'player': 's', 'bid': 'dbl'},
                {'player': 'w', 'bid': 'rdbl'}
            ]
        }
        
        normalized = normalizer.normalize(data)
        
        assert normalized['bidding'][0]['bid'] == '1H'
        assert normalized['bidding'][1]['bid'] == 'PASS'
        assert normalized['bidding'][2]['bid'] == 'DBL'
        assert normalized['bidding'][3]['bid'] == 'RDBL'
    
    def test_normalize_contract_string(self):
        """测试定约字符串标准化"""
        normalizer = BridgeDataNormalizer()
        
        data = {
            'contract': '4hx'
        }
        
        normalized = normalizer.normalize(data)
        
        assert isinstance(normalized['contract'], dict)
        assert normalized['contract']['level'] == 4
        assert normalized['contract']['strain'] == 'H'
        assert normalized['contract']['doubled'] is True
        assert normalized['contract']['redoubled'] is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])