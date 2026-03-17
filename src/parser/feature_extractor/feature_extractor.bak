"""
特征提取器
Feature Extractor

从游戏状态中提取对手特征、叫牌特征、打牌特征等
"""

from typing import Dict, Any, List
from abc import ABC, abstractmethod


class BaseFeatureExtractor(ABC):
    """特征提取器基类"""
    
    @abstractmethod
    def extract(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        提取特征
        
        Args:
            context: 游戏上下文
            
        Returns:
            特征字典
        """
        pass


class OpponentFeatureExtractor(BaseFeatureExtractor):
    """对手特征提取器"""
    
    def __init__(self):
        """
        初始化对手特征提取器
        """
        self.features = {}
    
    def extract(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        提取对手特征
        
        Args:
            context: 游戏上下文，包含对手叫牌、出牌历史等
            
        Returns:
            对手特征字典
        """
        result = {
            'aggressiveness': self._calculate_aggressiveness(context),
            'conservativeness': self._calculate_conservativeness(context),
            'bidding_style': self._analyze_bidding_style(context),
            'play_style': self._analyze_play_style(context),
            'bluff_probability': self._estimate_bluff_probability(context),
        }
        
        return result
    
    def _calculate_aggressiveness(self, context: Dict[str, Any]) -> float:
        """
        计算对手激进度
        
        Args:
            context: 游戏上下文
            
        Returns:
            激进度（0-1之间）
        """
        bidding_history = context.get('bidding_history', [])
        play_history = context.get('play_history', [])
        
        # 叫牌激进度：经常开叫、争叫、扣叫
        aggressive_bids = 0
        for bid in bidding_history:
            if bid['player'] in context.get('opponents', []):
                if bid['level'] >= 2 or bid['strain'] in ['S', 'H']:
                    aggressive_bids += 1
        
        # 出牌激进度：经常主动进攻
        aggressive_plays = 0
        for play in play_history:
            if play['player'] in context.get('opponents', []):
                if play['is_attack'] or play['is_finesse']:
                    aggressive_plays += 1
        
        total_actions = len(bidding_history) + len(play_history)
        if total_actions == 0:
            return 0.5
        
        aggression = (aggressive_bids + aggressive_plays) / max(total_actions, 1)
        return min(aggression, 1.0)
    
    def _calculate_conservativeness(self, context: Dict[str, Any]) -> float:
        """
        计算对手保守度
        
        Args:
            context: 游戏上下文
            
        Returns:
            保守度（0-1之间）
        """
        # 保守度是激进度相反的概念
        aggressiveness = self._calculate_aggressiveness(context)
        return 1.0 - aggressiveness
    
    def _analyze_bidding_style(self, context: Dict[str, Any]) -> str:
        """
        分析对手叫牌风格
        
        Args:
            context: 游戏上下文
            
        Returns:
            叫牌风格字符串
        """
        bidding_history = context.get('bidding_history', [])
        opponents = context.get('opponents', [])
        
        opponent_bids = [bid for bid in bidding_history if bid['player'] in opponents]
        
        if not opponent_bids:
            return "unknown"
        
        # 计算叫牌平均水平
        avg_level = sum(bid['level'] for bid in opponent_bids) / len(opponent_bids)
        
        # 统计叫牌类型
        jump_bids = sum(1 for bid in opponent_bids if self._is_jump_bid(bid))
        preemptive_bids = sum(1 for bid in opponent_bids if self._is_preemptive_bid(bid))
        
        if jump_bids > len(opponent_bids) * 0.3:
            return "aggressive"
        elif preemptive_bids > len(opponent_bids) * 0.2:
            return "preemptive"
        elif avg_level < 2.0:
            return "conservative"
        else:
            return "standard"
    
    def _analyze_play_style(self, context: Dict[str, Any]) -> str:
        """
        分析对手打牌风格
        
        Args:
            context: 游戏上下文
            
        Returns:
            打牌风格字符串
        """
        play_history = context.get('play_history', [])
        opponents = context.get('opponents', [])
        
        opponent_plays = [play for play in play_history if play['player'] in opponents]
        
        if not opponent_plays:
            return "unknown"
        
        # 统计打牌类型
        finesse_count = sum(1 for play in opponent_plays if play['is_finesse'])
        signal_count = sum(1 for play in opponent_plays if play['is_signal'])
        attack_count = sum(1 for play in opponent_plays if play['is_attack'])
        
        total_plays = len(opponent_plays)
        
        if finesse_count > total_plays * 0.3:
            return "tactical"
        elif signal_count > total_plays * 0.3:
            return "communicative"
        elif attack_count > total_plays * 0.3:
            return "aggressive"
        else:
            return "standard"
    
    def _estimate_bluff_probability(self, context: Dict[str, Any]) -> float:
        """
        估计对手诈叫概率
        
        Args:
            context: 游戏上下文
            
        Returns:
            诈叫概率（0-1之间）
        """
        bidding_history = context.get('bidding_history', [])
        opponents = context.get('opponents', [])
        
        opponent_bids = [bid for bid in bidding_history if bid['player'] in opponents]
        
        if not opponent_bids:
            return 0.0
        
        # 分析叫牌一致性
        consistency_score = self._check_bid_consistency(opponent_bids)
        
        # 分析叫牌激进度
        aggressiveness = self._calculate_aggressiveness(context)
        
        # 诈叫概率 = (1 - 一致性) * 激进度
        bluff_prob = (1.0 - consistency_score) * aggressiveness
        
        return min(bluff_prob, 1.0)
    
    def _is_jump_bid(self, bid: Dict[str, Any]) -> bool:
        """判断是否为跳叫"""
        # 跳叫的定义：比最低叫品高2级以上
        return bid.get('is_jump', False)
    
    def _is_preemptive_bid(self, bid: Dict[str, Any]) -> bool:
        """判断是否为阻击叫"""
        # 阻击叫：3阶以上开叫
        return bid.get('is_preemptive', False)
    
    def _check_bid_consistency(self, bids: List[Dict[str, Any]]) -> float:
        """
        检查叫牌一致性
        
        Args:
            bids: 叫牌列表
            
        Returns:
            一致性分数（0-1之间）
        """
        if not bids:
            return 1.0
        
        # 简单的一致性检查：叫牌强度是否一致
        # 这里简化实现，实际应该更复杂
        return 0.7  # 默认值


class BiddingFeatureExtractor(BaseFeatureExtractor):
    """叫牌特征提取器"""
    
    def __init__(self):
        """初始化叫牌特征提取器"""
        pass
    
    def extract(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        提取叫牌特征
        
        Args:
            context: 游戏上下文
            
        Returns:
            叫牌特征字典
        """
        bidding_history = context.get('bidding_history', [])
        
        result = {
            'final_contract': context.get('contract', {}),
            'bidding_sequence': self._get_bidding_sequence(bidding_history),
            'partnership_strength': self._estimate_partnership_strength(bidding_history),
            'high_card_points': self._estimate_high_card_points(bidding_history),
            'distribution': self._estimate_distribution(bidding_history),
            'fitting': self._check_fitting(bidding_history),
            'game_force': self._check_game_force(bidding_history),
            'slam_interest': self._check_slam_interest(bidding_history),
        }
        
        return result
    
    def _get_bidding_sequence(self, bidding_history: List[Dict[str, Any]]) -> str:
        """
        获取叫牌序列字符串
        
        Args:
            bidding_history: 叫牌历史
            
        Returns:
            叫牌序列字符串
        """
        return ' '.join(f"{bid['player']}: {bid['bid']}" for bid in bidding_history)
    
    def _estimate_partnership_strength(self, bidding_history: List[Dict[str, Any]]) -> str:
        """
        估计联手牌力
        
        Args:
            bidding_history: 叫牌历史
            
        Returns:
            联手牌力评估字符串
        """
        # 根据最终定约估计联手牌力
        contract = bidding_history[-1]['bid'] if bidding_history else "PASS"
        
        if "7" in contract or "Grand" in contract:
            return "37+ (Grand Slam)"
        elif "6" in contract or "Slam" in contract:
            return "33+ (Small Slam)"
        elif "3NT" in contract or "4H" in contract or "4S" in contract:
            return "26-29 (Game)"
        elif "5H" in contract or "5S" in contract or "5C" in contract or "5D" in contract:
            return "29-31 (Minor Game)"
        else:
            return "< 26 (Part Score)"
    
    def _estimate_high_card_points(self, bidding_history: List[Dict[str, Any]]) -> Dict[str, int]:
        """
        估计高牌点
        
        Args:
            bidding_history: 叫牌历史
            
        Returns:
            高牌点估计字典
        """
        # 简化实现，实际需要根据叫牌体系估计
        return {
            'north': 12,
            'south': 12,
            'east': 8,
            'west': 8,
        }
    
    def _estimate_distribution(self, bidding_history: List[Dict[str, Any]]) -> Dict[str, str]:
        """
        估计牌型分布
        
        Args:
            bidding_history: 叫牌历史
            
        Returns:
            牌型分布字典
        """
        # 简化实现
        return {
            'north': '5-3-3-2',
            'south': '4-4-3-2',
            'east': '4-3-3-3',
            'west': '4-4-4-1',
        }
    
    def _check_fitting(self, bidding_history: List[Dict[str, Any]]) -> bool:
        """
        检查是否有配
        
        Args:
            bidding_history: 叫牌历史
            
        Returns:
            是否有配
        """
        # 简化实现：如果找到了将牌花色
        for bid in bidding_history:
            if bid['strain'] in ['S', 'H', 'D', 'C']:
                return True
        return False
    
    def _check_game_force(self, bidding_history: List[Dict[str, Any]]) -> bool:
        """
        检查是否成局逼叫
        
        Args:
            bidding_history: 叫牌历史
            
        Returns:
            是否成局逼叫
        """
        # 简化实现
        return False
    
    def _check_slam_interest(self, bidding_history: List[Dict[str, Any]]) -> bool:
        """
        检查是否有满贯兴趣
        
        Args:
            bidding_history: 叫牌历史
            
        Returns:
            是否有满贯兴趣
        """
        # 简化实现
        return False


class PlayFeatureExtractor(BaseFeatureExtractor):
    """打牌特征提取器"""
    
    def __init__(self):
        """初始化打牌特征提取器"""
        pass
    
    def extract(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        提取打牌特征
        
        Args:
            context: 游戏上下文
            
        Returns:
            打牌特征字典
        """
        play_history = context.get('play_history', [])
        
        result = {
            'play_pattern': self._analyze_play_pattern(play_history),
            'signals': self._extract_signals(play_history),
            'tactics_used': self._identify_tactics(play_history),
            'tricks_won': self._count_tricks_won(play_history),
            'mistakes': self._identify_mistakes(play_history),
        }
        
        return result
    
    def _analyze_play_pattern(self, play_history: List[Dict[str, Any]]) -> str:
        """
        分析打牌模式
        
        Args:
            play_history: 出牌历史
            
        Returns:
            打牌模式字符串
        """
        if not play_history:
            return "no_plays"
        
        # 简化实现
        return "standard"
    
    def _extract_signals(self, play_history: List[Dict[str, Any]]) -> List[str]:
        """
        提取信号
        
        Args:
            play_history: 出牌历史
            
        Returns:
            信号列表
        """
        signals = []
        
        for play in play_history:
            if play.get('is_signal'):
                signals.append({
                    'player': play['player'],
                    'type': play.get('signal_type', 'unknown'),
                    'meaning': play.get('signal_meaning', ''),
                })
        
        return signals
    
    def _identify_tactics(self, play_history: List[Dict[str, Any]]) -> List[str]:
        """
        识别战术
        
        Args:
            play_history: 出牌历史
            
        Returns:
            战术列表
        """
        tactics = []
        
        for play in play_history:
            if play.get('is_finesse'):
                tactics.append('finesse')
            elif play.get('is_squeeze'):
                tactics.append('squeeze')
            elif play.get('is_endplay'):
                tactics.append('endplay')
        
        return tactics
    
    def _count_tricks_won(self, play_history: List[Dict[str, Any]) -> Dict[str, int]:
        """
        统计赢墩数
        
        Args:
            play_history: 出牌历史
            
        Returns:
            各方赢墩数
        """
        tricks = {'north': 0, 'south': 0, 'east': 0, 'west': 0}
        
        for play in play_history:
            if play.get('won_trick'):
                winner = play['winner']
                tricks[winner] += 1
        
        return tricks
    
    def _identify_mistakes(self, play_history: List[Dict[str, Any]]) -> List[str]:
        """
        识别失误
        
        Args:
            play_history: 出牌历史
            
        Returns:
            失误列表
        """
        # 简化实现
        return []


class FeatureExtractorFactory:
    """特征提取器工厂"""
    
    @staticmethod
    def create_opponent_extractor() -> OpponentFeatureExtractor:
        """创建对手特征提取器"""
        return OpponentFeatureExtractor()
    
    @staticmethod
    def create_bidding_extractor() -> BiddingFeatureExtractor:
        """创建叫牌特征提取器"""
        return BiddingFeatureExtractor()
    
    @staticmethod
    def create_play_extractor() -> PlayFeatureExtractor:
        """创建打牌特征提取器"""
        return PlayFeatureExtractor()
    
    @staticmethod
    def create_all_extractors() -> Dict[str, BaseFeatureExtractor]:
        """创建所有特征提取器"""
        return {
            'opponent': FeatureExtractorFactory.create_opponent_extractor(),
            'bidding': FeatureExtractorFactory.create_bidding_extractor(),
            'play': FeatureExtractorFactory.create_play_extractor(),
        }
