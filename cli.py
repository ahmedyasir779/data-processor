import argparse
import sys
import os
from pathlib import Path
from colorama import Fore, Style, init
from tqdm import tqdm
import time
from datetime import datetime

# Initialize colorama for cross-platform colored output
init()

# Import our modules
from loader import DataLoader
from cleaner import DataCleaner
from analyzer import DataAnalyzer
from dashboard import DashboardGenerator
from logger_config import get_logger

logger = get_logger(__name__)

class Colors:
    SUCCESS = Fore.GREEN
    ERROR = Fore.RED
    WARNING = Fore.YELLOW
    INFO = Fore.CYAN
    RESET = Style.RESET_ALL


def print_success(message):
    print(f"{Colors.SUCCESS}✓ {message}{Colors.RESET}")


def print_error(message):
    print(f"{Colors.ERROR}✗ {message}{Colors.RESET}")


def print_warning(message):
    print(f"{Colors.WARNING}⚠ {message}{Colors.RESET}")


def print_info(message):
    print(f"{Colors.INFO}ℹ {message}{Colors.RESET}")


def print_header(title):
    print(f"\n{Colors.INFO}{'='*60}")
    print(f"{title}")
    print(f"{'='*60}{Colors.RESET}\n")


def load_data(file_path):
    try:
        print_info(f"Loading data from {file_path}...")
        logger.info(f"Attempting to load file: {file_path}")

        loader = DataLoader(file_path)
        data = loader.load()

        print_success(f"Loaded {len(data)} rows, {len(data.columns)} columns")
        logger.info(f"Successfully loaded {len(data)} rows")

        return data
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")

        print_error(f"File not found: {file_path}")
        print_info(f"Tip: Check the file path or use an absolute path")

        return None
    except PermissionError as e:
        logger.error(f"Permission denied: {file_path}")
        
        print_error(f"Permission denied: Cannot read {file_path}")
        print_info(f"Tip: Check file permissions")
        
        return None
    except ValueError as e:
        logger.error(f"Invalid file format: {e}")
        
        print_error(f"Invalid file format: {e}")
        print_info(f"Tip: Supported formats are CSV, JSON, and Excel")
        
        return None
    except Exception as e:
        logger.error(f"Unexpected error loading file: {e}", exc_info=True)
        print_error(f"Error loading file: {e}")
        return None


def clean_data(data, strategy='drop'):
    print_info("Cleaning data...")
    
    # Show progress
    with tqdm(total=4, desc="Cleaning", unit="step") as pbar:
        cleaner = DataCleaner(data)
        
        # Step 1: Handle missing values
        cleaner.handle_missing_values(strategy=strategy)
        pbar.update(1)
        
        # Step 2: Remove duplicates
        cleaner.remove_duplicates()
        pbar.update(1)
        
        # Step 3: Clean strings
        cleaner.clean_strings()
        pbar.update(1)
        
        # Step 4: Get cleaned data
        cleaned = cleaner.get_cleaned_data()
        pbar.update(1)
    
    # Show report
    report = cleaner.get_report()
    original = report['original_rows']
    final = report['final_rows']
    removed = original - final
    
    print_success(f"Cleaned: {original} → {final} rows (removed {removed} problematic rows)")
    
    return cleaned


def analyze_data(data, output_dir):
    print_info("Analyzing data...")
    
    analyzer = DataAnalyzer(data)
    
    # Generate report
    report = analyzer.generate_report()
    print(report)
    
    # Save report
    os.makedirs(output_dir, exist_ok=True)
    report_path = os.path.join(output_dir, 'analysis_report.txt')
    analyzer.export_report(report_path)
    print_success(f"Report saved to {report_path}")
    
    return analyzer


def create_dashboard(data, output_dir, title="Data Analysis Dashboard"):
    print_info("Creating dashboard...")
    
    os.makedirs(output_dir, exist_ok=True)
    dashboard = DashboardGenerator(data, title=title)
    
    # Create overview dashboard
    dashboard_path = os.path.join(output_dir, 'dashboard.png')
    dashboard.create_overview_dashboard(save_path=dashboard_path)
    
    print_success(f"Dashboard saved to {dashboard_path}")


