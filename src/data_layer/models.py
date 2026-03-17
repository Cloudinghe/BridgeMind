"""
数据层模型
Data Layer Models

定义数据库表结构和数据模型
"""

from datetime import datetime
from typing import List, Optional
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class BridgeGame(Base):
    """牌局表"""
    __tablename__ = 'bridge_games'
    
    id = Column(Integer, primary_key=True)
    dealer = Column(String(10))  # 发牌人 (N/E/S/W)
    vul = Column(String(20))  # 局况 (None/NS/EW/BOTH)
    contract = Column(String(20))  # 定约 (e.g., "4H", "3NT")
    declarer = Column(String(10))  # 庄家
    dummy = Column(String(10))  # 明手
    result = Column(Integer)  # 结果 (超额/宕墩数)
    created_at = Column(DateTime, default=datetime.now)
    notes = Column(Text)  # 备注
    
    # 关联表
    bidding_records = relationship("BiddingRecord", back_populates="game")
    play_records = relationship("PlayRecord", back_populates="game")


class BiddingRecord(Base):
    """叫牌记录表"""
    __tablename__ = 'bidding_records'
    
    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey('bridge_games.id'))
    player = Column(String(10))  # 叫牌人 (N/E/S/W)
    bid = Column(String(10))  # 叫牌 (e.g., "1C", "PASS", "DBL", "RDBL")
    sequence = Column(Integer)  # 叫牌序号
    created_at = Column(DateTime, default=datetime.now)
    
    # 关联表
    game = relationship("BridgeGame", back_populates="bidding_records")


class PlayRecord(Base):
    """打牌记录表"""
    __tablename__ = 'play_records'
    
    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey('bridge_games.id'))
    trick_number = Column(Integer)  # 墩数
    player = Column(String(10))  # 出牌人 (N/E/S/W)
    card = Column(String(10))  # 牌张 (e.g., "SA", "HK", "D2")
    sequence = Column(Integer)  # 出牌序号
    created_at = Column(DateTime, default=datetime.now)
    
    # 关联表
    game = relationship("BridgeGame", back_populates="play_records")


class CardDistribution(Base):
    """牌型分布概率表"""
    __tablename__ = 'card_distributions'
    
    id = Column(Integer, primary_key=True)
    distribution = Column(String(20), unique=True)  # 分布类型 (e.g., "4-3-3-3")
    probability = Column(Float)  # 概率
    description = Column(Text)  # 描述


class ModelMetadata(Base):
    """模型元数据表"""
    __tablename__ = 'model_metadata'
    
    id = Column(Integer, primary_key=True)
    model_name = Column(String(100))  # 模型名称
    model_version = Column(String(50))  # 模型版本
    model_path = Column(String(500))  # 模型文件路径
    performance = Column(Float)  # 性能指标 (e.g., 胜率)
    training_episodes = Column(Integer)  # 训练回合数
    created_at = Column(DateTime, default=datetime.now)
    notes = Column(Text)  # 备注