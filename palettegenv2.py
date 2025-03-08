
# --- START OF FILE Bitwig Color Palette Generator.py ---
from PIL import Image
import random
import os
import datetime
import colorsys

# Dynamically determine the user's Documents directory and Bitwig path
USER_DOCUMENTS = os.path.expanduser("~/Documents")
BITWIG_PALETTE_DIR = os.path.join(USER_DOCUMENTS, "Bitwig Studio", "Color Palettes")
GENERATED_PALETTES_SUBFOLDER = "generated_palettes" # Define subfolder name

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

def generate_random_palette(strategy):
    """Generate a palette based on the chosen strategy."""
    palette = [
        ["" for _ in range(9)],
        ["" for _ in range(9)],
        ["" for _ in range(9)]
    ]

    # Randomize the seed for truly different results each time
    random.seed(datetime.datetime.now().timestamp())

    # Generate row hue shifts (each row has a slight hue shift)
    row_shifts = [0]  # First row has no shift
    row_shifts.append(random.uniform(0.03, 0.08))  # Second row shifts slightly
    row_shifts.append(random.uniform(0.06, 0.12))  # Third row shifts more

    # Randomize shift direction
    if random.choice([True, False]):
        row_shifts[1] *= -1
        row_shifts[2] *= -1

    if strategy == "distinct_hues":
        # 9 distinct hues with lightness variations by row
        base_hues = [(i / 9 + random.random() * 0.05) % 1.0 for i in range(9)]
        random.shuffle(base_hues)  # Shuffle for unpredictability

        for col in range(9):
            base_hue = base_hues[col]
            for row in range(3):
                # Apply row-specific hue shift
                shifted_hue = (base_hue + row_shifts[row]) % 1.0

                # Vary saturation and value by row
                saturation = 0.3 + row * 0.25 + random.random() * 0.1
                value = 0.9 - row * 0.15 + random.random() * 0.1

                palette[row][col] = hsv_to_hex(shifted_hue, saturation, value)

    elif strategy == "split_complementary":
        # Base hue with its split complements
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
                # Apply row-specific hue shift
                shifted_hue = (hues[col] + row_shifts[row]) % 1.0

                saturation = 0.4 + row * 0.2 + random.random() * 0.1
                value = 0.9 - row * 0.15 + random.random() * 0.1
                palette[row][col] = hsv_to_hex(shifted_hue, saturation, value)

    elif strategy == "triadic_variations":
        # Three main hues with variations
        hue1 = random.random()
        hue2 = (hue1 + 0.33) % 1.0
        hue3 = (hue1 + 0.66) % 1.0

        # Create variations of each hue
        hue_variations = []
        for hue in [hue1, hue2, hue3]:
            hue_variations.extend([
                hue,
                (hue + 0.03) % 1.0,
                (hue - 0.03) % 1.0
            ])

        random.shuffle(hue_variations)

        for col in range(9):
            for row in range(3):
                # Apply row-specific hue shift
                shifted_hue = (hue_variations[col] + row_shifts[row]) % 1.0

                # Vary saturation and value differently for each row
                saturation = 0.4 + row * 0.2 + random.random() * 0.2
                value = 0.9 - row * 0.2 + random.random() * 0.1
                palette[row][col] = hsv_to_hex(shifted_hue, saturation, value)

    elif strategy == "analogous_extended":
        # Extended analogous palette (colors near each other on wheel)
        start_hue = random.random()
        hue_range = 0.3  # Cover about 1/3 of the color wheel

        for col in range(9):
            hue_offset = (col / 9) * hue_range
            base_hue = (start_hue + hue_offset) % 1.0

            # Vary saturation and value for each row
            for row in range(3):
                # Apply row-specific hue shift
                shifted_hue = (base_hue + row_shifts[row]) % 1.0

                saturation = 0.5 + row * 0.15 + random.random() * 0.2
                value = 0.9 - row * 0.15 + random.random() * 0.1
                palette[row][col] = hsv_to_hex(shifted_hue, saturation, value)

    elif strategy == "monochromatic_columns":
        # Each column is monochromatic, but different hues across columns
        for col in range(9):
            base_hue = random.random()

            # Create three shades in the column with hue shifts
            for row in range(3):
                # Apply row-specific hue shift
                shifted_hue = (base_hue + row_shifts[row]) % 1.0

                saturation = 0.4 + row * 0.15 + random.random() * 0.1
                value = 0.9 - row * 0.2 + random.random() * 0.1
                palette[row][col] = hsv_to_hex(shifted_hue, saturation, value)

    elif strategy == "warm_cool_contrast":
        # Mix of warm (reds, oranges, yellows) and cool colors (blues, greens, purples)
        warm_hues = [random.uniform(0.95, 0.15) for _ in range(5)]  # Red to Yellow
        cool_hues = [random.uniform(0.4, 0.7) for _ in range(4)]    # Green to Purple

        all_hues = warm_hues + cool_hues
        random.shuffle(all_hues)

        for col in range(9):
            base_hue = all_hues[col]

            # Create variations by row with hue shifts
            for row in range(3):
                # Apply row-specific hue shift
                shifted_hue = (base_hue + row_shifts[row]) % 1.0

                saturation = 0.6 + row * 0.1 + random.random() * 0.1
                value = 0.9 - row * 0.2 + random.random() * 0.1
                palette[row][col] = hsv_to_hex(shifted_hue, saturation, value)

    elif strategy == "pastel_dark_contrast":
        # First row: pastels, Second: medium, Third: deep/dark
        hues = [random.random() for _ in range(9)]

        for col in range(9):
            for row in range(3):
                # Apply row-specific hue shift
                shifted_hue = (hues[col] + row_shifts[row]) % 1.0

                if row == 0:
                    # Pastels (high value, low saturation)
                    saturation = 0.3 + random.random() * 0.2
                    value = 0.9 + random.random() * 0.1
                elif row == 1:
                    # Medium
                    saturation = 0.6 + random.random() * 0.2
                    value = 0.7 + random.random() * 0.1
                else:
                    # Deep/dark (high saturation, low value)
                    saturation = 0.8 + random.random() * 0.2
                    value = 0.4 + random.random() * 0.2

                palette[row][col] = hsv_to_hex(shifted_hue, saturation, value)

    elif strategy == "random_with_harmony":
        # Completely random but with some harmony principles
        for col in range(9):
            # Pick a random hue for each column
            base_hue = random.random()

            for row in range(3):
                # Apply row-specific hue shift
                shifted_hue = (base_hue + row_shifts[row]) % 1.0

                # Create a pattern with saturation and value
                if row == 0:
                    # Top row: lighter
                    saturation = random.uniform(0.3, 0.6)
                    value = random.uniform(0.8, 1.0)
                elif row == 1:
                    # Middle row: medium
                    saturation = random.uniform(0.5, 0.8)
                    value = random.uniform(0.6, 0.8)
                else:
                    # Bottom row: deeper
                    saturation = random.uniform(0.7, 1.0)
                    value = random.uniform(0.4, 0.7)

                palette[row][col] = hsv_to_hex(shifted_hue, saturation, value)

    elif strategy == "complementary":
        # Complementary color scheme
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

    elif strategy == "shades_of_gray":
        # Shades of gray with slight hue variation
        base_hue = random.uniform(0, 1) # slight tint
        for col in range(9):
            for row in range(3):
                shifted_hue = (base_hue + row_shifts[row] * 0.5) % 1.0 # Less hue shift
                saturation = 0.05 + random.random() * 0.05 # Very low saturation
                value = 0.2 + (col / 9) * 0.7 + (row / 3) * 0.1 # Value range from dark to light
                palette[row][col] = hsv_to_hex(shifted_hue, saturation, value)

    elif strategy == "tetradic":
        # Tetradic color scheme
        base_hue = random.random()
        hue2 = (base_hue + 0.33) % 1.0
        hue3 = (base_hue + 0.5) % 1.0
        hue4 = (base_hue + 0.83) % 1.0
        hues = [base_hue, base_hue, hue2, hue2, hue3, hue3, hue4, hue4, (base_hue + 0.1) % 1.0] # Added a slight variation
        random.shuffle(hues)

        for col in range(9):
            base_hue = hues[col]
            for row in range(3):
                shifted_hue = (base_hue + row_shifts[row]) % 1.0
                saturation = 0.5 + row * 0.15 + random.random() * 0.1
                value = 0.8 - row * 0.1 + random.random() * 0.1
                palette[row][col] = hsv_to_hex(shifted_hue, saturation, value)
    elif strategy == "manual_input": # Added manual input strategy
        palette = [
            ["" for _ in range(9)],
            ["" for _ in range(9)],
            ["" for _ in range(9)]
        ]

        print("Please enter 27 colors in hex format (#RRGGBB)")
        print("---------------------------------------------")

        # Get all colors from user input
        for row in range(3):
            for col in range(9):
                palette[row][col] = get_color_input(row, col)
        return palette, strategy


    return palette, strategy

