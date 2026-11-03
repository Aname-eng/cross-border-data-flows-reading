import Mathlib

namespace CCWZ

/-- The calibrated open-economy reduced profit, reparameterized by `Φ = x^3`,
    is unbounded above when its leading coefficient is positive. -/
theorem open_profit_unbounded
    (A q : ℝ) (hA : 0 < A) :
    ∀ M : ℝ, ∃ x : ℝ, 0 ≤ x ∧ M < A * x ^ 4 - q * x ^ 3 := by
  intro M
  let x : ℝ := max 1 ((q + |M| + 1) / A)
  have hx1 : 1 ≤ x := le_max_left _ _
  have hx0 : 0 ≤ x := le_trans (by norm_num) hx1
  have hratio : (q + |M| + 1) / A ≤ x := le_max_right _ _
  have hlinear : q + |M| + 1 ≤ A * x := by
    have := (div_le_iff₀ hA).mp hratio
    nlinarith
  have hfactor : M < A * x - q := by
    have hM : M ≤ |M| := le_abs_self M
    nlinarith
  have hpow : 1 ≤ x ^ 3 := one_le_pow₀ hx1
  have hfactor_pos : 0 < A * x - q := by
    have habs : 0 ≤ |M| := abs_nonneg M
    nlinarith [hlinear]
  refine ⟨x, hx0, ?_⟩
  calc
    M < A * x - q := hfactor
    _ ≤ x ^ 3 * (A * x - q) := by nlinarith
    _ = A * x ^ 4 - q * x ^ 3 := by ring

/-- The calibrated closed-economy reduced profit, reparameterized by `Φ = x^3`,
    is unbounded above when its leading coefficient is positive. -/
theorem closed_profit_unbounded
    (A q : ℝ) (hA : 0 < A) :
    ∀ M : ℝ, ∃ x : ℝ, 0 ≤ x ∧ M < A * x ^ 20 - q * x ^ 3 := by
  intro M
  let x : ℝ := max 1 ((q + |M| + 1) / A)
  have hx1 : 1 ≤ x := le_max_left _ _
  have hx0 : 0 ≤ x := le_trans (by norm_num) hx1
  have hratio : (q + |M| + 1) / A ≤ x := le_max_right _ _
  have hlinear : q + |M| + 1 ≤ A * x := by
    have := (div_le_iff₀ hA).mp hratio
    nlinarith
  have hxpow : x ≤ x ^ 17 := by
    simpa using (pow_le_pow_right₀ hx1 (show 1 ≤ 17 by norm_num))
  have hfactor : M < A * x ^ 17 - q := by
    have hM : M ≤ |M| := le_abs_self M
    nlinarith
  have hpow : 1 ≤ x ^ 3 := one_le_pow₀ hx1
  have hfactor_pos : 0 < A * x ^ 17 - q := by
    have habs : 0 ≤ |M| := abs_nonneg M
    nlinarith [hlinear]
  refine ⟨x, hx0, ?_⟩
  calc
    M < A * x ^ 17 - q := hfactor
    _ ≤ x ^ 3 * (A * x ^ 17 - q) := by nlinarith
    _ = A * x ^ 20 - q * x ^ 3 := by ring

/-- Rational exponents used in the paper become integer powers on the ray `Φ = x^3`. -/
theorem open_rpow_on_cube (x : ℝ) (hx : 0 ≤ x) :
    (x ^ 3) ^ ((4 : ℝ) / 3) = x ^ 4 := by
  rw [← Real.rpow_natCast x 3]
  rw [← Real.rpow_mul hx]
  norm_num

/-- Rational exponents used in the paper become integer powers on the ray `Φ = x^3`. -/
theorem closed_rpow_on_cube (x : ℝ) (hx : 0 ≤ x) :
    (x ^ 3) ^ ((20 : ℝ) / 3) = x ^ 20 := by
  rw [← Real.rpow_natCast x 3]
  rw [← Real.rpow_mul hx]
  norm_num

end CCWZ
