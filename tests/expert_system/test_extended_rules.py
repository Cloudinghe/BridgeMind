"""
扩展专家规则测试
Tests for Extended Expert Rules
"""

import pytest
from src.expert_system.rules import get_extended_rules


class TestExtendedRules:
    """测试扩展规则"""
    
    def test_get_extended_rules_count(self):
        """测试扩展规则数量"""
        rules = get_extended_rules()
        # 应该有18条扩展规则（10-28）
        assert len(rules) == 18
    
    def test_extended_rules_types(self):
        """测试扩展规则类型"""
        rules = get_extended_rules()
        rule_names = [rule.name for rule in rules]
        
        # 检查是否包含预期的规则类型
        assert 'open_weak_2_major' in rule_names
        assert 'preemptive_3_bid' in rule_names
        assert 'new_suit_response' in rule_names
        assert 'support_partner' in rule_names
        assert 'lead_top_from_sequence' in rule_names
        assert 'lead_partner_suit' in rule_names
        assert 'lead_top_of_honor_doubleton' in rule_names
        assert 'draw_trumps_first' in rule_names
        assert 'finesse_to_honor' in rule_names
        assert 'establish_long_suit' in rule_names
        assert 'second_hand_low' in rule_names
        assert 'third_hand_high' in rule_names
        assert 'cover_honor_with_honor' in rule_names
        assert 'signal_attitude' in rule_names
        assert 'squeeze_play' in rule_names
        assert 'endplay' in rule_names
        assert 'unblock' in rule_names
        assert 'promote_minor' in rule_names
    
    def test_all_extended_rules_are_callable(self):
        """测试所有扩展规则都是可调用的"""
        rules = get_extended_rules()
        
        for rule in rules:
            assert hasattr(rule, 'condition'), f"Rule {rule.name} missing condition method"
            assert hasattr(rule, 'action'), f"Rule {rule.name} missing action method"
            assert hasattr(rule, 'apply'), f"Rule {rule.name} missing apply method"
    
    def test_all_rules_have_metadata(self):
        """测试所有规则都有元数据"""
        rules = get_extended_rules()
        
        for rule in rules:
            assert rule.name, f"Rule missing name"
            assert rule.description, f"Rule {rule.name} missing description"
            assert rule.priority is not None, f"Rule {rule.name} missing priority"
            assert 0 <= rule.priority <= 100, f"Rule {rule.name} has invalid priority {rule.priority}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])