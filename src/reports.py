import csv
from tabulate import tabulate
from abc import ABC, abstractmethod


class BaseReport(ABC):
    def __init__(self, files, reportName):
        self.files = files
        self.reportName = reportName
        self.stats = {}

    def process_files(self):
        for filename in self.files:

            try:
                with open(filename, "r", encoding="utf-8") as file:
                    reader = csv.DictReader(file)

                    for row in reader:
                        self.process_row(row)
            except FileNotFoundError:
                print(f"{filename} not found")
            except PermissionError:
                print("PermissionError")

    @abstractmethod
    def process_row(row):
        pass

    def get_averages(self):
        averages = {}
        for key, (total, count) in self.stats.items():
            if count > 0:
                averages[key] = total / count
        return averages

    @abstractmethod
    def print_report(self):
        pass

    @abstractmethod
    def create_report(self):
        pass


class GDPReport(BaseReport):
    def process_row(self, row):
        country = row["country"]
        gdp_value = row["gdp"]

        if country and gdp_value:
            try:
                gdp = float(gdp_value)
                if country in self.stats:
                    total, count = self.stats[country]
                    self.stats[country] = (total + gdp, count + 1)
                else:
                    self.stats[country] = (gdp, 1)
            except ValueError:
                pass

    def print_report(self):
        averages = self.get_averages()

        if not averages:
            print("Data error")
            return

        table = []
        for i, (country, (total, count)) in enumerate(self.stats.items(), 1):
            avg = total / count
            table.append([i, country, f"{avg:.2f}"])
        headers = ["", "country", "gdp"]
        print(tabulate(table, headers=headers, tablefmt="github"))

    def create_report(self):
        headers = ["", "country", "gdp"]
        with open(self.reportName, "w", encoding="utf-8") as file:
            table = []
            for i, (country, (total, count)) in enumerate(self.stats.items(), 1):
                avg = total / count
                table.append([i, country, f"{avg:.2f}"])
            file.write(tabulate(table, headers=headers, tablefmt="github"))
