import camelot
import pandas as pd
import os
import sys
import pypdf # Import pypdf for page counting
import subprocess # For checking Ghostscript from Python
import shutil # For finding executable path

# --- Constants ---
DEFAULT_FLAVOR: str = 'lattice'
DEFAULT_DELIMITER: str = ';'
DEFAULT_PAGE_NUMBER: str = 'all'
GS_EXECUTABLE_NAME: str = 'gs' # Name of the Ghostscript executable

# --- Utility Functions ---

def get_pdf_page_count(pdf_path: str) -> int:
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

def _configure_camelot_environment() -> None:
    """
    Configures the environment variables required by Camelot,
    specifically setting GS_PATH for Ghostscript.
    This function also verifies Ghostscript's presence.
    """
    print(f"Python's PATH environment variable: {os.environ.get('PATH')}")

    gs_executable_path = shutil.which(GS_EXECUTABLE_NAME)
    if gs_executable_path:
        print(f"shutil.which found Ghostscript at: {gs_executable_path}")
        # Explicitly set GS_PATH for Camelot, even if it's found in system PATH
        os.environ['GS_PATH'] = gs_executable_path
        print(f"Explicitly set GS_PATH environment variable for Camelot to: {os.environ['GS_PATH']}")
        try:
            # Verify Ghostscript is callable from Python
            result = subprocess.run([gs_executable_path, '-v'], capture_output=True, text=True, check=True)
            print("Ghostscript found and callable by Python via subprocess.run:")
            # Print only the first line of gs -v output for brevity
            print(result.stdout.strip().split('\n')[0])
        except subprocess.CalledProcessError as e:
            print(f"Error calling Ghostscript from Python via subprocess.run: {e}")
            print(f"Stderr: {e.stderr}")
        except FileNotFoundError:
            # This case should ideally not be hit if shutil.which worked, but for robustness
            print(f"Ghostscript executable not found at '{gs_executable_path}' despite shutil.which finding it.")
        except Exception as e:
            print(f"An unexpected error occurred while checking Ghostscript via subprocess.run: {e}")
    else:
        print(f"shutil.which could NOT find Ghostscript ('{GS_EXECUTABLE_NAME}') in Python's PATH.")
        print("Camelot's 'lattice' flavor requires Ghostscript. Please ensure it's installed and in your system's PATH.")
        print("You may need to manually set the GS_PATH environment variable if it's installed in a non-standard location.")

def extract_table_from_pdf_to_csv(
    pdf_path: str,
    output_csv_path: str,
    page_number: str = DEFAULT_PAGE_NUMBER,
    flavor: str = DEFAULT_FLAVOR,
    output_delimiter: str = DEFAULT_DELIMITER
) -> bool:
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

    Returns:
        bool: True if tables were successfully extracted and saved, False otherwise.
    """
    if not os.path.exists(pdf_path):
        print(f"Error: PDF file not found at '{pdf_path}'")
        return False

    # --- Automatic Page Detection ---
    pages_to_extract = page_number
    if page_number == 'all':
        total_pages = get_pdf_page_count(pdf_path)
        if total_pages == -1:
            print("Cannot determine total pages. Please specify page numbers manually (e.g., '1-5').")
            return False
        pages_to_extract = f'1-{total_pages}'
        print(f"Detected {total_pages} pages. Attempting extraction from pages: {pages_to_extract}")
    # --- End of Automatic Page Detection ---

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
                # Use pd.concat for efficient DataFrame concatenation
                all_tables_df = pd.concat([all_tables_df, df], ignore_index=True)

        all_tables_df.to_csv(output_csv_path, index=False, sep=output_delimiter)
        print(f"Successfully extracted table(s) to '{output_csv_path}' with delimiter '{output_delimiter}'")
        return True

    except Exception as e:
        print(f"An error occurred during table extraction: {e}")
        print("This might be due to Ghostscript issues (especially for 'lattice' flavor), or the PDF structure.")
        print("Consider trying a different 'flavor' ('lattice' or 'stream') or adjusting page numbers/table areas.")
        return False


if __name__ == "__main__":
    # Configure Camelot environment (including Ghostscript path)
    _configure_camelot_environment()

    # Check if a PDF filename was provided as a command-line argument
    if len(sys.argv) < 2:
        print("Usage: python extract_pdf_table.py <input_pdf_filename> [output_csv_filename] [page_number(s)] [flavor] [output_delimiter]")
        print("\nExamples:")
        print(f"  python {sys.argv[0]} my_document.pdf                                 # Detects all pages, default CSV, {DEFAULT_FLAVOR}")
        print(f"  python {sys.argv[0]} annual_report.pdf report.csv                    # Detects all pages, 'report.csv', {DEFAULT_FLAVOR}")
        print(f"  python {sys.argv[0]} multi_page.pdf output.csv all stream            # Explicitly extracts all pages, 'output.csv', stream")
        print(f"  python {sys.argv[0]} data.pdf output.csv 1-4 lattice ;               # Extracts pages 1 to 4, semicolon delimiter")
        print(f"  python {sys.argv[0]} another.pdf final.tsv 2,4 stream '\\t'           # Extracts pages 2 and 4, tab delimiter")
        sys.exit(1)

    input_pdf_path = sys.argv[1]

    # Determine output CSV path
    if len(sys.argv) > 2:
        output_csv_path = sys.argv[2]
    else:
        base_name = os.path.splitext(input_pdf_path)[0]
        output_csv_path = f"{base_name}.csv"

    # Determine page number
    page_num = sys.argv[3] if len(sys.argv) > 3 else DEFAULT_PAGE_NUMBER

    # Determine flavor
    extraction_flavor = sys.argv[4] if len(sys.argv) > 4 else DEFAULT_FLAVOR

    # Determine output delimiter
    csv_delimiter = DEFAULT_DELIMITER
    if len(sys.argv) > 5:
        if sys.argv[5] == '\\t':
            csv_delimiter = '\t'
        elif sys.argv[5] == '\\n':
            csv_delimiter = '\n'
        else:
            csv_delimiter = sys.argv[5]

    # Call the extraction function
    success = extract_table_from_pdf_to_csv(
        input_pdf_path,
        output_csv_path,
        page_num,
        extraction_flavor,
        csv_delimiter
    )

    if not success:
        print("\n--- Troubleshooting Tip ---")
        print(f"Table extraction failed with flavor '{extraction_flavor}'.")
        # Provide specific tip if lattice failed, and stream worked previously
        if extraction_flavor == 'lattice':
            print(f"The 'lattice' flavor often requires robust Ghostscript image processing. Since you previously confirmed 'stream' worked,")
            print(f"please try running the script with the 'stream' flavor instead:")
            print(f"  python {sys.argv[0]} {input_pdf_path} {output_csv_path} {page_num} stream {csv_delimiter}")
            print("The 'stream' flavor relies more on text and whitespace, which might be more suitable for this PDF.")
        sys.exit(1)


