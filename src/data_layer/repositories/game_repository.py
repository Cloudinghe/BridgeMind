"""
牌局数据仓库
Game Repository

负责牌局数据的CRUD操作
"""

from typing import List, Dict, Any, Optional
from datetime import datetime

from ..database.manager import DatabaseManager
from ..models import BridgeGame, BiddingRecord, PlayRecord
from ...parser.models import Position


class GameRepository:
    """牌局数据仓库"""
    
    def __init__(self, db_manager: DatabaseManager):
        """
        初始化牌局数据仓库
        
        Args:
            db_manager: 数据库管理器
        """
        self.db_manager = db_manager
    
    def save_game(self, game_data: Dict[str, Any]) -> int:
        """
        保存牌局
        
        Args:
            game_data: 牌局数据字典
            
        Returns:
            牌局ID
        """
        session = self.db_manager.get_session()
        
        try:
            # 创建牌局记录
            game = BridgeGame(
                dealer=game_data.get('dealer'),
                vul=game_data.get('vul'),
                contract=game_data.get('contract'),
                declarer=game_data.get('declarer'),
                dummy=game_data.get('dummy'),
                result=game_data.get('result'),
                notes=game_data.get('notes')
            )
            session.add(game)
            session.flush()
            
            # 保存叫牌记录
            for i, bid_record in enumerate(game_data.get('bidding', [])):
                bidding = BiddingRecord(
                    game_id=game.id,
                    player=bid_record.get('player'),
                    bid=bid_record.get('bid'),
                    sequence=i
                )
                session.add(bidding)
            
            # 保存打牌记录
            for i, play_record in enumerate(game_data.get('plays', [])):
                play = PlayRecord(
                    game_id=game.id,
                    trick_number=play_record.get('trick_number'),
                    player=play_record.get('player'),
                    card=play_record.get('card'),
                    sequence=i
                )
                session.add(play)
            
            session.commit()
            return game.id
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def get_game(self, game_id: int) -> Optional[Dict[str, Any]]:
        """
        获取牌局
        
        Args:
            game_id: 牌局ID
            
        Returns:
            牌局数据字典，如果不存在则返回None
        """
        session = self.db_manager.get_session()
        
        try:
            game = session.query(BridgeGame).filter(BridgeGame.id == game_id).first()
            if game is None:
                return None
            
            # 构建牌局数据字典
            game_data = {
                'id': game.id,
                'dealer': game.dealer,
                'vul': game.vul,
                'contract': game.contract,
                'declarer': game.declarer,
                'dummy': game.dummy,
                'result': game.result,
                'created_at': game.created_at.isoformat() if game.created_at else None,
                'notes': game.notes,
                'bidding': [
                    {
                        'player': bid.player,
                        'bid': bid.bid,
                        'sequence': bid.sequence
                    }
                    for bid in game.bidding_records
                ],
                'plays': [
                    {
                        'trick_number': play.trick_number,
                        'player': play.player,
                        'card': play.card,
                        'sequence': play.sequence
                    }
                    for play in game.play_records
                ]
            }
            
            return game_data
        finally:
            session.close()
    
    def search_games(self, filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        搜索牌局
        
        Args:
            filters: 过滤条件
            
        Returns:
            牌局列表
        """
        session = self.db_manager.get_session()
        
        try:
            query = session.query(BridgeGame)
            
            # 应用过滤条件
            if filters:
                if 'contract' in filters:
                    query = query.filter(BridgeGame.contract == filters['contract'])
                if 'declarer' in filters:
                    query = query.filter(BridgeGame.declarer == filters['declarer'])
                if 'result' in filters:
                    query = query.filter(BridgeGame.result == filters['result'])
                if 'vul' in filters:
                    query = query.filter(BridgeGame.vul == filters['vul'])
            
            games = query.all()
            
            return [
                {
                    'id': game.id,
                    'contract': game.contract,
                    'declarer': game.declarer,
                    'result': game.result,
                    'vul': game.vul,
                    'created_at': game.created_at.isoformat() if game.created_at else None
                }
                for game in games
            ]
        finally:
            session.close()
    
    def delete_game(self, game_id: int) -> bool:
        """
        删除牌局
        
        Args:
            game_id: 牌局ID
            
        Returns:
            是否删除成功
        """
        session = self.db_manager.get_session()
        
        try:
            game = session.query(BridgeGame).filter(BridgeGame.id == game_id).first()
            if game is None:
                return False
            
            session.delete(game)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def get_recent_games(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        获取最近的牌局
        
        Args:
            limit: 返回数量
            
        Returns:
            牌局列表
        """
        session = self.db_manager.get_session()
        
        try:
            games = session.query(BridgeGame).order_by(
                BridgeGame.created_at.desc()
            ).limit(limit).all()
            
            return [
                {
                    'id': game.id,
                    'contract': game.contract,
                    'declarer': game.declarer,
                    'result': game.result,
                    'vul': game.vul,
                    'created_at': game.created_at.isoformat() if game.created_at else None
                }
                for game in games
            ]
        finally:
            session.close()
    
    def count_games(self) -> int:
        """
        统计牌局总数
        
        Returns:
            牌局总数
        """
        session = self.db_manager.get_session()
        
        try:
            return session.query(BridgeGame).count()
        finally:
            session.close()
