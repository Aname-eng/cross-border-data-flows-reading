# Production, Trade, and Cross-Border Data Flows｜读书会协作仓库

本仓库整理 Chang、Cong、Wang、Zhang 的 NBER Working Paper 31416，包含逐步中文解析、35 页 explorable 学术演示、完整读书会汇报、可审计的前序—后续文献谱系、企业有限最优复核、三种数学修复、三条现实扩展和一个可分支阅读的静态网站。

## 直接使用

- **互动网页：**打开 [`docs/index.html`](docs/index.html)。建议启动本地服务器后访问，以获得稳定的 MathJax 公式渲染：

  ```bash
  python -m http.server 8000 --directory docs
  ```

  浏览器访问 <http://127.0.0.1:8000/>。

- **35 页互动演示：**[`docs/slides/index.html`](docs/slides/index.html)。采用 1280×720 Quarto reveal.js，含讲者驱动的模型阶段、可调尾部指数、10 个附录 side rooms 和每页 speaker notes。
- **演示 PDF：**[`deliverables/CCWZ-explorable-deck.pdf`](deliverables/CCWZ-explorable-deck.pdf)。35 页静态版会显示互动图形的完整终态，可脱离网页独立阅读。
- **逐步解析 PDF：**[`deliverables/逐步解析.pdf`](deliverables/逐步解析.pdf)
- **原公式课件：**[`deliverables/公式讲解.pdf`](deliverables/公式讲解.pdf)
- **解析 Markdown：**[`content/论文解析.md`](content/论文解析.md)
- **文献谱系：**[`content/文献脉络与扩展文献.md`](content/文献脉络与扩展文献.md)，逐篇区分前置机制、CCWZ 的改进、后续直接扩展、经验检验和背景引用。
- **全文深读关系矩阵：**[`content/深读关系矩阵.md`](content/深读关系矩阵.md) 与 [`research/deep-reading-matrix.csv`](research/deep-reading-matrix.csv)，把前置机制、CCWZ 增量、后续继承或偏离、页码证据和报告边界放在同一记录中。
- **背景全文复核：**[`research/background-reading-notes.md`](research/background-reading-notes.md)，记录 OECD（2019）、周念利等（2022）、刘斌与甄洋（2022）、Sun–Trefler（2023 工作论文版）和代丽华等（2024）的样本、定量结果与识别边界。
- **修复与扩展总览：**[`content/修复与扩展总览.md`](content/修复与扩展总览.md)，用同一套尾部公式连接三种数学闭合、三条经济路线、制度背景、文献依据和重算顺序；网站另提供可调 $\theta=\alpha\xi(e-1)$ 检查器。

互动网页按“研究问题 → 发现 → 文献谱系 → 错误与修复 → 完整复核 → 三条扩展 → 原始解析”线性展开，到扩展部分可以选择：

- 路线 A：安全、许可与固定合规成本；
- 路线 B：数据质量、收益饱和与算力互补；
- 路线 C：训练、研发与利用能力积累；
- 或保留默认的 A → B → C 全部通读。

路线选择只改变显示顺序；全部材料仍保存在页面和仓库中。

## 最重要的研究判断

论文把原始数据提供地、工作数据加工和使用地、最终商品消费地分开，从而能分析商品贸易与数据流动的共同福利效果。作者报告，在一个代表性校准切片中，加入双向数据流把双方愿意开放的本国数据重要性区间从 `[0.75, 1.22]` 扩到 `[0.48, 1.61]`。这些数值是作者的参数化机制展示，不是本项目独立复现或现实政策估计。

本项目重新从原文附录检查了企业数据问题。若工作数据按线性单位价格出售、单个企业可连续且无限采购，优化产量后的利润指数为：

- 封闭经济：`αξ(ρ−1)=20/3>1`；
- 开放经济：`αξ(m−1)=4/3>1`。

