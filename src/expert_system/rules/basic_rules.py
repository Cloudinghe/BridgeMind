"""
基础桥牌专家规则
Basic Bridge Expert Rules

实现10条核心的桥牌专家规则
"""

from typing import Dict, Any
from ..engine.expert_rule import TacticRule, BiddingRule, RuleCondition


class OpeningRules:
    """开叫规则"""
    
    @staticmethod
    def rule_1_open_with_12_plus_hcp() -> BiddingRule:
        """
        规则1：开叫规则
        
        当手牌高牌点≥12时应该开叫
        """
        class OpenWith12PlusHCP(BiddingRule):
            def condition(self, context: Dict[str, Any]) -> bool:
                hcp = context.get('hcp', 0)
                return hcp >= 12
            
            def action(self, context: Dict[str, Any]) -> Dict[str, Any]:
                return {
                    'action': 'open',
                    'reason': 'HCP >= 12',
                    'suggested_bid': context.get('suggested_bid', '1H')
                }
        
        return OpenWith12PlusHCP(
            name="open_with_12_plus_hcp",
            description="手牌高牌点≥12时应该开叫",
            bid_type="opening",
            priority=100
        )
    
    @staticmethod
    def rule_2_pass_with_less_than_12_hcp() -> BiddingRule:
        """
        规则2：PASS规则
        
        当手牌高牌点<12时应该PASS
        """
        class PassWithLessThan12HCP(BiddingRule):
            def condition(self, context: Dict[str, Any]) -> bool:
                hcp = context.get('hcp', 0)
                return hcp < 12
            
            def action(self, context: Dict[str, Any]) -> Dict[str, Any]:
                return {
                    'action': 'pass',
                    'reason': 'HCP < 12',
                    'suggested_bid': 'PASS'
                }
        
        return PassWithLessThan12HCP(
            name="pass_with_less_than_12_hcp",
            description="手牌高牌点<12时应该PASS",
            bid_type="opening",
            priority=90
        )
    
    @staticmethod
    def rule_3_open_notrump_15_17_balanced() -> BiddingRule:
        """
        规则3：1NT开叫
        
        当手牌高牌点15-17且平均牌型时开叫1NT
        """
        class OpenNotrump15_17Balanced(BiddingRule):
            def condition(self, context: Dict[str, Any]) -> bool:
                hcp = context.get('hcp', 0)
                distribution = context.get('distribution', '')
                is_balanced = (
                    '4-3-3-3' in distribution or
                    '4-4-3-2' in distribution or
                    '5-3-3-2' in distribution
                )
                return 15 <= hcp <= 17 and is_balanced
            
            def action(self, context: Dict[str, Any]) -> Dict[str, Any]:
                return {
                    'action': 'open_notrump',
                    'reason': '15-17 HCP且平均牌型',
                    'suggested_bid': '1NT'
                }
        
        return OpenNotrump15_17Balanced(
            name="open_notrump_15_17_balanced",
            description="手牌高牌点15-17且平均牌型时开叫1NT",
            bid_type="opening",
            priority=95
        )


class ResponseRules:
    """应叫规则"""
    
    @staticmethod
    def rule_4_respond_with_6_plus_hcp() -> BiddingRule:
        """
        规则4：应叫规则
        
        当搭档开叫且自己高牌点≥6时应叫
        """
        class RespondWith6PlusHCP(BiddingRule):
            def condition(self, context: Dict[str, Any]) -> bool:
                hcp = context.get('hcp', 0)
                partner_opened = context.get('partner_opened', False)
                return hcp >= 6 and partner_opened
            
            def action(self, context: Dict[str, Any]) -> Dict[str, Any]:
                return {
                    'action': 'respond',
                    'reason': 'HCP >= 6且搭档已开叫',
                    'suggested_bid': context.get('suggested_bid', '1H')
                }
        
        return RespondWith6PlusHCP(
            name="respond_with_6_plus_hcp",
            description="搭档开叫且自己高牌点≥6时应叫",
            bid_type="response",
            priority=85
        )


