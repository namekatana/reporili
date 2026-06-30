<script lang="ts">
  import type { Snippet } from "svelte";

  type ScrollVariant = "site" | "document";

  type CustomScrollbarProps = {
    variant: ScrollVariant;
    class?: string;
    children: Snippet;
  };

  let { variant, class: className = "", children }: CustomScrollbarProps = $props();

  let viewport = $state<HTMLDivElement | null>(null);
  let trackEl = $state<HTMLDivElement | null>(null);
  let thumbHeight = $state(0);
  let thumbTop = $state(0);
  let scrollable = $state(false);
  let dragging = $state(false);

  let dragStartY = 0;
  let dragStartScrollTop = 0;
  let metricsFrame = 0;

  const isDocument = $derived(variant === "document");
  const showTrack = $derived(isDocument || scrollable);

  const rootClass = $derived(
    ["scroll-wrap", variant === "site" ? "scroll-site" : "scroll-document", className]
      .filter(Boolean)
      .join(" "),
  );

  function trackHeight() {
    if (isDocument && trackEl) {
      return trackEl.clientHeight;
    }
    return viewport?.clientHeight ?? 0;
  }

  function updateMetrics() {
    const el = viewport;
    if (!el) {
      return;
    }

    const { scrollHeight, clientHeight, scrollTop } = el;
    const nextScrollable = scrollHeight > clientHeight + 1;

    if (!nextScrollable) {
      scrollable = false;
      thumbHeight = 0;
      thumbTop = 0;
      return;
    }

    const track = trackHeight();
    const ratio = clientHeight / scrollHeight;
    const nextThumbHeight = Math.max(ratio * track, 40);
    const maxThumbTop = track - nextThumbHeight;
    const maxScroll = scrollHeight - clientHeight;
    const nextThumbTop = maxScroll > 0 ? (scrollTop / maxScroll) * maxThumbTop : 0;

    scrollable = true;
    thumbHeight = nextThumbHeight;
    thumbTop = nextThumbTop;
  }

  function scheduleMetrics() {
    if (metricsFrame) {
      return;
    }

    metricsFrame = requestAnimationFrame(() => {
      metricsFrame = 0;
      updateMetrics();
    });
  }

  function onScroll() {
    if (!dragging) {
      scheduleMetrics();
    }
  }

  function onThumbMouseDown(event: MouseEvent) {
    event.preventDefault();
    event.stopPropagation();
    dragging = true;
    dragStartY = event.clientY;
    dragStartScrollTop = viewport?.scrollTop ?? 0;
    window.addEventListener("mousemove", onDragMove);
    window.addEventListener("mouseup", onDragEnd);
  }

  function onDragMove(event: MouseEvent) {
    const el = viewport;
    if (!el) {
      return;
    }

    const track = trackHeight();
    const maxThumbTop = track - thumbHeight;
    const maxScroll = el.scrollHeight - el.clientHeight;
    const deltaY = event.clientY - dragStartY;
    const scrollDelta = maxThumbTop > 0 ? (deltaY / maxThumbTop) * maxScroll : 0;
    el.scrollTop = dragStartScrollTop + scrollDelta;
    scheduleMetrics();
  }

  function onDragEnd() {
    dragging = false;
    window.removeEventListener("mousemove", onDragMove);
    window.removeEventListener("mouseup", onDragEnd);
  }

  function onTrackMouseDown(event: MouseEvent) {
    if (event.target !== event.currentTarget || !scrollable) {
      return;
    }

    const el = viewport;
    if (!el) {
      return;
    }

    const rect = (event.currentTarget as HTMLElement).getBoundingClientRect();
    const clickY = event.clientY - rect.top;
    const track = trackHeight();
    const maxThumbTop = track - thumbHeight;
    const maxScroll = el.scrollHeight - el.clientHeight;
    const thumbCenter = clickY - thumbHeight / 2;
    const clamped = Math.max(0, Math.min(maxThumbTop, thumbCenter));
    el.scrollTop = maxThumbTop > 0 ? (clamped / maxThumbTop) * maxScroll : 0;
    scheduleMetrics();
  }

  $effect(() => {
    const el = viewport;
    const track = trackEl;
    if (!el) {
      return;
    }

    scheduleMetrics();

    const resizeObserver = new ResizeObserver(() => scheduleMetrics());
    resizeObserver.observe(el);
    if (track) {
      resizeObserver.observe(track);
    }

    const mutationObserver = new MutationObserver(() => scheduleMetrics());
    mutationObserver.observe(el, { childList: true, subtree: true });

    return () => {
      resizeObserver.disconnect();
      mutationObserver.disconnect();
      window.removeEventListener("mousemove", onDragMove);
      window.removeEventListener("mouseup", onDragEnd);
      if (metricsFrame) {
        cancelAnimationFrame(metricsFrame);
        metricsFrame = 0;
      }
    };
  });
