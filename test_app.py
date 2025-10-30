import unittest
import os
from fpdf import FPDF
from tasks import process_pdf

class TestApp(unittest.TestCase):

    def setUp(self):
        # Create a dummy PDF for testing
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="This is a test.", ln=1, align="C")
        self.test_pdf_path = "test_for_unit.pdf"
        pdf.output(self.test_pdf_path)

    def tearDown(self):
        # Clean up the created files
        os.remove(self.test_pdf_path)
        os.remove("results/test_for_unit.txt")
        os.remove("results/test_for_unit.docx")

    def test_process_pdf(self):
        # Process the dummy PDF
        result = process_pdf(self.test_pdf_path, "test_for_unit.pdf")

        # Check if the process was successful
        self.assertEqual(result['status'], 'SUCCESS')

        # Check if the output files were created
        self.assertTrue(os.path.exists(result['txt_path']))
        self.assertTrue(os.path.exists(result['docx_path']))

        # Check the content of the text file
        with open(result['txt_path'], 'r') as f:
            content = f.read()
        self.assertIn("This is a test.", content)

if __name__ == '__main__':
    unittest.main()
