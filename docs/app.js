(() => {
  const root = document.documentElement;
  const routeButtons = [...document.querySelectorAll('[data-route-choice]')];
  const routePanels = [...document.querySelectorAll('[data-route-panel]')];
  const status = document.querySelector('.route-status');
  const labels = {
    all: '当前：线性通读三条路线',
    a: '当前：路线 A · 安全、许可与固定合规成本',
    b: '当前：路线 B · 数据质量、收益饱和与算力互补',
    c: '当前：路线 C · 训练、研发与利用能力积累'
  };

  function selectRoute(route, updateUrl = true) {
    const valid = ['all', 'a', 'b', 'c'].includes(route) ? route : 'all';
    root.dataset.route = valid;
    routeButtons.forEach((button) => {
      const selected = button.dataset.routeChoice === valid;
      button.classList.toggle('active', selected);
      button.setAttribute('aria-pressed', String(selected));
    });
    routePanels.forEach((panel) => {
      panel.hidden = valid !== 'all' && panel.dataset.routePanel !== valid;
    });
    status.textContent = labels[valid];
    localStorage.setItem('ccwz-route', valid);
    if (updateUrl) {
      const url = new URL(window.location.href);
      if (valid === 'all') url.searchParams.delete('route');
      else url.searchParams.set('route', valid);
      history.replaceState({}, '', `${url.pathname}${url.search}${url.hash}`);
    }
    if (window.MathJax?.typesetPromise) {
      window.MathJax.typesetPromise(routePanels.filter((panel) => !panel.hidden)).catch(() => {});
    }
  }

  routeButtons.forEach((button) => {
    button.addEventListener('click', () => {
      selectRoute(button.dataset.routeChoice);
      const firstVisible = routePanels.find((panel) => !panel.hidden);
      firstVisible?.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
  });

  const initial = new URLSearchParams(window.location.search).get('route')
    || localStorage.getItem('ccwz-route')
    || 'all';
  selectRoute(initial, false);

  const thetaExplorer = document.querySelector('[data-theta-explorer]');
  if (thetaExplorer) {
    const thetaInputs = Object.fromEntries(
      [...thetaExplorer.querySelectorAll('[data-theta-input]')]
        .map((input) => [input.dataset.thetaInput, input])
    );
    const thetaOutputs = Object.fromEntries(
      [...thetaExplorer.querySelectorAll('[data-theta-output]')]
        .map((output) => [output.dataset.thetaOutput, output])
    );
    const thetaValue = thetaExplorer.querySelector('[data-theta-value]');
    const thetaVerdict = thetaExplorer.querySelector('[data-theta-verdict]');
    const thetaResult = thetaExplorer.querySelector('[data-theta-result]');
    const thetaPresets = [...thetaExplorer.querySelectorAll('[data-theta-preset]')];
    const presets = {
      closed: { alpha: 1 / 3, xi: 1, elasticity: 21 },
      open: { alpha: 1 / 3, xi: 1, elasticity: 5 },
      boundary: { alpha: 0.25, xi: 1, elasticity: 5 }
    };

    function updateTheta() {
      const alpha = Number(thetaInputs.alpha.value);
      const xi = Number(thetaInputs.xi.value);
      const elasticity = Number(thetaInputs.elasticity.value);
      const theta = alpha * xi * (elasticity - 1);
      thetaOutputs.alpha.textContent = alpha.toFixed(3);
      thetaOutputs.xi.textContent = xi.toFixed(2);
      thetaOutputs.elasticity.textContent = elasticity.toFixed(2);
      thetaValue.textContent = theta.toFixed(3);

      if (theta > 1.0005) {
        thetaResult.dataset.regime = 'superlinear';
        thetaVerdict.textContent = '目标无上界；有限正驻点是局部最小值。';
      } else if (theta < 0.9995) {
        thetaResult.dataset.regime = 'sublinear';
        thetaVerdict.textContent = '线性成本控制这条尾部偏离；完整动态存在性仍需另证。';
      } else {
        thetaResult.dataset.regime = 'boundary';
        thetaVerdict.textContent = '边界情形取决于 −q + βC 的符号，不能只看指数。';
      }
    }

    thetaPresets.forEach((button) => {
      button.addEventListener('click', () => {
        const preset = presets[button.dataset.thetaPreset];
        Object.entries(preset).forEach(([name, value]) => {
          thetaInputs[name].value = String(value);
        });
        thetaPresets.forEach((candidate) => candidate.classList.toggle('active', candidate === button));
        updateTheta();
      });
    });
    Object.values(thetaInputs).forEach((input) => {
      input.addEventListener('input', () => {
        thetaPresets.forEach((button) => button.classList.remove('active'));
        updateTheta();
      });
    });
    updateTheta();
  }

  document.querySelector('[data-action="print"]')?.addEventListener('click', () => {
    const details = document.querySelector('.analysis-disclosure');
    if (details) details.open = true;
    window.print();
  });

  const progress = document.querySelector('.reading-progress span');
  function updateProgress() {
    const scrollable = document.documentElement.scrollHeight - window.innerHeight;
    const fraction = scrollable > 0 ? window.scrollY / scrollable : 0;
    progress.style.width = `${Math.min(100, Math.max(0, fraction * 100))}%`;
  }
  updateProgress();
  window.addEventListener('scroll', updateProgress, { passive: true });

  document.querySelectorAll('.prose table').forEach((table) => {
    if (table.parentElement?.classList.contains('table-wrapper')) return;
    const wrapper = document.createElement('div');
    wrapper.className = 'table-wrapper';
    table.parentNode.insertBefore(wrapper, table);
    wrapper.appendChild(table);
  });
})();
