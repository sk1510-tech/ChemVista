from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'chemvista_secret_key_2024'

# Complete periodic table data with all 118 elements
COMPLETE_ELEMENTS = [
    {"atomic_number": 1, "symbol": "H", "name": "Hydrogen", "category": "reactive-nonmetal", "group": 1, "period": 1, "atomic_mass": 1.008, "description": "The lightest and most abundant element in the universe."},
    {"atomic_number": 2, "symbol": "He", "name": "Helium", "category": "noble-gas", "group": 18, "period": 1, "atomic_mass": 4.003, "description": "Noble gas used in balloons and cooling applications."},
    {"atomic_number": 3, "symbol": "Li", "name": "Lithium", "category": "alkali-metal", "group": 1, "period": 2, "atomic_mass": 6.941, "description": "Lightest metal, used in batteries."},
    {"atomic_number": 4, "symbol": "Be", "name": "Beryllium", "category": "alkaline-earth-metal", "group": 2, "period": 2, "atomic_mass": 9.012, "description": "Light, strong metal used in aerospace."},
    {"atomic_number": 5, "symbol": "B", "name": "Boron", "category": "metalloid", "group": 13, "period": 2, "atomic_mass": 10.811, "description": "Metalloid used in glass and ceramics."},
    {"atomic_number": 6, "symbol": "C", "name": "Carbon", "category": "reactive-nonmetal", "group": 14, "period": 2, "atomic_mass": 12.011, "description": "Essential element for all life forms."},
    {"atomic_number": 7, "symbol": "N", "name": "Nitrogen", "category": "reactive-nonmetal", "group": 15, "period": 2, "atomic_mass": 14.007, "description": "Makes up 78% of Earth's atmosphere."},
    {"atomic_number": 8, "symbol": "O", "name": "Oxygen", "category": "reactive-nonmetal", "group": 16, "period": 2, "atomic_mass": 15.999, "description": "Essential for respiration and combustion."},
    {"atomic_number": 9, "symbol": "F", "name": "Fluorine", "category": "halogen", "group": 17, "period": 2, "atomic_mass": 18.998, "description": "Most electronegative element."},
    {"atomic_number": 10, "symbol": "Ne", "name": "Neon", "category": "noble-gas", "group": 18, "period": 2, "atomic_mass": 20.180, "description": "Noble gas used in lighting."},
    {"atomic_number": 11, "symbol": "Na", "name": "Sodium", "category": "alkali-metal", "group": 1, "period": 3, "atomic_mass": 22.990, "description": "Highly reactive alkali metal."},
    {"atomic_number": 12, "symbol": "Mg", "name": "Magnesium", "category": "alkaline-earth-metal", "group": 2, "period": 3, "atomic_mass": 24.305, "description": "Light metal essential for chlorophyll."},
    {"atomic_number": 13, "symbol": "Al", "name": "Aluminum", "category": "post-transition-metal", "group": 13, "period": 3, "atomic_mass": 26.982, "description": "Lightweight, corrosion-resistant metal."},
    {"atomic_number": 14, "symbol": "Si", "name": "Silicon", "category": "metalloid", "group": 14, "period": 3, "atomic_mass": 28.086, "description": "Essential for electronics and computer chips."},
    {"atomic_number": 15, "symbol": "P", "name": "Phosphorus", "category": "reactive-nonmetal", "group": 15, "period": 3, "atomic_mass": 30.974, "description": "Essential for DNA, RNA, and ATP."},
    {"atomic_number": 16, "symbol": "S", "name": "Sulfur", "category": "reactive-nonmetal", "group": 16, "period": 3, "atomic_mass": 32.065, "description": "Non-metal essential for proteins."},
    {"atomic_number": 17, "symbol": "Cl", "name": "Chlorine", "category": "halogen", "group": 17, "period": 3, "atomic_mass": 35.453, "description": "Halogen used for water purification."},
    {"atomic_number": 18, "symbol": "Ar", "name": "Argon", "category": "noble-gas", "group": 18, "period": 3, "atomic_mass": 39.948, "description": "Noble gas used in welding."},
    {"atomic_number": 19, "symbol": "K", "name": "Potassium", "category": "alkali-metal", "group": 1, "period": 4, "atomic_mass": 39.098, "description": "Essential for nerve and muscle function."},
    {"atomic_number": 20, "symbol": "Ca", "name": "Calcium", "category": "alkaline-earth-metal", "group": 2, "period": 4, "atomic_mass": 40.078, "description": "Essential for bones and teeth."},
    {"atomic_number": 21, "symbol": "Sc", "name": "Scandium", "category": "transition-metal", "group": 3, "period": 4, "atomic_mass": 44.956, "description": "Rare earth metal used in aerospace."},
    {"atomic_number": 22, "symbol": "Ti", "name": "Titanium", "category": "transition-metal", "group": 4, "period": 4, "atomic_mass": 47.867, "description": "Strong, lightweight metal."},
    {"atomic_number": 23, "symbol": "V", "name": "Vanadium", "category": "transition-metal", "group": 5, "period": 4, "atomic_mass": 50.942, "description": "Used in steel alloys."},
    {"atomic_number": 24, "symbol": "Cr", "name": "Chromium", "category": "transition-metal", "group": 6, "period": 4, "atomic_mass": 51.996, "description": "Used for chrome plating."},
    {"atomic_number": 25, "symbol": "Mn", "name": "Manganese", "category": "transition-metal", "group": 7, "period": 4, "atomic_mass": 54.938, "description": "Essential trace element."},
    {"atomic_number": 26, "symbol": "Fe", "name": "Iron", "category": "transition-metal", "group": 8, "period": 4, "atomic_mass": 55.845, "description": "Most common element on Earth."},
    {"atomic_number": 27, "symbol": "Co", "name": "Cobalt", "category": "transition-metal", "group": 9, "period": 4, "atomic_mass": 58.933, "description": "Used in magnets and batteries."},
    {"atomic_number": 28, "symbol": "Ni", "name": "Nickel", "category": "transition-metal", "group": 10, "period": 4, "atomic_mass": 58.693, "description": "Corrosion-resistant metal."},
    {"atomic_number": 29, "symbol": "Cu", "name": "Copper", "category": "transition-metal", "group": 11, "period": 4, "atomic_mass": 63.546, "description": "Excellent electrical conductor."},
    {"atomic_number": 30, "symbol": "Zn", "name": "Zinc", "category": "transition-metal", "group": 12, "period": 4, "atomic_mass": 65.38, "description": "Essential trace element."},
    {"atomic_number": 31, "symbol": "Ga", "name": "Gallium", "category": "post-transition-metal", "group": 13, "period": 4, "atomic_mass": 69.723, "description": "Metal that melts in your hand."},
    {"atomic_number": 32, "symbol": "Ge", "name": "Germanium", "category": "metalloid", "group": 14, "period": 4, "atomic_mass": 72.630, "description": "Semiconductor material."},
    {"atomic_number": 33, "symbol": "As", "name": "Arsenic", "category": "metalloid", "group": 15, "period": 4, "atomic_mass": 74.922, "description": "Toxic metalloid."},
    {"atomic_number": 34, "symbol": "Se", "name": "Selenium", "category": "reactive-nonmetal", "group": 16, "period": 4, "atomic_mass": 78.971, "description": "Essential trace element."},
    {"atomic_number": 35, "symbol": "Br", "name": "Bromine", "category": "halogen", "group": 17, "period": 4, "atomic_mass": 79.904, "description": "Only liquid halogen at room temperature."},
    {"atomic_number": 36, "symbol": "Kr", "name": "Krypton", "category": "noble-gas", "group": 18, "period": 4, "atomic_mass": 83.798, "description": "Noble gas used in lighting."},
    {"atomic_number": 37, "symbol": "Rb", "name": "Rubidium", "category": "alkali-metal", "group": 1, "period": 5, "atomic_mass": 85.468, "description": "Highly reactive alkali metal."},
    {"atomic_number": 38, "symbol": "Sr", "name": "Strontium", "category": "alkaline-earth-metal", "group": 2, "period": 5, "atomic_mass": 87.62, "description": "Used in fireworks for red color."},
    {"atomic_number": 39, "symbol": "Y", "name": "Yttrium", "category": "transition-metal", "group": 3, "period": 5, "atomic_mass": 88.906, "description": "Used in LED phosphors."},
    {"atomic_number": 40, "symbol": "Zr", "name": "Zirconium", "category": "transition-metal", "group": 4, "period": 5, "atomic_mass": 91.224, "description": "Corrosion-resistant metal."},
    {"atomic_number": 41, "symbol": "Nb", "name": "Niobium", "category": "transition-metal", "group": 5, "period": 5, "atomic_mass": 92.906, "description": "Superconducting metal."},
    {"atomic_number": 42, "symbol": "Mo", "name": "Molybdenum", "category": "transition-metal", "group": 6, "period": 5, "atomic_mass": 95.95, "description": "Used in steel alloys."},
    {"atomic_number": 43, "symbol": "Tc", "name": "Technetium", "category": "transition-metal", "group": 7, "period": 5, "atomic_mass": 98, "description": "First artificially produced element."},
    {"atomic_number": 44, "symbol": "Ru", "name": "Ruthenium", "category": "transition-metal", "group": 8, "period": 5, "atomic_mass": 101.07, "description": "Precious metal used in catalysts."},
    {"atomic_number": 45, "symbol": "Rh", "name": "Rhodium", "category": "transition-metal", "group": 9, "period": 5, "atomic_mass": 102.91, "description": "Rare precious metal."},
    {"atomic_number": 46, "symbol": "Pd", "name": "Palladium", "category": "transition-metal", "group": 10, "period": 5, "atomic_mass": 106.42, "description": "Precious metal used in catalysts."},
    {"atomic_number": 47, "symbol": "Ag", "name": "Silver", "category": "transition-metal", "group": 11, "period": 5, "atomic_mass": 107.87, "description": "Precious metal with highest conductivity."},
    {"atomic_number": 48, "symbol": "Cd", "name": "Cadmium", "category": "transition-metal", "group": 12, "period": 5, "atomic_mass": 112.41, "description": "Toxic metal used in batteries."},
    {"atomic_number": 49, "symbol": "In", "name": "Indium", "category": "post-transition-metal", "group": 13, "period": 5, "atomic_mass": 114.82, "description": "Soft metal used in touchscreens."},
    {"atomic_number": 50, "symbol": "Sn", "name": "Tin", "category": "post-transition-metal", "group": 14, "period": 5, "atomic_mass": 118.71, "description": "Metal used in alloys and plating."},
    {"atomic_number": 51, "symbol": "Sb", "name": "Antimony", "category": "metalloid", "group": 15, "period": 5, "atomic_mass": 121.76, "description": "Metalloid used in flame retardants."},
    {"atomic_number": 52, "symbol": "Te", "name": "Tellurium", "category": "metalloid", "group": 16, "period": 5, "atomic_mass": 127.60, "description": "Rare metalloid."},
    {"atomic_number": 53, "symbol": "I", "name": "Iodine", "category": "halogen", "group": 17, "period": 5, "atomic_mass": 126.90, "description": "Essential for thyroid function."},
    {"atomic_number": 54, "symbol": "Xe", "name": "Xenon", "category": "noble-gas", "group": 18, "period": 5, "atomic_mass": 131.29, "description": "Noble gas used in lighting."},
    {"atomic_number": 55, "symbol": "Cs", "name": "Cesium", "category": "alkali-metal", "group": 1, "period": 6, "atomic_mass": 132.91, "description": "Most reactive alkali metal."},
    {"atomic_number": 56, "symbol": "Ba", "name": "Barium", "category": "alkaline-earth-metal", "group": 2, "period": 6, "atomic_mass": 137.33, "description": "Used in medical imaging."},
    {"atomic_number": 57, "symbol": "La", "name": "Lanthanum", "category": "lanthanide", "group": 3, "period": 6, "atomic_mass": 138.91, "description": "First lanthanide element."},
    {"atomic_number": 58, "symbol": "Ce", "name": "Cerium", "category": "lanthanide", "group": 3, "period": 6, "atomic_mass": 140.12, "description": "Most abundant rare earth element."},
    {"atomic_number": 59, "symbol": "Pr", "name": "Praseodymium", "category": "lanthanide", "group": 3, "period": 6, "atomic_mass": 140.91, "description": "Rare earth metal."},
    {"atomic_number": 60, "symbol": "Nd", "name": "Neodymium", "category": "lanthanide", "group": 3, "period": 6, "atomic_mass": 144.24, "description": "Used in powerful magnets."},
    {"atomic_number": 61, "symbol": "Pm", "name": "Promethium", "category": "lanthanide", "group": 3, "period": 6, "atomic_mass": 145, "description": "Radioactive rare earth metal."},
    {"atomic_number": 62, "symbol": "Sm", "name": "Samarium", "category": "lanthanide", "group": 3, "period": 6, "atomic_mass": 150.36, "description": "Used in magnets and lasers."},
    {"atomic_number": 63, "symbol": "Eu", "name": "Europium", "category": "lanthanide", "group": 3, "period": 6, "atomic_mass": 151.96, "description": "Used in red phosphors."},
    {"atomic_number": 64, "symbol": "Gd", "name": "Gadolinium", "category": "lanthanide", "group": 3, "period": 6, "atomic_mass": 157.25, "description": "Used in MRI contrast agents."},
    {"atomic_number": 65, "symbol": "Tb", "name": "Terbium", "category": "lanthanide", "group": 3, "period": 6, "atomic_mass": 158.93, "description": "Used in green phosphors."},
    {"atomic_number": 66, "symbol": "Dy", "name": "Dysprosium", "category": "lanthanide", "group": 3, "period": 6, "atomic_mass": 162.50, "description": "Used in hard disk drives."},
    {"atomic_number": 67, "symbol": "Ho", "name": "Holmium", "category": "lanthanide", "group": 3, "period": 6, "atomic_mass": 164.93, "description": "Has strongest magnetic moment."},
    {"atomic_number": 68, "symbol": "Er", "name": "Erbium", "category": "lanthanide", "group": 3, "period": 6, "atomic_mass": 167.26, "description": "Used in fiber optic amplifiers."},
    {"atomic_number": 69, "symbol": "Tm", "name": "Thulium", "category": "lanthanide", "group": 3, "period": 6, "atomic_mass": 168.93, "description": "Least abundant rare earth."},
    {"atomic_number": 70, "symbol": "Yb", "name": "Ytterbium", "category": "lanthanide", "group": 3, "period": 6, "atomic_mass": 173.05, "description": "Used in atomic clocks."},
    {"atomic_number": 71, "symbol": "Lu", "name": "Lutetium", "category": "lanthanide", "group": 3, "period": 6, "atomic_mass": 174.97, "description": "Last lanthanide element."},
    {"atomic_number": 72, "symbol": "Hf", "name": "Hafnium", "category": "transition-metal", "group": 4, "period": 6, "atomic_mass": 178.49, "description": "Used in nuclear reactors."},
    {"atomic_number": 73, "symbol": "Ta", "name": "Tantalum", "category": "transition-metal", "group": 5, "period": 6, "atomic_mass": 180.95, "description": "Used in electronic components."},
    {"atomic_number": 74, "symbol": "W", "name": "Tungsten", "category": "transition-metal", "group": 6, "period": 6, "atomic_mass": 183.84, "description": "Highest melting point of all elements."},
    {"atomic_number": 75, "symbol": "Re", "name": "Rhenium", "category": "transition-metal", "group": 7, "period": 6, "atomic_mass": 186.21, "description": "One of the rarest elements."},
    {"atomic_number": 76, "symbol": "Os", "name": "Osmium", "category": "transition-metal", "group": 8, "period": 6, "atomic_mass": 190.23, "description": "Densest naturally occurring element."},
    {"atomic_number": 77, "symbol": "Ir", "name": "Iridium", "category": "transition-metal", "group": 9, "period": 6, "atomic_mass": 192.22, "description": "Second densest element."},
    {"atomic_number": 78, "symbol": "Pt", "name": "Platinum", "category": "transition-metal", "group": 10, "period": 6, "atomic_mass": 195.08, "description": "Precious metal used in catalysts."},
    {"atomic_number": 79, "symbol": "Au", "name": "Gold", "category": "transition-metal", "group": 11, "period": 6, "atomic_mass": 196.97, "description": "Precious metal, symbol of wealth."},
    {"atomic_number": 80, "symbol": "Hg", "name": "Mercury", "category": "transition-metal", "group": 12, "period": 6, "atomic_mass": 200.59, "description": "Only liquid metal at room temperature."},
    {"atomic_number": 81, "symbol": "Tl", "name": "Thallium", "category": "post-transition-metal", "group": 13, "period": 6, "atomic_mass": 204.38, "description": "Toxic heavy metal."},
    {"atomic_number": 82, "symbol": "Pb", "name": "Lead", "category": "post-transition-metal", "group": 14, "period": 6, "atomic_mass": 207.2, "description": "Dense metal, toxic to humans."},
    {"atomic_number": 83, "symbol": "Bi", "name": "Bismuth", "category": "post-transition-metal", "group": 15, "period": 6, "atomic_mass": 208.98, "description": "Last stable element."},
    {"atomic_number": 84, "symbol": "Po", "name": "Polonium", "category": "post-transition-metal", "group": 16, "period": 6, "atomic_mass": 209, "description": "Highly radioactive element."},
    {"atomic_number": 85, "symbol": "At", "name": "Astatine", "category": "halogen", "group": 17, "period": 6, "atomic_mass": 210, "description": "Rarest naturally occurring element."},
    {"atomic_number": 86, "symbol": "Rn", "name": "Radon", "category": "noble-gas", "group": 18, "period": 6, "atomic_mass": 222, "description": "Radioactive noble gas."},
    {"atomic_number": 87, "symbol": "Fr", "name": "Francium", "category": "alkali-metal", "group": 1, "period": 7, "atomic_mass": 223, "description": "Most radioactive alkali metal."},
    {"atomic_number": 88, "symbol": "Ra", "name": "Radium", "category": "alkaline-earth-metal", "group": 2, "period": 7, "atomic_mass": 226, "description": "Highly radioactive metal."},
    {"atomic_number": 89, "symbol": "Ac", "name": "Actinium", "category": "actinide", "group": 3, "period": 7, "atomic_mass": 227, "description": "First actinide element."},
    {"atomic_number": 90, "symbol": "Th", "name": "Thorium", "category": "actinide", "group": 3, "period": 7, "atomic_mass": 232.04, "description": "Radioactive fuel alternative."},
    {"atomic_number": 91, "symbol": "Pa", "name": "Protactinium", "category": "actinide", "group": 3, "period": 7, "atomic_mass": 231.04, "description": "Rare radioactive element."},
    {"atomic_number": 92, "symbol": "U", "name": "Uranium", "category": "actinide", "group": 3, "period": 7, "atomic_mass": 238.03, "description": "Nuclear fuel element."},
    {"atomic_number": 93, "symbol": "Np", "name": "Neptunium", "category": "actinide", "group": 3, "period": 7, "atomic_mass": 237, "description": "First transuranium element."},
    {"atomic_number": 94, "symbol": "Pu", "name": "Plutonium", "category": "actinide", "group": 3, "period": 7, "atomic_mass": 244, "description": "Nuclear weapon material."},
    {"atomic_number": 95, "symbol": "Am", "name": "Americium", "category": "actinide", "group": 3, "period": 7, "atomic_mass": 243, "description": "Used in smoke detectors."},
    {"atomic_number": 96, "symbol": "Cm", "name": "Curium", "category": "actinide", "group": 3, "period": 7, "atomic_mass": 247, "description": "Named after Marie Curie."},
    {"atomic_number": 97, "symbol": "Bk", "name": "Berkelium", "category": "actinide", "group": 3, "period": 7, "atomic_mass": 247, "description": "Synthetic radioactive element."},
    {"atomic_number": 98, "symbol": "Cf", "name": "Californium", "category": "actinide", "group": 3, "period": 7, "atomic_mass": 251, "description": "Neutron source element."},
    {"atomic_number": 99, "symbol": "Es", "name": "Einsteinium", "category": "actinide", "group": 3, "period": 7, "atomic_mass": 252, "description": "Named after Einstein."},
    {"atomic_number": 100, "symbol": "Fm", "name": "Fermium", "category": "actinide", "group": 3, "period": 7, "atomic_mass": 257, "description": "Named after Enrico Fermi."},
    {"atomic_number": 101, "symbol": "Md", "name": "Mendelevium", "category": "actinide", "group": 3, "period": 7, "atomic_mass": 258, "description": "Named after Mendeleev."},
    {"atomic_number": 102, "symbol": "No", "name": "Nobelium", "category": "actinide", "group": 3, "period": 7, "atomic_mass": 259, "description": "Named after Alfred Nobel."},
    {"atomic_number": 103, "symbol": "Lr", "name": "Lawrencium", "category": "actinide", "group": 3, "period": 7, "atomic_mass": 262, "description": "Last actinide element."},
    {"atomic_number": 104, "symbol": "Rf", "name": "Rutherfordium", "category": "transition-metal", "group": 4, "period": 7, "atomic_mass": 267, "description": "Synthetic super-heavy element."},
    {"atomic_number": 105, "symbol": "Db", "name": "Dubnium", "category": "transition-metal", "group": 5, "period": 7, "atomic_mass": 270, "description": "Synthetic super-heavy element."},
    {"atomic_number": 106, "symbol": "Sg", "name": "Seaborgium", "category": "transition-metal", "group": 6, "period": 7, "atomic_mass": 271, "description": "Named after Glenn Seaborg."},
    {"atomic_number": 107, "symbol": "Bh", "name": "Bohrium", "category": "transition-metal", "group": 7, "period": 7, "atomic_mass": 270, "description": "Named after Niels Bohr."},
    {"atomic_number": 108, "symbol": "Hs", "name": "Hassium", "category": "transition-metal", "group": 8, "period": 7, "atomic_mass": 277, "description": "Named after the German state Hesse."},
    {"atomic_number": 109, "symbol": "Mt", "name": "Meitnerium", "category": "transition-metal", "group": 9, "period": 7, "atomic_mass": 276, "description": "Named after Lise Meitner."},
    {"atomic_number": 110, "symbol": "Ds", "name": "Darmstadtium", "category": "transition-metal", "group": 10, "period": 7, "atomic_mass": 281, "description": "Named after Darmstadt, Germany."},
    {"atomic_number": 111, "symbol": "Rg", "name": "Roentgenium", "category": "transition-metal", "group": 11, "period": 7, "atomic_mass": 280, "description": "Named after Wilhelm Roentgen."},
    {"atomic_number": 112, "symbol": "Cn", "name": "Copernicium", "category": "transition-metal", "group": 12, "period": 7, "atomic_mass": 285, "description": "Named after Nicolaus Copernicus."},
    {"atomic_number": 113, "symbol": "Nh", "name": "Nihonium", "category": "post-transition-metal", "group": 13, "period": 7, "atomic_mass": 284, "description": "Named after Japan (Nihon)."},
    {"atomic_number": 114, "symbol": "Fl", "name": "Flerovium", "category": "post-transition-metal", "group": 14, "period": 7, "atomic_mass": 289, "description": "Named after Georgy Flyorov."},
    {"atomic_number": 115, "symbol": "Mc", "name": "Moscovium", "category": "post-transition-metal", "group": 15, "period": 7, "atomic_mass": 288, "description": "Named after Moscow."},
    {"atomic_number": 116, "symbol": "Lv", "name": "Livermorium", "category": "post-transition-metal", "group": 16, "period": 7, "atomic_mass": 293, "description": "Named after Livermore, California."},
    {"atomic_number": 117, "symbol": "Ts", "name": "Tennessine", "category": "halogen", "group": 17, "period": 7, "atomic_mass": 294, "description": "Named after Tennessee."},
    {"atomic_number": 118, "symbol": "Og", "name": "Oganesson", "category": "noble-gas", "group": 18, "period": 7, "atomic_mass": 294, "description": "Named after Yuri Oganessian."}
]

