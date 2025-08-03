import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

# Define SVG and Inkscape namespaces
# It's crucial to use the full namespace URI when searching for elements
# or attributes that belong to a specific namespace.
SVG_NAMESPACE = "http://www.w3.org/2000/svg"
INKSCAPE_NAMESPACE = "http://www.inkscape.org/namespaces/inkscape"

# Register namespaces for cleaner output (optional, but good practice)
ET.register_namespace('', SVG_NAMESPACE)
ET.register_namespace('inkscape', INKSCAPE_NAMESPACE)

# Helper function to create a tag with a namespace
def ns_tag(namespace, tag_name):
    return f"{{{namespace}}}{tag_name}"

def get_next_weekday_strictly_after(start_date: datetime, target_weekday: int) -> datetime:
    """
    Calculates the next occurrence of a specific weekday strictly AFTER a start date.
    (0=Monday, 1=Tuesday, 2=Wednesday, 3=Thursday, 4=Friday, 5=Saturday, 6=Sunday).
    If start_date is already the target_weekday, it returns target_weekday of the NEXT week.

    Args:
        start_date (datetime): The starting date.
        target_weekday (int): The target weekday (0=Monday, 6=Sunday).

    Returns:
        datetime: The date of the next occurrence of the target weekday, strictly after start_date.
    """
    days_ahead = target_weekday - start_date.weekday()
    if days_ahead <= 0: # If target is today or in the past, move to next week
        days_ahead += 7
    return start_date + timedelta(days=days_ahead)


def update_svg_dates(svg_file_path: str, output_file_path: str, initial_date_str: str) -> None:
    """
    Updates date fields in an SVG file based on an initial date and sequential weekday logic.

    Args:
        svg_file_path (str): Path to the input SVG file.
        output_file_path (str): Path where the modified SVG will be saved.
        initial_date_str (str): The initial date in DD/MM/YYYY format.
    """
    try:
        # Parse the SVG file
        tree = ET.parse(svg_file_path)
        root = tree.getroot()

        # Convert the initial input date string to a datetime object
        # Assuming DD/MM/YYYY format
        initial_date = datetime.strptime(initial_date_str, "%d/%m/%Y")

        # This variable will hold the date that the *next* calculation should be based on.
        # It gets updated after each sequential date field is processed.
        current_base_date = initial_date

        # Define the order of processing and the logic for each field
        # Values are target weekdays (0=Monday, 4=Friday, 2=Wednesday) or special flags
        date_update_sequence = [
            ("txtSignDate", "initial"),
            ("txtDate1", "initial"),
            ("txtDate2", 4),  # Next Friday
            ("txtDate3", 2),  # Next Wednesday
            ("txtDate4", 4),  # Next Friday
            ("txtDate5", 2),  # Next Wednesday
            ("txtDate6", 4),  # Next Friday
            ("txtDate7", 2),  # Next Wednesday
            ("txtDate8", 4)   # Next Friday
        ]

        # First, build a dictionary of all relevant text elements for quick lookup
        text_elements_by_label = {}
        for text_element in root.findall(f".//{ns_tag(SVG_NAMESPACE, 'text')}"):
            inkscape_label = text_element.get(ns_tag(INKSCAPE_NAMESPACE, 'label'))
            if inkscape_label:
                text_elements_by_label[inkscape_label] = text_element

        # Iterate through the defined sequence to update dates
        for label, logic in date_update_sequence:
            text_element = text_elements_by_label.get(label)
            if not text_element:
                print(f"Warning: Text element with inkscape:label='{label}' not found. Skipping.")
                continue

            new_date_for_field = None

            if label in ["txtSignDate", "txtDate1"]:
                # These fields are directly set to the initial input date
                new_date_for_field = initial_date
            else:
                # For sequential dates, calculate based on the current_base_date
                # We use get_next_weekday_strictly_after to ensure progression
                new_date_for_field = get_next_weekday_strictly_after(current_base_date, logic)

            if new_date_for_field:
                # Format the date back to DD/MM/YYYY
                formatted_date = new_date_for_field.strftime("%d/%m/%Y")

                # Find the first <tspan> child and update its text
                # The text content is typically within the first tspan
                tspan_element = text_element.find(ns_tag(SVG_NAMESPACE, 'tspan'))
                if tspan_element is not None:
                    tspan_element.text = formatted_date
                    print(f"Updated '{label}' to: {formatted_date}")
                    # IMPORTANT: Update the current_base_date for the *next* sequential calculation
                    current_base_date = new_date_for_field
                else:
                    print(f"Warning: <tspan> not found within <text id='{text_element.get('id')}' inkscape:label='{label}'>. Cannot update text.")
            else:
                print(f"Error: Could not calculate date for '{label}'.")

        # Save the modified SVG to the output file
        tree.write(output_file_path, encoding="utf-8", xml_declaration=True)
        print(f"\nSVG file successfully updated and saved to '{output_file_path}'")

    except FileNotFoundError:
        print(f"Error: Input SVG file not found at '{svg_file_path}'")
    except ValueError as e:
        print(f"Error parsing date: {e}. Please ensure the input date is in DD/MM/YYYY format.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # --- How to use the script ---
    # 1. Save your original SVG file (e.g., 'your_template.svg')
    # 2. Save this Python script as a .py file (e.g., 'update_svg_dates_sequential.py')
    # 3. Run this Python script from your terminal:
    #    python update_svg_dates_sequential.py your_template.svg output_with_dates.svg 01/08/2025

    import sys

    if len(sys.argv) != 4:
        print("Usage: python update_svg_dates_sequential.py <input_svg_path> <output_svg_path> <start_date_DD/MM/YYYY>")
        print("\nExample: python update_svg_dates_sequential.py template.svg updated.svg 25/07/2025")
        sys.exit(1)

    input_svg = sys.argv[1]
    output_svg = sys.argv[2]
    start_date = sys.argv[3]

    update_svg_dates(input_svg, output_svg, start_date)
