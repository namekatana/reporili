import { Document, HeadingLevel, Packer, Paragraph, PageBreak } from "docx";
import { markdownToParagraphs } from "./markdown-to-docx";
import { slugifyProjectName } from "./slugify";
import type { GeneratedDocuments } from "./types";
import { documentList } from "./types";

export async function exportDocx(documents: GeneratedDocuments, projectName: string): Promise<void> {
  const children: Paragraph[] = [
    new Paragraph({
      text: `${projectName} Legal Documents`,
      heading: HeadingLevel.TITLE,
      spacing: { after: 320 },
    }),
  ];

  const sectionsWithContent = documentList.filter((doc) => documents[doc.key].trim());

  sectionsWithContent.forEach((doc, index) => {
    children.push(
      new Paragraph({
        text: doc.label,
        heading: HeadingLevel.HEADING_1,
        spacing: { before: index === 0 ? 0 : 240, after: 200 },
      }),
    );
    children.push(...markdownToParagraphs(documents[doc.key]));

    if (index < sectionsWithContent.length - 1) {
      children.push(
        new Paragraph({
          children: [new PageBreak()],
        }),
      );
    }
  });

  const docxFile = new Document({
    sections: [{ children }],
  });

  const blob = await Packer.toBlob(docxFile);
  const slug = slugifyProjectName(projectName);
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = `${slug}-legal.docx`;
  anchor.click();
  URL.revokeObjectURL(url);
}
