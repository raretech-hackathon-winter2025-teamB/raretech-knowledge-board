(() => {
  const VANTA_PAGE_SELECTOR = "[data-vanta-page='birds']";
  let isVantaActive = false;

  const teardownVanta = () => {
    if (window.__vantaEffect) {
      try {
        window.__vantaEffect.destroy();
      } catch (_error) {
        // htmx swap timing can remove canvas before Vanta destroy runs.
      }
      window.__vantaEffect = null;
    }
    isVantaActive = false;
  };

  const applyVantaBirds = () => {
    const hasVantaPage = Boolean(document.querySelector(VANTA_PAGE_SELECTOR));

    if (!hasVantaPage) {
      if (isVantaActive || window.__vantaEffect) {
        document.body.style.background = "";
        teardownVanta();
      }
      return;
    }

    document.body.style.background = "transparent";
    if (isVantaActive && window.__vantaEffect) return;
    if (!window.VANTA || !window.VANTA.BIRDS) return;

    window.__vantaEffect = window.VANTA.BIRDS({
      el: document.body,
      mouseControls: true,
      touchControls: true,
      gyroControls: false,
      minHeight: 200,
      minWidth: 200,
      scale: 1,
      scaleMobile: 1,
      backgroundColor: 0xfeecd3,
      color1: 0xc93400,
      color2: 0x1838b3,
      backgroundAlpha: 0.98,
    });
    const vantaCanvas = document.querySelector(".vanta-canvas");
    if (vantaCanvas) {
      vantaCanvas.style.pointerEvents = "none";
      vantaCanvas.style.zIndex = "0";
    }
    isVantaActive = true;
  };

  const queueApplyVantaBirds = () => requestAnimationFrame(applyVantaBirds);

  window.applyVantaBirds = applyVantaBirds;
  window.addEventListener("DOMContentLoaded", queueApplyVantaBirds);
  document.addEventListener("htmx:afterSettle", queueApplyVantaBirds);
  document.addEventListener("htmx:load", queueApplyVantaBirds);
})();
