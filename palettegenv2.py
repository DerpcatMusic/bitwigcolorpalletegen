
# --- START OF FILE Bitwig Color Palette Generator.py ---
from PIL import Image
import random
import os
import datetime
import colorsys
from typing import List
import json

# Dynamically determine the user's Documents directory and Bitwig path
USER_DOCUMENTS = os.path.expanduser("~/Documents")
BITWIG_PALETTE_DIR = os.path.join(USER_DOCUMENTS, "Bitwig Studio", "Color Palettes")
GENERATED_PALETTES_SUBFOLDER = "generated_palettes" # Define subfolder name

MF_TWISTER_COLORS_JSON_FILE = "mf_twister_colors.json" # Filename of JSON file
distinct_27_rgb_colors = [] # Initialize as empty list
try:
    with open(MF_TWISTER_COLORS_JSON_FILE, 'r') as f:
        distinct_27_rgb_colors = json.load(f)
    print(f"Loaded {len(distinct_27_rgb_colors)} distinct colors from: {MF_TWISTER_COLORS_JSON_FILE}")
except FileNotFoundError:
    print(f"Warning: {MF_TWISTER_COLORS_JSON_FILE} not found. 'mf_twister' strategy will use default colors or might not work.")
except json.JSONDecodeError:
    print(f"Error decoding JSON from {MF_TWISTER_COLORS_JSON_FILE}. File might be corrupted.")
except Exception as e:
    print(f"Error loading colors from {MF_TWISTER_COLORS_JSON_FILE}: {e}")

def validate_hex_color(color):
    """Validate if the input is a proper hex color code."""
    if not color.startswith('#') or len(color) != 7:
        return False
    try:
        # Check if the hex part can be converted to an integer
        int(color[1:], 16)
        return True
    except ValueError:
        return False

def get_color_input(row, col):
    """Get and validate color input from user."""
    while True:
        color = input(f"Enter hex color for position [{row+1}][{col+1}] (format #RRGGBB): ")
        color = color.strip().upper()
        if validate_hex_color(color):
            return color
        else:
            print("Invalid hex color format. Please use format #RRGGBB (e.g., #FF0000 for red)")

def hsv_to_hex(h, s, v):
    """Convert HSV color to hex color code."""
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    r = int(r * 255)
    g = int(g * 255)
    b = int(b * 255)
    return f"#{r:02X}{g:02X}{b:02X}"

def create_empty_palette() -> List[List[str]]:
    """Creates and returns an empty 3x9 palette (list of lists)."""
    return [
        ["" for _ in range(9)],
        ["" for _ in range(9)],
        ["" for _ in range(9)]
    ]

def distinct_hues_palette(row_shifts):
    """Generate palette using distinct hues strategy."""
    palette = create_empty_palette()
    base_hues = [(i / 9 + random.random() * 0.05) % 1.0 for i in range(9)]
    random.shuffle(base_hues)

    for col in range(9):
        base_hue = base_hues[col]
        for row in range(3):
            shifted_hue = (base_hue + row_shifts[row]) % 1.0
            saturation = 0.3 + row * 0.25 + random.random() * 0.1
            value = 0.9 - row * 0.15 + random.random() * 0.1
            palette[row][col] = hsv_to_hex(shifted_hue, saturation, value)
    return palette

def split_complementary_palette(row_shifts):
    """Generate palette using split complementary strategy."""
    palette = create_empty_palette()
    base_hue = random.random()
    complement1 = (base_hue + 0.5 - 0.05) % 1.0
    complement2 = (base_hue + 0.5 + 0.05) % 1.0
    hues = [base_hue] * 3 + [
        (base_hue + 0.02) % 1.0,
        (base_hue - 0.02) % 1.0,
        complement1,
        (complement1 + 0.03) % 1.0,
        complement2,
        (complement2 - 0.03) % 1.0
    ]
    random.shuffle(hues)
    for col in range(9):
        for row in range(3):
            shifted_hue = (hues[col] + row_shifts[row]) % 1.0
            saturation = 0.4 + row * 0.2 + random.random() * 0.1
            value = 0.9 - row * 0.15 + random.random() * 0.1
            palette[row][col] = hsv_to_hex(shifted_hue, saturation, value)
    return palette

