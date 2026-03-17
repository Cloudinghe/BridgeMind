"""
核心数据模型测试
Tests for Core Data Models
"""

import pytest
from src.parser.models import (
    Suit, Rank, Position, Strain, Card, Contract, Hand, GameState
)


class TestSuit:
    """测试花色枚举"""
    
    def test_suit_creation(self):
        """测试花色创建"""
        assert Suit.CLUBS == Suit.CLUBS
        assert Suit.SPADES.value == "S"
    
    def test_suit_string(self):
        """测试花色字符串表示"""
        assert str(Suit.CLUBS) == "♣"
        assert str(Suit.DIAMONDS) == "♦"
        assert str(Suit.HEARTS) == "♥"
        assert str(Suit.SPADES) == "♠"
    
    def test_suit_comparison(self):
        """测试花色比较"""
        assert Suit.CLUBS < Suit.DIAMONDS
        assert Suit.DIAMONDS < Suit.HEARTS
        assert Suit.HEARTS < Suit.SPADES


class TestRank:
    """测试点数枚举"""
    
    def test_rank_creation(self):
        """测试点数创建"""
        assert Rank.TWO.value == 2
        assert Rank.ACE.value == 14
    
    def test_rank_string(self):
        """测试点数字符串表示"""
        assert str(Rank.TWO) == "2"
        assert str(Rank.TEN) == "T"
        assert str(Rank.JACK) == "J"
        assert str(Rank.QUEEN) == "Q"
        assert str(Rank.KING) == "K"
        assert str(Rank.ACE) == "A"
    
    def test_rank_comparison(self):
        """测试点数比较"""
        assert Rank.TWO < Rank.THREE
        assert Rank.TEN < Rank.JACK
        assert Rank.ACE > Rank.KING


class TestPosition:
    """测试方位枚举"""
    
    def test_position_creation(self):
        """测试方位创建"""
        assert Position.NORTH.value == "N"
        assert Position.EAST.value == "E"
        assert Position.SOUTH.value == "S"
        assert Position.WEST.value == "W"
    
    def test_get_partner(self):
        """测试获取搭档"""
        assert Position.NORTH.get_partner() == Position.SOUTH
        assert Position.SOUTH.get_partner() == Position.NORTH
        assert Position.EAST.get_partner() == Position.WEST
        assert Position.WEST.get_partner() == Position.EAST
    
    def test_get_left_opponent(self):
        """测试获取左手对手"""
        assert Position.NORTH.get_left_opponent() == Position.EAST
        assert Position.EAST.get_left_opponent() == Position.SOUTH
        assert Position.SOUTH.get_left_opponent() == Position.WEST
        assert Position.WEST.get_left_opponent() == Position.NORTH
    
    def test_get_right_opponent(self):
        """测试获取右手对手"""
        assert Position.NORTH.get_right_opponent() == Position.WEST
        assert Position.WEST.get_right_opponent() == Position.SOUTH
        assert Position.SOUTH.get_right_opponent() == Position.EAST
        assert Position.EAST.get_right_opponent() == Position.NORTH


class TestStrain:
    """测试定约花色枚举"""
    
    def test_strain_creation(self):
        """测试定约花色创建"""
        assert Strain.CLUBS.value == "C"
        assert Strain.NOTRUMP.value == "NT"
    
    def test_is_major(self):
        """测试是否为高花"""
        assert Strain.HEARTS.is_major()
        assert Strain.SPADES.is_major()
        assert not Strain.CLUBS.is_major()
        assert not Strain.DIAMONDS.is_major()
        assert not Strain.NOTRUMP.is_major()
    
    def test_is_minor(self):
        """测试是否为低花"""
        assert Strain.CLUBS.is_minor()
        assert Strain.DIAMONDS.is_minor()
        assert not Strain.HEARTS.is_minor()
        assert not Strain.SPADES.is_minor()
        assert not Strain.NOTRUMP.is_minor()


