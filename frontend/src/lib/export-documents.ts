import { marked } from "marked";
import type { GeneratedDocuments } from "./types";
import { documentList } from "./types";

marked.setOptions({ gfm: true, breaks: true });

function buildMarkdown(documents: GeneratedDocuments, projectName: string): string {
  const sections = documentList
    .map((doc) => {
      const body = documents[doc.key].trim();
      if (!body) {
        return "";
      }
      return `# ${doc.label}\n\n${body}`;
    })
    .filter(Boolean);

  return `# ${projectName} Legal Documents\n\n${sections.join("\n\n---\n\n")}\n`;
}

function buildHtmlShell(title: string, bodyHtml: string): string {
  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>${title}</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
      background: #0c0c0c;
      color: #f0f0f0;
      line-height: 1.65;
      padding: 48px 24px;
    }
    main {
      max-width: 760px;
      margin: 0 auto;
      background: #1a1a1a;
      border-radius: 24px;
      padding: 40px 48px;
      box-shadow: 0 24px 80px rgba(0, 0, 0, 0.55);
    }
    h1 { font-size: 1.75rem; margin-bottom: 2rem; color: #fff; }
    h2 { font-size: 1.35rem; margin: 2.5rem 0 1rem; color: #e8e8e8; }
    h3 { font-size: 1.1rem; margin: 1.5rem 0 0.75rem; color: #ddd; }
    p { margin-bottom: 1rem; color: #c8c8c8; }
    ul, ol { margin: 0 0 1rem 1.25rem; color: #c8c8c8; }
    li { margin-bottom: 0.35rem; }
    a { color: #e0e0e0; }
    hr { border: none; height: 1px; background: #2e2e2e; margin: 2.5rem 0; }
  </style>
</head>
<body>
  <main>
    ${bodyHtml}
  </main>
</body>
</html>`;
}

function buildHtml(documents: GeneratedDocuments, projectName: string): string {
  const sections = documentList
    .map((doc) => {
      const body = documents[doc.key].trim();
      if (!body) {
        return "";
      }
      const html = marked.parse(body);
      return `<h2>${doc.label}</h2>\n${html}`;
    })
    .filter(Boolean);

  const bodyHtml = `<h1>${projectName} Legal Documents</h1>\n${sections.join("\n<hr />\n")}`;
  return buildHtmlShell(`${projectName} Legal Documents`, bodyHtml);
}

function downloadFile(filename: string, content: string, mime: string): void {
  const blob = new Blob([content], { type: mime });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = filename;
  anchor.click();
  URL.revokeObjectURL(url);
}

export function exportMarkdown(documents: GeneratedDocuments, projectName: string): void {
  const content = buildMarkdown(documents, projectName);
  const slug = projectName.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "") || "documents";
  downloadFile(`${slug}-legal.md`, content, "text/markdown;charset=utf-8");
}

export function exportHtml(documents: GeneratedDocuments, projectName: string): void {
  const content = buildHtml(documents, projectName);
  const slug = projectName.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "") || "documents";
  downloadFile(`${slug}-legal.html`, content, "text/html;charset=utf-8");
}

export function renderMarkdown(markdown: string): string {
  return marked.parse(markdown) as string;
}