# Load element data
def load_element_data():
    """Load element data from embedded complete dataset"""
    try:
        # Use the complete elements data embedded in the application
        print(f"Loading {len(COMPLETE_ELEMENTS)} elements from embedded dataset")
        return COMPLETE_ELEMENTS
    except Exception as e:
        print(f"Error loading element data: {e}")
        # Fallback to JSON file if available
        try:
            if os.path.exists('data/complete_elements.json'):
                with open('data/complete_elements.json', 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                print("No element data available")
                return []
        except Exception as e2:
            print(f"Fallback loading also failed: {e2}")
            return []

# Load chemical compounds data
def load_compounds_data():
    """Load compounds data from JSON file with error handling"""
    try:
        # Try to load from expanded compounds first, fallback to regular compounds
        if os.path.exists('data/expanded_compounds.json'):
            with open('data/expanded_compounds.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            with open('data/compounds.json', 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading compounds data: {e}")
        return []

@app.route('/')
def index():
    """Homepage with complete periodic table and formula finder"""
    elements = load_element_data()
    return render_template('index_complete.html', elements=elements)

@app.route('/element/<int:atomic_number>')
def element_detail(atomic_number):
    """Display detailed information about a specific element"""
    elements = load_element_data()
    element = next((el for el in elements if el['atomic_number'] == atomic_number), None)
    
    if element:
        return render_template('element_detail.html', element=element)
    else:
        return render_template('404.html'), 404

@app.route('/search')
def search():
    """Search for chemical compounds"""
    query = request.args.get('q', '').strip().lower()
    
    if not query:
        return render_template('search_results.html', results=[], query='')
    
    compounds = load_compounds_data()
    results = []
    
    # Search by name or formula
    for compound in compounds:
        if (query in compound['name'].lower() or 
            query in compound['formula'].lower() or
            query.replace(' ', '') in compound['formula'].lower().replace(' ', '')):
            results.append(compound)
    
    return render_template('search_results.html', results=results, query=query)

@app.route('/compound/<compound_id>')
def compound_detail(compound_id):
    """Display detailed information about a specific compound"""
    compounds = load_compounds_data()
    compound = next((comp for comp in compounds if comp['id'] == compound_id), None)
    
    if compound:
        return render_template('compound_detail.html', compound=compound)
    else:
        return render_template('404.html'), 404

@app.route('/api/search')
def api_search():
    """API endpoint for live search suggestions"""
    query = request.args.get('q', '').strip().lower()
    compounds = load_compounds_data()
    
    suggestions = []
    for compound in compounds[:10]:  # Limit to 10 suggestions
        if (query in compound['name'].lower() or 
            query in compound['formula'].lower()):
            suggestions.append({
                'name': compound['name'],
                'formula': compound['formula'],
                'id': compound['id']
            })
    
    return jsonify(suggestions)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