class TestCard:
    """测试牌张类"""
    
    def test_card_creation(self):
        """测试牌张创建"""
        card = Card(Suit.SPADES, Rank.ACE)
        assert card.suit == Suit.SPADES
        assert card.rank == Rank.ACE
    
    def test_card_string(self):
        """测试牌张字符串表示"""
        assert str(Card(Suit.SPADES, Rank.ACE)) == "♠A"
        assert str(Card(Suit.HEARTS, Rank.KING)) == "♥K"
        assert str(Card(Suit.CLUBS, Rank.TWO)) == "♣2"
    
    def test_card_equality(self):
        """测试牌张相等"""
        card1 = Card(Suit.SPADES, Rank.ACE)
        card2 = Card(Suit.SPADES, Rank.ACE)
        card3 = Card(Suit.HEARTS, Rank.ACE)
        
        assert card1 == card2
        assert card1 != card3
    
    def test_card_comparison(self):
        """测试牌张比较"""
        card1 = Card(Suit.CLUBS, Rank.ACE)
        card2 = Card(Suit.DIAMONDS, Rank.TWO)
        
        # 先比花色
        assert card1 < card2
        
        # 同花色比点数
        card3 = Card(Suit.SPADES, Rank.KING)
        card4 = Card(Suit.SPADES, Rank.ACE)
        assert card3 < card4
    
    def test_card_hash(self):
        """测试牌张哈希"""
        card1 = Card(Suit.SPADES, Rank.ACE)
        card2 = Card(Suit.SPADES, Rank.ACE)
        card3 = Card(Suit.HEARTS, Rank.ACE)
        
        # 相同的牌有相同的哈希
        assert hash(card1) == hash(card2)
        # 不同的牌有不同的哈希
        assert hash(card1) != hash(card3)
        
        # 可以放入集合
        card_set = {card1, card2, card3}
        assert len(card_set) == 2
    
    def test_card_hcp(self):
        """测试高牌点计算"""
        assert Card(Suit.SPADES, Rank.ACE).hcp == 4
        assert Card(Suit.HEARTS, Rank.KING).hcp == 3
        assert Card(Suit.DIAMONDS, Rank.QUEEN).hcp == 2
        assert Card(Suit.CLUBS, Rank.JACK).hcp == 1
        assert Card(Suit.SPADES, Rank.TWO).hcp == 0
    
    def test_card_to_index(self):
        """测试牌张转索引"""
        # 梅花2 -> 0
        assert Card(Suit.CLUBS, Rank.TWO).to_index() == 0
        # 梅花A -> 12
        assert Card(Suit.CLUBS, Rank.ACE).to_index() == 12
        # 方块2 -> 13
        assert Card(Suit.DIAMONDS, Rank.TWO).to_index() == 13
        # 黑桃A -> 51
        assert Card(Suit.SPADES, Rank.ACE).to_index() == 51
    
    def test_card_from_index(self):
        """测试索引转牌张"""
        assert Card.from_index(0) == Card(Suit.CLUBS, Rank.TWO)
        assert Card.from_index(12) == Card(Suit.CLUBS, Rank.ACE)
        assert Card.from_index(13) == Card(Suit.DIAMONDS, Rank.TWO)
        assert Card.from_index(51) == Card(Suit.SPADES, Rank.ACE)
    
    def test_card_from_string(self):
        """测试字符串转牌张"""
        assert Card.from_string("SA") == Card(Suit.SPADES, Rank.ACE)
        assert Card.from_string("HK") == Card(Suit.HEARTS, Rank.KING)
        assert Card.from_string("D2") == Card(Suit.DIAMONDS, Rank.TWO)
        assert Card.from_string("CJ") == Card(Suit.CLUBS, Rank.JACK)
    
    def test_card_from_string_invalid(self):
        """测试无效字符串"""
        with pytest.raises(ValueError):
            Card.from_string("S")  # 太短
        
        with pytest.raises(ValueError):
            Card.from_string("SA1")  # 太长
        
        with pytest.raises(ValueError):
            Card.from_string("XA")  # 无效花色
        
        with pytest.raises(ValueError):
            Card.from_string("S1")  # 无效点数


