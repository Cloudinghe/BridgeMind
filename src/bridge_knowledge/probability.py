"""
牌型分布概率计算模块
Card Distribution Probability

计算和存储桥牌牌型分布的概率数据
"""

from typing import Dict


class CardDistributionProbability:
    """
    牌型分布概率计算器
    
    计算52张牌在四个方位的各种分布概率
    """
    
    def __init__(self):
        # 预计算的牌型分布概率表
        self.distribution_probs = {
            # 4-3-3-3分布概率21.55%
            '4-3-3-3': 0.2155,
            # 4-4-3-2分布概率21.55%
            '4-4-3-2': 0.2155,
            # 5-3-3-2分布概率15.52%
            '5-3-3-2': 0.1552,
            # 5-4-3-1分布概率12.93%
            '5-4-3-1': 0.1293,
            # 5-4-2-2分布概率10.58%
            '5-4-2-2': 0.1058,
            # 4-4-4-1分布概率2.99%
            '4-4-4-1': 0.0299,
            # 其他常见分布...
            '5-5-2-1': 0.0317,
            '5-5-3-0': 0.0090,
            '6-3-2-2': 0.0470,
            '6-3-3-1': 0.0345,
            '6-4-2-1': 0.0196,
            '6-4-3-0': 0.0062,
            '6-5-1-1': 0.0065,
            '6-5-2-0': 0.0030,
            '6-6-1-0': 0.0007,
            '7-2-2-2': 0.0051,
            '7-3-2-1': 0.0038,
            '7-3-3-0': 0.0026,
            '7-4-1-1': 0.0039,
            '7-4-2-0': 0.0018,
            '7-5-1-0': 0.0005,
            '7-6-0-0': 0.0001,
            '8-2-2-1': 0.0019,
            '8-3-1-1': 0.0012,
            '8-3-2-0': 0.0005,
            '8-4-1-0': 0.0003,
            '9-2-1-1': 0.0002,
            '9-2-2-0': 0.0001,
            '9-3-1-0': 0.0000,
            '10-1-1-1': 0.0000,
            '10-2-1-0': 0.0000,
            '11-1-1-0': 0.0000,
            '12-1-0-0': 0.0000,
            '13-0-0-0': 0.0000,
        }
    
    def get_distribution_probability(self, distribution: str) -> float:
        """
        获取指定牌型分布的概率
        
        Args:
            distribution: 分布类型，如 "4-3-3-3", "5-4-3-1"
            
        Returns:
            概率值（0-1之间）
        """
        return self.distribution_probs.get(distribution, 0.0)
    
    def get_all_distributions(self) -> Dict[str, float]:
        """
        获取所有已知的牌型分布及其概率
        
        Returns:
            字典，键为分布类型，值为概率
        """
        return self.distribution_probs.copy()
    
    def is_valid_distribution(self, distribution: str) -> bool:
        """
        验证牌型分布是否有效
        
        Args:
            distribution: 分布类型
            
        Returns:
            是否有效
        """
        # 检查格式是否正确
        if not distribution:
            return False
        
        parts = distribution.split('-')
        if len(parts) != 4:
            return False
        
        # 检查每部分是否为数字且和为13
        try:
            numbers = [int(p) for p in parts]
            return sum(numbers) == 13
        except ValueError:
            return False