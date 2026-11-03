# 路线 B：数据质量、收益饱和与算力互补

这条路线区分物理数据量与有效信息，并让数据和算力共同决定有上界的生产率。以下逐步模型完整保留原解析的 B.1—B.5。它既是现实扩展，也是本项目推荐的有限最优修复方向。

### 12B. 跨境字节数不等于有效信息：数据质量、饱和与算力互补

#### B.1 后续文献改变了什么判断

Farboodi–Veldkamp 的 2024 版把信息价值建在预测误差下降上，旧数据因预测对象变化而贬值；Veldkamp–Chung（2024，§4.1）强调预测改进存在边界。它们支持将原文恒定弹性 $\Phi^{\alpha\xi}$ 改为有限的预测生产率收益，但没有要求采用下面某个特定函数。[S7–S8]

Sun 和 Trefler 的 2023 年工作论文用 35,575 款应用和 63,679 件 AI 专利测量应用级 AI。其基准 IV 报告，一四分位距 AI 增加对应外国用户增加 2.67 个对数点；在 25 个最大经济体的高低数据限制比较中，作者计算的指数化乘数从 13.2 降至 7.5。[S45，Tables 1、5] 这支持数据可达性与算法互补，却不识别下面函数的饱和参数；成本移位工具变量的排除限制仍是因果解释的条件。

本扩展给出一种可解析、可估计的替换：质量不同的数据先换成有效单位，数据与算力再共同决定有上界的生产率。

#### B.2 先将外国数据换成有效单位

令 $\upsilon_F>0$ 表示一单位外国工作数据对本国任务的有效质量，可包含语言适配、行业覆盖和记录准确度。设

$$
z_F=\upsilon_F\varphi_F,\qquad
\varphi=\left[\chi^{1/\omega}\varphi_H^{(\omega-1)/\omega}
+(1-\chi)^{1/\omega}z_F^{(\omega-1)/\omega}\right]^{\omega/(\omega-1)}.
$$

取得一单位 $z_F$ 需要购买 $1/\upsilon_F$ 单位原外国数据，所以其有效单价是 $\widetilde p_F=p_F/\upsilon_F$。按 C7—C8：

$$
q=\left[\chi p_H^{1-\omega}+(1-\chi)(p_F/\upsilon_F)^{1-\omega}\right]^{1/(1-\omega)},
$$

$$
z_F=(1-\chi)\left(\frac{p_F/\upsilon_F}{q}\right)^{-\omega}\varphi.
$$

原始外国工作数据量为 $\varphi_F=z_F/\upsilon_F$，故

$$
\boxed{\frac{\varphi_F}{\varphi_H}
=\frac{1-\chi}{\chi}\,\upsilon_F^{\omega-1}(p_F/p_H)^{-\omega}.}
\tag{B1}
$$

对 $\ln\upsilon_F$ 求导：

$$
\frac{\partial\ln(\varphi_F/\varphi_H)}{\partial\ln\upsilon_F}=\omega-1,
\qquad
\frac{\partial\ln(z_F/\varphi_H)}{\partial\ln\upsilon_F}=\omega.
$$

因此，外国数据质量改善总会提高其相对有效使用量；但当 $\omega<1$ 时，达到更高有效用量可能反而需要更少的原始外国数据。这给出一个直接的测量结论：物理流量下降不必表示信息利用下降。

#### B.3 再替换生产函数中的无限数据乘数

令 $\mathcal M_t\ge0$ 为算力服务，价格为 $c_M>0$。设

$$
\boxed{T_t=A_tK_t^\alpha n_t^{1-\alpha}
\exp\left[\zeta\frac{\Phi_t}{k_0+\Phi_t}
\frac{\mathcal M_t}{m_0+\mathcal M_t}\right],}
\tag{B2}
$$

其中 $k_0,m_0,\zeta>0$。$\Phi$ 仍按原文方式积累；改变的是其生产率映射，而不是将存量悄悄换成当期数据流。

因为两个分式都在 $[0,1)$，有

$$
1\le\exp\left[\zeta\frac\Phi{k_0+\Phi}\frac{\mathcal M}{m_0+\mathcal M}\right]<e^\zeta.
$$