def triadic_variations_palette(row_shifts):
    """Generate palette using triadic variations strategy."""
    palette = create_empty_palette()
    hue1 = random.random()
    hue2 = (hue1 + 0.33) % 1.0
    hue3 = (hue1 + 0.66) % 1.0
    hue_variations = []
    for hue in [hue1, hue2, hue3]:
        hue_variations.extend([hue, (hue + 0.03) % 1.0, (hue - 0.03) % 1.0])
    random.shuffle(hue_variations)
    for col in range(9):
        for row in range(3):
            shifted_hue = (hue_variations[col] + row_shifts[row]) % 1.0
            saturation = 0.4 + row * 0.2 + random.random() * 0.2
            value = 0.9 - row * 0.2 + random.random() * 0.1
            palette[row][col] = hsv_to_hex(shifted_hue, saturation, value)
    return palette

def analogous_extended_palette(row_shifts):
    """Generate palette using analogous extended strategy."""
    palette = create_empty_palette()
    start_hue = random.random()
    hue_range = 0.3
    for col in range(9):
        hue_offset = (col / 9) * hue_range
        base_hue = (start_hue + hue_offset) % 1.0
        for row in range(3):
            shifted_hue = (base_hue + row_shifts[row]) % 1.0
            saturation = 0.5 + row * 0.15 + random.random() * 0.2
            value = 0.9 - row * 0.15 + random.random() * 0.1
            palette[row][col] = hsv_to_hex(shifted_hue, saturation, value)
    return palette

def monochromatic_columns_palette(row_shifts):
    """Generate palette using monochromatic columns strategy."""
    palette = create_empty_palette()
    for col in range(9):
        base_hue = random.random()
        for row in range(3):
            shifted_hue = (base_hue + row_shifts[row]) % 1.0
            saturation = 0.4 + row * 0.15 + random.random() * 0.1
            value = 0.9 - row * 0.2 + random.random() * 0.1
            palette[row][col] = hsv_to_hex(shifted_hue, saturation, value)
    return palette

def warm_cool_contrast_palette(row_shifts):
    """Generate palette using warm cool contrast strategy."""
    palette = create_empty_palette()
    warm_hues = [random.uniform(0.95, 0.15) for _ in range(5)]
    cool_hues = [random.uniform(0.4, 0.7) for _ in range(4)]
    all_hues = warm_hues + cool_hues
    random.shuffle(all_hues)
    for col in range(9):
        base_hue = all_hues[col]
        for row in range(3):
            shifted_hue = (base_hue + row_shifts[row]) % 1.0
            saturation = 0.6 + row * 0.1 + random.random() * 0.1
            value = 0.9 - row * 0.2 + random.random() * 0.1
            palette[row][col] = hsv_to_hex(shifted_hue, saturation, value)
    return palette

def pastel_dark_contrast_palette(row_shifts):
    """Generate palette using pastel dark contrast strategy."""
    palette = create_empty_palette()
    hues = [random.random() for _ in range(9)]
    for col in range(9):
        for row in range(3):
            shifted_hue = (hues[col] + row_shifts[row]) % 1.0
            if row == 0:
                saturation = 0.3 + random.random() * 0.2
                value = 0.9 + random.random() * 0.1
            elif row == 1:
                saturation = 0.6 + random.random() * 0.2
                value = 0.7 + random.random() * 0.1
            else:
                saturation = 0.8 + random.random() * 0.2
                value = 0.4 + random.random() * 0.2
            palette[row][col] = hsv_to_hex(shifted_hue, saturation, value)
    return palette

def random_with_harmony_palette(row_shifts):
    """Generate palette using random with harmony strategy."""
    palette = create_empty_palette()
    for col in range(9):
        base_hue = random.random()
        for row in range(3):
            shifted_hue = (base_hue + row_shifts[row]) % 1.0
            if row == 0:
                saturation = random.uniform(0.3, 0.6)
                value = random.uniform(0.8, 1.0)
            elif row == 1:
                saturation = random.uniform(0.5, 0.8)
                value = random.uniform(0.6, 0.8)
            else:
                saturation = random.uniform(0.7, 1.0)
                value = random.uniform(0.4, 0.7)
            palette[row][col] = hsv_to_hex(shifted_hue, saturation, value)
    return palette

