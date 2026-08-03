# Axiom Lab

> 面向数学建模竞赛的证据驱动型研究、求解与论文生成系统。

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Codex Skill](https://img.shields.io/badge/OpenAI-Codex-green.svg)](https://developers.openai.com/codex)

Axiom Lab 将赛题理解、数据审计、方法检索、稳定基线、创新验证、算法沉淀和论文写作连接为一条可追溯工作流。它先检索 Kaggle、原始论文和本地算法库，分别标记候选成熟度与创新类型并完成最近方法和过时性审查；基线通过后，再从真实误差和题目约束中提出可证伪创新，通过同协议比较与消融决定晋升或回退，最后只把经过验证的通用实现沉淀到算法库。

---

## 仓库结构

```
.
├── .agents/skills/solve-math-modeling-competition/  # Codex 自动发现的标准 Skill
├── Skill/          # 示例比赛工作区与 Codex Skill 可读副本
├── 模板/           # 论文 LaTeX 模板源头（format.cls + 空白 tex + 字体）
└── 算法/           # 常用数学建模算法库（按类型分类）
```

## 各模块说明

### `.agents/skills/solve-math-modeling-competition/`
Axiom Lab 的正式 Codex Skill。直接在本仓库打开 Codex 即可被发现，也可将该目录复制到 `$HOME/.agents/skills/` 作为用户级 Skill。调用后会连续完成：读取输入 → 检索与最近方法审查 → 验证稳定基线 → 提出并消融创新假设 → 晋升或回退 → 逐题求解 → 沉淀通用算法 → 撰写论文 → 编译并逐页检查 PDF。

入口为 `.agents/skills/solve-math-modeling-competition/SKILL.md`。

### Skill/
保留示例输入、求解结果、论文和一份便于阅读的 Codex Skill 副本；正式运行以 `.agents/skills/solve-math-modeling-competition/` 为准。

### 模板/
论文 LaTeX 模板的**唯一源头**。包含 `format.cls` 样式文件、思源宋体字体和章节模板。正式 skill 的 `assets/论文模板/` 由本目录同步而来。

详见 [模板/README.md](模板/README.md)。

### 算法/
跨赛题复用的算法库，按问题类型分类。Skill 会在求解前检索其中的已验证条目，并在公平实验结束后把通过复用性、许可和测试检查的方法沉淀回来。

详见 [算法/README.md](算法/README.md)。

---

## 使用方式

### 使用 Axiom Lab
1. 在独立比赛工作区中准备 `题目/` 与 `数据/`；也可让 Codex 运行 skill 自带的 `scripts/init_workspace.py`
2. 将赛题放入 `题目/`，附件放入 `数据/`
3. 在该工作区调用 `$solve-math-modeling-competition`，或直接说“开始求解”

### 安装 Python 依赖

```text
python -m pip install -r requirements.txt
```

生成论文还需要可用的 XeLaTeX 环境。

### 单独使用论文模板
1. 复制 `模板/` 下所有文件到工作目录
2. 编辑各 tex 文件填写内容
3. `xelatex 论文.tex` 编译

---

## 维护约定

- **论文模板**：`模板/` 为源头，修改后同步至 `.agents/skills/solve-math-modeling-competition/assets/论文模板/`
- **编译产物**：`.aux` `.log` `.pdf` 等已通过 `.gitignore` 忽略
- **命名规范**：代码、图、CSV、tex 文件一律中文命名

---

## 参与贡献

提交算法、Skill 或模板改进前，请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。安全问题请按 [SECURITY.md](SECURITY.md) 私密报告。

## 许可证

Axiom Lab 的原创代码和文档采用 [MIT License](LICENSE)。仓库捆绑的思源宋体文件采用 SIL Open Font License 1.1，详见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) 和 [LICENSES/OFL-1.1.txt](LICENSES/OFL-1.1.txt)。
