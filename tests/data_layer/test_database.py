"""
数据层测试
Tests for Data Layer
"""

import pytest
import tempfile
import os

from src.data_layer import DatabaseManager, GameRepository, ProbabilityStorage


class TestDatabaseManager:
    """测试数据库管理器"""
    
    def test_database_manager_creation(self):
        """测试数据库管理器创建"""
        # 使用临时数据库
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = os.path.join(tmpdir, 'test.db')
            db_url = f'sqlite:///{db_path}'
            
            manager = DatabaseManager(db_url)
            
            assert manager is not None
            assert manager.get_engine() is not None
    
    def test_create_tables(self):
        """测试创建表"""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = os.path.join(tmpdir, 'test.db')
            db_url = f'sqlite:///{db_path}'
            
            manager = DatabaseManager(db_url)
            
            # 表应该已创建（在__init__中调用）
            # 再次调用也不应该报错
            manager.create_tables()
    
    def test_get_session(self):
        """测试获取会话"""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = os.path.join(tmpdir, 'test.db')
            db_url = f'sqlite:///{db_path}'
            
            manager = DatabaseManager(db_url)
            session = manager.get_session()
            
            assert session is not None
            
            session.close()


class TestGameRepository:
    """测试牌局数据仓库"""
    
    def test_save_game(self):
        """测试保存牌局"""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = os.path.join(tmpdir, 'test.db')
            db_url = f'sqlite:///{db_path}'
            
            manager = DatabaseManager(db_url)
            repository = GameRepository(manager)
            
            game_data = {
                'dealer': 'N',
                'vul': 'None',
                'contract': '4♥',
                'declarer': 'S',
                'dummy': 'N',
                'result': 1,
                'notes': 'Test game',
                'bidding': [
                    {'player': 'N', 'bid': '1♥'},
                    {'player': 'E', 'bid': 'PASS'},
                ],
                'plays': [
                    {'trick_number': 1, 'player': 'N', 'card': 'SA'},
                    {'trick_number': 1, 'player': 'E', 'card': 'S2'},
                ]
            }
            
            game_id = repository.save_game(game_data)
            
            assert game_id is not None
            assert game_id > 0
    
    def test_get_game(self):
        """测试获取牌局"""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = os.path.join(tmpdir, 'test.db')
            db_url = f'sqlite:///{db_path}'
            
            manager = DatabaseManager(db_url)
            repository = GameRepository(manager)
            
            # 保存牌局
            game_data = {
                'dealer': 'N',
                'vul': 'None',
                'contract': '4♥',
                'declarer': 'S',
                'dummy': 'N',
                'result': 1,
                'notes': 'Test game',
                'bidding': [
                    {'player': 'N', 'bid': '1♥'},
                    {'player': 'E', 'bid': 'PASS'},
                ],
                'plays': [
                    {'trick_number': 1, 'player': 'N', 'card': 'SA'},
                ]
            }
            
            game_id = repository.save_game(game_data)
            
            # 获取牌局
            retrieved_game = repository.get_game(game_id)
            
            assert retrieved_game is not None
            assert retrieved_game['id'] == game_id
            assert retrieved_game['dealer'] == 'N'
            assert retrieved_game['contract'] == '4♥'
            assert len(retrieved_game['bidding']) == 2
            assert len(retrieved_game['plays']) == 1
    
    def test_get_nonexistent_game(self):
        """测试获取不存在的牌局"""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = os.path.join(tmpdir, 'test.db')
            db_url = f'sqlite:///{db_path}'
            
            manager = DatabaseManager(db_url)
            repository = GameRepository(manager)
            
            game = repository.get_game(999999)
            
            assert game is None
    
    def test_search_games(self):
        """测试搜索牌局"""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = os.path.join(tmpdir, 'test.db')
            db_url = f'sqlite:///{db_path}'
            
            manager = DatabaseManager(db_url)
            repository = GameRepository(manager)
            
            # 保存多个牌局
            for i in range(3):
                game_data = {
                    'dealer': 'N',
                    'vul': 'None',
                    'contract': '4♥' if i < 2 else '3NT',
                    'declarer': 'S',
                    'dummy': 'N',
                    'result': i,
                    'notes': f'Test game {i}',
                    'bidding': [],
                    'plays': []
                }
                repository.save_game(game_data)
            
            # 搜索所有牌局
            games = repository.search_games()
            assert len(games) == 3
            
            # 搜索特定定约
            games_4h = repository.search_games({'contract': '4♥'})
            assert len(games_4h) == 2
            
            # 搜索特定结果
            games_result_1 = repository.search_games({'result': 1})
            assert len(games_result_1) == 1
    
    def test_delete_game(self):
        """测试删除牌局"""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = os.path.join(tmpdir, 'test.db')
            db_url = f'sqlite:///{db_path}'
            
            manager = DatabaseManager(db_url)
            repository = GameRepository(manager)
            
            # 保存牌局
            game_data = {
                'dealer': 'N',
                'vul': 'None',
                'contract': '4♥',
                'declarer': 'S',
                'dummy': 'N',
                'result': 1,
                'notes': 'Test game',
                'bidding': [],
                'plays': []
            }
            
            game_id = repository.save_game(game_data)
            
            # 删除牌局
            success = repository.delete_game(game_id)
            assert success is True
            
            # 确认已删除
            deleted_game = repository.get_game(game_id)
            assert deleted_game is None
    
    def test_get_recent_games(self):
        """测试获取最近牌局"""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = os.path.join(tmpdir, 'test.db')
            db_url = f'sqlite:///{db_path}'
            
            manager = DatabaseManager(db_url)
            repository = GameRepository(manager)
            
            # 保存多个牌局
            for i in range(5):
                game_data = {
                    'dealer': 'N',
                    'vul': 'None',
                    'contract': '4♥',
                    'declarer': 'S',
                    'dummy': 'N',
                    'result': i,
                    'notes': f'Test game {i}',
                    'bidding': [],
                    'plays': []
                }
                repository.save_game(game_data)
            
            # 获取最近3个牌局
            recent_games = repository.get_recent_games(limit=3)
            assert len(recent_games) == 3
    
    def test_count_games(self):
        """测试统计牌局数"""
        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = os.path.join(tmpdir, 'test.db')
            db_url = f'sqlite:///{db_path}'
            
            manager = DatabaseManager(db_url)
            repository = GameRepository(manager)
            
            # 初始为0
            count = repository.count_games()
            assert count == 0
            
            # 保存牌局
            for i in range(3):
                game_data = {
                    'dealer': 'N',
                    'vul': 'None',
                    'contract': '4♥',
                    'declarer': 'S',
                    'dummy': 'N',
                    'result': i,
                    'notes': f'Test game {i}',
                    'bidding': [],
                    'plays': []
                }
                repository.save_game(game_data)
            
            # 统计为3
            count = repository.count_games()
            assert count == 3


