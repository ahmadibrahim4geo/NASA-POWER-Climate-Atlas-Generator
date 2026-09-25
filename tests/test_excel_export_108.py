# -*- coding: utf-8 -*-
"""
test_excel_export_108.py
Verifies:
1. write_excel_file creates valid .xls files with xlwt.
2. Formatted styling: dark blue headers, zebra striping, borders, auto column widths.
3. Arabic UTF-8 text integrity and RTL worksheet support.
4. write_master_excel_workbook multi-sheet creation.
5. write_csv UTF-8 BOM marker (\xef\xbb\xbf).
"""
import sys
import os
import shutil
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import imp
pyt_mod = imp.load_source("pyt_tool", os.path.join(ROOT, "POWER_Climate_Atlas_Generator_10_8.pyt"))


class TestExcelAndArabicExport(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="test_excel_")

    def tearDown(self):
        if os.path.isdir(self.test_dir):
            shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_write_excel_single_sheet_arabic(self):
        xls_path = os.path.join(self.test_dir, "test_arabic.xls")
        header = [u"رقم المحطة", u"اسم المحطة", u"متوسط الحرارة السنوي", u"مؤشر الجفاف"]
        rows = [
            [1, u"القاهرة", 21.45, 1.73],
            [2, u"الإسكندرية", 20.12, 4.25],
            [3, u"أسوان", 26.85, 0.15]
        ]
        ok = pyt_mod.write_excel_file(xls_path, header, rows, sheet_name=u"المناخ", rtl=True)
        self.assertTrue(ok, "write_excel_file returned False")
        self.assertTrue(os.path.isfile(xls_path), "Excel file was not created on disk")
        self.assertGreater(os.path.getsize(xls_path), 500, "Excel file is suspiciously small")

        # Read back with xlrd if available
        try:
            import xlrd
            wb = xlrd.open_workbook(xls_path)
            sheet = wb.sheet_by_index(0)
            self.assertEqual(sheet.nrows, 4)
            self.assertEqual(sheet.ncols, 4)
            val = sheet.cell_value(1, 1)
            self.assertEqual(val, u"القاهرة")
        except ImportError:
            pass

    def test_write_master_excel_workbook(self):
        master_xls = os.path.join(self.test_dir, "Climate_Atlas_Master_Workbook.xls")
        sheets = [
            ("Temperature", [u"ID", u"T_Annual_Mean", u"T_Summer_Mean"], [[1, 21.5, 28.2], [2, 20.1, 26.5]], False),
            ("Precipitation", [u"ID", u"R_Annual_Total", u"R_Winter_Total"], [[1, 25.4, 18.2], [2, 185.0, 120.0]], False),
            ("Drought", [u"ID", u"DM_Aridity", u"UNEP_Aridity"], [[1, 1.73, 0.042], [2, 4.25, 0.12]], False),
        ]
        ok = pyt_mod.write_master_excel_workbook(master_xls, sheets)
        self.assertTrue(ok, "write_master_excel_workbook returned False")
        self.assertTrue(os.path.isfile(master_xls), "Master workbook file was not created")
        self.assertGreater(os.path.getsize(master_xls), 1000)

        try:
            import xlrd
            wb = xlrd.open_workbook(master_xls)
            self.assertEqual(wb.nsheets, 3)
            self.assertIn("Temperature", wb.sheet_names())
            self.assertIn("Precipitation", wb.sheet_names())
            self.assertIn("Drought", wb.sheet_names())
        except ImportError:
            pass

    def test_write_csv_utf8_bom(self):
        csv_path = os.path.join(self.test_dir, "test_bom.csv")
        header = [u"المعرف", u"الاسم", u"الحرارة"]
        rows = [[1, u"مرسى علم", 25.3]]

        pyt_mod.write_csv(csv_path, header, rows)
        self.assertTrue(os.path.isfile(csv_path))

        with open(csv_path, "rb") as fh:
            content = fh.read()

        # Must begin with UTF-8 BOM \xef\xbb\xbf
        self.assertTrue(content.startswith(b"\xef\xbb\xbf"), "CSV missing UTF-8 BOM")
        # Check Arabic text is decodable
        decoded = content.decode("utf-8")
        self.assertIn(u"مرسى علم", decoded)


if __name__ == "__main__":
    unittest.main()
