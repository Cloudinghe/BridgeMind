"""
扩展桥牌专家规则
Extended Bridge Expert Rules

实现更多桥牌专家规则（首攻、做庄、防守、残局等）
"""

from typing import Dict, Any
from ..engine.expert_rule import TacticRule, BiddingRule, RuleCondition


class OpeningRulesExtended:
    """扩展开叫规则"""
    
    @staticmethod
    def rule_11_open_weak_2_major() -> BiddingRule:
        """
        规则11：弱二开叫
        
        当有6张高花且6-10点时开叫弱二（2S/2H）
        """
        class OpenWeak2Major(BiddingRule):
            def condition(self, context: Dict[str, Any]) -> bool:
                hcp = context.get('hcp', 0)
                distribution = context.get('distribution', '')
                parts = list(map(int, distribution.split('-')))
                spade_length = parts[0]
                heart_length = parts[1]
                return (6 <= hcp <= 10) and (spade_length >= 6 or heart_length >= 6)
            
            def action(self, context: Dict[str, Any]) -> Dict[str, Any]:
                return {
                    'action': 'open_weak_2',
                    'reason': '6张高花且6-10点',
                    'suggested_bid': context.get('suggested_bid', '2S')
                }
        
        return OpenWeak2Major(
            name="open_weak_2_major",
            description="有6张高花且6-10点时开叫弱二（2S/2H）",
            bid_type="opening",
            priority=85
        )
    
    @staticmethod
    def rule_12_preemptive_3_bid() -> BiddingRule:
        """
        规则12：阻击性3阶开叫
        
        当有7张套且5-9点时开叫3阶阻击
        """
        class Preemptive3Bid(BiddingRule):
            def condition(self, context: Dict[str, Any]) -> bool:
                hcp = context.get('hcp', 0)
                distribution = context.get('distribution', '')
                parts = list(map(int, distribution.split('-')))
                max_length = max(parts)
                return (5 <= hcp <= 9) and max_length >= 7
            
            def action(self, context: Dict[str, Any]) -> Dict[str, Any]:
                return {
                    'action': 'preemptive_3',
                    'reason': '7张套且5-9点，阻击开叫',
                    'suggested_bid': context.get('suggested_bid', '3H')
                }
        
        return Preemptive3Bid(
            name="preemptive_3_bid",
            description="有7张套且5-9点时开叫3阶阻击",
            bid_type="opening",
            priority=80
        )


class ResponseRulesExtended:
    """扩展应叫规则"""
    
    @staticmethod
    def rule_13_new_suit_response() -> BiddingRule:
        """
        规则13：新花应叫
        
        当搭档开叫1阶，自己有6点以上且有4张以上新花时，应叫新花
        """
        class NewSuitResponse(BiddingRule):
            def condition(self, context: Dict[str, Any]) -> bool:
                hcp = context.get('hcp', 0)
                partner_opened = context.get('partner_opened', False)
                has_new_suit = context.get('has_new_suit', False)
                return hcp >= 6 and partner_opened and has_new_suit
            
            def action(self, context: Dict[str, Any]) -> Dict[str, Any]:
                return {
                    'action': 'new_suit_response',
                    'reason': '6点以上且有4张以上新花',
                    'suggested_bid': context.get('suggested_bid', '1S')
                }
        
        return NewSuitResponse(
            name="new_suit_response",
            description="搭档开叫且自己有6点以上和4张以上新花时，应叫新花",
            bid_type="response",
            priority=80
        )
    
    @staticmethod
    def rule_14_support_partner() -> BiddingRule:
        """
        规则14：支持搭档花色
        
        当搭档开叫高花且自己有3张以上支持时，应叫支持
        """
        class SupportPartner(BiddingRule):
            def condition(self, context: Dict[str, Any]) -> bool:
                partner_bid = context.get('partner_bid', '')
                has_support = context.get('has_support', False)
                hcp = context.get('hcp', 0)
                is_major_bid = partner_bid in ['1S', '1H', '2S', '2H']
                return hcp >= 6 and is_major_bid and has_support
            
            def action(self, context: Dict[str, Any]) -> Dict[str, Any]:
                return {
                    'action': 'support_partner',
                    'reason': '有3张以上支持搭档高花',
                    'suggested_bid': context.get('suggested_bid', '2H')
                }
        
        return SupportPartner(
            name="support_partner",
            description="搭档开叫高花且自己有3张以上支持时，应叫支持",
            bid_type="response",
            priority=82
        )