def generate_unique_filename(base_name="pixel_palette", extension=".png"):
    """Generate a unique filename based on timestamp."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{base_name}_{timestamp}{extension}"

def get_save_location_choice():
    """Asks the user for the output folder choice."""
    while True:
        choice1 = input(f"Save to Bitwig Color Palettes folder? (y/n, default: y): ").lower()
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
    """Presents a menu of palette generation strategies to the user."""
    strategies = {
        "0": "manual_input", # Added manual input as option 0
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
        "11": "tetradic"
    }

    print("\nChoose a palette generation strategy:")
    for number, strategy_name in strategies.items():
        print(f"{number}. {strategy_name.replace('_', ' ').title()}") # Nicer display

    while True:
        choice = input("Enter the number of your choice: ")
        if choice in strategies:
            return strategies[choice]
        else:
            print("Invalid choice. Please enter a number from the menu.")


def create_palette_image(hex_codes):
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
            r = int(hex_code[1:3], 16)  # Extract R, G, B components from hex
            g = int(hex_code[3:5], 16)
            b = int(hex_code[5:7], 16)
            pixels[col_index, row_index] = (r, g, b)  # Set pixel color at (x, y)

    # Generate unique filename
    filename = generate_unique_filename()

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
        create_palette_image(hex_codes)

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

# --- END OF FILE Bitwig Color Palette Generator.py ---
if __name__ == "__main__":
    main()
# --- END OF FILE Bitwig Color Palette Generator.py ---