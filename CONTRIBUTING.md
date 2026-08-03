# Contributing to Axiom Lab

感谢你改进 Axiom Lab。提交变更前，请确保内容可复现、来源清楚，并且没有包含比赛私有数据或密钥。

## 本地准备

1. 安装 Python 3.10 或更高版本。
2. 创建虚拟环境并运行 `pip install -r requirements.txt`。
3. 若修改论文模板，安装 XeLaTeX 并至少编译两遍 `论文.tex`。
4. 运行 `python .github/scripts/validate_repository.py`。

## 修改 Skill

正式 Skill 位于 `.agents/skills/solve-math-modeling-competition/`。`Skill/` 中保留一份可读副本和示例工作区；修改 Skill 时必须同步以下内容：

- `SKILL.md`
- `agents/`
- `references/`
- `scripts/`
- `assets/`

仓库校验会拒绝不同步的提交。

## 贡献算法

每个算法使用独立目录：

```text
算法/<分类>/<算法名>/
├── 算法实现.py
├── 最小示例.py
├── 测试.py
└── metadata.json
```

算法必须满足：

- 不依赖固定绝对路径、比赛字段名或私有数据；
- 明确输入、输出、参数、随机种子和失败条件；
- 包含可独立运行的最小示例和测试；
- 在 `metadata.json` 中记录来源、许可证、依赖和真实验证结果；
- 上游许可证允许重新分发，或代码为独立实现并准确注明思想来源。

添加或更新算法后，运行：

```text
python .agents/skills/solve-math-modeling-competition/scripts/update_algorithm_index.py 算法
```

## Pull Request

保持每个 PR 聚焦一个目标，并说明：问题、改动、验证命令、结果、兼容性影响、来源与许可证。不要提交 `.env`、访问令牌、个人数据、未获授权的竞赛附件或生成缓存。
