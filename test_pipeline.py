import unittest
import os
import shutil
from tasks import process_pdf

class TestPipeline(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create a test PDF if it doesn't exist
        if not os.path.exists('test_input.pdf'):
            from fpdf import FPDF
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="This is a test PDF for the OCR application pipeline.", ln=1, align="C")
            pdf.add_page()
            pdf.cell(200, 10, txt="Second page content for multi-page test.", ln=1, align="C")
            pdf.output("test_input.pdf")

    @classmethod
    def tearDownClass(cls):
        # Cleanup test files if needed
        # if os.path.exists('test_input.pdf'):
        #     os.remove('test_input.pdf')
        pass

    def test_full_pipeline(self):
        print("\nRunning full pipeline test...")
        result = process_pdf('test_input.pdf', 'test_input.pdf')

        self.assertEqual(result['status'], 'SUCCESS', f"Pipeline failed with message: {result.get('message')}")
        self.assertTrue(os.path.exists(result['txt_path']), "TXT output not found")
        self.assertTrue(os.path.exists(result['docx_path']), "DOCX output not found")

        # Verify content
        with open(result['txt_path'], 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn("test PDF", content)
            self.assertIn("Second page", content)

        print("Pipeline test passed successfully.")

if __name__ == '__main__':
    unittest.main()
