import java.io.FileOutputStream;
import org.apache.poi.xwpf.usermodel.*;
public class Foo {

    public void createWordFile(String text, int fontSize) {
        // Create a new document
        XWPFDocument document = new XWPFDocument();

        // Create a paragraph
        XWPFParagraph paragraph = document.createParagraph();

        // Set font size for the paragraph
        XWPFRun run = paragraph.createRun();
        run.setFontSize(fontSize);

        // Set text content
        run.setText(text);

        // Save the document
        try (FileOutputStream out = new FileOutputStream("output.docx")) {
            document.write(out);
            System.out.println("Word file created successfully!");
        } catch (Exception e) {
            System.err.println("Error creating Word file: " + e.getMessage());
        }
    }

    public void createParagraph() {

    }

    public void createPdfFile(String text, int fontSize) {
        // Create a new document
        Document document = new Document();

        // Create a paragraph
        Paragraph paragraph = new Paragraph();

        // Set font size for the paragraph
        paragraph.setFontSize(fontSize);

        // Set text content
        paragraph.add(text);

        // Save the document
        try {
            PdfWriter.getInstance(document, new FileOutputStream("output.pdf"));
            document.open();
            document.add(paragraph);
            document.close();
            System.out.println("PDF file created successfully!");
        } catch (Exception e) {
            System.err.println("Error creating PDF file: " + e.getMessage());
        }
    }
}