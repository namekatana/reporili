import type { GenerateResponse } from "./types";

const apiBase = import.meta.env.PUBLIC_API_URL ?? "";

function resolveUrl(path: string): string {
  if (apiBase) {
    return `${apiBase.replace(/\/$/, "")}${path}`;
  }
  return path;
}

async function parseError(response: Response): Promise<string> {
  try {
    const body = await response.json();
    if (typeof body.detail === "string") {
      return body.detail;
    }
    return JSON.stringify(body.detail ?? body);
  } catch {
    return response.statusText || "Request failed";
  }
}

export async function generateFromZip(file: File): Promise<GenerateResponse> {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(resolveUrl("/api/generate/zip"), {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error(await parseError(response));
  }

  return response.json();
}

export async function generateFromGithub(githubUrl: string): Promise<GenerateResponse> {
  const response = await fetch(resolveUrl("/api/generate/github"), {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ githubUrl }),
  });

  if (!response.ok) {
    throw new Error(await parseError(response));
  }

  return response.json();
}
