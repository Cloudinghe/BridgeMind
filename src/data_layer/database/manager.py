"""
数据库管理器
Database Manager

管理数据库连接和表创建
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Optional
import os

from ..models import Base


class DatabaseManager:
    """数据库管理器"""
    
    def __init__(self, db_url: Optional[str] = None):
        """
        初始化数据库管理器
        
        Args:
            db_url: 数据库URL，如果为None则使用默认SQLite
        """
        if db_url is None:
            # 创建data目录
            data_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data')
            os.makedirs(data_dir, exist_ok=True)
            
            # 使用SQLite
            db_path = os.path.join(data_dir, 'bridge_games.db')
            db_url = f'sqlite:///{db_path}'
        
        self.engine = create_engine(db_url, echo=False)
        self.SessionLocal = sessionmaker(bind=self.engine, autocommit=False, autoflush=False)
        self.create_tables()
    
    def create_tables(self):
        """创建所有表"""
        Base.metadata.create_all(self.engine)
    
    def drop_tables(self):
        """删除所有表（谨慎使用）"""
        Base.metadata.drop_all(self.engine)
    
    def get_session(self) -> Session:
        """
        获取数据库会话
        
        Returns:
            SQLAlchemy Session对象
        """
        return self.SessionLocal()
    
    def get_engine(self):
        """
        获取数据库引擎
        
        Returns:
            SQLAlchemy Engine对象
        """
        return self.engine