class TestProbabilityStorage:
    """测试概率存储"""
    
    def test_probability_storage_creation(self):
        """测试概率存储创建"""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage_path = os.path.join(tmpdir, 'probabilities.h5')
            storage = ProbabilityStorage(storage_path)
            
            assert storage is not None
            assert storage.get_storage_path() == storage_path
    
    def test_save_and_get_probability(self):
        """测试保存和获取概率"""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage_path = os.path.join(tmpdir, 'probabilities.h5')
            storage = ProbabilityStorage(storage_path)
            
            # 保存概率
            storage.save_probability('4-3-3-3', 0.2155)
            
            # 获取概率
            prob = storage.get_probability('4-3-3-3')
            assert prob == 0.2155
    
    def test_get_nonexistent_probability(self):
        """测试获取不存在的概率"""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage_path = os.path.join(tmpdir, 'probabilities.h5')
            storage = ProbabilityStorage(storage_path)
            
            prob = storage.get_probability('invalid-distribution')
            assert prob is None
    
    def test_save_and_get_all_probabilities(self):
        """测试批量保存和获取所有概率"""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage_path = os.path.join(tmpdir, 'probabilities.h5')
            storage = ProbabilityStorage(storage_path)
            
            # 批量保存
            probabilities = {
                '4-3-3-3': 0.2155,
                '4-4-3-2': 0.2155,
                '5-3-3-2': 0.1552,
            }
            storage.save_probabilities(probabilities)
            
            # 获取所有
            all_probs = storage.get_all_probabilities()
            assert len(all_probs) == 3
            assert all_probs['4-3-3-3'] == 0.2155
            assert all_probs['4-4-3-2'] == 0.2155
            assert all_probs['5-3-3-2'] == 0.1552
    
    def test_clear_probabilities(self):
        """测试清空概率"""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage_path = os.path.join(tmpdir, 'probabilities.h5')
            storage = ProbabilityStorage(storage_path)
            
            # 保存一些概率
            storage.save_probability('4-3-3-3', 0.2155)
            
            # 清空
            storage.clear_probabilities()
            
            # 确认已清空
            prob = storage.get_probability('4-3-3-3')
            assert prob is None
            assert storage.get_probability_count() == 0
    
    def test_probability_persistence(self):
        """测试概率持久化"""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage_path = os.path.join(tmpdir, 'probabilities.h5')
            
            # 第一次保存
            storage1 = ProbabilityStorage(storage_path)
            storage1.save_probability('4-3-3-3', 0.2155)
            
            # 第二次加载
            storage2 = ProbabilityStorage(storage_path)
            prob = storage2.get_probability('4-3-3-3')
            
            assert prob == 0.2155


if __name__ == "__main__":
    pytest.main([__file__, "-v"])