class TacticRules:
    """打牌战术规则"""
    
    @staticmethod
    def rule_5_lead_top_of_sequence() -> TacticRule:
        """
        规则5：首攻长四
        
        当首攻且有5张以上套时，首攻长四（第4大的牌）
        """
        class LeadTopOfSequence(TacticRule):
            def condition(self, context: Dict[str, Any]) -> bool:
                is_leading = context.get('is_leading', False)
                has_long_suit = context.get('has_long_suit', False)
                return is_leading and has_long_suit
            
            def action(self, context: Dict[str, Any]) -> Dict[str, Any]:
                return {
                    'action': 'lead_top_of_sequence',
                    'reason': '首攻且有5张以上长套',
                    'suggested_card': context.get('suggested_card', 'S4')
                }
        
        return LeadTopOfSequence(
            name="lead_top_of_sequence",
            description="首攻且有5张以上套时，首攻长四（第4大的牌）",
            tactic_type="lead",
            priority=80
        )
    
    @staticmethod
    def rule_6_finesse_when_possible() -> TacticRule:
        """
        规则6：飞牌战术
        
        当有飞牌机会时，尝试飞牌而不是硬砸
        """
        class FinesseWhenPossible(TacticRule):
            def condition(self, context: Dict[str, Any]) -> bool:
                has_finesse_opportunity = context.get('has_finesse_opportunity', False)
                return has_finesse_opportunity
            
            def action(self, context: Dict[str, Any]) -> Dict[str, Any]:
                return {
                    'action': 'finesse',
                    'reason': '有飞牌机会时，尝试飞牌而不是硬砸',
                    'suggested_card': context.get('suggested_card', 'HJ')
                }
        
        return FinesseWhenPossible(
            name="finesse_when_possible",
            description="有飞牌机会时，尝试飞牌而不是硬砸",
            tactic_type="finesse",
            priority=90
        )
    
    @staticmethod
    def rule_7_return_partner_suit() -> TacticRule:
        """
        规则7：回攻搭档花色
        
        当搭档出过牌时，回攻搭档花色表示支持
        """
        class ReturnPartnerSuit(TacticRule):
            def condition(self, context: Dict[str, Any]) -> bool:
                partner_played = context.get('partner_played', False)
                can_return = context.get('can_return', True)
                return partner_played and can_return
            
            def action(self, context: Dict[str, Any]) -> Dict[str, Any]:
                return {
                    'action': 'return_partner_suit',
                    'reason': '当搭档出过牌时，回攻搭档花色表示支持',
                    'suggested_card': context.get('suggested_card', 'S3')
                }
        
        return ReturnPartnerSuit(
            name="return_partner_suit",
            description="当搭档出过牌时，回攻搭档花色表示支持",
            tactic_type="lead",
            priority=75
        )
    
    @staticmethod
    def rule_8_third_hand_high() -> TacticRule:
        """
        规则8：第三家高攻
        
        作为第三家出牌时，出该花色最大的牌
        """
        class ThirdHandHigh(TacticRule):
            def condition(self, context: Dict[str, Any]) -> bool:
                is_third_hand = context.get('is_third_hand', False)
                return is_third_hand
            
            def action(self, context: Dict[str, Any]) -> Dict[str, Any]:
                return {
                    'action': 'third_hand_high',
                    'reason': '作为第三家出牌时，出该花色最大的牌',
                    'suggested_card': context.get('suggested_card', 'HA')
                }
        
        return ThirdHandHigh(
            name="third_hand_high",
            description="作为第三家出牌时，出该花色最大的牌",
            tactic_type="play",
            priority=70
        )


class SafetyRules:
    """安全规则"""
    
    @staticmethod
    def rule_9_dont_break_honor_sequence() -> TacticRule:
        """
        规则9：不打断大牌序列
        
        尽量保持A-K、K-Q等大牌序列的完整性
        """
        class DontBreakHonorSequence(TacticRule):
            def condition(self, context: Dict[str, Any]) -> bool:
                has_honor_sequence = context.get('has_honor_sequence', False)
                return has_honor_sequence
            
            def action(self, context: Dict[str, Any]) -> Dict[str, Any]:
                return {
                    'action': 'preserve_honors',
                    'reason': '尽量保持A-K、K-Q等大牌序列的完整性',
                    'suggested_card': context.get('suggested_card', 'SK')
                }
        
        return DontBreakHonorSequence(
            name="dont_break_honor_sequence",
            description="尽量保持A-K、K-Q等大牌序列的完整性",
            tactic_type="play",
            priority=85
        )
    
    @staticmethod
    def rule_10_preserve_entries() -> TacticRule:
        """
        规则10：保留进手张
        
        注意保留进手张，避免长套无法兑现
        """
        class PreserveEntries(TacticRule):
            def condition(self, context: Dict[str, Any]) -> bool:
                needs_entries = context.get('needs_entries', False)
                return needs_entries
            
            def action(self, context: Dict[str, Any]) -> Dict[str, Any]:
                return {
                    'action': 'preserve_entries',
                    'reason': '注意保留进手张，避免长套无法兑现',
                    'suggested_card': context.get('suggested_card', 'D2')
                }
        
        return PreserveEntries(
            name="preserve_entries",
            description="注意保留进手张，避免长套无法兑现",
            tactic_type="play",
            priority=80
        )


def get_basic_rules() -> list:
    """
    获取所有基础规则
    
    Returns:
        规则列表
    """
    return [
        OpeningRules.rule_1_open_with_12_plus_hcp(),
        OpeningRules.rule_2_pass_with_less_than_12_hcp(),
        OpeningRules.rule_3_open_notrump_15_17_balanced(),
        ResponseRules.rule_4_respond_with_6_plus_hcp(),
        TacticRules.rule_5_lead_top_of_sequence(),
        TacticRules.rule_6_finesse_when_possible(),
        TacticRules.rule_7_return_partner_suit(),
        TacticRules.rule_8_third_hand_high(),
        SafetyRules.rule_9_dont_break_honor_sequence(),
        SafetyRules.rule_10_preserve_entries(),
    ]
