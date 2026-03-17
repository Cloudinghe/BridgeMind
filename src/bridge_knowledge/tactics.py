"""
战术模式模块
Tactic Patterns

定义和实现各种桥牌战术模式
"""

from typing import Callable, TYPE_CHECKING

if TYPE_CHECKING:
    from ..parser.models import GameState


class TacticPattern:
    """
    战术模式基类
    
    定义桥牌战术的模式匹配逻辑
    """
    
    def __init__(self, name: str, condition: Callable, score: int):
        """
        初始化战术模式
        
        Args:
            name: 战术名称
            condition: 战术触发条件函数
            score: 战术权重评分
        """
        self.name = name
        self.condition = condition  # 判断是否满足战术条件的函数
        self.score = score  # 战术权重评分
    
    def match(self, game_state: 'GameState') -> bool:
        """
        匹配当前牌局状态是否满足战术模式
        
        Args:
            game_state: 当前游戏状态
            
        Returns:
            是否匹配该战术模式
        """
        return self.condition(game_state)


class FinesseTactic(TacticPattern):
    """
    飞牌战术
    
    通过在某个方位出小牌，试图让另一个方位的大牌获胜
    """
    
    def __init__(self):
        super().__init__(
            name="飞牌战术",
            condition=lambda state: self._check_finesse_condition(state),
            score=80
        )
    
    def _check_finesse_condition(self, game_state: 'GameState') -> bool:
        """
        检查是否适合使用飞牌战术
        
        Args:
            game_state: 当前游戏状态
            
        Returns:
            是否适合使用飞牌
        """
        # TODO: 实现飞牌战术的判断逻辑
        # 需要检查：
        # 1. 是否缺少关键牌张（如K）
        # 2. 是否有足够的进手张
        # 3. 飞牌失败的风险是否可控
        
        return False
