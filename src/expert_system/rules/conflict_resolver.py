"""
规则冲突解决器
Rule Conflict Resolver

解决多个规则同时激活时的冲突
"""

from typing import List, Dict, Any, Optional
from ..engine.expert_rule import ExpertRule


class ConflictResolutionStrategy:
    """冲突解决策略枚举"""
    HIGHEST_PRIORITY = "highest_priority"  # 最高优先级
    HIGHEST_SUCCESS_RATE = "highest_success_rate"  # 最高成功率
    MOST_ACTIVATED = "most_activated"  # 激活次数最多
    WEIGHTED_VOTING = "weighted_voting"  # 加权投票
    CONSENSUS = "consensus"  # 共识（需要多数同意）


class RuleConflictResolver:
    """
    规则冲突解决器
    
    当多个规则同时激活时，根据不同策略选择最佳规则
    """
    
    def __init__(self, default_strategy: str = ConflictResolutionStrategy.HIGHEST_PRIORITY):
        """
        初始化冲突解决器
        
        Args:
            default_strategy: 默认冲突解决策略
        """
        self.default_strategy = default_strategy
        self.resolution_history: List[Dict[str, Any]] = []
    
    def resolve(self, candidates: List[Dict[str, Any]], 
                strategy: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        解决规则冲突
        
        Args:
            candidates: 候选规则列表（包含rule, result, priority等）
            strategy: 冲突解决策略（如果为None则使用默认策略）
            
        Returns:
            解决冲突后的最佳规则，如果没有候选则返回None
        """
        if not candidates:
            return None
        
        if len(candidates) == 1:
            return candidates[0]
        
        strategy = strategy or self.default_strategy
        
        # 根据不同策略解决冲突
        if strategy == ConflictResolutionStrategy.HIGHEST_PRIORITY:
            resolved = self._resolve_by_priority(candidates)
        elif strategy == ConflictResolutionStrategy.HIGHEST_SUCCESS_RATE:
            resolved = self._resolve_by_success_rate(candidates)
        elif strategy == ConflictResolutionStrategy.MOST_ACTIVATED:
            resolved = self._resolve_by_activation(candidates)
        elif strategy == ConflictResolutionStrategy.WEIGHTED_VOTING:
            resolved = self._resolve_by_weighted_voting(candidates)
        elif strategy == ConflictResolutionStrategy.CONSENSUS:
            resolved = self._resolve_by_consensus(candidates)
        else:
            # 默认使用优先级
            resolved = self._resolve_by_priority(candidates)
        
        # 记录解决历史
        self.resolution_history.append({
            'candidates_count': len(candidates),
            'strategy_used': strategy,
            'resolved_rule': resolved['rule'].name if resolved else None,
            'candidate_rules': [c['rule'].name for c in candidates]
        })
        
        return resolved
    
    def _resolve_by_priority(self, candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        按优先级解决冲突
        
        Args:
            candidates: 候选规则列表
            
        Returns:
            优先级最高的规则
        """
        candidates.sort(key=lambda x: x['priority'], reverse=True)
        return candidates[0]
    
    def _resolve_by_success_rate(self, candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        按成功率解决冲突
        
        Args:
            candidates: 候选规则列表
            
        Returns:
            成功率最高的规则
        """
        # 过滤掉激活次数太少的规则（统计不稳定）
        stable_candidates = [
            c for c in candidates 
            if c['rule'].activation_count >= 5
        ]
        
        if stable_candidates:
            candidates = stable_candidates
        
        candidates.sort(key=lambda x: x['success_rate'], reverse=True)
        return candidates[0]
    
    def _resolve_by_activation(self, candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        按激活次数解决冲突
        
        Args:
            candidates: 候选规则列表
            
        Returns:
            激活次数最多的规则
        """
        candidates.sort(key=lambda x: x['rule'].activation_count, reverse=True)
        return candidates[0]
    
    def _resolve_by_weighted_voting(self, candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        按加权投票解决冲突
        
        权重 = 优先级 * 成功率 * 激活次数归一化
        
        Args:
            candidates: 候选规则列表
            
        Returns:
            加权得分最高的规则
        """
        max_activation = max(c['rule'].activation_count for c in candidates) or 1
        
        for candidate in candidates:
            rule = candidate['rule']
            # 计算加权得分
            score = (
                candidate['priority'] * 0.5 +
                candidate['success_rate'] * 100 * 0.3 +
                (rule.activation_count / max_activation) * 100 * 0.2
            )
            candidate['weighted_score'] = score
        
        candidates.sort(key=lambda x: x['weighted_score'], reverse=True)
        return candidates[0]
    
    def _resolve_by_consensus(self, candidates: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """
        按共识解决冲突
        
        需要至少2/3的候选规则给出相同的建议
        
        Args:
            candidates: 候选规则列表
            
        Returns:
            达成共识的规则，如果没有共识则返回优先级最高的
        """
        if len(candidates) < 3:
            # 候选规则太少，无法形成共识
            return self._resolve_by_priority(candidates)
        
        # 统计建议的相似性
        # 这里简化处理：如果至少2/3的规则推荐相同的动作类型
        action_types = {}
        for candidate in candidates:
            result = candidate['result']
            action_type = result.get('action_type', 'unknown')
            action_types[action_type] = action_types.get(action_type, 0) + 1
        
        # 检查是否有共识
        threshold = len(candidates) * 2 / 3
        consensus_type = None
        for action_type, count in action_types.items():
            if count >= threshold:
                consensus_type = action_type
                break
        
        if consensus_type:
            # 返回第一个推荐共识动作类型的规则（按优先级）
            for candidate in candidates:
                if candidate['result'].get('action_type') == consensus_type:
                    return candidate
        
        # 没有共识，使用优先级
        return self._resolve_by_priority(candidates)
    
    def get_resolution_statistics(self) -> Dict[str, Any]:
        """
        获取冲突解决统计信息
        
        Returns:
            统计信息字典
        """
        if not self.resolution_history:
            return {
                'total_resolutions': 0,
                'strategy_distribution': {}
            }
        
        strategy_count = {}
        for record in self.resolution_history:
            strategy = record['strategy_used']
            strategy_count[strategy] = strategy_count.get(strategy, 0) + 1
        
        return {
            'total_resolutions': len(self.resolution_history),
            'strategy_distribution': strategy_count,
            'average_candidates': sum(
                r['candidates_count'] for r in self.resolution_history
            ) / len(self.resolution_history),
            'most_used_strategy': max(strategy_count.items(), key=lambda x: x[1])[0] if strategy_count else None
        }
    
    def clear_history(self):
        """清空解决历史"""
        self.resolution_history = []
    
    def set_default_strategy(self, strategy: str):
        """
        设置默认冲突解决策略
        
        Args:
            strategy: 新的默认策略
        """
        if strategy in [
            ConflictResolutionStrategy.HIGHEST_PRIORITY,
            ConflictResolutionStrategy.HIGHEST_SUCCESS_RATE,
            ConflictResolutionStrategy.MOST_ACTIVATED,
            ConflictResolutionStrategy.WEIGHTED_VOTING,
            ConflictResolutionStrategy.CONSENSUS
        ]:
            self.default_strategy = strategy
        else:
            raise ValueError(f"Invalid conflict resolution strategy: {strategy}")
