# Axiom Lab：数学建模研究与求解

> 先建立可信基线，再验证题目定制创新；从赛题和数据出发，完成求解、算法沉淀、论文写作与 PDF 验收。

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](../LICENSE)
[![Platform](https://img.shields.io/badge/OpenAI-Codex-green)](https://developers.openai.com/codex)

---

## 简介

**Axiom Lab** 是一个面向数学建模竞赛的 Codex Skill，适用于国赛、美赛、MathorCup 等场景。将赛题和数据放入比赛工作区后，调用 `$solve-math-modeling-competition` 或说 **“开始求解”**，Codex 即可连续完成：

- 读取赛题（PDF/DOCX）与附件数据（xlsx/docx/csv）
- 检索 Kaggle、原始论文和本地算法库
- 验证稳定基线，从真实误差和题目约束中生成创新假设
- 通过统一实验、必要消融和失败回退选择最终方法
- 编写 Python 代码逐题求解，自动生成结果与图表
- 将通过复用性、许可和测试检查的方法沉淀到公共算法库
- 撰写完整论文（LaTeX），含摘要/建模/检验/评价/参考文献
- 编译并逐页检查 PDF，修复错误和明显版式问题

---

## 核心特性

- **一键启动** - 说“开始求解”即可由 Codex 连续推进
- **完整流程** - 覆盖读取→规划→建模→求解→论文→编译的全部环节
- **证据检索** - 先检索 Kaggle、论文和本地算法库，再形成候选方法
- **候选分层** - 使用 `Baseline`、`Proven`、`Frontier` 区分实验角色，不按新旧机械排序
- **过时审查** - 核查维护状态、依赖兼容性、替代方法、泄漏、复现、许可与安全风险
- **创新诊断** - 从基线误差、题目结构和最近方法限制中寻找机会，不把新模型自动视为创新
- **消融验收** - 为核心创新预声明成功标准，验证失败时回退稳定方案并保留反证
- **公平比较** - 使用统一数据切分、指标、随机种子和调参预算比较候选
- **算法沉淀** - 将通过复用性、许可和测试检查的方法写回公共算法库
- **高质量论文** - 内置详尽的 LaTeX 规范（摘要≤900字/1页、流程图固定模板、统一 longtable 表格样式等）
- **跨平台中文** - Python 绘图自动适配 macOS/Windows/Linux 中文字体
- **鲁棒性强** - 含异常预案、灵敏度分析、交叉验证等学术规范环节
- **模块化论文** - 每问拆分为 分析与准备 + 建模与求解 两个子文件，便于组织与修改
- **自适应排版** - 表格自动换页、自动修正编译错误、排版优化循环

---

## 适用场景

- 全国大学生数学建模竞赛（CUMCM）
- 美国大学生数学建模竞赛（MCM/ICM）
- MathorCup 高校数学建模挑战赛
- 亚太地区大学生数学建模竞赛（APMCM）
- 研究生数学建模竞赛
- 其他各类数学建模竞赛

覆盖问题类型：优化/预测/分类/评价/机理分析/数据分析/建议总结等。

---

## 快速开始

### 第一步：安装配置

#### 1.1 安装并注册 Skill

本仓库的正式包位于 `../.agents/skills/solve-math-modeling-competition/`，直接打开仓库即可发现。若要在其他项目中使用，可复制该正式包：

```text
# 用户级：复制正式包到
$HOME/.agents/skills/solve-math-modeling-competition/

# 其他仓库级：复制正式包到
<repo>/.agents/skills/solve-math-modeling-competition/
```

目录内必须直接包含 `SKILL.md`。Codex 通常会自动发现变更；若未显示，重启 Codex。

#### 1.2 安装 Python 环境

**macOS/Linux：**
```bash
# 使用 conda（推荐）
conda create -n math建模 python=3.10
conda activate math建模

# 安装依赖
pip install pandas numpy matplotlib scipy scikit-learn chardet openpyxl xlrd
```

**Windows：**
```bash
# 使用 pip
pip install pandas numpy matplotlib scipy scikit-learn chardet openpyxl xlrd
```

#### 1.3 安装 LaTeX 环境

**macOS：**
```bash
# 安装 MacTeX（约 5GB）
brew install --cask mactex
```

**Windows：**
```bash
# 安装 MiKTeX
# 下载地址：https://miktex.org/download
# 安装完成后，在命令提示符中验证：
xelatex --version
```

**Ubuntu/Debian：**
```bash
sudo apt install texlive-xetex
```

### 第二步：准备比赛工作区

可让 Codex 运行本 skill 自带的初始化脚本，也可手动创建目录：

```text
python <skill-dir>/scripts/init_workspace.py <比赛工作区>
```

脚本会创建 `题目/`、`数据/`、`求解/`、`论文/`，并复制内置论文模板；默认不会覆盖已有文件。

### 第三步：放入赛题和数据

1. 将赛题文件（PDF 或 DOCX 格式）放入 `题目/` 文件夹
2. 将附件数据文件（xlsx/docx/csv 格式）放入 `数据/` 文件夹

示例：
```
题目/
├── 题目B：零售销售额的预测与数据分析.pdf
数据/
├── data.csv
```

### 第四步：在 Codex 中开始求解

1. 在 Codex 中打开比赛工作区，或在 Codex CLI 中进入该目录：
```bash
cd <比赛工作区>
```

2. 显式调用 skill：
```bash
$solve-math-modeling-competition 开始求解
```

3. Codex 将依次执行：
   - 读取赛题和数据
   - 检索候选并建立稳定基线
   - 诊断核心瓶颈，验证创新假设与消融
   - 根据创新验收结果晋升或回退
   - 逐题编写 Python 代码求解
   - 生成图表
   - 撰写完整 LaTeX 论文
   - 编译并逐页检查 PDF

---

## 项目结构

```
solve-math-modeling-competition/
├── SKILL.md                     # Codex 必需入口
├── agents/openai.yaml           # UI 元数据与调用策略
├── scripts/
│   ├── init_workspace.py        # 安全初始化比赛工作区
│   └── update_algorithm_index.py # 重建公共算法索引
├── references/
│   ├── solution-workflow.md     # 读题、建模、编码与验证规范
│   ├── research-and-promotion.md # 方法检索、实验比较与算法沉淀
│   └── paper-spec.md             # 论文写作、编译与视觉验收规范
├── assets/论文模板/              # 初始化时复制的只读模板
└── README.md
```

---

## 执行流程详解

### Step 0：读取输入
- 解析 `题目/` 下的 PDF/DOCX 文件
- 全量读取 `数据/` 下所有 xlsx/docx/csv
- 打印数据总览，自动识别问题数量 N

### Step 1：方法检索
- 检索本地 `算法/` 中的已验证条目
- 检索相似 Kaggle 竞赛、公开 Notebook 与特征工程方案
- 检索原始论文和领域研究，核验方法假设、来源与许可证
- 分别标记候选成熟度 `Baseline / Proven / Frontier` 与创新类型 `复现 / 适配 / 组合 / 题目定制假设`
- 找出最近方法，记录共同点、实质差异和未解决限制
- 审查更新时间、维护与依赖状态、替代方法及泄漏、复现、许可和安全风险
- 生成 `求解/方法调研.md` 和 `求解/候选方法清单.csv`

### Step 2：求解计划
生成 `求解/求解计划.md`，明确候选来源、公平比较协议、稳定基线门槛、核心创新问题、创新预算、预声明成功标准、失败回退和算法沉淀目标。

### Step 3：验证稳定基线
- 每问至少运行一个 `Baseline` 和足以形成可靠参照的成熟方法
- 统一数据切分、指标、随机种子和调参预算
- 基线未通过数据链路、验证协议和指标检查时先修复，不进入创新实验

### Step 4：创新假设与消融
- 从真实基线误差、题目约束、多问依赖和最近方法限制中生成 3–5 个可证伪假设
- 选择 1–2 个核心假设写入 `求解/创新实验矩阵.csv`
- 在同一协议下比较稳定基线、成熟强方法、前沿借鉴、题目定制创新和必要消融
- 达到预声明标准则晋升，失败则回退并写入 `求解/创新性审查报告.md`

### Step 5：完成逐问求解
- 根据创新验收选择创新、混合或稳定方案，不要求每问强行创新
- 保存全部成功与失败实验，更新 `模型比较.csv` 和 `模型比较.md`
- 生成最终数值、图表、稳健性和灵敏度结果

### Step 6：沉淀通用算法
- 去除赛题路径、字段和一次性业务逻辑
- 添加 `metadata.json`、最小示例和测试
- 核验来源与许可证后写入公共 `算法/`
- 生成 `求解/算法沉淀报告.md` 并更新 `算法/算法索引.md`

### Step 7：撰写论文
- 按规范逐章生成 LaTeX 文件
- 摘要 ≤900字、严格 1 页
- 用实际比较实验支持方法选择与模型检验
- 只把创新审查中“已验证”的项目写成创新点，并给出最近方法差异和消融证据

### Step 8：编译与视觉检查 PDF
```bash
cd 论文
xelatex -interaction=nonstopmode 论文.tex
xelatex -interaction=nonstopmode 论文.tex
```

编译后检查日志并逐页检查 PDF，反复修复直到无阻断错误和明显版式问题。

---

## 论文规范一览

| 章节 | 核心要求 |
|------|---------|
| 摘要 | ≤900字，必须=1页 |
| 引言 | 2-3段背景 + 问题重述 |
| 总体分析 | 三段式，逐问串联 |
| 模型假设 | itemize 格式，每条带编号 |
| 符号说明 | 统一 longtable 模板 |
| 模型建立与求解 | 每问拆 2 子文件 |
| 模型检验 | 误差分析 + 灵敏度分析 |
| 模型评价 | 优点4条 + 缺点2条 |
| 参考文献 | GB/T 7714-2015，8-15条 |

### 核心规范
- 正文禁止分点符号（1. 2. 3.）
- 禁止正文加粗（摘要和问题重述除外）
- 图宽 0.8\textwidth，表宽 \textwidth
- 所有表格统一使用 longtable 样式

---

## Python 代码规范

- 仅允许使用 matplotlib
- 先算后画：计算全部完成后再绘图
- 跨平台中文字体自动适配

```python
# 中文字体配置
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'Heiti TC', 'STHeiti', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False
```

---

## 自定义配置

### 调整论文模板
编辑 `论文/format.cls` 可自定义论文样式。

### 调整 AI 行为
编辑 `SKILL.md` 可调整主流程；检索与算法沉淀规范位于 `references/research-and-promotion.md`，详细求解和论文规范分别位于 `references/solution-workflow.md` 与 `references/paper-spec.md`。

---

## 版本历史

| 版本 | 更新内容 |
|------|---------|
| V3.0 | 新增稳定基线门槛、创新假设、消融验收与失败回退流程 |
| V2.7 | 修改模板小 bug |
| V2.5 | 表格自动换页、排版优化循环 |
| V2.0 | 论文模块化拆分、完整规范体系 |
| V1.0 | 初始版本 |

---

## 交流与支持

### 联系方式

flyningggg@gmail.com

### 获取帮助

如果你在使用过程中遇到问题，可以通过在 GitHub 提交 Issue 来获取联系

---

## 许可证

原创代码和文档采用 MIT License，详见 [../LICENSE](../LICENSE)。捆绑字体的许可证见 [../THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md)。

---