所以，在 $\zeta$ 固定时，单靠不断堆积数据和算力，不能让这一生产率乘数无限增长。在第 7.6 节固定价格的单企业问题中，令该乘数为 $G$，重新优化商品产量后的经营利润为 $c_1G^{\rho-1}\le c_1e^{\zeta(\rho-1)}$；数据采购和算力支出均非负，确定性无限期利润的上界因而为 $c_1e^{\zeta(\rho-1)}/(1-\beta)$。这排除了无限采购数据带来无界超线性收益的偏离。其他技术进步仍可带来增长。

#### B.4 逐步求两项边际收益

对 B2 取对数：

$$
\ln T=\ln A+\alpha\ln K+(1-\alpha)\ln n
+\zeta\frac\Phi{k_0+\Phi}\frac{\mathcal M}{m_0+\mathcal M}.
$$

先求分式导数：

$$
\frac{d[\Phi/(k_0+\Phi)]}{d\Phi}
=\frac{k_0+\Phi-\Phi}{(k_0+\Phi)^2}
=\frac{k_0}{(k_0+\Phi)^2}.
$$

于是

$$
\frac{\partial\ln T}{\partial\Phi}
=\zeta\frac{k_0}{(k_0+\Phi)^2}\frac{\mathcal M}{m_0+\mathcal M},
$$

$$
\boxed{\frac{\partial T}{\partial\Phi}
=T\zeta\frac{k_0}{(k_0+\Phi)^2}\frac{\mathcal M}{m_0+\mathcal M}.}
\tag{B3}
$$

算力分式的导数为 $d[\mathcal M/(m_0+\mathcal M)]/d\mathcal M=m_0/(m_0+\mathcal M)^2$。将它乘上 $T\zeta\Phi/(k_0+\Phi)$，得到

$$
\boxed{\frac{\partial T}{\partial\mathcal M}
=T\zeta\frac\Phi{k_0+\Phi}\frac{m_0}{(m_0+\mathcal M)^2}.}
\tag{B4}
$$

对 $\ln T$ 求交叉导数：

$$
\boxed{\frac{\partial^2\ln T}{\partial\Phi\partial\mathcal M}
=\frac{\zeta k_0m_0}{(k_0+\Phi)^2(m_0+\mathcal M)^2}>0.}
\tag{B5}
$$

所以两者具有对数互补性。产出水平的交叉导数也为正，因为 $T_{\Phi\mathcal M}=T[(\ln T)_\Phi(\ln T)_{\mathcal M}+(\ln T)_{\Phi\mathcal M}]$，括号两项都非负且在正投入时为正。

数据弹性现在变为

$$
\frac{\partial\ln T}{\partial\ln\Phi}
=\zeta\frac{k_0\Phi}{(k_0+\Phi)^2}\frac{\mathcal M}{m_0+\mathcal M}.
\tag{B6}
$$

$\Phi\to0$ 或 $\Phi\to\infty$ 时该弹性均趋于零，不再被外生固定为 $\alpha\xi$。

#### B.5 算力选择与新的数据 Euler

给定当前状态，企业购买算力，条件是 $MC_tT_{\mathcal M,t}=c_M$：

$$
\boxed{c_M=MC_tT_t\zeta\frac{\Phi_t}{k_0+\Phi_t}
\frac{m_0}{(m_0+\mathcal M_t)^2}.}
\tag{B7}
$$

这是包含 $T_t(\mathcal M_t)$ 的隐式条件，不能把 $T_t$ 当常数后声称已显式解出最优算力。还要比较 $\mathcal M=0$ 与所有内点候选；本函数的互补性不保证企业利润全局凹。

沿用 F9—F11 的 Bellman 步骤，仅将数据边际产出替换为 B3：

$$
\boxed{q_t=E_t\left[M_{t,t+1}\left(
MC_{t+1}T_{t+1}\zeta\frac{k_0}{(k_0+\Phi_{t+1})^2}
\frac{\mathcal M_{t+1}}{m_0+\mathcal M_{t+1}}
+(1-\delta_\Phi)q_{t+1}\right)\right].}
\tag{B8}
$$

若算力服务每单位消耗 $c_M$ 单位最终品、竞争供应且零利润，国内资源约束需改为 $Y=C+I+c_M\mathcal M$。采用两国模型时，应分别记录算力的生产地与使用地；若算力也跨境进口，则另加算力贸易和相应支付，不把它自动并入工作数据贸易。

**新的经济含义**是：算力不足的国家即便获得低价数据，其生产收益也可能有限；任务不适配的外国数据未必能填补国内有效信息缺口。该模型允许检验跨境数据成本下降的生产率效果是否随初始算力、任务匹配和数据丰富度而变化。