class LeadingRules:
    """首攻规则"""
    
    @staticmethod
    def rule_15_lead_top_from_sequence() -> TacticRule:
        """
        规则15：大牌序列首攻
        
        当有AKQ、KQJ等连续大牌时，首攻最大牌
        """
        class LeadTopFromSequence(TacticRule):
            def condition(self, context: Dict[str, Any]) -> bool:
                is_leading = context.get('is_leading', False)
                has_sequence = context.get('has_sequence', False)
                return is_leading and has_sequence
            
            def action(self, context: Dict[str, Any]) -> Dict[str, Any]:
                return {
                    'action': 'lead_top_from_sequence',
                    'reason': '有连续大牌序列，首攻最大牌',
                    'suggested_card': context.get('suggested_card', 'SA')
                }
        
        return LeadTopFromSequence(
            name="lead_top_from_sequence",
            description="有AKQ、KQJ等连续大牌时，首攻最大牌",
            tactic_type="lead",
            priority=88
        )
    
    @staticmethod
    def rule_16_lead_partner_suit() -> TacticRule:
        """
        规则16：首攻搭档叫过的花色
        
        当搭档叫过花色时，优先首攻该花色
        """
        class LeadPartnerSuit(TacticRule):
            def condition(self, context: Dict[str, Any]) -> bool:
                is_leading = context.get('is_leading', False)
                partner_bid_suit = context.get('partner_bid_suit', '')
                has_partner_suit = bool(partner_bid_suit)
                return is_leading and has_partner_suit
            
            def action(self, context: Dict[str, Any]) -> Dict[str, Any]:
                return {
                    'action': 'lead_partner_suit',
                    'reason': '首攻搭档叫过的花色表示支持',
                    'suggested_card': context.get('suggested_card', 'SK')
                }
        
        return LeadPartnerSuit(
            name="lead_partner_suit",
            description="首攻搭档叫过的花色表示支持",
            tactic_type="lead",
            priority=85
        )
    
    @staticmethod
    def rule_17_lead_top_of_honor_doubleton() -> TacticRule:
        """
        规则17：双张大牌首攻
        
        当有双张大牌（如AK、KQ）时，首攻大牌
        """
        class LeadTopOfHonorDoubleton(TacticRule):
            def condition(self, context: Dict[str, Any]) -> bool:
                is_leading = context.get('is_leading', False)
                has_honor_doubleton = context.get('has_honor_doubleton', False)
                return is_leading and has_honor_doubleton
            
            def action(self, context: Dict[str, Any]) -> Dict[str, Any]:
                return {
                    'action': 'lead_honor_doubleton',
                    'reason': '双张大牌首攻大牌',
                    'suggested_card': context.get('suggested_card', 'HA')
                }
        
        return LeadTopOfHonorDoubleton(
            name="lead_top_of_honor_doubleton",
            description="有双张大牌（如AK、KQ）时，首攻大牌",
            tactic_type="lead",
            priority=83
        )


class DeclarerPlayRules:
    """庄家打牌规则"""
    
    @staticmethod
    def rule_18_draw_trumps_first() -> TacticRule:
        """
        规则18：先清将牌
        
        定约人应该优先清将牌，避免对方将吃
        """
        class DrawTrumpsFirst(TacticRule):
            def condition(self, context: Dict[str, Any]) -> bool:
                is_declarer = context.get('is_declarer', False)
                has_trump_control = context.get('has_trump_control', True)
                return is_declarer and has_trump_control
            
            def action(self, context: Dict[str, Any]) -> Dict[str, Any]:
                return {
                    'action': 'draw_trumps_first',
                    'reason': '优先清将牌，避免对方将吃',
                    'suggested_card': context.get('suggested_card', 'SA')
                }
        
        return DrawTrumpsFirst(
            name="draw_trumps_first",
            description="定约人应该优先清将牌，避免对方将吃",
            tactic_type="play",
            priority=90
        )
    
    @staticmethod
    def rule_19_finesse_to_honor() -> TacticRule:
        """
        规则19：飞牌大牌
        
        当需要捕捉对方大牌时，使用飞牌战术
        """
        class FinesseToHonor(TacticRule):
            def condition(self, context: Dict[str, Any]) -> bool:
                is_declarer = context.get('is_declarer', False)
                has_finesse_position = context.get('has_finesse_position', False)
                return is_declarer and has_finesse_position
            
            def action(self, context: Dict[str, Any]) -> Dict[str, Any]:
                return {
                    'action': 'finesse_to_honor',
                    'reason': '使用飞牌战术捕捉对方大牌',
                    'suggested_card': context.get('suggested_card', 'HJ')
                }
        
        return FinesseToHonor(
            name="finesse_to_honor",
            description="需要捕捉对方大牌时，使用飞牌战术",
            tactic_type="finesse",
            priority=88
        )
    
    @staticmethod
    def rule_20_establish_long_suit() -> TacticRule:
        """
        规则20：树立长套
        
        当有长套且有进手张时，优先树立长套
        """
        class EstablishLongSuit(TacticRule):
            def condition(self, context: Dict[str, Any]) -> bool:
                is_declarer = context.get('is_declarer', False)
                has_long_suit = context.get('has_long_suit', False)
                has_entries = context.get('has_entries', True)
                return is_declarer and has_long_suit and has_entries
            
            def action(self, context: Dict[str, Any]) -> Dict[str, Any]:
                return {
                    'action': 'establish_long_suit',
                    'reason': '有长套和进手张，优先树立长套',
                    'suggested_card': context.get('suggested_card', 'D2')
                }
        
        return EstablishLongSuit(
            name="establish_long_suit",
            description="有长套且有进手张时，优先树立长套",
            tactic_type="play",
            priority=85
        )


