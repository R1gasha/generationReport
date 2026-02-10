import tempfile
import os
from ..reports import GDPReport
# import pytest


class TestGDPReport:

    def test_process_row_single_country(self):
        report = GDPReport([], "test_report.txt")

        report.process_row({"country": "Spain", "gdp": "1000"})
        report.process_row({"country": "Spain", "gdp": "2000"})
        report.process_row({"country": "Spain", "gdp": "3000"})

        assert "Spain" in report.stats
        assert report.stats["Spain"] == (6000.0, 3)

    def test_process_row_multiple_countries(self):
        report = GDPReport([], "test_report.txt")

        report.process_row({"country": "Spain", "gdp": "1000"})
        report.process_row({"country": "France", "gdp": "2000"})
        report.process_row({"country": "Spain", "gdp": "1500"})

        assert "Spain" in report.stats
        assert "France" in report.stats
        assert report.stats["Spain"] == (2500.0, 2)
        assert report.stats["France"] == (2000.0, 1)

    def test_process_row_invalid_gdp(self):
        report = GDPReport([], "test_report.txt")

        report.process_row({"country": "Spain", "gdp": "dasdadas"})
        report.process_row({"country": "Spain", "gdp": ""})
        report.process_row({"country": "", "gdp": "1000"})

        assert not report.stats

    def test_get_averages(self):
        report = GDPReport([], "test_report.txt")

        report.stats = {"Spain": (3000.0, 3), "France": (6000.0, 2)}

        averages = report.get_averages()

        assert averages["Spain"] == 1000.0
        assert averages["France"] == 3000.0
        assert len(averages) == 2

    def test_process_files_with_valid_file(self):
        report = GDPReport(["./data_sets/economic2.csv"], "test_report.txt")
        report.process_files()

        assert "Spain" in report.stats
        assert "Mexico" in report.stats

        total, count = report.stats["Spain"]
        assert total == 4228.0
        assert count == 3

    def test_process_files_nonexistent_file(self, capsys):
        report = GDPReport(
            ["nonexistent.csv", "./data_sets/economic2.csv"], "test_report.txt"
        )

        report.process_files()
        captured = capsys.readouterr()

        assert "nonexistent.csv not found" in captured.out

        assert "Spain" in report.stats
        assert "Mexico" in report.stats

    def test_process_files_empty_file(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write("country,year,gdp\n")
            temp_file_path = f.name

        try:
            report = GDPReport([temp_file_path], "test_report.txt")
            report.process_files()

            assert not report.stats
        finally:
            os.unlink(temp_file_path)

    def test_print_report(self, capsys):
        report = GDPReport([], "test_report.txt")

        report.stats = {"Spain": (3000.0, 3), "France": (6000.0, 2)}

        report.print_report()

        captured = capsys.readouterr()

        assert "country" in captured.out
        assert "gdp" in captured.out
        assert "Spain" in captured.out
        assert "France" in captured.out
        assert "1000" in captured.out
        assert "3000" in captured.out

    def test_print_report_empty_stats(self, capsys):
        report = GDPReport([], "test_report.txt")
        report.print_report()

        captured = capsys.readouterr()
        assert "Data error" in captured.out

    def test_create_report(self, tmp_path):
        report_file = tmp_path / "test_report.txt"
        report = GDPReport(["./data_sets/economic2.csv"], str(report_file))

        report.process_files()
        report.create_report()

        assert report_file.exists()

        content = report_file.read_text()

        assert "Spain" in content
        assert "Mexico" in report.stats
        assert "Indonesia" in content
        assert "Netherlands" in content
        assert "Turkey" in content
        assert "Switzerland" in content
        assert "Saudi Arabia" in content
        assert "1409.33" in content
        assert "1016.33" in content

    def test_integration_with_sample_data(self, tmp_path):
        report_file = tmp_path / "integration_report.txt"
        report = GDPReport(["./data_sets/economic2.csv"], str(report_file))

        report.process_files()

        assert "Spain" in report.stats
        assert "Mexico" in report.stats
        assert "Indonesia" in report.stats
        assert "Netherlands" in report.stats
        assert "Turkey" in report.stats
        assert "Switzerland" in report.stats
        assert "Saudi Arabia" in report.stats

        assert report.stats["Spain"] == (4228.0, 3)
        assert report.stats["Mexico"] == (4178.0, 3)

        report.create_report()

        assert report_file.exists()

        report.print_report()