def run_pipeline(args):
    print_header("DATA PROCESSING PIPELINE")

    logger.info("="*60)
    logger.info("Starting pipeline execution")
    logger.info(f"Input file: {args.file}")
    logger.info(f"Options: clean={args.clean}, analyze={args.analyze}, dashboard={args.dashboard}")

    start_time = time.time()
    
    try:
        # Step 1: Load data
        data = load_data(args.file)
        if data is None:
            logger.error("Pipeline failed at loading stage")
            sys.exit(1)
        
        # Step 2: Clean data (if requested)
        if args.clean:
            data = clean_data(data, strategy=args.clean_strategy)
        else:
            print_warning("Skipping data cleaning (use --clean to enable)")
            logger.info("Data cleaning skipped")
        
        # Step 3: Analyze data (if requested)
        if args.analyze:
            analyze_data(data, args.output)
        else:
            print_warning("Skipping analysis (use --analyze to enable)")
            logger.info("Data analysis skipped")

        # Step 4: Create dashboard (if requested)
        if args.dashboard:
            title = args.title or f"Analysis of {Path(args.file).stem}"
            create_dashboard(data, args.output, title=title)
        else:
            print_warning("Skipping dashboard (use --dashboard to enable)")
            logger.info("Dashboard creation skipped")

        # Summary
        elapsed = time.time() - start_time
        print_header("PIPELINE COMPLETE")
        print_success(f"Total time: {elapsed:.2f} seconds")
        print_info(f"Output saved to: {args.output}/")

        logger.info(f"Pipeline completed in {elapsed:.2f} seconds")
        logger.info("="*60)

    except KeyboardInterrupt:
        logger.warning("Pipeline interrupted by user")
        print_warning("\n\nPipeline interrupted by user")

        sys.exit(0)
    except Exception as e:
        logger.error(f"Pipeline failed with unexpected error: {e}", exc_info=True)
        print_error(f"Pipeline failed: {e}")
        print_info(f"Check logs/pipeline_{datetime.now().strftime('%Y%m%d')}.log for details")
        sys.exit(1)


def interactive_mode():
    print_header("INTERACTIVE MODE")
    
    # Get file path
    file_path = input("Enter data file path: ").strip()
    
    # Get options
    clean = input("Clean data? (y/n): ").strip().lower() == 'y'
    analyze = input("Analyze data? (y/n): ").strip().lower() == 'y'
    dashboard = input("Create dashboard? (y/n): ").strip().lower() == 'y'
    
    output_dir = input("Output directory [output]: ").strip() or 'output'
    
    # Create mock args object
    class Args:
        pass
    
    args = Args()
    args.file = file_path
    args.clean = clean
    args.clean_strategy = 'drop'
    args.analyze = analyze
    args.dashboard = dashboard
    args.output = output_dir
    args.title = None
    
    run_pipeline(args)


def main():
    # Create argument parser
    parser = argparse.ArgumentParser(
        description='Data Processing Pipeline - Load, Clean, Analyze, Visualize',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
            Examples:
            # Load and clean data
            python cli.py --file data.csv --clean
            
            # Full pipeline
            python cli.py --file data.csv --clean --analyze --dashboard
            
            # Custom output directory
            python cli.py --file data.csv --clean --analyze --output results/
            
            # Interactive mode
            python cli.py --interactive
        """
    )
    
    # File argument
    parser.add_argument(
        '--file', '-f',
        type=str,
        help='Path to input data file (CSV, JSON, or Excel)'
    )
    
    # Processing options
    parser.add_argument(
        '--clean', '-c',
        action='store_true',
        help='Clean the data (remove missing values, duplicates, outliers)'
    )
    
    parser.add_argument(
        '--clean-strategy',
        type=str,
        choices=['drop', 'fill', 'forward_fill'],
        default='drop',
        help='Strategy for handling missing values (default: drop)'
    )
    
    parser.add_argument(
        '--analyze', '-a',
        action='store_true',
        help='Analyze data and generate statistics report'
    )
    
    parser.add_argument(
        '--dashboard', '-d',
        action='store_true',
        help='Create visualization dashboard'
    )
    
    # Output options
    parser.add_argument(
        '--output', '-o',
        type=str,
        default='output',
        help='Output directory for results (default: output/)'
    )
    
    parser.add_argument(
        '--title', '-t',
        type=str,
        help='Custom title for dashboard'
    )
    
    # Interactive mode
    parser.add_argument(
        '--interactive', '-i',
        action='store_true',
        help='Run in interactive mode (prompts for options)'
    )
    
    # Shortcut for full pipeline
    parser.add_argument(
        '--all',
        action='store_true',
        help='Run complete pipeline (clean + analyze + dashboard)'
    )
    
    
    # Parse arguments
    args = parser.parse_args()
    
    # Interactive mode
    if args.interactive:
        interactive_mode()
        return
    
    # Validate file argument
    if not args.file:
        parser.print_help()
        print_error("\nError: --file argument is required (or use --interactive)")
        sys.exit(1)
    
    # Handle --all shortcut
    if args.all:
        args.clean = True
        args.analyze = True
        args.dashboard = True
    
    # Run pipeline
    try:
        run_pipeline(args)
    except KeyboardInterrupt:
        print_warning("\n\nPipeline interrupted by user")
        sys.exit(0)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()