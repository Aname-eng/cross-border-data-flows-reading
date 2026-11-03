(() => {
  const COLORS = {
    coral: "#D06449",
    teal: "#177C7B",
    green: "#3C8A66",
    gold: "#D6A23D",
  };

  function setStage(root, stage) {
    const bounded = Math.max(1, Math.min(4, Number(stage) || 1));
    root.dataset.stageCurrent = String(bounded);
    root.querySelectorAll("[data-stage-min]").forEach((node) => {
      node.classList.toggle("stage-visible", Number(node.dataset.stageMin) <= bounded);
    });
    root.querySelectorAll("[data-stage-show]").forEach((button) => {
      const active = Number(button.dataset.stageShow) === bounded;
      button.classList.toggle("active", active);
      button.setAttribute("aria-pressed", active ? "true" : "false");
    });
  }

  function initStages() {
    document.querySelectorAll(".explorable-stage").forEach((root) => {
      setStage(root, root.dataset.stageInitial || 1);
      root.querySelectorAll("[data-stage-show]").forEach((button) => {
        button.addEventListener("click", () => setStage(root, button.dataset.stageShow));
      });
    });

    document.addEventListener("keydown", (event) => {
      if (!event.shiftKey || !["ArrowRight", "ArrowLeft"].includes(event.key)) return;
      const currentSlide = window.Reveal?.getCurrentSlide?.();
      const root = currentSlide?.querySelector(".explorable-stage");
      if (!root) return;
      event.preventDefault();
      const direction = event.key === "ArrowRight" ? 1 : -1;
      setStage(root, Number(root.dataset.stageCurrent || 1) + direction);
    });
  }

  function drawTheta(explorer) {
    const economy = explorer.dataset.economy || "closed";
    const xi = Number(explorer.querySelector("[data-xi-slider]").value);
    const eMinusOne = economy === "closed" ? 20 : 4;
    const theta = (xi * eMinusOne) / 3;
    const path = explorer.querySelector("[data-theta-path]");
    const point = explorer.querySelector("[data-theta-point]");
    const label = explorer.querySelector("[data-theta-label]");
    const xMin = 0.001, xMax = 2.5, yMin = -1.2, yMax = 8;
    const sx = (x) => 70 + ((x - xMin) / (xMax - xMin)) * 720;
    const sy = (y) => 255 - ((Math.max(yMin, Math.min(yMax, y)) - yMin) / (yMax - yMin)) * 215;
    const commands = [];
    for (let i = 0; i <= 220; i += 1) {
      const x = xMin + ((xMax - xMin) * i) / 220;
      const y = -x + Math.pow(x, theta);
      commands.push(`${i === 0 ? "M" : "L"}${sx(x).toFixed(1)},${sy(y).toFixed(1)}`);
    }
    path.setAttribute("d", commands.join(" "));
    const color = theta > 1.0001 ? COLORS.coral : theta < 0.9999 ? COLORS.green : COLORS.gold;
    path.setAttribute("stroke", color);

    if (theta > 1.0001) {
      const xStar = Math.pow(1 / theta, 1 / (theta - 1));
      const yStar = -xStar + Math.pow(xStar, theta);
      point.setAttribute("cx", sx(xStar));
      point.setAttribute("cy", sy(yStar));
      point.style.opacity = "1";
      label.textContent = `θ=${theta.toFixed(2)}：正根是谷底，尾部向上`;
    } else {
      point.style.opacity = "0";
      label.textContent = theta < 0.9999
        ? `θ=${theta.toFixed(2)}：线性成本控制尾部`
        : "θ=1：结论取决于收益与成本系数";
    }
    label.setAttribute("fill", color);
    explorer.querySelector("[data-xi-output]").textContent = xi.toFixed(2);
    const comparator = theta > 1.0001 ? ">" : theta < 0.9999 ? "<" : "=";
    explorer.querySelector("[data-theta-output]").textContent = `θ = ${theta.toFixed(2)} ${comparator} 1`;
  }

  function initThetaExplorers() {
    document.querySelectorAll("[data-theta-explorer]").forEach((explorer) => {
      explorer.dataset.economy = "closed";
      explorer.querySelectorAll("[data-economy]").forEach((button) => {
        button.addEventListener("click", () => {
          explorer.dataset.economy = button.dataset.economy;
          explorer.querySelectorAll("[data-economy]").forEach((other) => {
            const active = other === button;
            other.classList.toggle("active", active);
            other.setAttribute("aria-pressed", active ? "true" : "false");
          });
          drawTheta(explorer);
        });
      });
      explorer.querySelector("[data-xi-slider]").addEventListener("input", () => drawTheta(explorer));
      drawTheta(explorer);
    });
  }

  function init() {
    initStages();
    initThetaExplorers();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init, { once: true });
  } else {
    init();
  }
})();