class TestContract:
    """测试定约类"""
    
    def test_contract_creation(self):
        """测试定约创建"""
        contract = Contract(4, Strain.HEARTS)
        assert contract.level == 4
        assert contract.strain == Strain.HEARTS
        assert not contract.doubled
        assert not contract.redoubled
    
    def test_contract_string(self):
        """测试定约字符串表示"""
        assert str(Contract(4, Strain.HEARTS)) == "4♥"
        assert str(Contract(3, Strain.NOTRUMP)) == "3NT"
        assert str(Contract(1, Strain.CLUBS)) == "1♣"
    
    def test_contract_doubled(self):
        """测试加倍"""
        contract = Contract(4, Strain.HEARTS, doubled=True)
        assert str(contract) == "4♥X"
    
    def test_contract_redoubled(self):
        """测试再加倍"""
        contract = Contract(4, Strain.HEARTS, doubled=True, redoubled=True)
        assert str(contract) == "4♥XX"
    
    def test_contract_invalid_level(self):
        """测试无效阶数"""
        with pytest.raises(ValueError):
            Contract(0, Strain.HEARTS)  # 太小
        
        with pytest.raises(ValueError):
            Contract(8, Strain.HEARTS)  # 太大
    
    def test_contract_redoubled_without_doubled(self):
        """测试未加倍就再加倍"""
        with pytest.raises(ValueError):
            Contract(4, Strain.HEARTS, redoubled=True)
    
    def test_get_required_tricks(self):
        """测试获取所需墩数"""
        assert Contract(1, Strain.HEARTS).get_required_tricks() == 7
        assert Contract(3, Strain.NOTRUMP).get_required_tricks() == 9
        assert Contract(4, Strain.SPADES).get_required_tricks() == 10
        assert Contract(7, Strain.CLUBS).get_required_tricks() == 13
    
    def test_get_bonus(self):
        """测试定约分数"""
        # 4♥ = 4 * 30 = 120分
        assert Contract(4, Strain.HEARTS).get_bonus(vulnerable=False) == 120
        
        # 3NT = 40 + 2 * 30 = 100分
        assert Contract(3, Strain.NOTRUMP).get_bonus(vulnerable=False) == 100
        
        # 5♣ = 5 * 20 = 100分
        assert Contract(5, Strain.CLUBS).get_bonus(vulnerable=False) == 100
        
        # 加倍：4♥X = 120 * 2 = 240分
        assert Contract(4, Strain.HEARTS, doubled=True).get_bonus(vulnerable=False) == 240
        
        # 再加倍：4♥XX = 120 * 4 = 480分
        assert Contract(4, Strain.HEARTS, doubled=True, redoubled=True).get_bonus(vulnerable=False) == 480


class TestHand:
    """测试手牌类"""
    
    def test_hand_creation(self):
        """测试手牌创建"""
        cards = [
            Card(Suit.SPADES, Rank.ACE),
            Card(Suit.SPADES, Rank.KING),
            Card(Suit.HEARTS, Rank.QUEEN),
        ]
        # 补齐13张牌
        for i in range(10):
            cards.append(Card(Suit.CLUBS, Rank(i + 2)))
        
        hand = Hand(Position.NORTH, cards)
        assert hand.position == Position.NORTH
        assert len(hand.cards) == 13
    
    def test_hand_invalid_length(self):
        """测试无效手牌长度"""
        cards = [Card(Suit.SPADES, Rank.ACE)]
        
        with pytest.raises(ValueError):
            Hand(Position.NORTH, cards)
    
    def test_hand_duplicate_cards(self):
        """测试重复牌"""
        cards = [Card(Suit.SPADES, Rank.ACE)] * 13
        
        with pytest.raises(ValueError):
            Hand(Position.NORTH, cards)
    
    def test_get_suit(self):
        """测试获取花色"""
        cards = [
            Card(Suit.SPADES, Rank.ACE),
            Card(Suit.SPADES, Rank.KING),
            Card(Suit.HEARTS, Rank.QUEEN),
        ]
        # 补齐13张牌
        for i in range(10):
            cards.append(Card(Suit.CLUBS, Rank(i + 2)))
        
        hand = Hand(Position.NORTH, cards)
        spade_cards = hand.get_suit(Suit.SPADES)
        
        assert len(spade_cards) == 2
        assert Card(Suit.SPADES, Rank.ACE) in spade_cards
        assert Card(Suit.SPADES, Rank.KING) in spade_cards
    
    def test_get_suit_length(self):
        """测试获取花色长度"""
        cards = [
            Card(Suit.SPADES, Rank.ACE),
            Card(Suit.SPADES, Rank.KING),
            Card(Suit.SPADES, Rank.QUEEN),
            Card(Suit.SPADES, Rank.JACK),
            Card(Suit.SPADES, Rank.TEN),
        ]
        # 补齐13张牌
        for i in range(8):
            cards.append(Card(Suit.CLUBS, Rank(i + 2)))
        
        hand = Hand(Position.NORTH, cards)
        assert hand.get_suit_length(Suit.SPADES) == 5
        assert hand.get_suit_length(Suit.CLUBS) == 8
    
    def test_get_hcp(self):
        """测试获取高牌点"""
        cards = [
            Card(Suit.SPADES, Rank.ACE),      # 4点
            Card(Suit.HEARTS, Rank.KING),     # 3点
            Card(Suit.DIAMONDS, Rank.QUEEN),  # 2点
            Card(Suit.CLUBS, Rank.JACK),      # 1点
        ]
        # 补齐13张牌
        for i in range(9):
            cards.append(Card(Suit.CLUBS, Rank(i + 2)))
        
        hand = Hand(Position.NORTH, cards)
        assert hand.get_hcp() == 10
    
    def test_get_distribution(self):
        """测试获取牌型分布"""
        cards = [
            # 黑桃5张
            Card(Suit.SPADES, Rank.ACE),
            Card(Suit.SPADES, Rank.KING),
            Card(Suit.SPADES, Rank.QUEEN),
            Card(Suit.SPADES, Rank.JACK),
            Card(Suit.SPADES, Rank.TEN),
            # 红心3张
            Card(Suit.HEARTS, Rank.ACE),
            Card(Suit.HEARTS, Rank.KING),
            Card(Suit.HEARTS, Rank.QUEEN),
            # 方块3张
            Card(Suit.DIAMONDS, Rank.ACE),
            Card(Suit.DIAMONDS, Rank.KING),
            Card(Suit.DIAMONDS, Rank.QUEEN),
            # 梅花2张
            Card(Suit.CLUBS, Rank.ACE),
            Card(Suit.CLUBS, Rank.KING),
        ]
        
        hand = Hand(Position.NORTH, cards)
        assert hand.get_distribution() == "5-3-3-2"


