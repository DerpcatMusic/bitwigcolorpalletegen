import re
import random
import json # To save the selected colors to a JSON file

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

for line in scala_code.strip().split('\n'):
    match = rgb_pattern.search(line)
    if match:
        r, g, b = map(int, match.groups())
        scala_colors_rgb.append((r, g, b))

print(f"Extracted {len(scala_colors_rgb)} RGB colors from Scala code.")

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

    # 2. Check for and replace Dark Gray/Black (0, 0, 0)
    black_rgb = (0, 0, 0)
    if black_rgb in selected_colors:
        print("Dark Gray/Black color (0, 0, 0) found in selected colors. Attempting to replace it.")
        black_index = selected_colors.index(black_rgb)
        selected_colors.pop(black_index) # Remove black

        if remaining_colors: # Try to find a replacement if there are still colors left
            best_replacement_color = None
            max_min_distance_replacement = -1

            for color in remaining_colors:
                min_distance_replacement = float('inf')
                for selected_color in selected_colors: # Note: selected_colors now without black
                    distance = color_distance_rgb(color, selected_color)
                    min_distance_replacement = min(min_distance_replacement, distance)

                if min_distance_replacement > max_min_distance_replacement:
                    max_min_distance_replacement = min_distance_replacement
                    best_replacement_color = color

            if best_replacement_color:
                selected_colors.insert(black_index, best_replacement_color) # Insert replacement at black's original position
                remaining_colors.remove(best_replacement_color)
                print(f"Replaced Dark Gray/Black with a new distinct color: {best_replacement_color}")
            else:
                print("Warning: No suitable replacement found for Dark Gray/Black. Palette might have < 27 colors.")
        else:
            print("Warning: No remaining colors to replace Dark Gray/Black. Palette might have < 27 colors.")
    else:
        print("Dark Gray/Black color (0, 0, 0) not found in selected colors. No replacement needed.")

    return selected_colors

distinct_27_rgb_colors = select_distinct_colors(scala_colors_rgb, num_to_select=27)

print(f"Selected {len(distinct_27_rgb_colors)} distinct RGB colors:")
for color in distinct_27_rgb_colors:
    print(color)

# --- Save the selected colors to a JSON file ---
output_file = "mf_twister_colors.json" # Filename for saved colors
try:
    with open(output_file, 'w') as f:
        json.dump(distinct_27_rgb_colors, f, indent=4) # Save as JSON, nicely formatted
    print(f"Saved selected distinct colors to: {output_file}")
except Exception as e:
    print(f"Error saving olors to {output_file}: {e}")
