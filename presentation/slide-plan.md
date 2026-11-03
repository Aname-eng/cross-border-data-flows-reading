# Explorable deck plan｜CCWZ：数据跨境流动如何改变生产与贸易

## Brief

- **Audience:** economics graduate reading group; comfortable with CES demand and general equilibrium, but has not read CCWZ.
- **Occasion:** 45-minute paper presentation followed by 15 minutes of research discussion.
- **Outcome:** listeners can reconstruct the paper's data chain, interpret its welfare intervals as calibrated participation constraints, explain the finite-optimum problem under the literal contract, and distinguish three repair/extension routes.
- **Output:** Quarto reveal.js, 1280×720, no scrolling; live HTML plus a static PDF whose final fragment state carries the complete argument.
- **Running example:** consumers in Home and Foreign generate route logs; processors turn raw logs into destination-specific route datasets; firms accumulate the datasets as productive knowledge and trade differentiated goods.
- **Visual semantics:** Home = teal; Foreign = coral; raw data = gold; working data = violet; goods = navy; privacy/constraint = rust; repair = green. Solid line = author model/result; dashed or hatched = independent audit/extension.
- **Evidence boundary:** every quantitative claim is tagged as author calibration, independent derivation, or later empirical estimate. Working papers retain their version/date labels.

## Narrative arc

The first act earns the model by following one route log from a consumer to a traded good. The second act uses the author's welfare intervals to show what the model buys. The third act turns the model against itself: the same elasticities imply that the literal firm problem has no finite maximum. The final act repairs the problem and uses the literature to choose among contract, information-production, and capability extensions.

## Core slides