</script>

<div class={rootClass}>
  <div class="scroll-viewport" bind:this={viewport} onscroll={onScroll}>
    <div class="scroll-content">
      {@render children()}
    </div>
  </div>

  {#if showTrack}
    <div class="scroll-rail">
      <div
        class="scroll-track"
        class:inactive={!scrollable}
        class:dragging
        bind:this={trackEl}
        onmousedown={onTrackMouseDown}
        role="scrollbar"
        aria-hidden={!scrollable}
        aria-valuenow={thumbTop}
        aria-orientation="vertical"
      >
        {#if scrollable}
          <div
            class="scroll-thumb"
            style:height="{thumbHeight}px"
            style:transform="translateY({thumbTop}px)"
            onmousedown={onThumbMouseDown}
          ></div>
        {/if}
      </div>
    </div>
  {/if}
</div>

<style>
  .scroll-wrap {
    position: relative;
    min-height: 0;
  }

  .scroll-site {
    height: 100dvh;
    width: 100%;
  }

  .scroll-document {
    display: grid;
    grid-template-columns: minmax(0, 1fr) 2rem;
    align-items: stretch;
    height: 65vh;
    min-height: 360px;
    max-height: 65vh;
    overflow: hidden;
  }

  .scroll-viewport {
    overflow-x: hidden;
    overflow-y: auto;
    scrollbar-width: none;
    -ms-overflow-style: none;
    min-width: 0;
  }

  .scroll-viewport::-webkit-scrollbar {
    display: none;
    width: 0;
    height: 0;
  }

  .scroll-site .scroll-viewport {
    height: 100%;
    padding-right: 4px;
  }

  .scroll-document .scroll-viewport {
    grid-column: 1;
    min-height: 0;
    height: 100%;
  }

  .scroll-content {
    min-width: 0;
    max-width: 100%;
    box-sizing: border-box;
  }

  .scroll-document .scroll-content {
    padding: 1.75rem 1.25rem 1.75rem 2rem;
  }

  .scroll-rail {
    grid-column: 2;
    display: flex;
    justify-content: center;
    align-items: stretch;
    padding: 10px 10px 10px 0;
    box-sizing: border-box;
  }

  .scroll-track {
    position: relative;
    touch-action: none;
    user-select: none;
    flex-shrink: 0;
    height: 100%;
    width: 12px;
  }

  .scroll-site .scroll-rail {
    display: contents;
  }

  .scroll-site .scroll-track {
    position: absolute;
    top: 0;
    right: 0;
    bottom: 0;
    z-index: 2;
    width: 12px;
    padding: 4px 2px;
    height: auto;
  }

  .scroll-document .scroll-track {
    border-radius: 999px;
    background: #141414;
  }

  .scroll-document .scroll-track.inactive {
    opacity: 0.55;
  }

  .scroll-thumb {
    position: absolute;
    left: 2px;
    right: 2px;
    border-radius: 999px;
    cursor: grab;
    transition: background 0.15s;
  }

  .scroll-track.dragging .scroll-thumb,
  .scroll-thumb:active {
    cursor: grabbing;
  }

  .scroll-site .scroll-thumb {
    background: #2a2a2a;
  }

  .scroll-site .scroll-track:hover .scroll-thumb {
    background: #3d3d3d;
  }

  .scroll-document .scroll-thumb {
    background: #4a4a4a;
    border: 2px solid #141414;
    box-sizing: border-box;
  }

  .scroll-document .scroll-track:hover .scroll-thumb {
    background: #626262;
  }
</style>
