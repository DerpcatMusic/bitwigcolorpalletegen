import re
import random
import json  # To save the selected colors to JSON files

scala_code = """
Color.fromRGB255(0, 0, 0), // 0
Color.fromRGB255(0, 0, 255), // 1 - Blue
Color.fromRGB255(0, 21, 255), // 2 - Blue (Green Rising)
Color.fromRGB255(0, 34, 255), //
Color.fromRGB255(0, 46, 255), //
Color.fromRGB255(0, 59, 255), //
Color.fromRGB255(0, 68, 255), //
Color.fromRGB255(0, 80, 255), //
Color.fromRGB255(0, 93, 255), //
Color.fromRGB255(0, 106, 255), //
Color.fromRGB255(0, 119, 255), //
Color.fromRGB255(0, 127, 255), //
Color.fromRGB255(0, 140, 255), //
Color.fromRGB255(0, 153, 255), //
Color.fromRGB255(0, 165, 255), //
Color.fromRGB255(0, 178, 255), //
Color.fromRGB255(0, 191, 255), //
Color.fromRGB255(0, 199, 255), //
Color.fromRGB255(0, 212, 255), //
Color.fromRGB255(0, 225, 255), //
Color.fromRGB255(0, 238, 255), //
Color.fromRGB255(0, 250, 255), // 21 - End of Blue's Reign
Color.fromRGB255(0, 255, 250), // 22 - Green (Blue Fading)
Color.fromRGB255(0, 255, 237), //
Color.fromRGB255(0, 255, 225), //
Color.fromRGB255(0, 255, 212), //
Color.fromRGB255(0, 255, 199), //
Color.fromRGB255(0, 255, 191), //
Color.fromRGB255(0, 255, 178), //
Color.fromRGB255(0, 255, 165), //
Color.fromRGB255(0, 255, 153), //
Color.fromRGB255(0, 255, 140), //
Color.fromRGB255(0, 255, 127), //
Color.fromRGB255(0, 255, 119), //
Color.fromRGB255(0, 255, 106), //
Color.fromRGB255(0, 255, 93), //
Color.fromRGB255(0, 255, 80), //
Color.fromRGB255(0, 255, 67), //
Color.fromRGB255(0, 255, 59), //
Color.fromRGB255(0, 255, 46), //
Color.fromRGB255(0, 255, 33), //
Color.fromRGB255(0, 255, 21), //
Color.fromRGB255(0, 255, 8), //
Color.fromRGB255(0, 255, 0), // 43 - Green
Color.fromRGB255(12, 255, 0), // 44 - Green/Red Rising
Color.fromRGB255(25, 255, 0), //
Color.fromRGB255(38, 255, 0), //
Color.fromRGB255(51, 255, 0), //
Color.fromRGB255(63, 255, 0), //
Color.fromRGB255(72, 255, 0), //
Color.fromRGB255(84, 255, 0), //
Color.fromRGB255(97, 255, 0), //
Color.fromRGB255(110, 255, 0), //
Color.fromRGB255(123, 255, 0), //
Color.fromRGB255(131, 255, 0), //
Color.fromRGB255(144, 255, 0), //
Color.fromRGB255(157, 255, 0), //
Color.fromRGB255(170, 255, 0), //
Color.fromRGB255(182, 255, 0), //
Color.fromRGB255(191, 255, 0), //
Color.fromRGB255(203, 255, 0), //
Color.fromRGB255(216, 255, 0), //
Color.fromRGB255(229, 255, 0), //
Color.fromRGB255(242, 255, 0), //
Color.fromRGB255(255, 255, 0), // 64 - Green + Red (Yellow)
Color.fromRGB255(255, 246, 0), // 65 - Red, Green Fading
Color.fromRGB255(255, 233, 0), //
Color.fromRGB255(255, 220, 0), //
Color.fromRGB255(255, 208, 0), //
Color.fromRGB255(255, 195, 0), //
Color.fromRGB255(255, 187, 0), //
Color.fromRGB255(255, 174, 0), //
Color.fromRGB255(255, 161, 0), //
Color.fromRGB255(255, 148, 0), //
Color.fromRGB255(255, 135, 0), //
Color.fromRGB255(255, 127, 0), //
Color.fromRGB255(255, 114, 0), //
Color.fromRGB255(255, 102, 0), //
Color.fromRGB255(255, 89, 0), //
Color.fromRGB255(255, 76, 0), //
Color.fromRGB255(255, 63, 0), //
Color.fromRGB255(255, 55, 0), //
Color.fromRGB255(255, 42, 0), //
Color.fromRGB255(255, 29, 0), //
Color.fromRGB255(255, 16, 0), //
Color.fromRGB255(255, 4, 0), // 85 - End Red/Green Fading
Color.fromRGB255(255, 0, 4), // 86 - Red/ Blue Rising
Color.fromRGB255(255, 0, 16), //
Color.fromRGB255(255, 0, 29), //
Color.fromRGB255(255, 0, 42), //
Color.fromRGB255(255, 0, 55), //
Color.fromRGB255(255, 0, 63), //
Color.fromRGB255(255, 0, 76), //
Color.fromRGB255(255, 0, 89), //
Color.fromRGB255(255, 0, 102), //
Color.fromRGB255(255, 0, 114), //
Color.fromRGB255(255, 0, 127), //
Color.fromRGB255(255, 0, 135), //
Color.fromRGB255(255, 0, 148), //
Color.fromRGB255(255, 0, 161), //
Color.fromRGB255(255, 0, 174), //
Color.fromRGB255(255, 0, 186), //
Color.fromRGB255(255, 0, 195), //
Color.fromRGB255(255, 0, 208), //
Color.fromRGB255(255, 0, 221), //
Color.fromRGB255(255, 0, 233), //
Color.fromRGB255(255, 0, 246), //
Color.fromRGB255(255, 0, 255), // 107 - Blue + Red
Color.fromRGB255(242, 0, 255), // 108 - Blue/ Red Fading
Color.fromRGB255(229, 0, 255), //
Color.fromRGB255(216, 0, 255), //
Color.fromRGB255(204, 0, 255), //
Color.fromRGB255(191, 0, 255), //
Color.fromRGB255(182, 0, 255), //
Color.fromRGB255(169, 0, 255), //
Color.fromRGB255(157, 0, 255), //
Color.fromRGB255(144, 0, 255), //
Color.fromRGB255(131, 0, 255), //
Color.fromRGB255(123, 0, 255), //
Color.fromRGB255(110, 0, 255), //
Color.fromRGB255(97, 0, 255), //
Color.fromRGB255(85, 0, 255), //
Color.fromRGB255(72, 0, 255), //
Color.fromRGB255(63, 0, 255), //
Color.fromRGB255(50, 0, 255), //
Color.fromRGB255(38, 0, 255), //
Color.fromRGB255(25, 0, 255), // 126 - Blue-ish
Color.fromRGB255(240, 240, 225) // 127 - White ?
"""

