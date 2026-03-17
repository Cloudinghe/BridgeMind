"""
叫牌体系
Bidding Systems

定义和实现桥牌叫牌体系
"""

from typing import Dict, List, Tuple
from .probability import CardDistributionProbability


class BiddingSystem:
    """叫牌体系基类"""
    
    def __init__(self, name: str):
        """
        初始化叫牌体系
        
        Args:
            name: 叫牌体系名称
        """
        self.name = name
        self.probability = CardDistributionProbability()
    
    def evaluate_hand(self, hcp: int, distribution: str) -> Dict[str, any]:
        """
        评估一手牌的叫牌价值
        
        Args:
            hcp: 高牌点
            distribution: 牌型分布（如"5-3-3-2"）
            
        Returns:
            评估结果字典
        """
        result = {
            'hcp': hcp,
            'distribution': distribution,
            'high_card_points': self._get_high_card_points(hcp),
            'distribution_points': self._get_distribution_points(distribution),
            'total_points': hcp + self._get_distribution_points(distribution),
            'suggested_opening': None,
            'opening_probability': 0.0
        }
        
        # 计算开叫概率
        result['opening_probability'] = self.probability.get_distribution_probability(distribution)
        result['suggested_opening'] = self._suggest_opening(hcp, distribution)
        
        return result
    
    def _get_high_card_points(self, hcp: int) -> str:
        """
        获取高牌点评估
        
        Args:
            hcp: 高牌点
            
        Returns:
            高牌点评估字符串
        """
        if hcp < 6:
            return "very_weak"
        elif hcp < 10:
            return "weak"
        elif hcp < 13:
            return "medium"
        elif hcp < 16:
            return "good"
        elif hcp < 19:
            return "strong"
        elif hcp < 22:
            return "very_strong"
        else:
            return "slam"
    
    def _get_distribution_points(self, distribution: str) -> int:
        """
        获取牌型点数（长套点）
        
        Args:
            distribution: 牌型分布
            
        Returns:
            牌型点数
        """
        points = 0
        parts = list(map(int, distribution.split('-')))
        
        # 长套点：5张以上长套，每超过5张+1点
        for part in parts:
            if part > 5:
                points += part - 5
            # 单张缺门点：缺门+3点，单张+2点
            elif part == 0:
                points += 3
            elif part == 1:
                points += 2
        
        return points
    
    def _suggest_opening(self, hcp: int, distribution: str) -> str:
        """
        建议开叫
        
        Args:
            hcp: 高牌点
            distribution: 牌型分布
            
        Returns:
            建议的开叫（如"1H", "1NT"）
        """
        parts = list(map(int, distribution.split('-')))
        max_length = max(parts)
        max_index = parts.index(max_length)
        
        # 找到最长套
        suits = ['S', 'H', 'D', 'C']
        longest_suit = suits[max_index]
        
        # 计算长套数量
        long_suits = sum(1 for p in parts if p >= 5)
        
        # 判断是否平均牌型
        is_balanced = (
            '4-3-3-3' in distribution or
            '4-4-3-2' in distribution or
            '5-3-3-2' in distribution
        )
        
        # 开叫建议逻辑
        if hcp < 12:
            return "PASS"
        elif is_balanced and 15 <= hcp <= 17:
            return "1NT"
        elif is_balanced and 20 <= hcp <= 21:
            return "2NT"
        elif max_length >= 5:
            # 高花优先
            if longest_suit in ['S', 'H']:
                return f"1{longest_suit}"
            else:
                return f"1{longest_suit}"
        elif max_length == 4:
            # 两个4张高花，优先开叫高花
            if parts[0] == 4 and parts[1] == 4:
                return "1S"  # 两个4张高花，优先黑桃
            elif parts[0] == 4:
                return "1S"
            elif parts[1] == 4:
                return "1H"
            else:
                return "1D"  # 准备叫低花
        else:
            return "1C"  # 约定叫


class NaturalBiddingSystem(BiddingSystem):
    """自然叫牌体系"""
    
    def __init__(self):
        super().__init__("Natural System")
    
    def evaluate_hand(self, hcp: int, distribution: str) -> Dict[str, any]:
        """
        使用自然叫牌体系评估一手牌
        
        Args:
            hcp: 高牌点
            distribution: 牌型分布
            
        Returns:
            评估结果字典
        """
        result = super().evaluate_hand(hcp, distribution)
        result['system'] = 'natural'
        
        # 自然叫牌体系特有的评估
        result['natural_eval'] = {
            'five_card_majors': self._has_five_card_majors(distribution),
            'balanced': self._is_balanced(distribution),
            'strong_notrump_range': (15, 17),
            'weak_notrump_range': (12, 14)
        }
        
        return result
    
    def _has_five_card_majors(self, distribution: str) -> Tuple[bool, bool]:
        """
        是否有5张高花
        
        Args:
            distribution: 牌型分布
            
        Returns:
            (有5张黑桃, 有5张红心)
        """
        parts = list(map(int, distribution.split('-')))
        return (parts[0] >= 5, parts[1] >= 5)
    
    def _is_balanced(self, distribution: str) -> bool:
        """
        是否为平均牌型
        
        Args:
            distribution: 牌型分布
            
        Returns:
            是否为平均牌型
        """
        balanced_distributions = ['4-3-3-3', '4-4-3-2', '5-3-3-2']
        return distribution in balanced_distributions


class PrecisionBiddingSystem(BiddingSystem):
    """精确叫牌体系"""
    
    def __init__(self):
        super().__init__("Precision System")
    
    def evaluate_hand(self, hcp: int, distribution: str) -> Dict[str, any]:
        """
        使用精确叫牌体系评估一手牌
        
        Args:
            hcp: 高牌点
            distribution: 牌型分布
            
        Returns:
            评估结果字典
        """
        result = super().evaluate_hand(hcp, distribution)
        result['system'] = 'precision'
        
        # 精确叫牌体系特有的评估
        result['precision_eval'] = {
            'strong_club_range': (16, 18),
            'weak_notrump_range': (13, 15),
            'strong_notrump_range': (14, 15)
        }
        
        # 精确体系1C是约定叫
        if 16 <= hcp <= 18:
            result['suggested_opening'] = "1C (Strong)"
        
        return result


class BlueClubBiddingSystem(BiddingSystem):
    """蓝梅花叫牌体系"""
    
    def __init__(self):
        super().__init__("Blue Club System")
    
    def evaluate_hand(self, hcp: int, distribution: str) -> Dict[str, any]:
        """
        使用蓝梅花叫牌体系评估一手牌
        
        Args:
            hcp: 高牌点
            distribution: 牌型分布
            
        Returns:
            评估结果字典
        """
        result = super().evaluate_hand(hcp, distribution)
        result['system'] = 'blue_club'
        
        # 蓝梅花体系特有的评估
        result['blue_club_eval'] = {
            'club_range': (17, 18),
            'notrump_range': (13, 16),
            'two_club_range': (19, 20)
        }
        
        return result