因此，该字面选择集没有有限最大值。正文也可被理解为数据商向所有企业授权同一个有限数据包；若采用这种解释，需要显式加入容量或许可合同。仓库提出三种修复，并推荐使用在基准稳态保留局部弹性、长期收益有界的有效数据服务 `g(Φ)`。

完整推导见 [`content/有限最优复核与修复.md`](content/有限最优复核与修复.md)。[`scripts/check_finite_optimum.py`](scripts/check_finite_optimum.py) 用 SymPy 验证一般利润指数并作数值尾部检查；[`verification/lean/CCWZFiniteOptimum/Basic.lean`](verification/lean/CCWZFiniteOptimum/Basic.lean) 形式化证明两个基准多项式尾部无上界。Lean 只验证抽象命题，经济合同与价格口径仍由原文审计和人工推导确定。

文献复核表明，CCWZ 的可辩护增量不是首次研究非竞争性、隐私、数据中介或数据积累，而是把**原始数据—目的地专用工作数据—企业数据存量—商品贸易—跨境政策**接进同一个两国一般均衡。当前语料清单登记 25 份 PDF、1,012 页，并用阅读状态区分模型审计、全文通读、聚焦全文、节读、版本比较和被替代版本。原有 5 份待读背景论文已全部完成聚焦全文复核，清单中不再有 `queued` 项。Google Scholar 的 20 条引用结果已全部分类；Lee（2025）经参考文献复核不属于 CCWZ 引用者，王永进等（2025）则由《金融研究》官方全文确认直接引用 CCWZ，但采用 Caliendo–Parro 量化贸易骨架。Dubus、Kässi–Lehdonvirta、Ito–Tomiura、Demirer 等论文的模型条件、识别设计和数量级均已回到全文核验。目前仍未找到直接修复 CCWZ 线性无上限采购问题并重算福利的论文。

## 目录

```text
content/
  论文解析.md                 既有逐步解析，内容保持不改
  完整汇报.md                 动机、结果、政策、贡献与质疑
  文献脉络与扩展文献.md       前置文献、CCWZ增量与后续研究分类
  深读关系矩阵.md             18项全文/摘要关系与证据综合
  修复与扩展总览.md           尾部诊断、三种闭合、三条路线与文献边界
  有限最优复核与修复.md       独立复核和三种闭合方式
  扩展现实基础.md             三条路线的制度与研究依据
  routes/                     A、B、C 的完整逐步模型

deliverables/
  CCWZ-explorable-deck.pdf    35页静态学术汇报
  逐步解析.pdf                既有解析的排版 PDF
  公式讲解.pdf                原 57 页公式课件
docs/
  index.html                  包含全部内容的单页网站
  slides/                     Quarto reveal.js 互动演示
  styles.css / app.js         视觉与交互
presentation/
  index.qmd                   25页主线 + 10页附录
  theme.scss / stage.js       视觉系统与讲者驱动交互
  slide-plan.md               逐页论证、节奏和静态导出契约
  scripts/                    资产生成与演示验收
research/
  research-brief.md           研究边界和完成标准
  review-plan.md              文献检索合同
  source-ledger.csv           来源台账
  claim-evidence-matrix.csv   论断—证据表
  citation-lineage.csv        逐篇文献关系与核验边界
  deep-reading-matrix.csv     前置—CCWZ—后续的18项全文关系矩阵
  paper-corpus-manifest.csv   25份PDF、1012页及人工阅读状态
  background-reading-notes.md 5份背景论文的结果与识别边界
  deep-reading-brief.md       全文深读问题、证据协议与完成标准
  openalex-citing-works.json  OpenAlex 8 条引用候选快照
  google-scholar-citing-works.json  Google Scholar 20 条引用结果快照
  finite-optimum-check.json   模型检查输出
scripts/
  build_lineage.py            校验并发布规范文献谱系
  build_site.py               从 Markdown 重建网页
  check_finite_optimum.py     符号和数值尾部检查
  extract_paper_corpus.py     更新本地PDF清单且保留人工阅读状态
  check_site.py               网页与交付物验收
  verify_workspace.py         一条命令运行确定性验收链
.github/workflows/verify.yml  PR与分支推送的远端验收
verification/lean/
  CCWZFiniteOptimum/Basic.lean  基准尾部无上界形式化证明
archive/
  公式讲解.tex                原课件源文件
  check_math.py               原 51 项数学检查脚本
```

