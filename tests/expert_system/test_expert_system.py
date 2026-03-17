"""
专家系统测试
Tests for Expert System
"""

import pytest
from src.expert_system import (
    ExpertRule, TacticRule, BiddingRule, RuleCondition,
    ExpertSystemEngine, RuleConflictResolver, ConflictResolutionStrategy
)
from src.expert_system.rules.basic_rules import get_basic_rules


class TestExpertRule:
    """测试专家规则基类"""
    
    def test_rule_creation(self):
        """测试规则创建"""
        rule = ExpertRule("test_rule", "Test rule", priority=10)
        assert rule.name == "test_rule"
        assert rule.description == "Test rule"
        assert rule.priority == 10
        assert rule.activation_count == 0
        assert rule.success_count == 0
    
    def test_tactic_rule_creation(self):
        """测试战术规则创建"""
        rule = TacticRule("test_tactic", "Test tactic", 
                          tactic_type="finesse", priority=15)
        assert rule.tactic_type == "finesse"
        assert isinstance(rule, ExpertRule)
    
    def test_bidding_rule_creation(self):
        """测试叫牌规则创建"""
        rule = BiddingRule("test_bidding", "Test bidding",
                          bid_type="opening", priority=20)
        assert rule.bid_type == "opening"
        assert isinstance(rule, ExpertRule)
    
    def test_get_success_rate(self):
        """测试成功率计算"""
        rule = ExpertRule("test", "Test")
        
        # 初始成功率为0
        assert rule.get_success_rate() == 0.0
        
        rule.activation_count = 10
        rule.success_count = 8
        
        assert rule.get_success_rate() == 0.8
    
    def test_rule_str_representation(self):
        """测试规则字符串表示"""
        rule = ExpertRule("test", "Test", priority=5)
        assert str(rule) == "Rule[test](priority=5)"


class TestRuleCondition:
    """测试规则条件构建器"""
    
    def test_always_true(self):
        """测试总是为True的条件"""
        condition = RuleCondition.always_true()
        assert condition({}) is True
    
    def test_always_false(self):
        """测试总是为False的条件"""
        condition = RuleCondition.always_false()
        assert condition({}) is False
    
    def test_has_key(self):
        """测试键存在条件"""
        condition = RuleCondition.has_key('hcp')
        assert condition({'hcp': 10}) is True
        assert condition({'suit': 'H'}) is False
    
    def test_equals(self):
        """测试相等条件"""
        condition = RuleCondition.equals('hcp', 12)
        assert condition({'hcp': 12}) is True
        assert condition({'hcp': 10}) is False
    
    def test_greater_than(self):
        """测试大于条件"""
        condition = RuleCondition.greater_than('hcp', 10)
        assert condition({'hcp': 12}) is True
        assert condition({'hcp': 10}) is False
    
    def test_less_than(self):
        """测试小于条件"""
        condition = RuleCondition.less_than('hcp', 15)
        assert condition({'hcp': 12}) is True
        assert condition({'hcp': 15}) is False
    
    def test_in_range(self):
        """测试范围条件"""
        condition = RuleCondition.in_range('hcp', 10, 15)
        assert condition({'hcp': 12}) is True
        assert condition({'hcp': 9}) is False
        assert condition({'hcp': 16}) is False
    
    def test_contains(self):
        """测试包含条件"""
        condition = RuleCondition.contains('suits', 'S')
        assert condition({'suits': ['S', 'H', 'D']}) is True
        assert condition({'suits': ['H', 'D', 'C']}) is False
    
    def test_and_condition(self):
        """测试逻辑与条件"""
        cond1 = RuleCondition.greater_than('hcp', 10)
        cond2 = RuleCondition.less_than('hcp', 15)
        
        condition = RuleCondition.and_(cond1, cond2)
        
        assert condition({'hcp': 12}) is True
        assert condition({'hcp': 9}) is False
        assert condition({'hcp': 16}) is False
    
    def test_or_condition(self):
        """测试逻辑或条件"""
        cond1 = RuleCondition.equals('hcp', 10)
        cond2 = RuleCondition.equals('hcp', 12)
        
        condition = RuleCondition.or_(cond1, cond2)
        
        assert condition({'hcp': 10}) is True
        assert condition({'hcp': 12}) is True
        assert condition({'hcp': 11}) is False
    
    def test_not_condition(self):
        """测试逻辑非条件"""
        cond = RuleCondition.greater_than('hcp', 10)
        condition = RuleCondition.not_(cond)
        
        assert condition({'hcp': 9}) is True
        assert condition({'hcp': 12}) is False


