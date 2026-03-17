"""
专家系统引擎
Expert System Engine

实现专家规则推理引擎
"""

from typing import List, Dict, Any, Optional, Tuple
from collections import defaultdict

from .expert_rule import ExpertRule, TacticRule, BiddingRule, RuleCondition


class ExpertSystemEngine:
    """
    专家系统引擎
    
    负责规则的加载、匹配、执行和冲突解决
    """
    
    def __init__(self):
        """初始化专家系统引擎"""
        self.rules: List[ExpertRule] = []
        self.rule_index: Dict[str, List[ExpertRule]] = defaultdict(list)
        self.execution_history: List[Dict[str, Any]] = []
    
    def add_rule(self, rule: ExpertRule):
        """
        添加规则
        
        Args:
            rule: 专家规则对象
        """
        self.rules.append(rule)
        
        # 按规则类型建立索引
        rule_type = 'general'
        if isinstance(rule, TacticRule):
            rule_type = f'tactic_{rule.get_tactic_type()}'
        elif isinstance(rule, BiddingRule):
            rule_type = f'bidding_{rule.get_bid_type()}'
        
        self.rule_index[rule_type].append(rule)
        
        # 按优先级排序
        self.rules.sort(key=lambda r: r.priority, reverse=True)
        for rules in self.rule_index.values():
            rules.sort(key=lambda r: r.priority, reverse=True)
    
    def remove_rule(self, rule_name: str) -> bool:
        """
        移除规则
        
        Args:
            rule_name: 规则名称
            
        Returns:
            是否成功移除
        """
        for i, rule in enumerate(self.rules):
            if rule.name == rule_name:
                # 从索引中移除
                rule_type = 'general'
                if isinstance(rule, TacticRule):
                    rule_type = f'tactic_{rule.get_tactic_type()}'
                elif isinstance(rule, BiddingRule):
                    rule_type = f'bidding_{rule.get_bid_type()}'
                
                if rule_name in self.rule_index[rule_type]:
                    self.rule_index[rule_type].remove(rule)
                
                # 从规则列表中移除
                self.rules.pop(i)
                return True
        
        return False
    
    def get_rule(self, rule_name: str) -> Optional[ExpertRule]:
        """
        获取规则
        
        Args:
            rule_name: 规则名称
            
        Returns:
            规则对象，不存在则返回None
        """
        for rule in self.rules:
            if rule.name == rule_name:
                return rule
        return None
    
    def get_rules_by_type(self, rule_type: str) -> List[ExpertRule]:
        """
        按类型获取规则
        
        Args:
            rule_type: 规则类型（如'tactic_finesse', 'bidding_opening'）
            
        Returns:
            规则列表
        """
        return self.rule_index.get(rule_type, [])
    
    def evaluate(self, context: Dict[str, Any], 
                max_results: int = 5) -> List[Dict[str, Any]]:
        """
        评估上下文，返回匹配的规则建议
        
        Args:
            context: 上下文信息
            max_results: 最大返回结果数
            
        Returns:
            匹配的规则建议列表（按优先级排序）
        """
        matched_rules = []
        
        for rule in self.rules:
            result = rule.apply(context)
            if result is not None:
                matched_rules.append({
                    'rule': rule,
                    'result': result,
                    'priority': rule.priority,
                    'success_rate': rule.get_success_rate()
                })
        
        # 按优先级排序
        matched_rules.sort(key=lambda x: (x['priority'], x['success_rate']), reverse=True)
        
        # 记录执行历史
        self.execution_history.append({
            'context': context,
            'matched_count': len(matched_rules),
            'rules': [r['rule'].name for r in matched_rules[:max_results]]
        })
        
        return matched_rules[:max_results]
    
    def get_top_recommendation(self, context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        获取最高优先级的推荐
        
        Args:
            context: 上下文信息
            
        Returns:
            最佳推荐，如果没有匹配规则则返回None
        """
        results = self.evaluate(context, max_results=1)
        if results:
            return results[0]
        return None
    
    def resolve_conflicts(self, candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        解决规则冲突
        
        Args:
            candidates: 候选规则列表
            
        Returns:
            解决冲突后的最佳规则
        """
        if not candidates:
            return None
        
        if len(candidates) == 1:
            return candidates[0]
        
        # 冲突解决策略：
        # 1. 优先级最高的优先
        # 2. 成功率高的优先
        # 3. 激活次数多的优先
        
        candidates.sort(key=lambda x: (
            x['priority'],
            x['success_rate'],
            x['rule'].activation_count
        ), reverse=True)
        
        return candidates[0]
    
    def get_rule_statistics(self) -> Dict[str, Any]:
        """
        获取规则统计信息
        
        Returns:
            统计信息字典
        """
        total_rules = len(self.rules)
        total_activations = sum(rule.activation_count for rule in self.rules)
        total_successes = sum(rule.success_count for rule in self.rules)
        
        rule_stats = []
        for rule in self.rules:
            rule_type = 'general'
            if isinstance(rule, TacticRule):
                rule_type = f'tactic_{rule.get_tactic_type()}'
            elif isinstance(rule, BiddingRule):
                rule_type = f'bidding_{rule.get_bid_type()}'
            
            rule_stats.append({
                'name': rule.name,
                'type': rule_type,
                'priority': rule.priority,
                'activation_count': rule.activation_count,
                'success_count': rule.success_count,
                'success_rate': rule.get_success_rate()
            })
        
        # 按激活次数排序
        rule_stats.sort(key=lambda x: x['activation_count'], reverse=True)
        
        return {
            'total_rules': total_rules,
            'total_activations': total_activations,
            'total_successes': total_successes,
            'overall_success_rate': total_successes / total_activations if total_activations > 0 else 0,
            'execution_count': len(self.execution_history),
            'rule_statistics': rule_stats
        }
    
    def get_execution_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        获取执行历史
        
        Args:
            limit: 返回历史记录数量
            
        Returns:
            执行历史列表
        """
        return self.execution_history[-limit:]
    
    def clear_history(self):
        """清空执行历史"""
        self.execution_history = []
    
    def export_rules(self) -> List[Dict[str, Any]]:
        """
        导出所有规则
        
        Returns:
            规则字典列表
        """
        exported_rules = []
        for rule in self.rules:
            rule_data = {
                'name': rule.name,
                'description': rule.description,
                'priority': rule.priority,
                'activation_count': rule.activation_count,
                'success_count': rule.success_count,
                'success_rate': rule.get_success_rate()
            }
            
            if isinstance(rule, TacticRule):
                rule_data['type'] = 'tactic'
                rule_data['tactic_type'] = rule.get_tactic_type()
            elif isinstance(rule, BiddingRule):
                rule_data['type'] = 'bidding'
                rule_data['bid_type'] = rule.get_bid_type()
            else:
                rule_data['type'] = 'general'
            
            exported_rules.append(rule_data)
        
        return exported_rules
    
    def import_rule(self, rule: ExpertRule):
        """
        导入规则（添加规则的便捷方法）
        
        Args:
            rule: 规则对象
        """
        self.add_rule(rule)
    
    def reset_statistics(self):
        """重置所有规则统计信息"""
        for rule in self.rules:
            rule.activation_count = 0
            rule.success_count = 0
    
    def optimize_rules(self, threshold: float = 0.5, min_activations: int = 10) -> List[str]:
        """
        优化规则，移除低效规则
        
        Args:
            threshold: 成功率阈值
            min_activations: 最小激活次数
            
        Returns:
            被移除的规则名称列表
        """
        removed_rules = []
        
        for rule in self.rules[:]:  # 创建副本遍历
            if (rule.activation_count >= min_activations and 
                rule.get_success_rate() < threshold):
                self.remove_rule(rule.name)
                removed_rules.append(rule.name)
        
        return removed_rules
