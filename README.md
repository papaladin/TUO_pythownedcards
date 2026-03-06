# TUO Python Owned Cards

A Python port of the PowerShell script created by [Zahalka](https://bence.zahalka.hu/2018/01/29/tyrant-unleashed-optimizer-powershell-tools-english-version/) for use with the [Tyrant Unleashed Optimizer (TUO)](https://github.com/zachanima/tyrant_optimize).

This script parses your Tyrant Unleashed game data and generates the `ownedcards.txt` and `currentdecks.txt` files required by TUO — without needing PowerShell.

---

## What It Does

- Reads your card inventory from your game's exported `json.txt` data file
- Cross-references card IDs against the TUO card definition XML files (`cards_section*.xml`)
- Sorts owned cards by faction base fusion material groups (Bloodthirsty, Imperial, Raider, Righteous, Xeno, Vindicator)
- Appends cards available for restore ("buyback") to the owned cards list
- Outputs your current deck compositions
- Produces two files ready for use with TUO:
  - **`ownedcards.txt`** — your full card inventory, grouped and formatted
  - **`currentdecks.txt`** — your saved deck configurations

---

## Requirements

- Python 3.x (no external libraries needed — uses only the standard library)
- The TUO data folder with:
  - One or more `cards_section*.xml` files (from the TUO installation)
  - A `json.txt` file exported from your Tyrant Unleashed game account

---

## Setup & Usage

1. **Get TUO** — Download the Tyrant Unleashed Optimizer and ensure you have the `cards_section*.xml` files in your TUO data folder.

2. **Export your game data** — Log into Tyrant Unleashed and export/save your account's JSON data as `json.txt` in the same TUO data folder. (Refer to Zahalka's original guide for how to obtain this file.)

3. **Place the script** — Copy `tyrant.py` into your TUO data folder (the same folder containing the XML and JSON files).

4. **Run the script**:
   ```bash
   python tyrant.py
   ```

5. **Use the output** — The generated `ownedcards.txt` and `currentdecks.txt` files are now ready to be used with TUO as you normally would.

---

## Output Files

### `ownedcards.txt`
Your owned card inventory, formatted for TUO. Cards are grouped in this order:
- Vindicator Reactors
- Bloodthirsty base fusion materials
- Imperial base fusion materials
- Raider base fusion materials
- Righteous base fusion materials
- Xeno base fusion materials
- All remaining owned cards
- Cards available from restore

Cards owned in quantities greater than 1 are shown with a count, e.g. `Iron Maiden (3)`.
Max-upgraded cards (level 6) have the level suffix removed, as TUO expects.

### `currentdecks.txt`
Your saved in-game decks, each on one line in the format TUO expects:
```
<deck_number>: <Commander>, <Card1>, <Card2> #<count>, ..., <Dominion>
```

---

## Folder Structure Example

```
/your-tuo-folder/
├── cards_section1.xml
├── cards_section2.xml
├── ...
├── json.txt          ← exported from your game account
├── tyrant.py         ← this script
├── ownedcards.txt    ← generated output
└── currentdecks.txt  ← generated output
```

---

## Credits

- Original PowerShell script and concept: **Bence Zahalka** — [zahalka.hu](https://bence.zahalka.hu/2018/01/29/tyrant-unleashed-optimizer-powershell-tools-english-version/)
- Python port: **papaladin**