class TestExpertSystemEngine:
    """测试专家系统引擎"""
    
    def test_engine_creation(self):
        """测试引擎创建"""
        engine = ExpertSystemEngine()
        assert len(engine.rules) == 0
        assert len(engine.execution_history) == 0
    
    def test_add_rule(self):
        """测试添加规则"""
        engine = ExpertSystemEngine()
        rule = ExpertRule("test", "Test", priority=10)
        
        engine.add_rule(rule)
        
        assert len(engine.rules) == 1
        assert engine.rules[0] == rule
    
    def test_remove_rule(self):
        """测试移除规则"""
        engine = ExpertSystemEngine()
        rule = ExpertRule("test", "Test", priority=10)
        engine.add_rule(rule)
        
        success = engine.remove_rule("test")
        
        assert success is True
        assert len(engine.rules) == 0
    
    def test_get_rule(self):
        """测试获取规则"""
        engine = ExpertSystemEngine()
        rule = ExpertRule("test", "Test", priority=10)
        engine.add_rule(rule)
        
        retrieved = engine.get_rule("test")
        
        assert retrieved == rule
        assert engine.get_rule("nonexistent") is None
    
    def test_evaluate_with_no_rules(self):
        """测试无规则时的评估"""
        engine = ExpertSystemEngine()
        results = engine.evaluate({})
        
        assert len(results) == 0
    
    def test_get_rule_statistics(self):
        """测试获取规则统计"""
        engine = ExpertSystemEngine()
        
        # 添加规则
        for i in range(5):
            rule = ExpertRule(f"rule_{i}", f"Rule {i}", priority=i)
            engine.add_rule(rule)
        
        stats = engine.get_rule_statistics()
        
        assert stats['total_rules'] == 5
        assert stats['total_activations'] == 0
        assert len(stats['rule_statistics']) == 5
    
    def test_execution_history(self):
        """测试执行历史"""
        engine = ExpertSystemEngine()
        rule = ExpertRule("test", "Test", priority=10)
        engine.add_rule(rule)
        
        # 执行几次评估
        for i in range(3):
            engine.evaluate({})
        
        history = engine.get_execution_history(limit=10)
        
        assert len(history) == 3
    
    def test_clear_history(self):
        """测试清空历史"""
        engine = ExpertSystemEngine()
        engine.evaluate({})
        
        engine.clear_history()
        
        assert len(engine.execution_history) == 0
    
    def test_optimize_rules(self):
        """测试规则优化"""
        engine = ExpertSystemEngine()
        
        # 添加一些规则
        for i in range(10):
            rule = ExpertRule(f"rule_{i}", f"Rule {i}", priority=i)
            rule.activation_count = 20
            rule.success_count = 5  # 25%成功率，低于阈值
            engine.add_rule(rule)
        
        removed = engine.optimize_rules(threshold=0.5, min_activations=10)
        
        assert len(removed) == 10
        assert len(engine.rules) == 0


