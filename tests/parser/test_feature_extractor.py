"""
特征提取器测试
Tests for Feature Extractor
"""

import pytest
from src.parser.feature_extractor import (
    OpponentFeatureExtractor,
    BiddingFeatureExtractor,
    PlayFeatureExtractor,
    FeatureExtractorFactory,
)


class TestOpponentFeatureExtractor:
    """测试对手特征提取器"""
    
    def test_extractor_creation(self):
        """测试创建对手特征提取器"""
        extractor = OpponentFeatureExtractor()
        assert extractor is not None
    
    def test_extract_features(self):
        """测试提取对手特征"""
        extractor = OpponentFeatureExtractor()
        
        context = {
            'opponents': ['east', 'west'],
            'bidding_history': [
                {'player': 'east', 'bid': '1S', 'level': 1, 'strain': 'S'},
                {'player': 'west', 'bid': '2H', 'level': 2, 'strain': 'H'},
            ],
            'play_history': [
                {'player': 'east', 'is_attack': True, 'is_finesse': False},
                {'player': 'west', 'is_attack': False, 'is_finesse': True},
            ]
        }
        
        features = extractor.extract(context)
        
        assert 'aggressiveness' in features
        assert 'conservativeness' in features
        assert 'bidding_style' in features
        assert 'play_style' in features
        assert 'bluff_probability' in features
    
    def test_aggressiveness_calculation(self):
        """测试激进度计算"""
        extractor = OpponentFeatureExtractor()
        
        # 高激进度场景
        context = {
            'opponents': ['east'],
            'bidding_history': [
                {'player': 'east', 'bid': '2S', 'level': 2, 'strain': 'S'},
                {'player': 'east', 'bid': '3S', 'level': 3, 'strain': 'S'},
            ],
            'play_history': [
                {'player': 'east', 'is_attack': True, 'is_finesse': True},
            ]
        }
        
        features = extractor.extract(context)
        assert features['aggressiveness'] > 0.5
    
    def test_no_data_scenario(self):
        """测试无数据场景"""
        extractor = OpponentFeatureExtractor()
        
        context = {
            'opponents': ['east', 'west'],
            'bidding_history': [],
            'play_history': []
        }
        
        features = extractor.extract(context)
        
        # 应该返回默认值
        assert 0 <= features['aggressiveness'] <= 1
        assert 0 <= features['bluff_probability'] <= 1


class TestBiddingFeatureExtractor:
    """测试叫牌特征提取器"""
    
    def test_extractor_creation(self):
        """测试创建叫牌特征提取器"""
        extractor = BiddingFeatureExtractor()
        assert extractor is not None
    
    def test_extract_features(self):
        """测试提取叫牌特征"""
        extractor = BiddingFeatureExtractor()
        
        context = {
            'contract': {'level': 4, 'strain': 'H', 'declarer': 'S'},
            'bidding_history': [
                {'player': 'north', 'bid': '1H'},
                {'player': 'east', 'bid': '1S'},
                {'player': 'south', 'bid': '4H'},
            ]
        }
        
        features = extractor.extract(context)
        
        assert 'final_contract' in features
        assert 'bidding_sequence' in features
        assert 'partnership_strength' in features
        assert 'high_card_points' in features
        assert 'distribution' in features
        assert 'fitting' in features
        assert 'game_force' in features
        assert 'slam_interest' in features
    
    def test_bidding_sequence(self):
        """测试叫牌序列"""
        extractor = BiddingFeatureExtractor()
        
        context = {
            'contract': {},
            'bidding_history': [
                {'player': 'north', 'bid': '1H'},
                {'player': 'east', 'bid': '1S'},
                {'player': 'south', 'bid': '2H'},
            ]
        }
        
        features = extractor.extract(context)
        
        assert 'north: 1H' in features['bidding_sequence']
        assert 'east: 1S' in features['bidding_sequence']
        assert 'south: 2H' in features['bidding_sequence']


