import camelot
import pandas as pd
import os
import sys
import pypdf # Import pypdf for page counting

def get_pdf_page_count(pdf_path):
    """
    Detects the number of pages in a PDF file.

    Args:
        pdf_path (str): The path to the PDF file.

    Returns:
        int: The number of pages, or -1 if an error occurs.
    """
    try:
        with open(pdf_path, 'rb') as f:
            reader = pypdf.PdfReader(f)
            return len(reader.pages)
    except Exception as e:
        print(f"Error reading PDF page count for '{pdf_path}': {e}")
        return -1

def extract_table_from_pdf_to_csv(pdf_path, output_csv_path, page_number='all', flavor='lattice', output_delimiter=';'):
    """
    Extracts tables from a PDF and saves them to a CSV file with a specified delimiter.

    Args:
        pdf_path (str): The path to the input PDF file.
        output_csv_path (str): The path where the output CSV file will be saved.
        page_number (str): The page number(s) to extract tables from.
                           Can be '1', '1,2,3', '1-4', or 'all'.
                           If 'all' is passed, the script will automatically detect
                           the total number of pages and pass that range to Camelot.
        flavor (str): The table extraction method. 'lattice' for tables with ruling lines,
                      'stream' for tables with whitespace separation.
        output_delimiter (str): The character to use as a field separator in the output CSV.
                                Defaults to ';'.
    """
    if not os.path.exists(pdf_path):
        print(f"Error: PDF file not found at '{pdf_path}'")
        return False

    # --- Automatic Page Detection Enhancement ---
    pages_to_extract = page_number
    if page_number == 'all':
        total_pages = get_pdf_page_count(pdf_path)
        if total_pages == -1:
            print("Cannot determine total pages. Please specify page numbers manually (e.g., '1-5').")
            return False
        pages_to_extract = f'1-{total_pages}'
        print(f"Detected {total_pages} pages. Extracting from pages: {pages_to_extract}")
    # --- End of Enhancement ---

    print(f"Attempting to extract tables from '{pdf_path}' (page(s): {pages_to_extract}, flavor: {flavor})...")
    try:
        tables = camelot.read_pdf(pdf_path, pages=pages_to_extract, flavor=flavor)

        if not tables:
            print(f"No tables found on page(s) {pages_to_extract} using '{flavor}' flavor.")
            return False

        print(f"Found {len(tables)} table(s) across the specified pages.")

        all_tables_df = pd.DataFrame()

        for i, table in enumerate(tables):
            print(f"Processing Table {i+1} (Page {table.page})...")
            df = table.df

            if all_tables_df.empty:
                all_tables_df = df
            else:
                all_tables_df = pd.concat([all_tables_df, df], ignore_index=True)

        all_tables_df.to_csv(output_csv_path, index=False, sep=output_delimiter)
        print(f"Successfully extracted table(s) to '{output_csv_path}' with delimiter '{output_delimiter}'")
        return True

    except Exception as e:
        print(f"An error occurred during table extraction: {e}")
        print("Please ensure Ghostscript is installed and in your system's PATH.")
        print("Also, consider trying a different 'flavor' ('lattice' or 'stream') or adjusting page numbers.")
        return False


if __name__ == "__main__":
    # Check if a PDF filename was provided as a command-line argument
    if len(sys.argv) < 2:
        print("Usage: python extract_pdf_table.py <input_pdf_filename> [output_csv_filename] [page_number(s)] [flavor] [output_delimiter]")
        print("\nExamples:")
        print("  python extract_pdf_table.py my_document.pdf                                 # Detects all pages, default CSV, lattice")
        print("  python extract_pdf_table.py annual_report.pdf report.csv                    # Detects all pages, 'report.csv', lattice")
        print("  python extract_pdf_table.py multi_page.pdf output.csv all stream            # Explicitly extracts all pages, 'output.csv', stream")
        print("  python extract_pdf_table.py data.pdf output.csv 1-4 lattice ;               # Extracts pages 1 to 4, semicolon delimiter")
        print("  python extract_pdf_table.py another.pdf final.tsv 2,4 stream '\t'          # Extracts pages 2 and 4, tab delimiter")
        sys.exit(1)

    input_pdf_path = sys.argv[1]

    # Determine output CSV path (default to same name as PDF, but with .csv extension)
    if len(sys.argv) > 2:
        output_csv_path = sys.argv[2]
    else:
        base_name = os.path.splitext(input_pdf_path)[0]
        output_csv_path = f"{base_name}.csv"

    # Determine page number (default to 'all' for automatic detection)
    page_num = 'all'
    if len(sys.argv) > 3:
        page_num = sys.argv[3]

    # Determine flavor (default to 'lattice')
    extraction_flavor = 'lattice'
    if len(sys.argv) > 4:
        extraction_flavor = sys.argv[4]

    # Determine output delimiter (default to ';')
    csv_delimiter = ';'
    if len(sys.argv) > 5:
        if sys.argv[5] == '\\t':
            csv_delimiter = '\t'
        elif sys.argv[5] == '\\n':
            csv_delimiter = '\n'
        else:
            csv_delimiter = sys.argv[5]

    # Call the extraction function
    success = extract_table_from_pdf_to_csv(input_pdf_path, output_csv_path, page_num, extraction_flavor, csv_delimiter)

    if not success:
        sys.exit(1)
