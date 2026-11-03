"""Independent finite-optimum check for CCWZ's intermediate producer.

This script does not reproduce the paper's full equilibrium.  It isolates the
firm-level deviation at fixed positive prices and aggregate demand, derives the
closed- and open-economy profit exponents, and checks three proposed closures.
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np
import sympy as sp
from scipy.optimize import minimize_scalar

ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "docs" / "assets"
RESULT_DIR = ROOT / "research"
ASSET_DIR.mkdir(parents=True, exist_ok=True)
RESULT_DIR.mkdir(parents=True, exist_ok=True)

# Paper's teaching calibration.
alpha = 1 / 3
xi = 1.0
rho = 21.0       # elasticity across final-good varieties in the closed economy
m = 5.0          # elasticity used for intermediate goods in the open economy
beta = 0.99

closed_exponent = alpha * xi * (rho - 1)
open_exponent = alpha * xi * (m - 1)

# Symbolic derivation: maximize A*y^((e-1)/e) - c*Phi^(-a)*y.
y, Phi, Y, c, e, a = sp.symbols("y Phi Y c e a", positive=True)
revenue = Y ** (1 / e) * y ** ((e - 1) / e)
unit_cost = c * Phi ** (-a)
profit = revenue - unit_cost * y
foc = sp.diff(profit, y)
y_star = sp.solve(sp.Eq(foc, 0), y)[0]
profit_star = sp.factor(profit.subs(y, y_star))
phi_power = sp.simplify(Phi * sp.diff(sp.log(profit_star), Phi))
assert sp.simplify(phi_power - a * (e - 1)) == 0

# A normalized one-shot deviation: -q*L + beta*C*L^theta.
# Coefficients are normalized because only tail behavior is at issue.
L = np.logspace(-2, 2, 1000)
q = 1.0
C = 0.04
baseline = -q * L + beta * C * L**closed_exponent

# Repair 1 (preferred): bounded usable-data services with local elasticity xi.
# g(Phi)=exp((xi/kappa)*(1-(Phi/Phi_bar)^(-kappa))) is normalized to 1
# at Phi_bar=1, has elasticity xi there, and is bounded above.
kappa = 1.0
g = np.exp((xi / kappa) * (1 - L ** (-kappa)))
bounded_profit = -q * L + beta * C * g ** (alpha * (rho - 1))

# Repair 2: convex installation cost.  Its tail exponent must dominate the
# operating-profit exponent.
nu = 6.5  # 1+nu=7.5 > 20/3
install_kappa = 0.02
convex_profit = (
    -q * L
    - install_kappa * L ** (1 + nu) / (1 + nu)
    + beta * C * L**closed_exponent
)

# Repair 3: a finite dataset/license capacity.
cap = 3.0
capacity_profit = np.where(L <= cap, baseline, np.nan)

# Numerical maxima on wide bounded search intervals.  For the baseline, the
# maximizing point moves to the upper bound as the interval expands.
def maximize(func, upper: float) -> tuple[float, float]:
    result = minimize_scalar(lambda x: -func(x), bounds=(1e-8, upper), method="bounded")
    return float(result.x), float(-result.fun)

base_fn = lambda x: -q * x + beta * C * x**closed_exponent
bounded_fn = lambda x: -q * x + beta * C * np.exp(
    (xi / kappa) * (1 - x ** (-kappa))
) ** (alpha * (rho - 1))
convex_fn = lambda x: (
    -q * x
    - install_kappa * x ** (1 + nu) / (1 + nu)
    + beta * C * x**closed_exponent
)

base_search = [maximize(base_fn, u) for u in (5, 10, 20, 40, 80, 160)]
bounded_max = maximize(bounded_fn, 160)
convex_max = maximize(convex_fn, 160)
capacity_max = maximize(base_fn, cap)


def report_pair(pair: tuple[float, float]) -> dict[str, float]:
    """Keep numerical evidence stable across SciPy/platform implementations."""
    x, value = pair
    return {
        "argmax": round(x, 6),
        "value": float(f"{value:.10g}"),
    }


# Plot in a range where all three repairs can be compared.  The y axis is
# clipped so the baseline's explosive tail does not erase the repaired curves.
font_path = Path("C:/Windows/Fonts/msyh.ttc")
if font_path.exists():
    font_manager.fontManager.addfont(font_path)
    plt.rcParams["font.family"] = font_manager.FontProperties(fname=font_path).get_name()
    plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["svg.hashsalt"] = "ccwz-finite-optimum-repairs"

fig, ax = plt.subplots(figsize=(9.2, 5.4))
ax.plot(L, baseline, color="#c84d3a", lw=2.3, label="原式：线性数据价格")
ax.plot(L, bounded_profit, color="#16697a", lw=2.3, label="修复 1：有界有效数据服务")
ax.plot(L, convex_profit, color="#5b5f97", lw=2.3, label="修复 2：凸安装成本")
ax.plot(L, capacity_profit, color="#c28e0e", lw=2.3, label="修复 3：有限授权容量")
ax.axhline(0, color="#7b817f", lw=0.9)
ax.axvline(cap, color="#c28e0e", lw=1, ls="--")
ax.set_xscale("log")
ax.set_ylim(-80, 120)
ax.set_xlabel("一次性工作数据采购 L（归一化，对数刻度）")
ax.set_ylabel("偏离的贴现净收益（归一化）")
ax.set_title("有限最优诊断：原式的尾部与三种闭合方式")
ax.legend(frameon=False, ncols=2, fontsize=9)
ax.grid(alpha=0.18)
fig.tight_layout()
svg_path = ASSET_DIR / "finite-optimum-repairs.svg"
fig.savefig(svg_path, format="svg", metadata={"Date": None})
plt.close(fig)
svg_path.write_text(
    "\n".join(line.rstrip() for line in svg_path.read_text(encoding="utf-8").splitlines()) + "\n",
    encoding="utf-8",
)

results = {
    "calibration": {"alpha": alpha, "xi": xi, "rho": rho, "m": m, "beta": beta},
    "derived_exponents": {
        "closed_alpha_xi_rho_minus_1": closed_exponent,
        "open_alpha_xi_m_minus_1": open_exponent,
    },
    "symbolic_profit_phi_elasticity": str(phi_power),
    "unbounded_thresholds": {"closed": closed_exponent > 1, "open": open_exponent > 1},
    "baseline_bounded_search": [
        {"upper": u, **report_pair(pair)}
        for u, pair in zip((5, 10, 20, 40, 80, 160), base_search)
    ],
    "repairs": {
        "bounded_service": report_pair(bounded_max),
        "convex_installation": {
            "cost_exponent": 1 + nu,
            "required_to_exceed": closed_exponent,
            **report_pair(convex_max),
        },
        "license_capacity": {"cap": cap, **report_pair(capacity_max)},
    },
    "checks": {
        "symbolic_power_is_a_times_e_minus_1": True,
        "closed_calibration_is_superlinear": closed_exponent > 1,
        "open_calibration_is_superlinear": open_exponent > 1,
        "bounded_service_max_is_interior_to_search": bounded_max[0] < 159,
        "convex_cost_dominates_tail": 1 + nu > closed_exponent,
        "convex_cost_max_is_interior_to_search": convex_max[0] < 159,
        "capacity_respects_bound": capacity_max[0] <= cap + 1e-6,
    },
}

out = RESULT_DIR / "finite-optimum-check.json"
out.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")

if not all(results["checks"].values()):
    raise SystemExit(json.dumps(results["checks"], ensure_ascii=False, indent=2))

print(json.dumps(results, ensure_ascii=False, indent=2))