# Regex to extract RGB values
rgb_pattern = re.compile(r"Color\.fromRGB255\((\d+),\s*(\d+),\s*(\d+)\)")
scala_colors_rgb = []
excluded_colors_rgb = [(0, 0, 0), (240, 240, 225)] # List of colors to exclude

for line in scala_code.strip().split('\n'):
    match = rgb_pattern.search(line)
    if match:
        r, g, b = map(int, match.groups())
        current_color_rgb = (r, g, b)
        if current_color_rgb not in excluded_colors_rgb: # Exclude black and "white?"
            scala_colors_rgb.append(current_color_rgb)

print(f"Extracted {len(scala_colors_rgb)} RGB colors from Scala code (excluding black and 'white?').")

def color_distance_rgb(color1_rgb, color2_rgb):
    """Calculates Euclidean distance between two RGB colors."""
    r1, g1, b1 = color1_rgb
    r2, g2, b2 = color2_rgb
    return ((r1 - r2)**2 + (g1 - g2)**2 + (b1 - b2)**2)**0.5

def select_distinct_colors(all_colors_rgb, num_to_select=27):
    """Selects a set of maximally distinct colors, excluding or replacing black (0,0,0)."""
    selected_colors = []
    remaining_colors = list(all_colors_rgb)

    if not remaining_colors:
        return []

    # 1. Select the first color randomly (or the first color in the list)
    first_color_index = random.randint(0, len(remaining_colors) - 1)
    selected_colors.append(remaining_colors.pop(first_color_index))

    while len(selected_colors) < num_to_select and remaining_colors:
        best_color = None
        max_min_distance = -1

        for color in remaining_colors:
            min_distance = float('inf')
            for selected_color in selected_colors:
                distance = color_distance_rgb(color, selected_color)
                min_distance = min(min_distance, distance)

            if min_distance > max_min_distance:
                max_min_distance = min_distance
                best_color = color

        if best_color:
            selected_colors.append(best_color)
            remaining_colors.remove(best_color)
        else:
            break

    # 2. Check for and replace Dark Gray/Black (0, 0, 0) - Removed replacement logic for simplicity

    return selected_colors

def save_twister_colors(colors, filename): # Modified to accept colors and filename
    try:
        with open(filename, 'w') as f:
            json.dump(colors, f, indent=4) # Save as JSON, nicely formatted
        print(f"Saved colors to: {filename}")
    except Exception as e:
        print(f"Error saving colors to {filename}: {e}")

# --- Save ALL extracted colors (excluding black and "white?") ---
all_colors_output_file = "mf_twister_all_colors.json" # Filename for all colors JSON
save_twister_colors(scala_colors_rgb, all_colors_output_file) # Save all extracted colors

# --- Save distinct color palettes (as before) ---
NUM_COLORS_27 = 27
distinct_colors_27 = select_distinct_colors(scala_colors_rgb, num_to_select=NUM_COLORS_27)
save_twister_colors(distinct_colors_27, f"mf_twister_{NUM_COLORS_27}_colors.json")

NUM_COLORS_64 = 64
distinct_colors_64 = select_distinct_colors(scala_colors_rgb, num_to_select=NUM_COLORS_64)
save_twister_colors(distinct_colors_64, f"mf_twister_{NUM_COLORS_64}_colors.json")
