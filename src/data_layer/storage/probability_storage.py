"""
概率数据存储
Probability Storage

管理牌型分布概率的存储和查询
"""

import os
from typing import Dict, Optional
import h5py


class ProbabilityStorage:
    """概率数据存储类"""
    
    def __init__(self, storage_path: Optional[str] = None):
        """
        初始化概率存储
        
        Args:
            storage_path: 存储文件路径，如果为None则使用默认路径
        """
        if storage_path is None:
            # 默认存储在data目录
            data_dir = os.path.join(
                os.path.dirname(__file__), '..', '..', '..'
            )
            storage_path = os.path.join(data_dir, 'data', 'probability_tables.h5')
        
        self.storage_path = storage_path
        self.probabilities = {}
        self.load_probabilities()
    
    def save_probability(self, distribution: str, probability: float):
        """
        保存概率
        
        Args:
            distribution: 分布类型，如 "4-3-3-3"
            probability: 概率值
        """
        self.probabilities[distribution] = probability
        self._save_to_file()
    
    def get_probability(self, distribution: str) -> Optional[float]:
        """
        获取概率
        
        Args:
            distribution: 分布类型
            
        Returns:
            概率值，如果不存在则返回None
        """
        return self.probabilities.get(distribution)
    
    def load_probabilities(self):
        """加载概率表"""
        if os.path.exists(self.storage_path):
            try:
                with h5py.File(self.storage_path, 'r') as f:
                    for key in f.keys():
                        self.probabilities[key] = f[key][()]
            except Exception as e:
                print(f"Warning: Failed to load probabilities from {self.storage_path}: {e}")
                self.probabilities = {}
        else:
            # 如果文件不存在，初始化为空字典
            self.probabilities = {}
    
    def _save_to_file(self):
        """保存到文件"""
        # 确保目录存在
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        
        with h5py.File(self.storage_path, 'w') as f:
            for key, value in self.probabilities.items():
                f[key] = value
    
    def get_all_probabilities(self) -> Dict[str, float]:
        """
        获取所有概率
        
        Returns:
            所有概率的字典
        """
        return self.probabilities.copy()
    
    def save_probabilities(self, probabilities: Dict[str, float]):
        """
        批量保存概率
        
        Args:
            probabilities: 概率字典
        """
        self.probabilities = probabilities.copy()
        self._save_to_file()
    
    def clear_probabilities(self):
        """清空所有概率"""
        self.probabilities = {}
        self._save_to_file()
    
    def get_storage_path(self) -> str:
        """
        获取存储路径
        
        Returns:
            存储文件路径
        """
        return self.storage_path
    
    def get_probability_count(self) -> int:
        """
        获取已保存的概率数量
        
        Returns:
            概率数量
        """
        return len(self.probabilities)
