from reports import GDPReport
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--files", nargs='+', required=True)
    parser.add_argument("--report")
    
    args = parser.parse_args()
    
    report = GDPReport(args.files, args.report)
    report.process_files()
    report.print_report()
    report.create_report()

if __name__ == "__main__":
    main()