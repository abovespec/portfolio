/**
 * Hero canvas — animated network mesh (blockchain-style node grid).
 * Renders on the #hero-canvas element. Zero dependencies, vanilla Canvas2D.
 *
 * - ~20 nodes drift slowly
 * - Lines drawn between nearby nodes (connection distance threshold)
 * - Nodes pulse subtly
 * - Respects prefers-reduced-motion
 */

function init() {
  const canvas = document.getElementById('hero-canvas') as HTMLCanvasElement | null;
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
  if (!ctx) return;

  const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Node count scales with viewport width
  const vw = window.innerWidth;
  const nodeCount = vw < 640 ? 14 : vw < 1024 ? 22 : 30;
  const connectionDist = 160;

  interface Node {
    x: number;
    y: number;
    vx: number;
    vy: number;
    r: number;
    phase: number;
  }

  const nodes: Node[] = [];
  for (let i = 0; i < nodeCount; i++) {
    nodes.push({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      vx: (Math.random() - 0.5) * 0.4,
      vy: (Math.random() - 0.5) * 0.4,
      r: 1.5 + Math.random() * 1.5,
      phase: Math.random() * Math.PI * 2,
    });
  }

  let animId: number;
  let t = 0;

  function resize() {
    const dpr = window.devicePixelRatio || 1;
    canvas.width = canvas.offsetWidth * dpr;
    canvas.height = canvas.offsetHeight * dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    // Re-wrap nodes that go out of bounds
    for (const n of nodes) {
      if (n.x > canvas.offsetWidth) n.x = Math.random() * canvas.offsetWidth;
      if (n.y > canvas.offsetHeight) n.y = Math.random() * canvas.offsetHeight;
    }
  }

  resize();
  window.addEventListener('resize', resize);

  function frame() {
    const w = canvas.offsetWidth;
    const h = canvas.offsetHeight;

    ctx.clearRect(0, 0, w, h);

    // Move nodes
    for (const n of nodes) {
      if (!prefersReduced) {
        n.x += n.vx;
        n.y += n.vy;
        // Wrap around edges
        if (n.x < -10) n.x = w + 10;
        if (n.x > w + 10) n.x = -10;
        if (n.y < -10) n.y = h + 10;
        if (n.y > h + 10) n.y = -10;
      }
      n.phase += 0.02;
    }

    // Draw connections
    for (let i = 0; i < nodes.length; i++) {
      for (let j = i + 1; j < nodes.length; j++) {
        const a = nodes[i];
        const b = nodes[j];
        const dx = a.x - b.x;
        const dy = a.y - b.y;
        const dist = Math.sqrt(dx * dx + dy * dy);

        if (dist < connectionDist) {
          const alpha = (1 - dist / connectionDist) * 0.12;
          const pulse = prefersReduced ? 1 : 0.7 + 0.3 * Math.sin(t * 0.01 + a.phase);
          ctx.beginPath();
          ctx.moveTo(a.x, a.y);
          ctx.lineTo(b.x, b.y);
          ctx.strokeStyle = `rgba(139, 92, 246, ${alpha * pulse})`;
          ctx.lineWidth = 0.8;
          ctx.stroke();
        }
      }
    }

    // Draw nodes
    for (const n of nodes) {
      const pulse = prefersReduced ? 1 : 0.6 + 0.4 * Math.sin(n.phase);
      const alpha = 0.25 * pulse;
      const r = n.r * (prefersReduced ? 1 : 0.8 + 0.4 * pulse);

      ctx.beginPath();
      ctx.arc(n.x, n.y, r, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(199, 160, 255, ${alpha})`;
      ctx.fill();
    }

    t++;
    animId = requestAnimationFrame(frame);
  }

  // Only animate if user doesn't prefer reduced motion
  if (prefersReduced) {
    // Draw a static frame with lower opacity
    frame();
  } else {
    frame();
  }

  // Cleanup on page unload
  return () => {
    cancelAnimationFrame(animId);
    window.removeEventListener('resize', resize);
  };
}

// Run on DOM ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init);
} else {
  init();
}
