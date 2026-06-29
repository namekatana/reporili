<script lang="ts">
  type DropZoneProps = {
    disabled?: boolean;
    onFileSelect: (file: File) => void;
  };

  let { disabled = false, onFileSelect }: DropZoneProps = $props();

  let dragging = $state(false);
  let inputEl: HTMLInputElement;

  function handleFiles(fileList: FileList | null) {
    if (!fileList?.length || disabled) {
      return;
    }
    const file = fileList[0];
    if (!file.name.toLowerCase().endsWith(".zip")) {
      return;
    }
    onFileSelect(file);
  }

  function onDrop(event: DragEvent) {
    event.preventDefault();
    dragging = false;
    handleFiles(event.dataTransfer?.files ?? null);
  }

  function onDragOver(event: DragEvent) {
    event.preventDefault();
    if (!disabled) {
      dragging = true;
    }
  }

  function onDragLeave() {
    dragging = false;
  }

  function onInputChange(event: Event) {
    const target = event.target as HTMLInputElement;
    handleFiles(target.files);
    target.value = "";
  }

  function openPicker() {
    if (!disabled) {
      inputEl.click();
    }
  }
</script>

<div
  class="drop-zone"
  class:active={dragging}
  class:disabled
  role="button"
  tabindex="0"
  onclick={openPicker}
  onkeydown={(e) => e.key === "Enter" && openPicker()}
  ondrop={onDrop}
  ondragover={onDragOver}
  ondragleave={onDragLeave}
>
  <input
    bind:this={inputEl}
    type="file"
    accept=".zip,application/zip"
    class="hidden-input"
    {disabled}
    onchange={onInputChange}
  />

  <div class="icon-wrap">
    <svg width="28" height="28" viewBox="0 0 24 24" fill="none" aria-hidden="true">
      <path
        d="M12 16V8m0 0l-3 3m3-3l3 3M4 16v2a2 2 0 002 2h12a2 2 0 002-2v-2"
        stroke="currentColor"
        stroke-width="1.5"
        stroke-linecap="round"
        stroke-linejoin="round"
      />
    </svg>
  </div>

  <p class="title">Drop your repo ZIP here</p>
  <p class="hint">Click to browse, .zip only</p>
</div>

<style>
  .drop-zone {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 0.4rem;
    min-height: 180px;
    height: 100%;
    padding: 1.75rem 1.25rem;
    background: var(--color-float);
    border-radius: var(--radius-panel);
    cursor: pointer;
    transition: background 0.2s, transform 0.2s;
  }

  .drop-zone:hover:not(.disabled) {
    background: var(--color-elevated);
    transform: translateY(-1px);
  }

  .drop-zone.active {
    background: var(--color-elevated);
    transform: scale(1.005);
  }

  .drop-zone.disabled {
    opacity: 0.45;
    cursor: not-allowed;
  }

  .hidden-input {
    display: none;
  }

  .icon-wrap {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 52px;
    height: 52px;
    border-radius: var(--radius-control);
    background: var(--color-elevated);
    color: var(--color-soft);
    margin-bottom: 0.35rem;
  }

  .title {
    font-size: 0.95rem;
    font-weight: 500;
    color: var(--color-bright);
  }

  .hint {
    font-size: 0.8rem;
    color: var(--color-muted);
  }
</style>
