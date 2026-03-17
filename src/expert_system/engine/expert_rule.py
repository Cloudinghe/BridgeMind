"""
专家规则定义
Expert Rule Definition

定义桥牌专家规则的数据结构
"""

from typing import Callable, Dict, Any, Optional, List
from abc import ABC, abstractmethod


class ExpertRule(ABC):
    """
    专家规则抽象基类
    
    定义专家规则的基本结构和接口
    """
    
    def __init__(self, name: str, description: str, priority: int = 0):
        """
        初始化专家规则
        
        Args:
            name: 规则名称
            description: 规则描述
            priority: 规则优先级（数字越大优先级越高）
        """
        self.name = name
        self.description = description
        self.priority = priority
        self.activation_count = 0
        self.success_count = 0
    
    @abstractmethod
    def condition(self, context: Dict[str, Any]) -> bool:
        """
        规则激活条件
        
        Args:
            context: 上下文信息，包含游戏状态、手牌等
            
        Returns:
            规则是否被激活
        """
        pass
    
    @abstractmethod
    def action(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        规则动作/建议
        
        Args:
            context: 上下文信息
            
        Returns:
            建议结果字典
        """
        pass
    
    def apply(self, context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        应用规则
        
        Args:
            context: 上下文信息
            
        Returns:
            如果规则被激活则返回建议，否则返回None
        """
        self.activation_count += 1
        
        if self.condition(context):
            self.success_count += 1
            return self.action(context)
        
        return None
    
    def get_success_rate(self) -> float:
        """
        获取规则成功率
        
        Returns:
            成功率（0-1之间）
        """
        if self.activation_count == 0:
            return 0.0
        return self.success_count / self.activation_count
    
    def __str__(self) -> str:
        """规则的字符串表示"""
        return f"Rule[{self.name}](priority={self.priority})"
    
    def __repr__(self) -> str:
        """规则的正式表示"""
        return f"ExpertRule(name='{self.name}', priority={self.priority})"


class TacticRule(ExpertRule):
    """
    战术规则
    
    用于打牌阶段的战术建议
    """
    
    def __init__(self, name: str, description: str, 
                 tactic_type: str, priority: int = 0):
        """
        初始化战术规则
        
        Args:
            name: 规则名称
            description: 规则描述
            tactic_type: 战术类型（如finesse, squeeze等）
            priority: 规则优先级
        """
        super().__init__(name, description, priority)
        self.tactic_type = tactic_type
    
    def get_tactic_type(self) -> str:
        """获取战术类型"""
        return self.tactic_type


class BiddingRule(ExpertRule):
    """
    叫牌规则
    
    用于叫牌阶段的叫牌建议
    """
    
    def __init__(self, name: str, description: str,
                 bid_type: str, priority: int = 0):
        """
        初始化叫牌规则
        
        Args:
            name: 规则名称
            description: 规则描述
            bid_type: 叫牌类型（如opening, response, overcall等）
            priority: 规则优先级
        """
        super().__init__(name, description, priority)
        self.bid_type = bid_type
    
    def get_bid_type(self) -> str:
        """获取叫牌类型"""
        return self.bid_type


class RuleCondition:
    """
    规则条件构建器
    
    用于构建复杂的规则条件
    """
    
    @staticmethod
    def always_true() -> Callable[[Dict[str, Any]], bool]:
        """总是返回True的条件"""
        return lambda context: True
    
    @staticmethod
    def always_false() -> Callable[[Dict[str, Any]], bool]:
        """总是返回False的条件"""
        return lambda context: False
    
    @staticmethod
    def has_key(key: str) -> Callable[[Dict[str, Any]], bool]:
        """
        检查上下文中是否存在某个键
        
        Args:
            key: 键名
            
        Returns:
            条件函数
        """
        return lambda context: key in context
    
    @staticmethod
    def equals(key: str, value: Any) -> Callable[[Dict[str, Any]], bool]:
        """
        检查键值是否等于指定值
        
        Args:
            key: 键名
            value: 期望值
            
        Returns:
            条件函数
        """
        return lambda context: context.get(key) == value
    
    @staticmethod
    def greater_than(key: str, threshold: Any) -> Callable[[Dict[str, Any]], bool]:
        """
        检查键值是否大于阈值
        
        Args:
            key: 键名
            threshold: 阈值
            
        Returns:
            条件函数
        """
        return lambda context: context.get(key, 0) > threshold
    
    @staticmethod
    def less_than(key: str, threshold: Any) -> Callable[[Dict[str, Any]], bool]:
        """
        检查键值是否小于阈值
        
        Args:
            key: 键名
            threshold: 阈值
            
        Returns:
            条件函数
        """
        return lambda context: context.get(key, float('inf')) < threshold
    
    @staticmethod
    def in_range(key: str, min_val: Any, max_val: Any) -> Callable[[Dict[str, Any]], bool]:
        """
        检查键值是否在指定范围内
        
        Args:
            key: 键名
            min_val: 最小值
            max_val: 最大值
            
        Returns:
            条件函数
        """
        return lambda context: min_val <= context.get(key, 0) <= max_val
    
    @staticmethod
    def contains(key: str, value: Any) -> Callable[[Dict[str, Any]], bool]:
        """
        检查键值（列表）是否包含指定元素
        
        Args:
            key: 键名
            value: 要查找的元素
            
        Returns:
            条件函数
        """
        return lambda context: value in context.get(key, [])
    
    @staticmethod
    def and_(*conditions: Callable[[Dict[str, Any]], bool]) -> Callable[[Dict[str, Any]], bool]:
        """
        逻辑与
        
        Args:
            *conditions: 条件列表
            
        Returns:
            组合条件函数
        """
        return lambda context: all(cond(context) for cond in conditions)
    
    @staticmethod
    def or_(*conditions: Callable[[Dict[str, Any]], bool]) -> Callable[[Dict[str, Any]], bool]:
        """
        逻辑或
        
        Args:
            *conditions: 条件列表
            
        Returns:
            组合条件函数
        """
        return lambda context: any(cond(context) for cond in conditions)
    
    @staticmethod
    def not_(condition: Callable[[Dict[str, Any]], bool]) -> Callable[[Dict[str, Any]], bool]:
        """
        逻辑非
        
        Args:
            condition: 条件
            
        Returns:
            取反后的条件函数
        """
        return lambda context: not condition(context)