def complementary_palette(row_shifts):
    """Generate palette using complementary strategy."""
    palette = create_empty_palette()
    base_hue = random.random()
    complement_hue = (base_hue + 0.5) % 1.0
    hues = [base_hue] * 5 + [complement_hue] * 4
    random.shuffle(hues)
    for col in range(9):
        base_hue = hues[col]
        for row in range(3):
            shifted_hue = (base_hue + row_shifts[row]) % 1.0
            saturation = 0.5 + row * 0.15 + random.random() * 0.1
            value = 0.8 - row * 0.1 + random.random() * 0.1
            palette[row][col] = hsv_to_hex(shifted_hue, saturation, value)
    return palette

def shades_of_gray_palette(row_shifts):
    """Generate palette using shades of gray strategy."""
    palette = create_empty_palette()
    base_hue = random.uniform(0, 1)
    for col in range(9):
        for row in range(3):
            shifted_hue = (base_hue + row_shifts[row] * 0.5) % 1.0
            saturation = 0.05 + random.random() * 0.05
            value = 0.2 + (col / 9) * 0.7 + (row / 3) * 0.1
            palette[row][col] = hsv_to_hex(shifted_hue, saturation, value)
    return palette

def tetradic_palette(row_shifts):
    """Generate palette using tetradic strategy."""
    palette = create_empty_palette()
    base_hue = random.random()
    hue2 = (base_hue + 0.33) % 1.0
    hue3 = (base_hue + 0.5) % 1.0
    hue4 = (base_hue + 0.83) % 1.0
    hues = [base_hue, base_hue, hue2, hue2, hue3, hue3, hue4, hue4, (base_hue + 0.1) % 1.0]
    random.shuffle(hues)
    for col in range(9):
        base_hue = hues[col]
        for row in range(3):
            shifted_hue = (base_hue + row_shifts[row]) % 1.0
            saturation = 0.5 + row * 0.15 + random.random() * 0.1
            value = 0.8 - row * 0.1 + random.random() * 0.1
            palette[row][col] = hsv_to_hex(shifted_hue, saturation, value)
    return palette

def mf_twister_palette(row_shifts: List[float]) -> List[List[str]]:
    """Generate palette using pre-selected 27 maximally distinct colors from JSON file."""
    palette = create_empty_palette()
    global distinct_27_rgb_colors # Access the globally loaded colors

    if not distinct_27_rgb_colors or len(distinct_27_rgb_colors) != 27:
        print("Error: 27 distinct RGB colors not loaded correctly for 'mf_twister' strategy.")
        return palette # Return empty palette in case of error

    hex_colors = [hsv_to_hex(*colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)) for r, g, b in distinct_27_rgb_colors]

    color_index = 0
    for col in range(9):
        for row in range(3):
            palette[row][col] = hex_colors[color_index]
            color_index += 1
    return palette

strategy_functions = {
    "distinct_hues": distinct_hues_palette,
    "split_complementary": split_complementary_palette,
    "triadic_variations": triadic_variations_palette,
    "analogous_extended": analogous_extended_palette,
    "monochromatic_columns": monochromatic_columns_palette,
    "warm_cool_contrast": warm_cool_contrast_palette,
    "pastel_dark_contrast": pastel_dark_contrast_palette,
    "random_with_harmony": random_with_harmony_palette,
    "complementary": complementary_palette,
    "shades_of_gray": shades_of_gray_palette,
    "tetradic": tetradic_palette,
    "mf_twister": mf_twister_palette
}

def generate_random_palette(strategy):
    """Generate a palette based on the chosen strategy."""
    # Randomize the seed for truly different results each time
    random.seed(datetime.datetime.now().timestamp())

    # Generate row hue shifts
    row_shifts = [0.0]
    row_shifts.append(random.uniform(0.03, 0.08))
    row_shifts.append(random.uniform(0.06, 0.12))

    # Randomize shift direction
    if random.choice([True, False]):
        row_shifts[1] *= -1
        row_shifts[2] *= -1

    if strategy in strategy_functions: # Check if strategy is in our dictionary
        palette_function = strategy_functions[strategy]
        palette = palette_function(row_shifts) # Call the corresponding function
        return palette, strategy
    else:
        # Handle cases where the strategy is not found (e.g., manual_input - although manual_input is handled outside this function now)
        return None, strategy # Or raise an exception if that's more appropriate for your error handling