class DefenseRules:
    """防守规则"""
    
    @staticmethod
    def rule_21_second_hand_low() -> TacticRule:
        """
        规则21：第二家出小牌
        
        作为第二个出牌的人，通常出小牌
        """
        class SecondHandLow(TacticRule):
            def condition(self, context: Dict[str, Any]) -> bool:
                is_second_hand = context.get('is_second_hand', False)
                return is_second_hand
            
            def action(self, context: Dict[str, Any]) -> Dict[str, Any]:
                return {
                    'action': 'second_hand_low',
                    'reason': '第二家出小牌',
                    'suggested_card': context.get('suggested_card', 'S3')
                }
        
        return SecondHandLow(
            name="second_hand_low",
            description="作为第二个出牌的人，通常出小牌",
            tactic_type="play",
            priority=85
        )
    
    @staticmethod
    def rule_22_third_hand_high() -> TacticRule:
        """
        规则22：第三家出大牌
        
        作为第三个出牌的人，通常出大牌
        """
        class ThirdHandHigh(TacticRule):
            def condition(self, context: Dict[str, Any]) -> bool:
                is_third_hand = context.get('is_third_hand', False)
                return is_third_hand
            
            def action(self, context: Dict[str, Any]) -> Dict[str, Any]:
                return {
                    'action': 'third_hand_high',
                    'reason': '第三家出大牌',
                    'suggested_card': context.get('suggested_card', 'HK')
                }
        
        return ThirdHandHigh(
            name="third_hand_high",
            description="作为第三个出牌的人，通常出大牌",
            tactic_type="play",
            priority=85
        )
    
    @staticmethod
    def rule_23_cover_honor_with_honor() -> TacticRule:
        """
        规则23：大牌盖大牌
        
        当同伴出大牌且对面也出大牌时，应该盖大牌
        """
        class CoverHonorWithHonor(TacticRule):
            def condition(self, context: Dict[str, Any]) -> bool:
                partner_played = context.get('partner_played', False)
                partner_card_is_honor = context.get('partner_card_is_honor', False)
                opponent_card_is_honor = context.get('opponent_card_is_honor', False)
                has_honor_to_cover = context.get('has_honor_to_cover', False)
                return (partner_played and partner_card_is_honor and 
                        opponent_card_is_honor and has_honor_to_cover)
            
            def action(self, context: Dict[str, Any]) -> Dict[str, Any]:
                return {
                    'action': 'cover_honor_with_honor',
                    'reason': '同伴出大牌且对面也出大牌时，应该盖大牌',
                    'suggested_card': context.get('suggested_card', 'HA')
                }
        
        return CoverHonorWithHonor(
            name="cover_honor_with_honor",
            description="同伴出大牌且对面也出大牌时，应该盖大牌",
            tactic_type="play",
            priority=87
        )
    
    @staticmethod
    def rule_24_signal_attitude() -> TacticRule:
        """
        规则24：态度信号
        
        通过跟牌大小向同伴传递是否喜欢该花色
        """
        class SignalAttitude(TacticRule):
            def condition(self, context: Dict[str, Any]) -> bool:
                partner_played = context.get('partner_played', False)
                should_signal = context.get('should_signal', False)
                return partner_played and should_signal
            
            def action(self, context: Dict[str, Any]) -> Dict[str, Any]:
                return {
                    'action': 'signal_attitude',
                    'reason': '通过跟牌大小传递态度信号',
                    'suggested_card': context.get('suggested_card', 'S5')
                }
        
        return SignalAttitude(
            name="signal_attitude",
            description="通过跟牌大小向同伴传递是否喜欢该花色",
            tactic_type="play",
            priority=80
        )