class TestPlayFeatureExtractor:
    """测试打牌特征提取器"""
    
    def test_extractor_creation(self):
        """测试创建打牌特征提取器"""
        extractor = PlayFeatureExtractor()
        assert extractor is not None
    
    def test_extract_features(self):
        """测试提取打牌特征"""
        extractor = PlayFeatureExtractor()
        
        context = {
            'play_history': [
                {'player': 'north', 'card': 'HA', 'is_signal': False, 'is_finesse': False, 'won_trick': True, 'winner': 'north'},
                {'player': 'east', 'card': 'S2', 'is_signal': True, 'signal_type': 'attitude', 'is_finesse': False},
                {'player': 'south', 'card': 'HK', 'is_signal': False, 'is_finesse': True, 'is_finesse': True, 'won_trick': True, 'winner': 'south'},
            ]
        }
        
        features = extractor.extract(context)
        
        assert 'play_pattern' in features
        assert 'signals' in features
        assert 'tactics_used' in features
        assert 'tricks_won' in features
        assert 'mistakes' in features
    
    def test_signal_extraction(self):
        """测试信号提取"""
        extractor = PlayFeatureExtractor()
        
        context = {
            'play_history': [
                {'player': 'east', 'card': 'S2', 'is_signal': True, 'signal_type': 'attitude', 'signal_meaning': 'like'},
            ]
        }
        
        features = extractor.extract(context)
        
        assert len(features['signals']) == 1
        assert features['signals'][0]['player'] == 'east'
        assert features['signals'][0]['type'] == 'attitude'
    
    def test_tactics_identification(self):
        """测试战术识别"""
        extractor = PlayFeatureExtractor()
        
        context = {
            'play_history': [
                {'player': 'south', 'card': 'HJ', 'is_finesse': True, 'is_squeeze': False},
                {'player': 'north', 'card': 'SA', 'is_finesse': False, 'is_squeeze': True},
                {'player': 'south', 'card': 'HA', 'is_finesse': False, 'is_endplay': True},
            ]
        }
        
        features = extractor.extract(context)
        
        assert 'finesse' in features['tactics_used']
        assert 'squeeze' in features['tactics_used']
        assert 'endplay' in features['tactics_used']
    
    def test_trick_counting(self):
        """测试赢墩统计"""
        extractor = PlayFeatureExtractor()
        
        context = {
            'play_history': [
                {'player': 'north', 'card': 'HA', 'won_trick': True, 'winner': 'north'},
                {'player': 'north', 'card': 'SA', 'won_trick': True, 'winner': 'north'},
                {'player': 'east', 'card': 'SK', 'won_trick': True, 'winner': 'east'},
            ]
        }
        
        features = extractor.extract(context)
        
        assert features['tricks_won']['north'] == 2
        assert features['tricks_won']['east'] == 1


class TestFeatureExtractorFactory:
    """测试特征提取器工厂"""
    
    def test_create_opponent_extractor(self):
        """测试创建对手特征提取器"""
        extractor = FeatureExtractorFactory.create_opponent_extractor()
        assert isinstance(extractor, OpponentFeatureExtractor)
    
    def test_create_bidding_extractor(self):
        """测试创建叫牌特征提取器"""
        extractor = FeatureExtractorFactory.create_bidding_extractor()
        assert isinstance(extractor, BiddingFeatureExtractor)
    
    def test_create_play_extractor(self):
        """测试创建打牌特征提取器"""
        extractor = FeatureExtractorFactory.create_play_extractor()
        assert isinstance(extractor, PlayFeatureExtractor)
    
    def test_create_all_extractors(self):
        """测试创建所有特征提取器"""
        extractors = FeatureExtractorFactory.create_all_extractors()
        
        assert 'opponent' in extractors
        assert 'bidding' in extractors
        assert 'play' in extractors
        assert isinstance(extractors['opponent'], OpponentFeatureExtractor)
        assert isinstance(extractors['bidding'], BiddingFeatureExtractor)
        assert isinstance(extractors['play'], PlayFeatureExtractor)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])