def generate_unique_filename(strategy_name="pixel_palette", extension=".png"):
    """Generate a unique filename based on strategy and persistent counter (no timestamp)."""
    # timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S") # <-- Comment out or remove timestamp line

    strategy_safe_name = strategy_name.replace("_", "-").lower()
    counter_file = f"{strategy_safe_name}_counter.txt"

    try:
        if os.path.exists(counter_file):
            with open(counter_file, "r") as f:
                try:
                    counter = int(f.read())
                except ValueError:
                    counter = 1
        else:
            counter = 1
    except Exception as e:
        print(f"Error reading counter file for strategy '{strategy_name}': {e}. Resetting counter to 1.")
        counter = 1

    counter_str = str(counter).zfill(3)
    base_name = f"{strategy_safe_name}_palette_{counter_str}"

    try:
        with open(counter_file, "w") as f:
            f.write(str(counter + 1))
    except Exception as e:
        print(f"Error writing to counter file for strategy '{strategy_name}': {e}. Counter persistence may not work for this strategy.")

    # return f"{base_name}_{timestamp}{extension}" # <-- Original line with timestamp
    return f"{base_name}{extension}" # <-- Modified line: Timestamp removed

def get_save_location_choice():
    """Asks the user for the output folder choice."""
    while True:
        choice1 = input("Save to Bitwig Color Palettes folder? (y/n, default: y): ").lower()
        if choice1 in ['y', 'yes', 'n', 'no', '']: # Allow empty input for default 'y'
            if choice1 in ['y', 'yes', '']:
                return "bitwig_palettes" # Save to Bitwig Palettes folder
            else: # choice1 is 'n' or 'no'
                while True:
                    choice2 = input(f"Save to '{GENERATED_PALETTES_SUBFOLDER}' subfolder within Color Palettes? (y/n, default: n): ").lower()
                    if choice2 in ['y', 'yes', 'n', 'no', '']: # Allow empty input for default 'n'
                        if choice2 in ['y', 'yes']:
                            return "generated_palettes_subfolder" # Save to generated_palettes subfolder
                        else:
                            return "script_folder" # Save to script's folder
                    print("Please enter 'y' or 'n'.")
        print("Please enter 'y' or 'n'.")

def get_strategy_choice():
    """Presents a menu with right-justified numbers and aligned 9x3 color grid previews (inline first row)."""
    strategies = get_strategies()
    print("\nChoose a palette generation strategy:")
    max_name_length = get_max_name_length(strategies)
    indentation = max_name_length + 4 # 4 spaces padding after longest name

    for number, strategy_name in strategies.items():
        display_strategy(indentation, number, strategy_name)

    while True:
        choice = input("Enter the number of your choice: ")
        if choice in strategies:
            return strategies[choice]
        else:
            print("Invalid choice. Please enter a number from the menu.")

def display_strategy(indentation, number, strategy_name):
    strategy_out = strategy_name.replace('_', ' ').title()
    prefix = f"{number:>2}. {strategy_out}"
    name_padding = " " * max(0, indentation - len(strategy_out))
    if strategy_name != "manual_input":
        display_generated_strategy(indentation, prefix, name_padding, number, strategy_out, strategy_name)
    else:
        print(f"{number:>2}. {strategy_out}")

def get_max_name_length(strategies):
    max_name_length = 0
    for strategy_name in strategies.values():
        max_name_length = max(max_name_length, len(strategy_name.replace('_', ' ').title()))
    return max_name_length

def get_strategies():
    strategies = {
        "0": "manual_input",
        "1": "distinct_hues",
        "2": "split_complementary",
        "3": "triadic_variations",
        "4": "analogous_extended",
        "5": "monochromatic_columns",
        "6": "warm_cool_contrast",
        "7": "pastel_dark_contrast",
        "8": "random_with_harmony",
        "9": "complementary",
        "10": "shades_of_gray",
        "11": "tetradic",
        "12": "mf_twister"
    }
    return strategies

