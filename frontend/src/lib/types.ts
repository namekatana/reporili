export type DetectedPattern = {
  category: string;
  keywords: string[];
  files: string[];
};

export type RepoAnalysis = {
  projectName: string;
  source: string;
  stack: string[];
  patterns: DetectedPattern[];
  fileCount: number;
  sampledFiles: string[];
};

export type GeneratedDocuments = {
  privacyPolicy: string;
  termsOfService: string;
  disclaimer: string;
};

export type GenerateResponse = {
  analysis: RepoAnalysis;
  documents: GeneratedDocuments;
};

export type DocumentKey = "privacyPolicy" | "termsOfService" | "disclaimer";

export type DocumentMeta = {
  key: DocumentKey;
  label: string;
};

export const documentList: DocumentMeta[] = [
  { key: "privacyPolicy", label: "Privacy Policy" },
  { key: "termsOfService", label: "Terms of Service" },
  { key: "disclaimer", label: "Disclaimer" },
];
