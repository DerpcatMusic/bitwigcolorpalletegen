# Bitwig Color Palette Generator

This script generates random color palettes for use in Bitwig Studio. You can either provide your own list of colors or let the script generate a palette for you.
It will create a Folder inside your Bitwig Color Pallete Directory for your generated Palettes.

[**Download Latest Release**](https://github.com/DerpcatMusic/bitwigcolorpalletegen/releases/latest/download/BitwigColorPaletteGen.py)

![Image Preview](https://preview.redd.it/i-created-a-bitwig-color-palette-generation-tool-v0-ng4eyknu84qe1.png?width=579&format=png&auto=webp&s=ba293f3578d9c205200b7ee35c437413d75870b8)

## Prerequisites

* Python 3.x
* Pillow (PIL) library: Install using `pip install numpy Pillow`

## Usage
   **Clicking Enter will consider as Yes (`y`) **
1.  **Ensure Dependencies:** Make sure Python and Pillow are installed on your system.
2.  **Run the Script:** Drag the `BitwigColorPaletteGen.py` file onto your terminal or execute it using `python BitwigColorPaletteGen.py`.

3.  **Follow Prompts:**
    * The script will prompt you: `Would you like to generate another palette? (y/n):`
    
    * You will be asked to Choose a Palette or Input your own (`0`)
   
    * You'll be Asked to Generate into the main Bitwig Color_Palettes folder: `Save to Bitwig Color Palettes folder? (y/n, default: y):`
      * Selecting `y` will generate inside the main bitwig folder.
      * Selecting `n` will generate into a sub folder within the Color_Palettes folder. (`Save to 'generated_palettes' subfolder within Color Palettes? (y/n, default: n):`)
    
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
