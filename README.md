# 专业级桥牌决策机器人

融合桥牌专业知识、AI算法和复杂工程架构的智能决策系统，具备长期自我迭代优化能力。

## 项目概述

本项目旨在构建一款兼具「桥牌专业大师」「AI算法工程师」「复杂工程架构师」三重身份的专家级桥牌决策机器人，能够基于未完成牌局的全量信息，精准输出：
- **最优出牌选择**：明确指出下一步应出的牌
- **决策核心原因**：分战术/概率/风险三维度说明
- **关键概率数据**：牌张分布、成功率等量化指标
- **备选方案风险**：其他选择的成功率及潜在损失

## 核心能力

### 1. 知识体系
- 完整的桥牌规则库（叫牌/打牌/计分）
- 主流叫牌体系（自然/精确/蓝梅花）
- 牌型分布概率数据库
- 专家战术模式库（≥50种战术）

### 2. 算法架构
- **概率引擎**：贝叶斯推理 + 蒙特卡洛模拟
- **搜索引擎**：蒙特卡洛树搜索（MCTS）
- **学习引擎**：强化学习（PPO）+ 自我对弈
- **专家系统**：固化桥牌大师核心规则

### 3. 工程架构
- **数据层**：结构化存储、概率数据库、模型管理
- **解析层**：多格式输入支持、数据校验、特征提取
- **推理层**：多模块决策融合、结果解释
- **输出层**：多格式输出、决策追溯
- **训练层**：数据生成、自我对弈、模型评估

## 技术栈

- **语言**：Python 3.8+
- **深度学习**：PyTorch 2.0+
- **强化学习**：Stable Baselines3 2.0+
- **数值计算**：NumPy, SciPy
- **数据库**：SQLite (开发), PostgreSQL (生产)
- **测试**：pytest, coverage

## 项目结构

```
bridge_decision_robot/
├── src/                          # 源代码
│   ├── bridge_knowledge/         # 知识体系
│   │   ├── rules/               # 规则引擎
│   │   ├── probability/          # 概率计算
│   │   ├── tactics/             # 战术模式
│   │   └── bidding_systems/     # 叫牌体系
│   ├── probability_engine/      # 概率引擎
│   │   ├── bayesian/            # 贝叶斯推理
│   │   ├── distribution/        # 概率分布
│   │   └── inference/           # 概率推断
│   ├── search_engine/           # 搜索引擎
│   │   ├── mcts/                # MCTS实现
│   │   ├── node/                # 搜索节点
│   │   └── simulation/          # 模拟策略
│   ├── rl_engine/               # 强化学习引擎
│   │   ├── environment/         # RL环境
│   │   ├── agent/               # RL智能体
│   │   ├── training/            # 训练流程
│   │   └── memory/              # 经验回放
│   ├── expert_system/           # 专家系统
│   │   ├── rules/               # 规则定义
│   │   ├── engine/              # 推理引擎
│   │   └── scoring/             # 评分系统
│   ├── data_layer/              # 数据层
│   │   ├── database/            # 数据库管理
│   │   ├── models/              # 数据模型
│   │   ├── repositories/        # 数据访问
│   │   └── storage/             # 文件存储
│   ├── parser/                  # 解析层
│   │   ├── input_parser/        # 输入解析
│   │   ├── validator/           # 数据校验
│   │   ├── normalizer/          # 数据标准化
│   │   └── feature_extractor/   # 特征提取
│   ├── inference_engine/        # 推理引擎
│   │   ├── ensemble/            # 集成学习
│   │   ├── fusion/              # 决策融合
│   │   └── explainer/           # 结果解释
│   ├── output_layer/            # 输出层
│   │   ├── formatters/          # 格式化器
│   │   ├── visualizers/         # 可视化器
│   │   └── trace/               # 决策追溯
│   └── training_layer/          # 训练层
│       ├── generators/          # 数据生成
│       ├── self_play/           # 自我对弈
│       ├── evaluation/          # 模型评估
│       └── model_manager/       # 模型管理
├── tests/                        # 测试代码
│   ├── knowledge/
│   ├── probability/
│   ├── search/
│   ├── rl/
│   ├── expert/
│   ├── data_layer/
│   ├── parser/
│   ├── inference/
│   └── output/
├── data/                         # 数据目录
│   ├── bridge_games.db           # 牌局数据库
│   ├── probability_tables.h5     # 概率表
│   └── rl_models/                # RL模型
├── docs/                         # 文档
├── .comate/                      # 规格文档
├── requirements.txt              # 依赖文件
├── setup.py                      # 安装配置
└── README.md                     # 项目说明
```

## 开发进度

### 当前状态：阶段1 - 项目基础设施搭建（Week 1）

**已完成**：
- ✅ 项目目录结构规划
- ✅ .gitignore配置
- ✅ 项目README文档

**进行中**：
- 🔄 任务1.1：初始化项目结构和配置
- ⏳ 任务1.2：实现核心数据模型
- ⏳ 任务1.3：搭建数据层基础
- ⏳ 任务1.4：实现基础解析器

### 计划进度

| 阶段 | 内容 | 时间 | 状态 |
|------|------|------|------|
| 阶段1 | 项目基础设施搭建 | Week 1 | 🔄 进行中 |
| 阶段2 | 知识体系构建 | Week 2-3 | ⏳ 计划中 |
| 阶段3 | 概率引擎开发 | Week 4-5 | ⏳ 计划中 |
| 阶段4 | MCTS搜索引擎 | Week 6-7 | ⏳ 计划中 |
| 阶段5 | 推理引擎集成 | Week 8 | ⏳ 计划中 |
| 阶段6 | 输出层实现 | Week 9 | ⏳ 计划中 |
| 阶段7 | 强化学习框架 | Week 10-12 | ⏳ 计划中 |
| 阶段8 | 系统集成优化 | Week 13-15 | ⏳ 计划中 |
| 阶段9 | 测试和文档 | Week 16 | ⏳ 计划中 |
| 阶段10 | 部署和监控 | 持续 | ⏳ 计划中 |

## 快速开始

### 环境要求

- Python 3.8+
- pip

### 安装

```bash
# 克隆仓库
git clone <repository-url>
cd bridge_decision_robot

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 运行测试
pytest tests/
```

### 使用示例

```python
from src.parser import BridgeInputParser
from src.inference_engine import BridgeInferenceEngine

# 解析输入
parser = BridgeInputParser()
game_state = parser.parse({
    'dealer': 'N',
    'hands': {...},
    'contract': '4H',
    'declarer': 'S',
    'dummy': 'N'
})

# 推理决策
engine = BridgeInferenceEngine()
result = engine.infer(game_state)

# 输出结果
print(f"最优出牌: {result.card}")
print(f"置信度: {result.confidence:.1%}")
print(f"决策原因: {result.explanation}")
```

## 性能目标

- ✅ 单局决策响应时间：≤ 1秒
- ✅ 决策准确率：≥ 70%（相比人类专家）
- ✅ 代码覆盖率：≥ 80%
- ✅ 自我优化：准确率随训练持续提升

## 贡献指南

欢迎贡献代码、报告问题或提出改进建议！

1. Fork本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

## 许可证

本项目采用 MIT 许可证 - 详见 LICENSE 文件

## 联系方式

项目维护者：Bridge AI Bot
邮箱：bridge-ai-bot@local.dev

## 致谢

感谢所有为本项目做出贡献的开发者和桥牌爱好者！