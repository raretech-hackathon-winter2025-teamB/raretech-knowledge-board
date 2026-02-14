(() => {
  const SELECTOR_MD_SOURCE = "[data-markdown-source='1']";
  const SELECTOR_COPY_BUTTON = "[data-copy-code-button='true']";

  const escapeHtml = (text = "") =>
    String(text)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#39;");

  const hasMarked = () => Boolean(window.marked && typeof window.marked.parse === "function");
  const hasPurify = () => Boolean(window.DOMPurify && typeof window.DOMPurify.sanitize === "function");
  const hasHighlightJs = () => Boolean(window.hljs && typeof window.hljs.highlight === "function");

  const renderMarkdownToHtml = (markdown = "") => {
    const source = String(markdown);
    if (!hasMarked()) return `<pre>${escapeHtml(source)}</pre>`;
    const raw = window.marked.parse(source);
    return hasPurify() ? window.DOMPurify.sanitize(raw) : raw;
  };

  const getCodeLanguage = (codeEl) => {
    const className = codeEl.className || "";
    const matched = className.match(/language-([a-zA-Z0-9_-]+)/);
    return matched ? matched[1] : "text";
  };

  const getHighlightedHtml = (codeText, language) => {
    if (!hasHighlightJs()) return escapeHtml(codeText);

    if (language !== "text" && typeof window.hljs.getLanguage === "function" && window.hljs.getLanguage(language)) {
      return window.hljs.highlight(codeText, { language }).value;
    }

    if (typeof window.hljs.highlightAuto === "function") {
      return window.hljs.highlightAuto(codeText).value;
    }

    return escapeHtml(codeText);
  };

  const buildCodeBlock = (codeText, language) => {
    const lines = codeText.split("\n");
    if (lines.length > 1 && lines.at(-1) === "") lines.pop();
    const safeLines = lines.length ? lines : [""];

    const lineNumbers = safeLines
      .map((_, idx) => `<div>${idx + 1}</div>`)
      .join("");

    const highlightedHtml = getHighlightedHtml(codeText, language);

    return `
      <div class="my-4 overflow-hidden rounded-lg border border-[#7c2808]/30" data-code-widget="1">
        <div class="flex items-center justify-between bg-[#7c2808] px-3 py-2 text-xs text-[#fff7ed]">
          <span class="font-mono uppercase tracking-wide opacity-80">${escapeHtml(language)}</span>
          <button
            type="button"
            class="rounded border border-[#fff7ed]/50 px-2 py-1 text-xs hover:bg-[#fff7ed]/10"
            data-copy-code-button="true"
            data-copied-label="Copied"
          >
            Copy
          </button>
        </div>
        <div class="grid grid-cols-[48px_1fr] bg-[#7c2808]">
          <div class="select-none border-r border-[#fff7ed]/20 px-2 py-3 text-right font-mono text-sm leading-6 text-[#fff7ed]/65">
            ${lineNumbers}
          </div>
          <pre class="m-0 overflow-x-auto px-3 py-3 text-[#fff7ed]"><code class="hljs block font-mono text-sm leading-6 language-${escapeHtml(language)}" style="margin:0;padding:0;background:transparent;">${highlightedHtml}</code></pre>
        </div>
      </div>
    `;
  };

  const decorateCodeBlocks = (rootEl) => {
    if (!rootEl) return;
    const preElements = rootEl.querySelectorAll("pre");
    preElements.forEach((preEl) => {
      if (preEl.closest("[data-code-widget='1']")) return;

      const codeEl = preEl.querySelector("code");
      if (!codeEl) return;

      const codeText = codeEl.textContent || "";
      const language = getCodeLanguage(codeEl);
      const wrapperHtml = buildCodeBlock(codeText, language);

      preEl.outerHTML = wrapperHtml;
    });
  };

  const renderPreview = (editorId, previewId) => {
    const editorEl = document.getElementById(editorId);
    const previewEl = document.getElementById(previewId);
    if (!editorEl || !previewEl) return;

    previewEl.innerHTML = renderMarkdownToHtml(editorEl.value || "");
    decorateCodeBlocks(previewEl);
  };

  const renderMarkdownBlocks = (root = document) => {
    const scope = root?.querySelectorAll ? root : document;
    const targets = scope.querySelectorAll(SELECTOR_MD_SOURCE);

    targets.forEach((node) => {
      if (node.getAttribute("data-rendered") === "1") return;

      const markdown = node.textContent || "";
      node.innerHTML = renderMarkdownToHtml(markdown);
      decorateCodeBlocks(node);

      node.setAttribute("data-rendered", "1");
    });
  };

  const handleCopyClick = async (event) => {
    const button = event.target.closest(SELECTOR_COPY_BUTTON);
    if (!button) return;

    const widget = button.closest("[data-code-widget='1']");
    if (!widget) return;

    const codeEl = widget.querySelector("pre code");
    if (!codeEl) return;

    try {
      await navigator.clipboard.writeText(codeEl.textContent || "");
      const originalLabel = button.textContent;
      button.textContent = button.getAttribute("data-copied-label") || "Copied";
      setTimeout(() => {
        button.textContent = originalLabel;
      }, 1000);
    } catch {
      // clipboard access denied
    }
  };

  const bindGlobalEvents = () => {
    document.addEventListener("click", handleCopyClick);

    document.addEventListener("DOMContentLoaded", () => {
      renderMarkdownBlocks(document);
    });

    document.addEventListener("htmx:afterSwap", (event) => {
      const target = event?.detail?.target ?? document;
      renderMarkdownBlocks(target);
    });

    document.addEventListener("htmx:load", (event) => {
      const loaded = event?.detail?.elt ?? document;
      renderMarkdownBlocks(loaded);
    });
  };

  window.MarkdownEditor = {
    renderPreview,
    renderMarkdownBlocks,
  };

  bindGlobalEvents();
})();
