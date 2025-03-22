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

MF_TWISTER_ALL_COLORS = "mf_twister_all_colors.json" # Filename of JSON file
distinct_all_colors = []

try:
    with open(MF_TWISTER_ALL_COLORS, 'r') as f:
        distinct_all_colors = json.load(f)
except FileNotFoundError:
    print(f"Warning: {MF_TWISTER_ALL_COLORS} not found. 'mf_twister' strategy will use default colors or might not work.")
except json.JSONDecodeError:
    print(f"Error decoding JSON from {MF_TWISTER_ALL_COLORS}. File might be corrupted.")
except Exception as e:
    print(f"Error loading colors from {MF_TWISTER_ALL_COLORS}: {e}")


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


def get_hue_shifts_input(num_rows):
    """Asks user if they want to shift hues per row and gets shift values in degrees."""
    hue_shifts_degrees = [0] * num_rows # Default no shift
    while True:
        shift_choice = input("Do you want to apply hue shifts to each row? (y/n, default: n): ").lower()
        if shift_choice in ['y', 'yes']:
            for i in range(num_rows):
                while True:
                    shift_input = input(f"Enter hue shift for row {i+1} in degrees (0-360, default: 0): ")
                    if shift_input == '':
                        shift_degrees = 0
                        break # Default to 0
                    try:
                        shift_degrees = int(shift_input)
                        if 0 <= shift_degrees <= 360:
                            break
                        else:
                            print("Hue shift must be between 0 and 360 degrees.")
                    except ValueError:
                        print("Invalid input. Please enter a number.")
                hue_shifts_degrees[i] = shift_degrees
            return [shift / 360.0 for shift in hue_shifts_degrees] # Convert to hue (0-1 range)
        elif shift_choice in ['n', 'no', '']:
            return [0] * num_rows # No hue shift
        else:
            print("Please enter 'y' or 'n'.")


def create_empty_palette(grid_rows, grid_cols) -> List[List[str]]:
    """Creates and returns an empty 3x9 or 4x16 palette (list of lists)."""
    return [
        ["" for _ in range(grid_cols)] for _ in range(grid_rows)
    ]


def distinct_hues_palette(grid_rows, grid_cols, row_shifts, hue_shifts, color_bias=None):
    """Generate palette using distinct hues strategy."""
    palette = create_empty_palette(grid_rows, grid_cols)
    # distinct hues with lightness variations by row
    base_hues = [(i / grid_cols + random.random() * 0.03) % 1.0 for i in range(grid_cols)] # Adjusted for grid_cols
    random.shuffle(base_hues)  # Shuffle for unpredictability
    for col in range(grid_cols):
        base_hue = base_hues[col]
        for row in range(grid_rows):
            # Apply row-specific hue shift and user hue shift
            shifted_hue = (base_hue + row_shifts[row] + hue_shifts[row]) % 1.0
            # Vary saturation and value by row
            saturation = 0.3 + row * (0.6 / grid_rows) + random.random() * 0.15 # Adjusted saturation range and row scaling
            value = 0.9 - row * (0.5 / grid_rows) + random.random() * 0.1 # Adjusted value range and row scaling
            palette[row][col] = hsv_to_hex(shifted_hue, saturation, value)
    return palette