class TestGameState:
    """测试游戏状态类"""
    
    def test_game_state_creation(self):
        """测试游戏状态创建"""
        # 创建完整的一副牌
        all_cards = []
        for suit in Suit:
            for rank in Rank:
                all_cards.append(Card(suit, rank))
        
        # 分配给四家
        hands = {
            Position.NORTH: all_cards[0:13],
            Position.EAST: all_cards[13:26],
            Position.SOUTH: all_cards[26:39],
            Position.WEST: all_cards[39:52],
        }
        
        state = GameState(hands=hands, dealer=Position.NORTH)
        assert state.dealer == Position.NORTH
        assert len(state.get_hand(Position.NORTH)) == 13
    
    def test_game_state_duplicate_cards(self):
        """测试重复牌"""
        cards = [Card(Suit.SPADES, Rank.ACE)] * 52
        
        hands = {
            Position.NORTH: cards[0:13],
            Position.EAST: cards[13:26],
            Position.SOUTH: cards[26:39],
            Position.WEST: cards[39:52],
        }
        
        with pytest.raises(ValueError):
            GameState(hands=hands, dealer=Position.NORTH)
    
    def test_game_state_invalid_card_count(self):
        """测试无效牌数"""
        hands = {
            Position.NORTH: [],
            Position.EAST: [],
            Position.SOUTH: [],
            Position.WEST: [],
        }
        
        with pytest.raises(ValueError):
            GameState(hands=hands, dealer=Position.NORTH)
    
    def test_get_hand(self):
        """测试获取手牌"""
        all_cards = []
        for suit in Suit:
            for rank in Rank:
                all_cards.append(Card(suit, rank))
        
        hands = {
            Position.NORTH: all_cards[0:13],
            Position.EAST: all_cards[13:26],
            Position.SOUTH: all_cards[26:39],
            Position.WEST: all_cards[39:52],
        }
        
        state = GameState(hands=hands, dealer=Position.NORTH)
        north_hand = state.get_hand(Position.NORTH)
        
        assert len(north_hand) == 13
        # 返回的是副本
        north_hand.append(Card(Suit.SPADES, Rank.ACE))
        assert len(state.get_hand(Position.NORTH)) == 13


if __name__ == "__main__":
    pytest.main([__file__, "-v"])