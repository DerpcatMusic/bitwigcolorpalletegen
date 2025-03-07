from PIL import Image
import random
import os
import datetime
import colorsys

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

def generate_random_palette():
    """Generate a random palette with hue shifts between rows."""
    palette = [
        ["" for _ in range(9)],
        ["" for _ in range(9)],
        ["" for _ in range(9)]
    ]
    
    # Choose a random palette generation strategy
    strategy = random.choice([
        "distinct_hues", 
        "split_complementary", 
        "triadic_variations", 
        "analogous_extended",
        "monochromatic_columns",
        "warm_cool_contrast",
        "pastel_dark_contrast",
        "random_with_harmony"
    ])
    
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
    
    return palette, strategy

def generate_unique_filename(base_name="pixel_palette", extension=".png"):
    """Generate a unique filename based on timestamp."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{base_name}_{timestamp}{extension}"

def create_palette_image(hex_codes, output_directory):
    """Create and save an image from the palette hex codes."""
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
    filename_base = generate_unique_filename()
    filename = os.path.join(output_directory, filename_base)
    
    # Save the image
    image.save(filename)
    print(f"Pixel palette image saved as {filename}")
    
    # Print the palette for reference
    print("\nHex color codes in this palette:")
    for row in hex_codes:
        print(" ".join(row))
    
    return filename

# Main program
def main():
    print("Welcome to the Color Palette Generator!")
    print("---------------------------------------------")

    # Determine the user's home directory
    user_home = os.path.expanduser("~")
    base_palette_dir = os.path.join(user_home, "Documents", "Bitwig Studio", "Color Palettes")
    generated_palettes_dir = os.path.join(base_palette_dir, "Generated Palettes")


    # Ask user if they want to create the base folder
    while True:
        create_base_folder = input(f"Do you want to create the base folder {base_palette_dir} if it doesn't exist? (y/n): ").lower()
        if create_base_folder in ['y', 'yes', 'n', 'no']:
            break
        print("Please enter 'y' or 'n'.")

    if create_base_folder in ['y', 'yes']:
        # Create the directory if it doesn't exist
        if not os.path.exists(base_palette_dir):
            try:
                os.makedirs(base_palette_dir)
                print(f"Created directory: {base_palette_dir}")
            except OSError as e:
                print(f"Error creating directory: {e}")
                base_palette_dir = "." #Save to current directory if creating default palette folder fails
                print("Saving to current Directory")
        #Ask if user wants to create the Generated Palettes folder
        while True:
            create_generated_folder = input(f"Do you want to create the 'Generated Palettes' folder inside {base_palette_dir} if it doesn't exist? (y/n): ").lower()
            if create_generated_folder in ['y', 'yes', 'n', 'no']:
                break
            print("Please enter 'y' or 'n'.")
        if create_generated_folder in ['y', 'yes']:
            if not os.path.exists(generated_palettes_dir):
                try:
                    os.makedirs(generated_palettes_dir)
                    print(f"Created directory: {generated_palettes_dir}")
                    output_directory = generated_palettes_dir
                except OSError as e:
                    print(f"Error creating directory: {e}")
                    output_directory = base_palette_dir #Save to base directory if creating default palette folder fails
                    print("Saving to base Directory")
        else:
            output_directory = base_palette_dir #Save to base directory if creating default palette folder fails
            print("Saving to base Directory")
    else:
        base_palette_dir = "." #Save to current directory if creating default palette folder fails
        output_directory = "." #Save to current directory if creating default palette folder fails
        print("Saving to current Directory")

    generate_another = True
    
    while generate_another:
        while True:
            choice = input("Would you like to generate a harmonious palette? (y/n): ").lower()
            if choice in ['y', 'yes', 'n', 'no']:
                break
            print("Please enter 'y' or 'n'.")
        
        if choice in ['y', 'yes']:
            # Generate random palette with a randomly selected strategy
            hex_codes, strategy = generate_random_palette()
            print(f"Palette generated using strategy: {strategy}")
        else:
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
        create_palette_image(hex_codes, output_directory)
        
        # Ask if user wants to generate another palette
        while True:
            another = input("\nWould you like to generate another palette? (y/n): ").lower()
            if another in ['y', 'yes', 'n', 'no']:
                break
            print("Please enter 'y' or 'n'.")
        
        generate_another = another in ['y', 'yes']

    print("Thank you for using the Color Palette Generator!")

if __name__ == "__main__":
    main()