def split_complementary_palette(grid_rows, grid_cols, row_shifts, hue_shifts, color_bias=None):
    """Generate palette using split complementary strategy."""
    palette = create_empty_palette(grid_rows, grid_cols)
    base_hue = random.random()
    complement1 = (base_hue + 0.5 - 0.05) % 1.0
    complement2 = (base_hue + 0.5 + 0.05) % 1.0
    hues = [base_hue] * (grid_cols // 4 + 2) + [ # Increased base hue count, adjusted for grid_cols
        (base_hue + 0.02) % 1.0,
        (base_hue - 0.02) % 1.0,
        complement1,
        (complement1 + 0.03) % 1.0,
        complement2,
        (complement2 - 0.03) % 1.0,
        (complement1 - 0.03) % 1.0, # Added more variations to fill grid_cols
        (complement2 + 0.03) % 1.0,
        base_hue, # Re-add base hue for more cols
        complement1, # Re-add complements
        complement2
    ]
    while len(hues) < grid_cols: # Ensure enough hues for grid_cols
        hues.extend(hues[:])
    hues = hues[:grid_cols]
    random.shuffle(hues)
    for col in range(grid_cols):
        for row in range(grid_rows):
            # Apply row-specific hue shift and user hue shift
            shifted_hue = (hues[col % len(hues)] + row_shifts[row] + hue_shifts[row]) % 1.0 # Use modulo for hue selection

            saturation = 0.4 + row * (0.5 / grid_rows) + random.random() * 0.1 # Adjusted saturation range and row scaling
            value = 0.9 - row * (0.5 / grid_rows) + random.random() * 0.1 # Adjusted value range and row scaling
            palette[row][col] = hsv_to_hex(shifted_hue, saturation, value)
    return palette


def triadic_variations_palette(grid_rows, grid_cols, row_shifts, hue_shifts, color_bias=None):
    """Generate palette using triadic variations strategy."""
    palette = create_empty_palette(grid_rows, grid_cols)
    hue1 = random.random()
    hue2 = (hue1 + 0.33) % 1.0
    hue3 = (hue1 + 0.66) % 1.0

    # Create variations of each hue, more variations for grid_cols
    hue_variations = []
    for hue in [hue1, hue2, hue3]:
        hue_variations.extend([
            hue,
            (hue + 0.02) % 1.0,
            (hue - 0.02) % 1.0,
            (hue + 0.04) % 1.0, # Added more variations
            (hue - 0.04) % 1.0
        ])
    while len(hue_variations) < grid_cols: # Ensure enough hues for grid_cols
        hue_variations.extend(hue_variations[:]) # Duplicate to fill if needed
    hue_variations = hue_variations[:grid_cols] # Trim to grid_cols

    random.shuffle(hue_variations)

    for col in range(grid_cols):
        for row in range(grid_rows):
            # Apply row-specific hue shift and user hue shift
            shifted_hue = (hue_variations[col] + row_shifts[row] + hue_shifts[row]) % 1.0

            # Vary saturation and value differently for each row
            saturation = 0.4 + row * (0.5 / grid_rows) + random.random() * 0.2 # Adjusted saturation range and row scaling
            value = 0.9 - row * (0.5 / grid_rows) + random.random() * 0.1 # Adjusted value range and row scaling
            palette[row][col] = hsv_to_hex(shifted_hue, saturation, value)
    return palette


def analogous_extended_palette(grid_rows, grid_cols, row_shifts, hue_shifts, color_bias=None):
    """Generate palette using analogous extended strategy."""
    palette = create_empty_palette(grid_rows, grid_cols)
    start_hue = random.random()
    hue_range = 0.4  # Slightly wider range for grid_cols columns

    for col in range(grid_cols):
        hue_offset = (col / grid_cols) * hue_range
        base_hue = (start_hue + hue_offset) % 1.0

        # Vary saturation and value for each row
        for row in range(grid_rows):
            # Apply row-specific hue shift and user hue shift
            shifted_hue = (base_hue + row_shifts[row] + hue_shifts[row]) % 1.0

            saturation = 0.5 + row * (0.4 / grid_rows) + random.random() * 0.2 # Adjusted saturation range and row scaling
            value = 0.9 - row * (0.5 / grid_rows) + random.random() * 0.1 # Adjusted value range and row scaling
            palette[row][col] = hsv_to_hex(shifted_hue, saturation, value)
    return palette