## 重新构建

环境要求：Python 3.11+、Node.js 18+、Pandoc 3.10.2；完整 Lean 验证另需 `lake`，重建演示另需 Quarto 1.11+。本仓库的 Python 依赖写在 `requirements.txt`。

```bash
pip install -r requirements.txt
python scripts/verify_workspace.py
# 加上 Lean 形式化验证：
python scripts/verify_workspace.py --with-lean
```

这条入口依次运行有限最优推导、文献谱系校验、网站重建、演示与网站验收、Python/JavaScript 语法和 Git 空白检查。GitHub Actions 会在 PR 和 `main` 分支推送时运行同一验收链，并在独立任务中编译 Lean；工作流只验证，不发布 GitHub Pages，避免同一功能分支同时触发 push 与 PR 两套重复任务。

若需要重建演示本身，再运行：

```bash
python presentation/scripts/build_deck.py
# 打开 docs/slides/?print-pdf，将35页打印为 deliverables/CCWZ-explorable-deck.pdf
python presentation/scripts/check_deck.py
```

`build_site.py` 从 `content/` 生成 `docs/index.html` 和打印用的 `docs/逐步解析.html`，并把演示 PDF 复制到网站下载区。网站使用 CDN 版 MathJax；断网时正文仍可阅读，联网后公式自动排版。`presentation/scripts/build_deck.py` 先在 `presentation/_render/` 完成 Quarto 构建，再原子式更新 `docs/slides/`，避免陈旧哈希资源残留；它优先使用系统 Quarto，也支持被忽略的 Windows 本地工具链 `tools/quarto/Quarto/bin/quarto.exe`。若要重建逐步解析 PDF，另需 XeLaTeX，再运行 `python scripts/build_pdf.py`。

## 协作方式

```bash
git clone https://github.com/Aname-eng/cross-border-data-flows-reading.git
cd cross-border-data-flows-reading
git checkout -b <你的分支名>
```

修改 Markdown 后运行构建和验收脚本，只提交源文件、生成后的 `docs/` 与需要更新的交付 PDF。建议将经济学判断、公式改动和纯排版改动分成不同提交，便于复核。

## 来源与边界

- 主模型和数值结论：NBER Working Paper 31416，2025 年 3 月修订版，<https://doi.org/10.3386/w31416>。
- 用户提供材料：作者 2026 年 AFA 报告，用于演讲主线。
- 文献与制度来源：见 [`research/source-ledger.csv`](research/source-ledger.csv)。
- 前置和后续论文的关系分类：见 [`research/citation-lineage.csv`](research/citation-lineage.csv)。
- 全文关系、页码和继承/偏离判断：见 [`research/deep-reading-matrix.csv`](research/deep-reading-matrix.csv)。
- PDF 阅读状态与证据边界：见 [`research/paper-corpus-manifest.csv`](research/paper-corpus-manifest.csv)。
- 每项重要论断的支持与边界：见 [`research/claim-evidence-matrix.csv`](research/claim-evidence-matrix.csv)。

本仓库没有收录 NBER 论文 PDF。请从 NBER 或 DOI 页面获取原文。`build/papers/` 中的研究 PDF 与提取文本仅用于本地核验，并由 `.gitignore` 排除；CSV 清单保留可审计的文件名、页数、阅读深度和来源边界。论文目前按 NBER 工作论文引用；仓库不会把工作论文写成已发表期刊论文。

有限最优诊断针对原文附录所写的线性价格、连续采购和无上限选择集。三个修复及三条扩展是本项目提出的研究方案，不是作者已经证明的结果。开放经济 IRF、完整福利图和修复后一般均衡尚未独立复现。