| # | Assertion title | Audience move | Evidence | Composition / build | Notes payload |
|---|---|---|---|---|---|
| 1 | **跨境数据流把“贸易什么”变成了一个动态问题** | See the paper as a bridge between data economics and trade, not as a generic privacy paper | CCWZ 2025 revision, title/abstract | Sparse title; two-country line plus moving data packet | Version: 2023 first draft, 2025-03 NBER revision; AFA 2026 is presentation material |
| 2 | **这场报告只回答三个问题** | Orient: mechanism, welfare, model closure | Project synthesis | Three large numbered questions | 45+15 timing; labels for author result / audit / extension |
| 3 | **一条路线日志会经历三次变形** | Separate raw data, working data, firm stock | CCWZ eqs. (3)–(5), (8)–(11) | Presenter-driven SVG: log → cleaned destination packet → stock cylinder | Running example remains schematic; notation mapping in appendix |
| 4 | **数据可以复制，但把它变成可用信息仍要花劳动** | Understand nonrivalry plus processing cost | CCWZ data producer; Jones–Tonetti | Split visual: copy at zero marginal duplication cost / processing labor meter | Nonrivalry does not imply zero processing cost or unlimited distinct information |
| 5 | **CCWZ 把四个地点和两条跨境流接进同一均衡** | See the paper's genuine integration | CCWZ model, pp.8–15 | Full-stage SVG with consumers, processors, firms, goods; click stages | Four places: source, processing, use, consumption |
| 6 | **开放制度不是一个开关，而是五种可比较的组合** | Map closed, goods-only, two unilateral data-flow cases, bilateral opening | CCWZ §2.3 | Five regime glyphs on one axis; active links highlighted | Explain direction of unilateral flow precisely |
| 7 | **没有数据流时，能力差距可能让商品贸易失去双方支持** | Replace “trade is always good” with participation constraints | CCWZ welfare analysis | Two welfare bands that stop overlapping as ξ diverges | Fixed calibration; welfare is steady-state utility |
| 8 | **双向数据流扩大双方都愿意开放的能力区间** | Learn the headline result | CCWZ Table 2, foreign ξ*=1 | Recoloured interval chart: [0.75,1.22] → [0.48,1.61] | Author calibration, not causal estimate or universal theorem |
| 9 | **区间扩大来自新的补偿渠道，不是“开放总是好”** | Explain mechanism behind the band | CCWZ Table 2 and text | Four-step causal strip: foreign data → productivity → prices/trade → both participation constraints | Country-specific gains can still be negative outside the interval |
| 10 | **数据开放还会改变冲击从哪里传来、向哪里扩散** | Understand dynamics beyond steady state | CCWZ §4 | Before/after stock-flow stage for productivity vs privacy shocks | No independent IRF replication; describe author mechanism only |
| 11 | **CCWZ 的贡献是连接五个环节，而不是发明每个环节** | Calibrate novelty claim | Deep-reading matrix D01–D09 | Literature river converging on focal bridge | Farboodi–Veldkamp predates broad “first data accumulation” claim |
| 12 | **四组前置文献分别交来了复用、隐私、增长和信息边界** | Place mechanisms accurately | JT; Ichihashi/Acemoglu/BBG; Cong; Farboodi–Veldkamp | Four-column mechanism map | Each predecessor's object and what CCWZ drops |
| 13 | **后续研究没有沿一条路走，而是向四个边际分叉** | Avoid treating every citation as direct extension | Deep-reading matrix D10–D18 | Branching map: growth, IO coordination, quantitative trade, empirical margins | Lee does not cite CCWZ; Wang 2025 does; Wang 2024 remains summary-only |
| 14 | **“数据效应”至少包含生产率、投入、区位和价值链四个量** | Interpret later estimates without pooling them | Ito; Demirer; Kässi–Lehdonvirta; Liu | Four aligned number cards with design labels | 4–5/5–6%; −25/−15%; +49/+32%; −0.0385 |
| 15 | **作者把数字定位为机制展示，而不是结构识别** | Read calibration with correct strength | CCWZ pp.16–17 | Recoloured crop of calibration table plus author quote callout | Data-related parameters partly discretionary; no full-scale calibration |
| 16 | **但字面企业合同让数据投资没有有限最大值** | Experience the conceptual reversal | CCWZ Appendix A.1/A.2; independent audit | Contract card: φ≥0, price Pφφ, no cap; red tail begins | Conditional on fixed positive prices/demand, continuous unbounded purchase |
| 17 | **优化商品产量后，问题只剩一个尾部指数** | Follow the derivation without algebra overload | Independent derivation | Three equation steps ending in θ=αξ(e−1) | Full derivation in appendix; e=ρ closed, e=m open |
| 18 | **基准指数在封闭和开放经济都大于 1** | See why linear cost loses | α=1/3, ξ=1, ρ=21, m=5 | Interactive SVG/slider with closed 20/3 and open 4/3; print shows baseline | Slider changes ξ; threshold lines at 0.15 and 0.75 |
| 19 | **一阶条件的正根反而是局部最小值** | Stop equating solver convergence with optimum | f(L)=−qL+βCL^θ | Curve stage: fall → stationary point → explosive tail; f''>0 callout | Numerical bounded search is illustration, not proof |
| 20 | **三种闭合方式修的是三个不同对象** | Compare technology, contract, and absorption cost | Project repairs | Three doors: bounded g(Φ), license cap, convex installation | Each repair changes different equilibrium conditions |
| 21 | **有界有效数据服务最适合作为基准修复** | Choose a preferred repair | Proposed g(Φ) | Local-tangent / global-saturation plot | Preserves g(Φ̄) and local elasticity ξ; benefits bounded at infinity |
| 22 | **修复保留局部机制，却要求重新计算所有福利区间** | Separate qualitative survival from quantitative invalidation | Independent audit | “Keep / recompute” two-column ledger | Recompute Euler, price, five regimes, IRFs, policy; no claim of replicated new equilibrium |
| 23 | **现实扩展也要分开：合同、信息生产、能力形成** | Map evidence to research designs | Routes A/B/C; deep-reading synthesis | Three route cards linked to appendix side rooms | A: licensing; B: quality/saturation/compute; C: R&D/capability |
| 24 | **开放、许可和吸收能力必须一起设计** | Leave with decision-facing policy meaning | Synthesis | Policy triangle with three failure modes | Flow volume alone is not welfare; onshore investment is not total compute |
| 25 | **保留这座桥，但要补上它的承重结构** | Close on balanced judgment | Whole presentation | Return to opening bridge, now with three supports | Paper remains valuable; repair before quantitative policy use |

## Appendix side rooms

| ID | Assertion title | Purpose / return path |
|---|---|---|
| A1 | **三个数据对象各有一条方程和一个价格口径** | Full notation map for slides 3–5 |
| A2 | **五种开放制度改变的是不同的箭头** | Exact regime definitions for slide 6 |
| A3 | **Table 2 的完整区间比一个标题数字更丰富** | Full recoloured table for slides 8–9 |
| A4 | **一次性偏离已经足以证明尾部无上界** | Complete proof and θ cases for slides 16–19 |
| A5 | **Lean 证明的是多项式尾部，不是整个经济模型** | Formal theorem statements and mapping boundary |
| A6 | **Dubus 的协调结论在 CES 下恰好消失** | Welfare derivative, variable-elasticity condition |
| A7 | **王永进等继承政策问题，却换成外部规模的量化贸易模型** | Model skeleton, calibration and welfare numbers |
| A8 | **四组经验结果来自四套不同识别设计** | DID / event study / IV / fixed-effects comparison |
| A9 | **25 份 PDF 不等于 25 篇逐页全文审计** | Corpus statuses, evidence grades, version boundaries |
| A10 | **参考文献与版本记录** | Full sources; return to closing slide |

## Static-export contract

- The final state of each staged SVG is visible in `?print-pdf` mode.
- Every interactive slide contains a declarative title and a baseline numeric state; no conclusion depends on moving a slider.
- Speaker notes hold derivation details, source pages, caveats, and transitions; visible slide text stays at projection size.
- Appendix links are optional during the talk. The linear core remains complete without visiting a side room.
