import type { GenerateResponse } from "./types";

const enabledKey = "reporili-history-enabled";
const entriesKey = "reporili-history";
const maxEntries = 12;

export type HistoryEntry = GenerateResponse & {
  id: string;
  savedAt: string;
};

function readEntries(): HistoryEntry[] {
  if (typeof localStorage === "undefined") {
    return [];
  }

  try {
    const raw = localStorage.getItem(entriesKey);
    if (!raw) {
      return [];
    }

    const parsed = JSON.parse(raw) as HistoryEntry[];
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    return [];
  }
}

function writeEntries(entries: HistoryEntry[]): void {
  if (typeof localStorage === "undefined") {
    return;
  }

  localStorage.setItem(entriesKey, JSON.stringify(entries));
}

export function isHistoryEnabled(): boolean {
  if (typeof localStorage === "undefined") {
    return false;
  }

  return localStorage.getItem(enabledKey) === "true";
}

export function setHistoryEnabled(enabled: boolean): void {
  if (typeof localStorage === "undefined") {
    return;
  }

  localStorage.setItem(enabledKey, enabled ? "true" : "false");

  if (!enabled) {
    return;
  }
}

export function loadHistory(): HistoryEntry[] {
  return readEntries();
}

export function saveHistoryEntry(payload: GenerateResponse): HistoryEntry | null {
  if (!isHistoryEnabled()) {
    return null;
  }

  const entry: HistoryEntry = {
    ...payload,
    id: crypto.randomUUID(),
    savedAt: new Date().toISOString(),
  };

  const next = [entry, ...readEntries()].slice(0, maxEntries);
  writeEntries(next);
  return entry;
}

export function removeHistoryEntry(id: string): HistoryEntry[] {
  const next = readEntries().filter((entry) => entry.id !== id);
  writeEntries(next);
  return next;
}

export function clearHistory(): void {
  writeEntries([]);
}

export function formatHistoryDate(iso: string): string {
  const date = new Date(iso);
  return date.toLocaleString(undefined, {
    month: "short",
    day: "numeric",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}