def display_generated_strategy(indentation, prefix, name_padding, number, strategy_out, strategy_name):
    palette, _ = generate_random_palette(strategy_name)
    if palette:
        grid_lines = []

        for row_index in range(3):
            grid_lines.append(get_grid_row(palette, grid_lines, row_index))

        print(f"{prefix}{name_padding}{grid_lines[0]}")
        indent = len(f"{prefix}{name_padding}")
        for i in range(1, 3):
            make_indent = " " * indent
            print(make_indent + grid_lines[i])

        print("")

    else:  # Fallback for palette generation failure
        print(f"{number:>2}. {strategy_out}")  # Plain text

def get_grid_row(palette, grid_lines, row_index):
    grid_row_line = ""
    for col_index in range(9):
        hex_color = palette[row_index][col_index]
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)
        preview_block_ansi = f"\033[48;2;{r};{g};{b}m  \033[0m"  # 2-char block
        grid_row_line += preview_block_ansi
    return grid_row_line

def create_palette_image(hex_codes, strategy_name): # <--- Added strategy_name parameter
    """Create and save an image from the palette hex codes, with folder choice."""
    # Image dimensions
    image_width = 9
    image_height = 3

    # Create the image
    image = Image.new("RGB", (image_width, image_height))
    pixels = image.load()

    # Set pixel colors
    for row_index, row_codes in enumerate(hex_codes):
        for col_index, hex_code in enumerate(row_codes):
            r = int(hex_code[1:3], 16)
            g = int(hex_code[3:5], 16)
            b = int(hex_code[5:7], 16)
            pixels[col_index, row_index] = (r, g, b) # type: ignore

    # Generate unique filename (now with strategy name)
    filename = generate_unique_filename(strategy_name=strategy_name) # <--- Pass strategy_name

    # Get user's folder choice
    save_location = get_save_location_choice()

    # Determine output folder based on user choice
    base_folder = os.getcwd()
    if save_location == "bitwig_palettes":
        output_folder = BITWIG_PALETTE_DIR
    elif save_location == "generated_palettes_subfolder":
        output_folder = os.path.join(BITWIG_PALETTE_DIR, GENERATED_PALETTES_SUBFOLDER)
    else: # save_location == "script_folder"
        output_folder = base_folder

    os.makedirs(output_folder, exist_ok=True) # Ensure folder exists
    filepath = os.path.join(output_folder, filename)

    # Save the image
    image.save(filepath)

    if save_location == "bitwig_palettes":
        print(f"Pixel palette image saved to Bitwig Color Palettes folder as: {filepath}")
    elif save_location == "generated_palettes_subfolder":
        print(f"Pixel palette image saved to '{GENERATED_PALETTES_SUBFOLDER}' subfolder as: {filepath}")
    else:
        print(f"Pixel palette image saved to script's folder as: {filepath}")


    # Print the palette for reference
    print("\nHex color codes in this palette:")
    for row in hex_codes:
        print(" ".join(row))

    return filename

# Main program
def main():
    print("Welcome to the Color Palette Generator!")
    print("---------------------------------------------")

    generate_another = True

    while generate_another:
        # Get strategy choice from menu
        strategy = get_strategy_choice()

        if strategy != "manual_input": # If not manual input, generate random
            # Generate random palette with the chosen strategy
            hex_codes, strategy = generate_random_palette(strategy)
            print(f"Palette generated using strategy: {strategy.replace('_', ' ').title()}") # Nicer display
        else: # Manual input selected
            # Initialize empty hex_codes list with the same structure
            hex_codes = [
                ["" for _ in range(9)],
                ["" for _ in range(9)],
                ["" for _ in range(9)]
            ]

            print("Please enter 27 colors in hex format (#RRGGBB)")
            print("---------------------------------------------")

            # Get all colors from user input
            for row in range(3):
                for col in range(9):
                    hex_codes[row][col] = get_color_input(row, col)

        # Create and save the palette image
        create_palette_image(hex_codes, strategy)

        # Ask if user wants to generate another palette
        while True:
            another_input = input("\nWould you like to generate another palette? (y/n, default: y): ").lower() # Modified prompt to show default
            if another_input == '': # Check for empty input
                another = 'y' # Default to 'yes'
                break
            elif another_input in ['y', 'yes', 'n', 'no']:
                another = another_input # Use user's input
                break
            print("Please enter 'y' or 'n'.")

        generate_another = another in ['y', 'yes']

    print("Thank you for using the Color Palette Generator!")

if __name__ == "__main__":
    main()
