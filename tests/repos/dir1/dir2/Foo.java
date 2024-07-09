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

import java.io.*;
import java.lang.*;
import java.util.*;
import java.math.*;

class MinCost {
    /** * * Write a function to find the minimum cost path to reach (m, n) from (0, 0) for
     * the given cost matrix cost[][] and a position (m, n) in
     * cost[][]. * * > minCost([[1, 2, 3], [4, 8, 2], [1, 5, 3]], 2, 2) * 8 * >
     * minCost([[2, 3, 4], [5, 9, 3], [2, 6, 4]], 2, 2) * 12 * >
     * minCost([[3, 4, 5], [6, 10, 4], [3, 7, 5]], 2, 2) * 16 */
    public static int minCost(List<List<Integer>> cost, int m, int n) {








}