class EndgameRules:
    """残局规则"""
    
    @staticmethod
    def rule_25_squeeze_play() -> TacticRule:
        """
        规则25：挤牌战术
        
        当对方在某套牌受威胁时，使用挤牌战术
        """
        class SqueezePlay(TacticRule):
            def condition(self, context: Dict[str, Any]) -> bool:
                is_endgame = context.get('is_endgame', False)
                squeeze_opportunity = context.get('squeeze_opportunity', False)
                return is_endgame and squeeze_opportunity
            
            def action(self, context: Dict[str, Any]) -> Dict[str, Any]:
                return {
                    'action': 'squeeze_play',
                    'reason': '对方在某套牌受威胁，使用挤牌战术',
                    'suggested_card': context.get('suggested_card', 'SA')
                }
        
        return SqueezePlay(
            name="squeeze_play",
            description="对方在某套牌受威胁时，使用挤牌战术",
            tactic_type="endgame",
            priority=92
        )
    
    @staticmethod
    def rule_26_endplay() -> TacticRule:
        """
        规则26：投入战术
        
        迫使对手出牌，让其被迫送出赢墩
        """
        class Endplay(TacticRule):
            def condition(self, context: Dict[str, Any]) -> bool:
                is_endgame = context.get('is_endgame', False)
                endplay_opportunity = context.get('endplay_opportunity', False)
                return is_endgame and endplay_opportunity
            
            def action(self, context: Dict[str, Any]) -> Dict[str, Any]:
                return {
                    'action': 'endplay',
                    'reason': '迫使对手出牌，让其被迫送出赢墩',
                    'suggested_card': context.get('suggested_card', 'HK')
                }
        
        return Endplay(
            name="endplay",
            description="迫使对手出牌，让其被迫送出赢墩",
            tactic_type="endgame",
            priority=90
        )
    
    @staticmethod
    def rule_27_unblock() -> TacticRule:
        """
        规则27：解封战术
        
        在适当时候垫掉大牌，以便后续进手
        """
        class Unblock(TacticRule):
            def condition(self, context: Dict[str, Any]) -> bool:
                has_blocking_card = context.get('has_blocking_card', False)
                should_unblock = context.get('should_unblock', False)
                return has_blocking_card and should_unblock
            
            def action(self, context: Dict[str, Any]) -> Dict[str, Any]:
                return {
                    'action': 'unblock',
                    'reason': '垫掉大牌以便后续进手',
                    'suggested_card': context.get('suggested_card', 'DA')
                }
        
        return Unblock(
            name="unblock",
            description="在适当时候垫掉大牌，以便后续进手",
            tactic_type="play",
            priority=83
        )
    
    @staticmethod
    def rule_28_promote_minor() -> TacticRule:
        """
        规则28：提升小牌
        
        反复出某花色，迫使对手出大牌，自己的小牌变成赢墩
        """
        class PromoteMinor(TacticRule):
            def condition(self, context: Dict[str, Any]) -> bool:
                has_promotion_opportunity = context.get('has_promotion_opportunity', False)
                has_entries = context.get('has_entries', True)
                return has_promotion_opportunity and has_entries
            
            def action(self, context: Dict[str, Any]) -> Dict[str, Any]:
                return {
                    'action': 'promote_minor',
                    'reason': '反复出花色提升小牌',
                    'suggested_card': context.get('suggested_card', 'C3')
                }
        
        return PromoteMinor(
            name="promote_minor",
            description="反复出某花色，迫使对手出大牌，自己的小牌变成赢墩",
            tactic_type="play",
            priority=82
        )


def get_extended_rules() -> list:
    """
    获取所有扩展规则
    
    Returns:
        规则列表
    """
    return [
        OpeningRulesExtended.rule_11_open_weak_2_major(),
        OpeningRulesExtended.rule_12_preemptive_3_bid(),
        ResponseRulesExtended.rule_13_new_suit_response(),
        ResponseRulesExtended.rule_14_support_partner(),
        LeadingRules.rule_15_lead_top_from_sequence(),
        LeadingRules.rule_16_lead_partner_suit(),
        LeadingRules.rule_17_lead_top_of_honor_doubleton(),
        DeclarerPlayRules.rule_18_draw_trumps_first(),
        DeclarerPlayRules.rule_19_finesse_to_honor(),
        DeclarerPlayRules.rule_20_establish_long_suit(),
        DefenseRules.rule_21_second_hand_low(),
        DefenseRules.rule_22_third_hand_high(),
        DefenseRules.rule_23_cover_honor_with_honor(),
        DefenseRules.rule_24_signal_attitude(),
        EndgameRules.rule_25_squeeze_play(),
        EndgameRules.rule_26_endplay(),
        EndgameRules.rule_27_unblock(),
        EndgameRules.rule_28_promote_minor(),
    ]