def monochromatic_columns_palette(grid_rows, grid_cols, row_shifts, hue_shifts, color_bias=None):
    """Generate palette using monochromatic columns strategy."""
    palette = create_empty_palette(grid_rows, grid_cols)
    for col in range(grid_cols):
        base_hue = random.random()

        # Create shades in the column with hue shifts
        for row in range(grid_rows):
            # Apply row-specific hue shift and user hue shift
            shifted_hue = (base_hue + row_shifts[row] + hue_shifts[row]) % 1.0

            saturation = 0.3 + row * (0.6 / grid_rows) + random.random() * 0.1 # Adjusted saturation range and row scaling
            value = 0.95 - row * (0.6 / grid_rows) + random.random() * 0.1 # Adjusted value range and row scaling
            palette[row][col] = hsv_to_hex(shifted_hue, saturation, value)
    return palette


def warm_cool_contrast_palette(grid_rows, grid_cols, row_shifts, hue_shifts, color_bias=None):
    """Generate palette using warm cool contrast strategy."""
    palette = create_empty_palette(grid_rows, grid_cols)
    warm_hues = [random.uniform(0.95, 0.15) for _ in range(grid_cols // 2 + 1)]  # Increased warm hues, adjusted for grid_cols
    cool_hues = [random.uniform(0.4, 0.7) for _ in range(grid_cols - (grid_cols // 2 + 1))]    # Increased cool hues, adjusted for grid_cols

    all_hues = warm_hues + cool_hues
    random.shuffle(all_hues)

    for col in range(grid_cols):
        base_hue = all_hues[col]

        # Create variations by row with hue shifts
        for row in range(grid_rows):
            # Apply row-specific hue shift and user hue shift
            shifted_hue = (base_hue + row_shifts[row] + hue_shifts[row]) % 1.0

            saturation = 0.5 + row * (0.4 / grid_rows) + random.random() * 0.1 # Adjusted saturation range and row scaling
            value = 0.9 - row * (0.5 / grid_rows) + random.random() * 0.1 # Adjusted value range and row scaling
            palette[row][col] = hsv_to_hex(shifted_hue, saturation, value)
    return palette


def pastel_dark_contrast_palette(grid_rows, grid_cols, row_shifts, hue_shifts, color_bias=None):
    """Generate palette using pastel dark contrast strategy."""
    palette = create_empty_palette(grid_rows, grid_cols)
    hues = [random.random() for _ in range(grid_cols)]

    for col in range(grid_cols):
        for row in range(grid_rows):
            # Apply row-specific hue shift and user hue shift
            shifted_hue = (hues[col] + row_shifts[row] + hue_shifts[row]) % 1.0

            if row <= grid_rows // 2 -1 : # First half rows pastel
                # Pastels (high value, low saturation)
                saturation = 0.2 + random.random() * 0.2
                value = 0.9 + random.random() * 0.1
            else: # Last half rows deep/dark
                # Deep/dark (high saturation, low value)
                saturation = 0.7 + random.random() * 0.2
                value = 0.4 + random.random() * 0.2

            palette[row][col] = hsv_to_hex(shifted_hue, saturation, value)
    return palette


def random_with_harmony_palette(grid_rows, grid_cols, row_shifts, hue_shifts, color_bias=None):
    """Generate palette using random with harmony strategy."""
    palette = create_empty_palette(grid_rows, grid_cols)
    for col in range(grid_cols):
        # Pick a random hue for each column
        base_hue = random.random()

        for row in range(grid_rows):
            # Apply row-specific hue shift and user hue shift
            shifted_hue = (base_hue + row_shifts[row] + hue_shifts[row]) % 1.0

            # Pattern for saturation and value across rows
            if row == 0: # Top row: lighter
                saturation = random.uniform(0.2, 0.5)
                value = random.uniform(0.85, 1.0)
            elif row == 1: # Second row: medium light
                saturation = random.uniform(0.4, 0.7)
                value = random.uniform(0.7, 0.9)
            elif grid_rows >= 3 and row == 2: # Third row: medium dark
                saturation = random.uniform(0.6, 0.9)
                value = random.uniform(0.55, 0.75)
            elif grid_rows >= 4 and row == 3: # Bottom row: deeper
                saturation = random.uniform(0.8, 1.0)
                value = random.uniform(0.4, 0.6)
            else: # For more rows, fall back to medium
                saturation = random.uniform(0.5, 0.8)
                value = random.uniform(0.6, 0.8)
            palette[row][col] = hsv_to_hex(shifted_hue, saturation, value)
    return palette


def complementary_palette(grid_rows, grid_cols, row_shifts, hue_shifts, color_bias=None):
    """Generate palette using complementary strategy."""
    palette = create_empty_palette(grid_rows, grid_cols)
    base_hue = random.random()
    complement_hue = (base_hue + 0.5) % 1.0
    hues = [base_hue] * (grid_cols // 2) + [complement_hue] * (grid_cols - (grid_cols // 2)) # Equal number of base and complement, adjusted for grid_cols
    random.shuffle(hues)

    for col in range(grid_cols):
        base_hue = hues[col]
        for row in range(grid_rows):
            shifted_hue = (base_hue + row_shifts[row] + hue_shifts[row]) % 1.0
            saturation = 0.4 + row * (0.5 / grid_rows) + random.random() * 0.1 # Adjusted saturation range and row scaling
            value = 0.85 - row * (0.5 / grid_rows) + random.random() * 0.1 # Adjusted value range and row scaling
            palette[row][col] = hsv_to_hex(shifted_hue, saturation, value)
    return palette


def shades_of_gray_palette(grid_rows, grid_cols, row_shifts, hue_shifts, color_bias=None):
    """Generate palette using shades of gray strategy."""
    palette = create_empty_palette(grid_rows, grid_cols)
    base_hue = random.uniform(0, 1) # slight tint
    for col in range(grid_cols):
        for row in range(grid_rows):
            shifted_hue = (base_hue + row_shifts[row] * 0.5 + hue_shifts[row]) % 1.0 # Less hue shift
            saturation = 0.03 + random.random() * 0.03 # Very low saturation
            value = 0.15 + (col / grid_cols) * 0.7 + (row / grid_rows) * 0.15 # Adjusted value range for rows and grid_cols
            palette[row][col] = hsv_to_hex(shifted_hue, saturation, value)
    return palette


def tetradic_palette(grid_rows, grid_cols, row_shifts, hue_shifts, color_bias=None):
    """Generate palette using tetradic strategy."""
    palette = create_empty_palette(grid_rows, grid_cols)
    base_hue = random.random()
    hue2 = (base_hue + 0.25) % 1.0 # Adjusted for tetradic (90 degrees)
    hue3 = (base_hue + 0.5) % 1.0
    hue4 = (base_hue + 0.75) % 1.0
    hues = [base_hue] * (grid_cols // 4 + 1) + [hue2] * (grid_cols // 4) + [hue3] * (grid_cols // 4) + [hue4] * (grid_cols - 3*(grid_cols // 4 + 1)) # Four of each hue, adjusted for grid_cols
    while len(hues) < grid_cols: # Ensure enough hues for grid_cols
        hues.extend(hues[:])
    hues = hues[:grid_cols]
    random.shuffle(hues)

    for col in range(grid_cols):
        base_hue = hues[col]
        for row in range(grid_rows):
            shifted_hue = (base_hue + row_shifts[row] + hue_shifts[row]) % 1.0
            saturation = 0.4 + row * (0.5 / grid_rows) + random.random() * 0.1 # Adjusted saturation range and row scaling
            value = 0.85 - row * (0.5 / grid_rows) + random.random() * 0.1 # Adjusted value range and row scaling
            palette[row][col] = hsv_to_hex(shifted_hue, saturation, value)
    return palette


def rainbow_desaturated_rows_palette(grid_rows, grid_cols, row_shifts, hue_shifts, color_bias=None):
    """Generate palette using rainbow desaturated rows strategy."""
    palette = create_empty_palette(grid_rows, grid_cols)
    for col in range(grid_cols):
        hue = col / float(grid_cols) # Hue from 0 to 1 across columns (rainbow)
        for row in range(grid_rows):
            # Decrease saturation with each row
            saturation = 1.0 - (row * (0.6 / grid_rows)) # Saturation from 1.0 to lower value (adjust as needed)
            value = 0.9 # Constant value (brightness)
            shifted_hue = (hue + hue_shifts[row]) % 1.0 # Apply user hue shift
            palette[row][col] = hsv_to_hex(shifted_hue, saturation, value)
    return palette


def mf_twister_palette(grid_rows, grid_cols, row_shifts: List[float], hue_shifts, color_bias=None) -> List[List[str]]:
    """Generate palette using pre-selected 27 or 64 maximally distinct colors from JSON file,
       with optional color bias (None, 'red', 'green', 'blue')."""
    palette = create_empty_palette(grid_rows, grid_cols)
    global distinct_all_colors
    source_colors = distinct_all_colors
    json_file_label = "all"

    if not source_colors:
        print(f"Error: distinct RGB colors not loaded correctly for 'mf_twister' strategy ({json_file_label} colors). Check '{MF_TWISTER_ALL_COLORS}'.")
        return palette # Return empty palette if colors not loaded

    if color_bias:
        biased_colors_rgb = get_biased_color_selection(source_colors, grid_rows * grid_cols, color_bias)
        hex_colors = [hsv_to_hex(*colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)) for r, g, b in biased_colors_rgb]
    else: # No bias, random selection
        hex_colors = random.sample([hsv_to_hex(*colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)) for r, g, b in source_colors], grid_rows * grid_cols) # Random sample without replacement, use grid_rows * grid_cols

    color_index = 0
    for col in range(grid_cols):
        for row in range(grid_rows):
            palette[row][col] = hex_colors[color_index]
            color_index += 1
    return palette


def get_biased_color_selection(source_colors_rgb, num_colors_needed, bias_amounts):
     """Selects colors with numerical bias towards red, green, or blue using weighted random choice."""
     biased_colors_rgb = []
     weights = []

     bias_r = bias_amounts.get('red', 1.0)   # Safely get bias amounts, default to 1.0 if not provided
     bias_g = bias_amounts.get('green', 1.0)
     bias_b = bias_amounts.get('blue', 1.0)

     for r, g, b in source_colors_rgb:
         # Calculate weight based on numerical bias amounts
         weight = (r * bias_r) + (g * bias_g) + (b * bias_b) # Simple weighting formula

         weights.append(weight)

     # Normalize weights to create probabilities
     total_weight = sum(weights)
     if total_weight == 0: # Avoid division by zero if all weights are zero (unlikely, but for robustness)
         probabilities = [1.0 / len(weights)] * len(weights) # Uniform probabilities if total weight is zero
     else:
         probabilities = [w / total_weight for w in weights]

     # Select colors based on probabilities
     choices = random.choices(source_colors_rgb, weights=probabilities, k=num_colors_needed)
     biased_colors_rgb.extend(choices)
     return biased_colors_rgb


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
    "rainbow_desaturated_rows": rainbow_desaturated_rows_palette,
    "mf_twister": mf_twister_palette
}


def generate_random_palette(grid_rows, grid_cols, strategy, hue_shifts, color_bias=None):
    """Generate a palette based on the chosen strategy."""
    # Randomize the seed for truly different results each time
    random.seed(datetime.datetime.now().timestamp())

    # Generate row hue shifts (each row has a slight hue shift)
    row_shifts = [0.0]  # First row has no shift
    if grid_rows >= 2:
        row_shifts.append(random.uniform(0.02, 0.06))  # Second row shifts slightly (reduced shift)
    if grid_rows >= 3:
        row_shifts.append(random.uniform(0.04, 0.10))  # Third row shifts more (adjusted range)
    if grid_rows >= 4:
        row_shifts.append(random.uniform(0.06, 0.14))  # Fourth row shifts even more (new row)
    while len(row_shifts) < grid_rows:  # Pad with 0s if more rows than default shifts
        row_shifts.append(0)
    row_shifts = row_shifts[:grid_rows]  # Truncate if less rows than default shifts

    # Randomize shift direction
    if random.choice([True, False]):
        for i in range(1, grid_rows):  # Apply to all shift rows
            row_shifts[i] *= -1

    if strategy in strategy_functions:  # Check if strategy is in our dictionary
        palette_function = strategy_functions[strategy]
        palette = palette_function(grid_rows, grid_cols, row_shifts, hue_shifts, color_bias=color_bias)
        return palette, strategy
    else:
        # Handle cases where the strategy is not found (e.g., manual_input - although manual_input is handled outside this function now)
        return None, strategy  # Or raise an exception if that's more appropriate for your error handling


def get_color_bias_input():
    """Asks the user for numerical color bias amounts for R, G, B (default 1.0 for no bias)."""
    bias_amounts = {} # Use a dictionary to store bias amounts

    print("\nEnter numerical bias amounts for Red, Green, Blue (default 1.0 for no bias):")

    while True: # Loop for Red bias input
        r_bias_input = input("  Red bias amount (default 1.0): ").strip() # Add .strip() to remove whitespace
        if r_bias_input == '':
            bias_amounts['red'] = 1.0 # Default for Red
            break
        try:
            bias_amounts['red'] = float(r_bias_input)
            break
        except ValueError:
            print("Invalid input. Please enter a valid number for Red bias (e.g., 1, 1.0, 1.5).") # More informative message

    while True: # Loop for Green bias input
        g_bias_input = input("  Green bias amount (default 1.0): ").strip() # Add .strip()
        if g_bias_input == '':
            bias_amounts['green'] = 1.0 # Default for Green
            break
        try:
            bias_amounts['green'] = float(g_bias_input)
            break
        except ValueError:
            print("Invalid input. Please enter a valid number for Green bias (e.g., 1, 1.0, 1.5).") # More informative message

    while True: # Loop for Blue bias input
        b_bias_input = input("  Blue bias amount (default 1.0): ").strip() # Add .strip()
        if b_bias_input == '':
            bias_amounts['blue'] = 1.0 # Default for Blue
            break
        try:
            bias_amounts['blue'] = float(b_bias_input)
            break
        except ValueError:
            print("Invalid input. Please enter a valid number for Blue bias (e.g., 1, 1.0, 1.5).") # More informative message

    return bias_amounts # Return the dictionary of bias amounts


def preview_mf_twister_palette(hex_codes, strategy, grid_rows, grid_cols, color_bias):
    """Displays a preview of the generated MF Twister palette with bias."""
    strategy_out = prettify_name(strategy)
    if color_bias:
        bias_text = f" (Bias: {color_bias.title()})" # e.g., " (Bias: Red)"
    else:
        bias_text = " (No Bias)"

    print(f"\nPreview of MF Twister Palette: {strategy_out}{bias_text} - {grid_cols}x{grid_rows} grid:")
    # Print the palette for preview with color blocks (similar to create_palette_image's print)
    for row in hex_codes:
        for hex_code in row:
            r = int(hex_code[1:3], 16)
            g = int(hex_code[3:5], 16)
            b = int(hex_code[5:7], 16)
            color_preview = f"\033[48;2;{r};{g};{b}m  \033[0m" # ANSI color block
            print(f"{color_preview} {hex_code}", end=" ")
        print() # New line for each row
    print() # Add extra blank line after preview


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


def get_strategy_choice(grid_cols, grid_rows, hue_shifts):
    """Presents a menu ... (unchanged - just removed the preview palette generation to avoid side-effects during menu creation)."""
    strategies = get_strategies()
    random_strategies = get_random_strategies()

    print("\nChoose a palette generation strategy:")
    max_name_length = get_max_name_length(strategies)
    indentation = max_name_length + 4

    for number, strategy_name in strategies.items():
        display_strategy(grid_cols, grid_rows, indentation, number, strategy_name, hue_shifts)

    while True:
        choice = input("Enter the number of your choice: ")
        if choice in strategies:
            chosen_strategy_key = strategies[choice]
            if chosen_strategy_key == "manual_input":
                while True:
                    manual_random_choice = input("Choose 'm' for Manual Input or 'r' for Random Algorithm: ").lower()
                    if manual_random_choice == 'm':
                        return "manual_input"
                    elif manual_random_choice == 'r':
                        return random.choice(random_strategies)
                    else:
                        print("Invalid choice. Please enter 'm' or 'r'.")
            else:
                return chosen_strategy_key
        else:
            print("Invalid choice. Please enter a number from the menu.")


def display_strategy(grid_cols, grid_rows, indentation, number, strategy_name, hue_shifts, hex_codes=None):
    strategy_out = prettify_name(strategy_name)
    prefix = f"{number:>2}. {strategy_out}"
    name_padding = " " * max(0, indentation - len(strategy_out))
    if strategy_name != "manual_input":
        display_generated_strategy(grid_cols, grid_rows, prefix, name_padding, number, strategy_out,
            strategy_name, hue_shifts, hex_codes=hex_codes)
    else:
        print(f"\n{number:>2}. {strategy_out}\n")


def prettify_name(name):
    name = name.replace('_', ' ').title()
    name = name.replace("Mf ", "MF ")
    return name


def get_max_name_length(strategies):
    max_name_length = 0
    for strategy_name in strategies.values():
        max_name_length = max(max_name_length, len(prettify_name(strategy_name)))
    return max_name_length


def get_strategies():
    strategies = {
        "0": "manual_input", # "0": "manual_input_or_random", # combined manual and random
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
        "12": "rainbow_desaturated_rows",
        "13": "mf_twister"
    }
    return strategies


def get_random_strategies() -> List[str]:
    strategies = [
        "distinct_hues",
        "split_complementary",
        "triadic_variations",
        "analogous_extended",
        "monochromatic_columns",
        "warm_cool_contrast",
        "pastel_dark_contrast",
        "random_with_harmony",
        "complementary",
        "shades_of_gray",
        "tetradic",
        "rainbow_desaturated_rows",
        "mf_twister"
    ]
    return strategies


def display_generated_strategy(grid_cols, grid_rows, prefix, name_padding, number,
        strategy_out, strategy_name, hue_shifts, hex_codes=None):
    if hex_codes:
        palette = hex_codes
    else:
        palette, _ = generate_random_palette(grid_rows, grid_cols, strategy_name, hue_shifts)
    if palette:
        grid_lines = []

        for row_index in range(grid_rows):
            grid_lines.append(get_grid_row(palette, grid_lines, row_index, grid_cols))

        print(f"{prefix}{name_padding}{grid_lines[0]}")
        indent = len(f"{prefix}{name_padding}")
        for i in range(1, grid_rows):
            make_indent = " " * indent
            print(make_indent + grid_lines[i])

        print("")
    else:  # Fallback for palette generation failure
        print(f"{number:>2}. {strategy_out}")  # Plain text


def get_grid_row(palette, grid_lines, row_index, grid_cols):
    grid_row_line = ""
    for col_index in range(grid_cols):
        hex_color = palette[row_index][col_index]
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)
        preview_block_ansi = f"\033[48;2;{r};{g};{b}m  \033[0m"  # 2-char block
        grid_row_line += preview_block_ansi
    return grid_row_line


def get_grid_size_choice():
    """Asks the user to choose the grid size."""
    while True:
        grid_choice = input("Choose grid size: '1' for 16x4 or '2' for 9x3 (default: 1): ")
        if grid_choice in ['1', '']:
            return 16, 4 # 16x4 grid
        elif grid_choice == '2':
            return 9, 3 # 9x3 grid
        else:
            print("Invalid choice. Please enter '1' or '2'.")


def create_palette_image(hex_codes, strategy, grid_rows, grid_cols):
    """Create and save an image from the palette hex codes, with folder choice and strategy for filename."""
    # Image dimensions
    image_width = grid_cols
    image_height = grid_rows

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
    # filename = generate_unique_filename(strategy, grid_rows, grid_cols)
    filename = generate_unique_filename(strategy)

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

    # Print the palette for reference with color preview
    print("\nHex color codes in this palette:")
    for row in hex_codes:
        for hex_code in row:
            r = int(hex_code[1:3], 16)
            g = int(hex_code[3:5], 16)
            b = int(hex_code[5:7], 16)
            color_preview = f"\033[48;2;{r};{g};{b}m  \033[0m" # ANSI color block
            print(f"{color_preview} {hex_code}", end=" ") # Print preview and hex code
        print() # New line for each row

    return filename


# Main program
def main():
    print("\nWelcome to the Color Palette Generator!")
    print("---------------------------------------")

    generate_another = True

    while generate_another:
        # Get grid size choice
        grid_cols, grid_rows = get_grid_size_choice()
        grid_size_text = f"{grid_cols}x{grid_rows}"
        print(f"Generating {grid_size_text} palette.")

        # Get strategy choice from menu
        hex_codes = []
        hue_shifts = [0] * grid_rows  # Initialize hue_shifts here
        strategy = get_strategy_choice(grid_cols, grid_rows, hue_shifts)

        color_bias_choice = None  # Initialize color_bias_choice

        match strategy: # Use match-case statement for strategy dispatch
            case "mf_twister": # MF Twister interactive preview loop
                strategies = get_strategies()
                max_name_length = get_max_name_length(strategies)
                indentation = max_name_length + 4
                bias_preview_loop = True
                while bias_preview_loop:
                    color_bias_choice = get_color_bias_input()
                    hex_codes, strategy = generate_random_palette(grid_rows, grid_cols, strategy,
                        hue_shifts, color_bias_choice)
                    display_strategy(grid_cols, grid_rows, indentation, 13, "mf_twister", hue_shifts, hex_codes=hex_codes)

                    while True: # Bias preview menu loop
                        preview_action = input("Choose option: 'a' - Accept Palette, 's' - See Another Preview, 'b' - Choose Different Bias: ").lower()
                        if preview_action == 'a':
                            bias_preview_loop = False
                            break
                        elif preview_action == 's':
                            break
                        elif preview_action == 'b':
                            bias_preview_loop = True
                            break
                        else:
                            print("Invalid choice. Please enter 'a', 's', or 'b'.")

            case "manual_input": # Manual input selected
                # Initialize empty hex_codes list with the grid size
                hex_codes = [
                    ["" for _ in range(grid_cols)] for _ in range(grid_rows)
                ]
                print(f"Please enter {grid_rows * grid_cols} colors in hex format (#RRGGBB)")
                print("---------------------------------------------")
                # Get all colors from user input
                for row in range(grid_rows): # Updated loop range
                    for col in range(grid_cols): # Updated loop range
                        hex_codes[row][col] = get_color_input(row, col)

            case "random_algorithm": # Random Algorithm selected
                hex_codes = [
                    ["" for _ in range(grid_cols)] for _ in range(grid_rows)
                ]  # Initialize empty hex_codes for random
                print("Random Algorithm")
                hex_codes, strategy = generate_random_palette(grid_rows, grid_cols, random.choice(get_random_strategies()), hue_shifts)
                print(f"Palette generated using strategy: {prettify_name(strategy)}")

            case _: # Default case for all other strategies
                hex_codes, strategy = generate_random_palette(grid_rows, grid_cols, strategy, hue_shifts, color_bias_choice)
                print(f"Palette generated using strategy: {prettify_name(strategy)}")


        # Create and save the palette image
        create_palette_image(hex_codes, strategy, grid_rows, grid_cols)

        # Ask if user wants to generate another palette
        while True:
            another_input = input("\nWould you like to generate another palette? (y/n, default: y): ").lower()  # Modified prompt to show default
            if another_input == '':  # Check for empty input
                another = 'y'
            elif another_input in ['y', 'yes', 'n', 'no']:
                another = another_input  # Use user's input
                break
            else:
                print("Please enter 'y' or 'n'.")

        generate_another = another in ['y', 'yes']

    print("Thank you for using the Color Palette Generator!")


if __name__ == "__main__":
    main()
