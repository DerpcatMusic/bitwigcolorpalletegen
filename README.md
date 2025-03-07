# Bitwig Color Palette Generator

This script generates random color palettes for use in Bitwig Studio. You can either provide your own list of colors or let the script generate a harmonious palette for you.
It will create a Folder inside your Bitwig Color Pallete Directory for your generated Palettes.

## Prerequisites

* Python 3.x
* Pillow (PIL) library: Install using `pip install Pillow`

## Usage

1.  **Ensure Dependencies:** Make sure Python and Pillow are installed on your system.
2.  **Run the Script:** Drag the `BitwigColorPaletteGen.py` file onto your terminal or execute it using `python BitwigColorPaletteGen.py`.
3.  **Follow Prompts:**
    * The script will prompt you: `Would you like to generate another palette? (y/n):`
    * If you choose to generate a palette (`y`), you will be asked: `Would you like to generate a harmonious palette? (y/n):`
        * Selecting `y` will generate a harmonious color palette.
        * Selecting `n` will allow you to input your own list of colors.
4.  **Input Custom Colors (Optional):**
    * If you chose `n` for harmonious palette generation, paste your list of colors in hexadecimal format, one color per line.
    * Example format:

    ```
    #FF0000
    #FF8C00
    #FFFF00
    #ADFF2F
    #00FF00
    #00FFFF
    #00BFFF
    #0000FF
    #8A2BE2
    #9932CC
    #DA70D6
    #FF1493
    #FF69B4
    #FF00FF
    #800080
    #A52A2A
    #D2691E
    #8B4513
    #CD853F
    #F4A460
    #D2B48C
    #BC8F8F
    #FA8072
    #E9967A
    #FFA07A
    #B22222
    #8B0000
    ```
