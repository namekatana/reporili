import {
  HeadingLevel,
  Paragraph,
  TextRun,
  type IParagraphOptions,
} from "docx";
import { marked } from "marked";
import type { Token, Tokens } from "marked";

type TextStyle = {
  bold?: boolean;
  italics?: boolean;
  font?: string;
};

function headingLevel(depth: number): (typeof HeadingLevel)[keyof typeof HeadingLevel] {
  if (depth <= 1) {
    return HeadingLevel.HEADING_1;
  }
  if (depth === 2) {
    return HeadingLevel.HEADING_2;
  }
  return HeadingLevel.HEADING_3;
}

function inlineRuns(tokens: Token[] | undefined, style: TextStyle = {}): TextRun[] {
  if (!tokens?.length) {
    return [new TextRun({ text: "", ...style })];
  }

  const runs: TextRun[] = [];

  for (const token of tokens) {
    if (token.type === "text") {
      runs.push(new TextRun({ text: (token as Tokens.Text).text, ...style }));
      continue;
    }

    if (token.type === "strong") {
      runs.push(...inlineRuns((token as Tokens.Strong).tokens, { ...style, bold: true }));
      continue;
    }

    if (token.type === "em") {
      runs.push(...inlineRuns((token as Tokens.Em).tokens, { ...style, italics: true }));
      continue;
    }

    if (token.type === "codespan") {
      runs.push(
        new TextRun({
          text: (token as Tokens.Codespan).text,
          font: "Consolas",
          ...style,
        }),
      );
      continue;
    }

    if (token.type === "link") {
      const linkToken = token as Tokens.Link;
      const label = linkToken.text || linkToken.href;
      runs.push(
        new TextRun({
          text: `${label} (${linkToken.href})`,
          ...style,
        }),
      );
    }
  }

  return runs.length ? runs : [new TextRun({ text: "", ...style })];
}

function paragraphFromTokens(
  tokens: Token[] | undefined,
  options: IParagraphOptions = {},
): Paragraph {
  return new Paragraph({
    ...options,
    children: inlineRuns(tokens),
  });
}

function listItemTokens(item: Tokens.ListItem): Token[] {
  const collected: Token[] = [];

  for (const nested of item.tokens) {
    if (nested.type === "text" && (nested as Tokens.Text).tokens?.length) {
      collected.push(...((nested as Tokens.Text).tokens ?? []));
      continue;
    }

    if (nested.type === "paragraph") {
      collected.push(...((nested as Tokens.Paragraph).tokens ?? []));
      continue;
    }

    collected.push(nested);
  }

  return collected;
}

function blockToParagraphs(token: Token, indentLeft = 0): Paragraph[] {
  const indent = indentLeft > 0 ? { indent: { left: indentLeft } } : {};

  if (token.type === "heading") {
    const heading = token as Tokens.Heading;
    return [
      new Paragraph({
        heading: headingLevel(heading.depth),
        children: inlineRuns(heading.tokens),
        ...indent,
      }),
    ];
  }

  if (token.type === "paragraph") {
    return [paragraphFromTokens((token as Tokens.Paragraph).tokens, indent)];
  }

  if (token.type === "blockquote") {
    const quote = token as Tokens.Blockquote;
    return quote.tokens.flatMap((nested) => blockToParagraphs(nested, indentLeft + 720));
  }

  if (token.type === "code") {
    const code = token as Tokens.Code;
    return code.text.split("\n").map(
      (line) =>
        new Paragraph({
          children: [new TextRun({ text: line, font: "Consolas" })],
          spacing: { after: 80 },
          ...indent,
        }),
    );
  }

  if (token.type === "list") {
    const list = token as Tokens.List;
    return list.items.flatMap((item, index) => {
      const itemToken = item as Tokens.ListItem;
      const contentTokens = listItemTokens(itemToken);

      if (list.ordered) {
        return [
          new Paragraph({
            children: [
              new TextRun({ text: `${index + 1}. ` }),
              ...inlineRuns(contentTokens.length ? contentTokens : itemToken.tokens),
            ],
            ...indent,
          }),
        ];
      }

      return [
        paragraphFromTokens(contentTokens.length ? contentTokens : itemToken.tokens, {
          bullet: { level: 0 },
          ...indent,
        }),
      ];
    });
  }

  if (token.type === "hr") {
    return [new Paragraph({ spacing: { before: 240, after: 240 }, ...indent })];
  }

  if (token.type === "space") {
    return [];
  }

  if (token.type === "text") {
    return [paragraphFromTokens([token], indent)];
  }

  return [];
}

export function markdownToParagraphs(markdown: string): Paragraph[] {
  const tokens = marked.lexer(markdown.trim());
  return tokens.flatMap((token) => blockToParagraphs(token));
}
