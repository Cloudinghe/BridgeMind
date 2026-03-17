#!/usr/bin/env python3
"""
修复feature_extractor.py中的类型注解语法错误
"""

def fix_type_annotations():
    with open('src/parser/feature_extractor/feature_extractor.py', 'r') as f:
        content = f.read()
    
    # 修复所有类型注解错误
    replacements = [
        ('Dict[str Any]', 'Dict[str, Any]'),
        ('Dict[str int]', 'Dict[str, int]'),
        ('Dict[str str]', 'Dict[str, str]'),
        ('List[Dict[str Any]]', 'List[Dict[str, Any]]'),
        ('Dict[str BaseFeatureExtractor]', 'Dict[str, BaseFeatureExtractor]'),
        ('def extract(self context:', 'def extract(self, context:'),
        ('def _calculate_aggressiveness(self context:', 'def _calculate_aggressiveness(self, context:'),
        ('def _calculate_conservativeness(self context:', 'def _calculate_conservativeness(self, context:'),
        ('def _analyze_bidding_style(self context:', 'def _analyze_bidding_style(self, context:'),
        ('def _analyze_play_style(self context:', 'def _analyze_play_style(self, context:'),
        ('def _estimate_bluff_probability(self context:', 'def _estimate_bluff_probability(self, context:'),
        ('def _is_jump_bid(self bid:', 'def _is_jump_bid(self, bid:'),
        ('def _is_preemptive_bid(self bid:', 'def _is_preemptive_bid(self, bid:'),
        ('def _check_bid_consistency(self bids:', 'def _check_bid_consistency(self, bids:'),
        ('def _get_bidding_sequence(self bidding_history:', 'def _get_bidding_sequence(self, bidding_history:'),
        ('def _estimate_partnership_strength(self bidding_history:', 'def _estimate_partnership_strength(self, bidding_history:'),
        ('def _estimate_high_card_points(self bidding_history:', 'def _estimate_high_card_points(self, bidding_history:'),
        ('def _estimate_distribution(self bidding_history:', 'def _estimate_distribution(self, bidding_history:'),
        ('def _check_fitting(self bidding_history:', 'def _check_fitting(self, bidding_history:'),
        ('def _check_game_force(self bidding_history:', 'def _check_game_force(self, bidding_history:'),
        ('def _check_slam_interest(self bidding_history:', 'def _check_slam_interest(self, bidding_history:'),
        ('def _analyze_play_pattern(self play_history:', 'def _analyze_play_pattern(self, play_history:'),
        ('def _extract_signals(self play_history:', 'def _extract_signals(self, play_history:'),
        ('def _identify_tactics(self play_history:', 'def _identify_tactics(self, play_history:'),
        ('def _count_tricks_won(self play_history:', 'def _count_tricks_won(self, play_history:'),
        ('def _identify_mistakes(self play_history:', 'def _identify_mistakes(self, play_history:'),
    ]
    
    for old, new in replacements:
        content = content.replace(old, new)
    
    with open('src/parser/feature_extractor/feature_extractor.py', 'w') as f:
        f.write(content)
    
    print("Type annotations fixed successfully!")

if __name__ == "__main__":
    fix_type_annotations()