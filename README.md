# Production, Trade, and Cross-Border Data Flows｜读书会协作仓库

本仓库整理 Chang、Cong、Wang、Zhang 的 NBER Working Paper 31416，包含逐步中文解析、完整读书会汇报、可审计的前序—后续文献谱系、企业有限最优复核、三个现实扩展和一个可分支阅读的静态网站。

## 直接使用

- **互动网页：**打开 [`docs/index.html`](docs/index.html)。建议启动本地服务器后访问，以获得稳定的 MathJax 公式渲染：

  ```bash
  python -m http.server 8000 --directory docs
  ```

  浏览器访问 <http://127.0.0.1:8000/>。

- **逐步解析 PDF：**[`deliverables/逐步解析.pdf`](deliverables/逐步解析.pdf)
- **原公式课件：**[`deliverables/公式讲解.pdf`](deliverables/公式讲解.pdf)
- **解析 Markdown：**[`content/论文解析.md`](content/论文解析.md)
- **文献谱系：**[`content/文献脉络与扩展文献.md`](content/文献脉络与扩展文献.md)，逐篇区分前置机制、CCWZ 的改进、后续直接扩展、经验检验和背景引用。

互动网页先按“研究问题 → 发现 → 文献谱系 → 有限最优复核 → 政策”线性展开，到扩展部分可以选择：

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

完整推导见 [`content/有限最优复核与修复.md`](content/有限最优复核与修复.md)，可运行检查见 [`scripts/check_finite_optimum.py`](scripts/check_finite_optimum.py)。

文献复核表明，CCWZ 的可辩护增量不是首次研究非竞争性、隐私、数据中介或数据积累，而是把**原始数据—目的地专用工作数据—企业数据存量—商品贸易—跨境政策**接进同一个两国一般均衡。后续文献主要推进到跨国政策协调、多国增长、企业创新和数据中心选址；目前未找到直接修复其线性无上限采购问题的论文。

## 目录

```text
content/
  论文解析.md                 既有逐步解析，内容保持不改
  完整汇报.md                 动机、结果、政策、贡献与质疑
  文献脉络与扩展文献.md       前置文献、CCWZ增量与后续研究分类
  有限最优复核与修复.md       独立复核和三种闭合方式
  扩展现实基础.md             三条路线的制度与研究依据
  routes/                     A、B、C 的完整逐步模型

deliverables/
  逐步解析.pdf                既有解析的排版 PDF
  公式讲解.pdf                原 57 页公式课件
docs/
  index.html                  包含全部内容的单页网站
  styles.css / app.js         视觉与交互
research/
  research-brief.md           研究边界和完成标准
  review-plan.md              文献检索合同
  source-ledger.csv           来源台账
  claim-evidence-matrix.csv   论断—证据表
  citation-lineage.csv        逐篇文献关系与核验边界
  openalex-citing-works.json  OpenAlex 引用候选快照
  finite-optimum-check.json   模型检查输出
scripts/
  build_site.py               从 Markdown 重建网页
  check_finite_optimum.py     符号和数值尾部检查
  check_site.py               网页与交付物验收
archive/
  公式讲解.tex                原课件源文件
  check_math.py               原 51 项数学检查脚本
```

## 重新构建

环境要求：Python 3.11+、Pandoc；本仓库的 Python 依赖写在 `requirements.txt`。

```bash
pip install -r requirements.txt
python scripts/check_finite_optimum.py
python scripts/build_site.py
python scripts/check_site.py
```

`build_site.py` 从 `content/` 生成 `docs/index.html` 和打印用的 `docs/逐步解析.html`。网站使用 CDN 版 MathJax；断网时正文仍可阅读，联网后公式自动排版。生成的 PDF 已提交仓库，普通协作者不需要本地 TeX 环境。若要重建 PDF，另需 XeLaTeX，再运行 `python scripts/build_pdf.py`。

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
- 每项重要论断的支持与边界：见 [`research/claim-evidence-matrix.csv`](research/claim-evidence-matrix.csv)。

本仓库没有收录 NBER 论文 PDF。请从 NBER 或 DOI 页面获取原文。论文目前按 NBER 工作论文引用；仓库不会把工作论文写成已发表期刊论文。

有限最优诊断针对原文附录所写的线性价格、连续采购和无上限选择集。三个修复及三条扩展是本项目提出的研究方案，不是作者已经证明的结果。开放经济 IRF、完整福利图和修复后一般均衡尚未独立复现。