class TestRuleConflictResolver:
    """测试规则冲突解决器"""
    
    def test_resolver_creation(self):
        """测试解决器创建"""
        resolver = RuleConflictResolver()
        assert resolver.default_strategy == ConflictResolutionStrategy.HIGHEST_PRIORITY
        assert len(resolver.resolution_history) == 0
    
    def test_resolve_single_candidate(self):
        """测试单个候选解决"""
        resolver = RuleConflictResolver()
        
        candidates = [{'rule': 'rule1', 'priority': 10}]
        resolved = resolver.resolve(candidates)
        
        assert resolved == candidates[0]
    
    def test_resolve_empty_candidates(self):
        """测试空候选解决"""
        resolver = RuleConflictResolver()
        resolved = resolver.resolve([])
        
        assert resolved is None
    
    def test_resolve_by_priority(self):
        """测试按优先级解决"""
        resolver = RuleConflictResolver(
            default_strategy=ConflictResolutionStrategy.HIGHEST_PRIORITY
        )
        
        candidates = [
            {'rule': 'rule1', 'priority': 10},
            {'rule': 'rule2', 'priority': 20},
            {'rule': 'rule3', 'priority': 15},
        ]
        
        resolved = resolver.resolve(candidates)
        
        assert resolved['priority'] == 20
    
    def test_resolve_by_success_rate(self):
        """测试按成功率解决"""
        resolver = RuleConflictResolver(
            default_strategy=ConflictResolutionStrategy.HIGHEST_SUCCESS_RATE
        )
        
        candidates = [
            {'rule': 'rule1', 'priority': 10, 'success_rate': 0.6},
            {'rule': 'rule2', 'priority': 20, 'success_rate': 0.8},
            {'rule': 'rule3', 'priority': 15, 'success_rate': 0.7},
        ]
        
        resolved = resolver.resolve(candidates)
        
        assert resolved['success_rate'] == 0.8
    
    def test_resolve_statistics(self):
        """测试解决统计"""
        resolver = RuleConflictResolver()
        
        # 执行几次解决
        for i in range(5):
            resolver.resolve([{'rule': f'rule_{i}', 'priority': i}])
        
        stats = resolver.get_resolution_statistics()
        
        assert stats['total_resolutions'] == 5
        assert stats['most_used_strategy'] is not None
    
    def test_clear_history(self):
        """测试清空历史"""
        resolver = RuleConflictResolver()
        resolver.resolve([{'rule': 'test', 'priority': 10}])
        
        resolver.clear_history()
        
        assert len(resolver.resolution_history) == 0


class TestBasicRules:
    """测试基础规则"""
    
    def test_get_basic_rules(self):
        """测试获取基础规则"""
        rules = get_basic_rules()
        
        assert len(rules) == 10
    
    def test_basic_rules_types(self):
        """测试基础规则类型"""
        rules = get_basic_rules()
        
        # 检查是否包含预期的规则类型
        rule_names = [rule.name for rule in rules]
        
        assert 'open_with_12_plus_hcp' in rule_names
        assert 'pass_with_less_than_12_hcp' in rule_names
        assert 'open_notrump_15_17_balanced' in rule_names
        assert 'respond_with_6_plus_hcp' in rule_names
        assert 'lead_top_of_sequence' in rule_names
        assert 'finesse_when_possible' in rule_names


class TestExpertSystemIntegration:
    """测试专家系统集成"""
    
    def test_full_workflow(self):
        """测试完整工作流"""
        # 创建引擎
        engine = ExpertSystemEngine()
        
        # 添加基础规则
        rules = get_basic_rules()
        for rule in rules:
            engine.add_rule(rule)
        
        # 验证规则已添加
        assert len(engine.rules) == 10
        
        # 获取统计
        stats = engine.get_rule_statistics()
        assert stats['total_rules'] == 10
        
        # 创建冲突解决器
        resolver = RuleConflictResolver()
        
        # 解决冲突（即使没有激活的规则）
        candidates = [{'rule': rules[0], 'priority': rules[0].priority}]
        resolved = resolver.resolve(candidates)
        
        assert resolved is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])