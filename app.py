#!/usr/bin/env python3
"""
ChemVista - Fresh Clean Chemistry Web Application
A modern, responsive chemistry explorer with complete periodic table and compound database
"""

from flask import Flask, render_template, jsonify, request
import json
import os
from functools import lru_cache
import re
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'chemvista-fresh-2025'

# Chemistry constants and data
FAMOUS_CHEMISTS = [
    {
        "name": "Marie Curie",
        "years": "1867-1934",
        "nationality": "Polish-French",
        "discoveries": ["Polonium", "Radium", "Radioactivity research"],
        "achievements": ["First woman to win Nobel Prize", "First person to win Nobel Prizes in two different sciences"],
        "image": "marie_curie.jpg",
        "biography": "Marie Curie was a pioneering physicist and chemist who conducted groundbreaking research on radioactivity. She was the first woman to win a Nobel Prize and the first person to win Nobel Prizes in two different scientific fields."
    },
    {
        "name": "Dmitri Mendeleev",
        "years": "1834-1907",
        "nationality": "Russian",
        "discoveries": ["Periodic Table", "Periodic Law"],
        "achievements": ["Created the first widely recognized periodic table", "Predicted properties of undiscovered elements"],
        "image": "mendeleev.jpg",
        "biography": "Dmitri Mendeleev was a Russian chemist who created the first widely recognized periodic table of elements. His periodic law and table organized all known elements and predicted the properties of elements yet to be discovered."
    },
    {
        "name": "Antoine Lavoisier",
        "years": "1743-1794",
        "nationality": "French",
        "discoveries": ["Conservation of mass", "Role of oxygen in combustion"],
        "achievements": ["Father of modern chemistry", "Developed chemical nomenclature"],
        "image": "lavoisier.jpg",
        "biography": "Known as the 'Father of Modern Chemistry', Lavoisier established the law of conservation of mass and identified oxygen's role in combustion. He developed systematic chemical nomenclature and helped establish chemistry as a quantitative science."
    },
    {
        "name": "Linus Pauling",
        "years": "1901-1994",
        "nationality": "American",
        "discoveries": ["Chemical bonding theory", "Protein structure"],
        "achievements": ["Nobel Prize in Chemistry", "Nobel Peace Prize", "Vitamin C research"],
        "image": "pauling.jpg",
        "biography": "Linus Pauling was one of the most influential chemists in history. He made groundbreaking contributions to understanding chemical bonding and molecular structure, and was awarded Nobel Prizes in both Chemistry and Peace."
    },
    {
        "name": "Robert Boyle",
        "years": "1627-1691",
        "nationality": "Irish",
        "discoveries": ["Boyle's Law", "Distinction between elements and compounds"],
        "achievements": ["Pioneer of modern chemistry", "Established experimental method in chemistry"],
        "image": "boyle.jpg",
        "biography": "Robert Boyle is considered one of the founders of modern chemistry. He distinguished between elements and compounds and formulated Boyle's Law, which describes the relationship between pressure and volume of gases."
    }
]

CHEMISTRY_CONCEPTS = [
    {
        "title": "Atomic Structure",
        "description": "Understanding the building blocks of matter",
        "content": "Atoms consist of protons, neutrons, and electrons. The nucleus contains protons and neutrons, while electrons orbit in shells.",
        "applications": ["Nuclear medicine", "Semiconductor technology", "Chemical bonding"],
        "examples": ["Hydrogen atom", "Carbon isotopes", "Ion formation"]
    },
    {
        "title": "Chemical Bonding",
        "description": "How atoms connect to form molecules",
        "content": "Chemical bonds form when atoms share or transfer electrons. Types include ionic, covalent, and metallic bonds.",
        "applications": ["Drug design", "Material science", "Polymer chemistry"],
        "examples": ["Water molecule", "Salt formation", "Diamond structure"]
    },
    {
        "title": "Thermodynamics",
        "description": "Energy changes in chemical reactions",
        "content": "Chemical thermodynamics studies energy changes during reactions, including enthalpy, entropy, and Gibbs free energy.",
        "applications": ["Industrial processes", "Battery technology", "Environmental chemistry"],
        "examples": ["Combustion reactions", "Phase transitions", "Equilibrium constants"]
    }
]

# Load chemistry data
@lru_cache(maxsize=1)
def load_elements():
    """Load complete periodic table data"""
    elements = [
        {"number": 1, "symbol": "H", "name": "Hydrogen", "atomic_mass": 1.008, "category": "nonmetal", "group": 1, "period": 1, "electron_config": "1s¹", "melting_point": -259.16, "boiling_point": -252.87, "density": 0.00008988, "discovered": 1766, "description": "The most abundant element in the universe, essential for water and life."},
        {"number": 2, "symbol": "He", "name": "Helium", "atomic_mass": 4.003, "category": "noble-gas", "group": 18, "period": 1, "electron_config": "1s²", "melting_point": -272.2, "boiling_point": -268.93, "density": 0.0001785, "discovered": 1868, "description": "Second most abundant element, used in balloons and as a coolant."},
        {"number": 3, "symbol": "Li", "name": "Lithium", "atomic_mass": 6.94, "category": "alkali-metal", "group": 1, "period": 2, "electron_config": "[He] 2s¹", "melting_point": 180.5, "boiling_point": 1342, "density": 0.534, "discovered": 1817, "description": "Lightest metal, used in batteries and mood stabilizers."},
        {"number": 4, "symbol": "Be", "name": "Beryllium", "atomic_mass": 9.012, "category": "alkaline-earth-metal", "group": 2, "period": 2, "electron_config": "[He] 2s²", "melting_point": 1287, "boiling_point": 2468, "density": 1.85, "discovered": 1798, "description": "Strong, lightweight metal used in aerospace applications."},
        {"number": 5, "symbol": "B", "name": "Boron", "atomic_mass": 10.81, "category": "metalloid", "group": 13, "period": 2, "electron_config": "[He] 2s² 2p¹", "melting_point": 2076, "boiling_point": 3927, "density": 2.34, "discovered": 1808, "description": "Essential for plant growth, used in glass and ceramics."},
        {"number": 6, "symbol": "C", "name": "Carbon", "atomic_mass": 12.011, "category": "nonmetal", "group": 14, "period": 2, "electron_config": "[He] 2s² 2p²", "melting_point": 3550, "boiling_point": 4027, "density": 2.267, "discovered": "Ancient", "description": "Basis of all organic chemistry and life on Earth."},
        {"number": 7, "symbol": "N", "name": "Nitrogen", "atomic_mass": 14.007, "category": "nonmetal", "group": 15, "period": 2, "electron_config": "[He] 2s² 2p³", "melting_point": -210.0, "boiling_point": -195.79, "density": 0.0012506, "discovered": 1772, "description": "Makes up 78% of Earth's atmosphere, essential for proteins."},
        {"number": 8, "symbol": "O", "name": "Oxygen", "atomic_mass": 15.999, "category": "nonmetal", "group": 16, "period": 2, "electron_config": "[He] 2s² 2p⁴", "melting_point": -218.79, "boiling_point": -182.962, "density": 0.001429, "discovered": 1774, "description": "Essential for respiration and combustion processes."},
        {"number": 9, "symbol": "F", "name": "Fluorine", "atomic_mass": 18.998, "category": "halogen", "group": 17, "period": 2, "electron_config": "[He] 2s² 2p⁵", "melting_point": -219.67, "boiling_point": -188.11, "density": 0.001696, "discovered": 1886, "description": "Most electronegative element, used in toothpaste and Teflon."},
        {"number": 10, "symbol": "Ne", "name": "Neon", "atomic_mass": 20.180, "category": "noble-gas", "group": 18, "period": 2, "electron_config": "[He] 2s² 2p⁶", "melting_point": -248.59, "boiling_point": -246.053, "density": 0.0008999, "discovered": 1898, "description": "Inert gas used in bright advertising signs."},
        {"number": 11, "symbol": "Na", "name": "Sodium", "atomic_mass": 22.990, "category": "alkali-metal", "group": 1, "period": 3, "electron_config": "[Ne] 3s¹", "melting_point": 97.794, "boiling_point": 883, "density": 0.971, "discovered": 1807, "description": "Essential for nerve function, found in salt."},
        {"number": 12, "symbol": "Mg", "name": "Magnesium", "atomic_mass": 24.305, "category": "alkaline-earth-metal", "group": 2, "period": 3, "electron_config": "[Ne] 3s²", "melting_point": 650, "boiling_point": 1090, "density": 1.74, "discovered": 1755, "description": "Essential for chlorophyll and enzyme function."},
        {"number": 13, "symbol": "Al", "name": "Aluminum", "atomic_mass": 26.982, "category": "post-transition-metal", "group": 13, "period": 3, "electron_config": "[Ne] 3s² 3p¹", "melting_point": 660.32, "boiling_point": 2519, "density": 2.70, "discovered": 1825, "description": "Lightweight, corrosion-resistant metal used in packaging."},
        {"number": 14, "symbol": "Si", "name": "Silicon", "atomic_mass": 28.086, "category": "metalloid", "group": 14, "period": 3, "electron_config": "[Ne] 3s² 3p²", "melting_point": 1414, "boiling_point": 3265, "density": 2.3296, "discovered": 1824, "description": "Second most abundant element in Earth's crust, basis of semiconductors."},
        {"number": 15, "symbol": "P", "name": "Phosphorus", "atomic_mass": 30.974, "category": "nonmetal", "group": 15, "period": 3, "electron_config": "[Ne] 3s² 3p³", "melting_point": 44.15, "boiling_point": 280.5, "density": 1.82, "discovered": 1669, "description": "Essential for DNA, RNA, and energy storage in cells."},
        {"number": 16, "symbol": "S", "name": "Sulfur", "atomic_mass": 32.065, "category": "nonmetal", "group": 16, "period": 3, "electron_config": "[Ne] 3s² 3p⁴", "melting_point": 115.21, "boiling_point": 444.61, "density": 2.067, "discovered": "Ancient", "description": "Important for protein structure and industrial chemicals."},
        {"number": 17, "symbol": "Cl", "name": "Chlorine", "atomic_mass": 35.453, "category": "halogen", "group": 17, "period": 3, "electron_config": "[Ne] 3s² 3p⁵", "melting_point": -101.5, "boiling_point": -34.04, "density": 0.003214, "discovered": 1774, "description": "Used for water purification and disinfection."},
        {"number": 18, "symbol": "Ar", "name": "Argon", "atomic_mass": 39.948, "category": "noble-gas", "group": 18, "period": 3, "electron_config": "[Ne] 3s² 3p⁶", "melting_point": -189.35, "boiling_point": -185.85, "density": 0.0017837, "discovered": 1894, "description": "Inert gas used in welding and light bulbs."},
        # Adding more elements for completeness
        {"number": 19, "symbol": "K", "name": "Potassium", "atomic_mass": 39.098, "category": "alkali-metal", "group": 1, "period": 4, "electron_config": "[Ar] 4s¹", "melting_point": 63.5, "boiling_point": 759, "density": 0.862, "discovered": 1807, "description": "Essential for nerve and muscle function."},
        {"number": 20, "symbol": "Ca", "name": "Calcium", "atomic_mass": 40.078, "category": "alkaline-earth-metal", "group": 2, "period": 4, "electron_config": "[Ar] 4s²", "melting_point": 842, "boiling_point": 1484, "density": 1.54, "discovered": 1808, "description": "Essential for bones and teeth."},
        # Continue with transition metals
        {"number": 21, "symbol": "Sc", "name": "Scandium", "atomic_mass": 44.956, "category": "transition-metal", "group": 3, "period": 4, "electron_config": "[Ar] 3d¹ 4s²", "melting_point": 1541, "boiling_point": 2836, "density": 2.99, "discovered": 1879, "description": "Rare earth metal used in aerospace alloys."},
        {"number": 22, "symbol": "Ti", "name": "Titanium", "atomic_mass": 47.867, "category": "transition-metal", "group": 4, "period": 4, "electron_config": "[Ar] 3d² 4s²", "melting_point": 1668, "boiling_point": 3287, "density": 4.506, "discovered": 1791, "description": "Strong, lightweight metal used in aerospace and medical implants."},
        {"number": 23, "symbol": "V", "name": "Vanadium", "atomic_mass": 50.942, "category": "transition-metal", "group": 5, "period": 4, "electron_config": "[Ar] 3d³ 4s²", "melting_point": 1910, "boiling_point": 3407, "density": 6.11, "discovered": 1801, "description": "Used in steel alloys for strength and corrosion resistance."},
        {"number": 24, "symbol": "Cr", "name": "Chromium", "atomic_mass": 51.996, "category": "transition-metal", "group": 6, "period": 4, "electron_config": "[Ar] 3d⁵ 4s¹", "melting_point": 1907, "boiling_point": 2671, "density": 7.15, "discovered": 1797, "description": "Used for chrome plating and stainless steel."},
        {"number": 25, "symbol": "Mn", "name": "Manganese", "atomic_mass": 54.938, "category": "transition-metal", "group": 7, "period": 4, "electron_config": "[Ar] 3d⁵ 4s²", "melting_point": 1246, "boiling_point": 2061, "density": 7.44, "discovered": 1774, "description": "Essential for steel production and enzyme function."},
        {"number": 26, "symbol": "Fe", "name": "Iron", "atomic_mass": 55.845, "category": "transition-metal", "group": 8, "period": 4, "electron_config": "[Ar] 3d⁶ 4s²", "melting_point": 1538, "boiling_point": 2862, "density": 7.874, "discovered": "Ancient", "description": "Most important metal for civilization, essential for blood."},
        {"number": 27, "symbol": "Co", "name": "Cobalt", "atomic_mass": 58.933, "category": "transition-metal", "group": 9, "period": 4, "electron_config": "[Ar] 3d⁷ 4s²", "melting_point": 1495, "boiling_point": 2927, "density": 8.86, "discovered": 1735, "description": "Used in batteries and as a blue pigment."},
        {"number": 28, "symbol": "Ni", "name": "Nickel", "atomic_mass": 58.693, "category": "transition-metal", "group": 10, "period": 4, "electron_config": "[Ar] 3d⁸ 4s²", "melting_point": 1455, "boiling_point": 2913, "density": 8.912, "discovered": 1751, "description": "Used in coins, stainless steel, and batteries."},
        {"number": 29, "symbol": "Cu", "name": "Copper", "atomic_mass": 63.546, "category": "transition-metal", "group": 11, "period": 4, "electron_config": "[Ar] 3d¹⁰ 4s¹", "melting_point": 1084.62, "boiling_point": 2562, "density": 8.96, "discovered": "Ancient", "description": "Excellent electrical conductor, used in wiring and plumbing."},
        {"number": 30, "symbol": "Zn", "name": "Zinc", "atomic_mass": 65.38, "category": "transition-metal", "group": 12, "period": 4, "electron_config": "[Ar] 3d¹⁰ 4s²", "melting_point": 419.53, "boiling_point": 907, "density": 7.134, "discovered": "Ancient", "description": "Essential nutrient and used for galvanizing steel."},
        # Continue with more periods...
        {"number": 31, "symbol": "Ga", "name": "Gallium", "atomic_mass": 69.723, "category": "post-transition-metal", "group": 13, "period": 4, "electron_config": "[Ar] 3d¹⁰ 4s² 4p¹", "melting_point": 29.76, "boiling_point": 2204, "density": 5.907, "discovered": 1875, "description": "Used in semiconductors and LEDs."},
        {"number": 32, "symbol": "Ge", "name": "Germanium", "atomic_mass": 72.630, "category": "metalloid", "group": 14, "period": 4, "electron_config": "[Ar] 3d¹⁰ 4s² 4p²", "melting_point": 938.25, "boiling_point": 2833, "density": 5.323, "discovered": 1886, "description": "Important semiconductor material."},
        {"number": 33, "symbol": "As", "name": "Arsenic", "atomic_mass": 74.922, "category": "metalloid", "group": 15, "period": 4, "electron_config": "[Ar] 3d¹⁰ 4s² 4p³", "melting_point": 817, "boiling_point": 614, "density": 5.776, "discovered": "Ancient", "description": "Toxic metalloid used in semiconductors."},
        {"number": 34, "symbol": "Se", "name": "Selenium", "atomic_mass": 78.971, "category": "nonmetal", "group": 16, "period": 4, "electron_config": "[Ar] 3d¹⁰ 4s² 4p⁴", "melting_point": 221, "boiling_point": 685, "density": 4.809, "discovered": 1817, "description": "Essential nutrient and used in electronics."},
        {"number": 35, "symbol": "Br", "name": "Bromine", "atomic_mass": 79.904, "category": "halogen", "group": 17, "period": 4, "electron_config": "[Ar] 3d¹⁰ 4s² 4p⁵", "melting_point": -7.2, "boiling_point": 58.8, "density": 3.122, "discovered": 1826, "description": "Red-brown liquid used in flame retardants."},
        {"number": 36, "symbol": "Kr", "name": "Krypton", "atomic_mass": 83.798, "category": "noble-gas", "group": 18, "period": 4, "electron_config": "[Ar] 3d¹⁰ 4s² 4p⁶", "melting_point": -157.36, "boiling_point": -153.22, "density": 0.003733, "discovered": 1898, "description": "Noble gas used in specialized lighting."},
    ]
    
    # Add remaining elements up to 118 with basic data
    additional_elements = [
        {"number": 37, "symbol": "Rb", "name": "Rubidium", "atomic_mass": 85.468, "category": "alkali-metal", "group": 1, "period": 5},
        {"number": 38, "symbol": "Sr", "name": "Strontium", "atomic_mass": 87.62, "category": "alkaline-earth-metal", "group": 2, "period": 5},
        {"number": 39, "symbol": "Y", "name": "Yttrium", "atomic_mass": 88.906, "category": "transition-metal", "group": 3, "period": 5},
        {"number": 40, "symbol": "Zr", "name": "Zirconium", "atomic_mass": 91.224, "category": "transition-metal", "group": 4, "period": 5},
        {"number": 41, "symbol": "Nb", "name": "Niobium", "atomic_mass": 92.906, "category": "transition-metal", "group": 5, "period": 5},
        {"number": 42, "symbol": "Mo", "name": "Molybdenum", "atomic_mass": 95.95, "category": "transition-metal", "group": 6, "period": 5},
        {"number": 43, "symbol": "Tc", "name": "Technetium", "atomic_mass": 98, "category": "transition-metal", "group": 7, "period": 5},
        {"number": 44, "symbol": "Ru", "name": "Ruthenium", "atomic_mass": 101.07, "category": "transition-metal", "group": 8, "period": 5},
        {"number": 45, "symbol": "Rh", "name": "Rhodium", "atomic_mass": 102.91, "category": "transition-metal", "group": 9, "period": 5},
        {"number": 46, "symbol": "Pd", "name": "Palladium", "atomic_mass": 106.42, "category": "transition-metal", "group": 10, "period": 5},
        {"number": 47, "symbol": "Ag", "name": "Silver", "atomic_mass": 107.87, "category": "transition-metal", "group": 11, "period": 5},
        {"number": 48, "symbol": "Cd", "name": "Cadmium", "atomic_mass": 112.41, "category": "transition-metal", "group": 12, "period": 5},
        {"number": 49, "symbol": "In", "name": "Indium", "atomic_mass": 114.82, "category": "post-transition-metal", "group": 13, "period": 5},
        {"number": 50, "symbol": "Sn", "name": "Tin", "atomic_mass": 118.71, "category": "post-transition-metal", "group": 14, "period": 5},
        {"number": 51, "symbol": "Sb", "name": "Antimony", "atomic_mass": 121.76, "category": "metalloid", "group": 15, "period": 5},
        {"number": 52, "symbol": "Te", "name": "Tellurium", "atomic_mass": 127.60, "category": "metalloid", "group": 16, "period": 5},
        {"number": 53, "symbol": "I", "name": "Iodine", "atomic_mass": 126.90, "category": "halogen", "group": 17, "period": 5},
        {"number": 54, "symbol": "Xe", "name": "Xenon", "atomic_mass": 131.29, "category": "noble-gas", "group": 18, "period": 5},
        {"number": 55, "symbol": "Cs", "name": "Cesium", "atomic_mass": 132.91, "category": "alkali-metal", "group": 1, "period": 6},
        {"number": 56, "symbol": "Ba", "name": "Barium", "atomic_mass": 137.33, "category": "alkaline-earth-metal", "group": 2, "period": 6},
        {"number": 57, "symbol": "La", "name": "Lanthanum", "atomic_mass": 138.91, "category": "lanthanide", "group": 0, "period": 6},
        {"number": 58, "symbol": "Ce", "name": "Cerium", "atomic_mass": 140.12, "category": "lanthanide", "group": 0, "period": 6},
        {"number": 59, "symbol": "Pr", "name": "Praseodymium", "atomic_mass": 140.91, "category": "lanthanide", "group": 0, "period": 6},
        {"number": 60, "symbol": "Nd", "name": "Neodymium", "atomic_mass": 144.24, "category": "lanthanide", "group": 0, "period": 6},
        {"number": 61, "symbol": "Pm", "name": "Promethium", "atomic_mass": 145, "category": "lanthanide", "group": 0, "period": 6},
        {"number": 62, "symbol": "Sm", "name": "Samarium", "atomic_mass": 150.36, "category": "lanthanide", "group": 0, "period": 6},
        {"number": 63, "symbol": "Eu", "name": "Europium", "atomic_mass": 151.96, "category": "lanthanide", "group": 0, "period": 6},
        {"number": 64, "symbol": "Gd", "name": "Gadolinium", "atomic_mass": 157.25, "category": "lanthanide", "group": 0, "period": 6},
        {"number": 65, "symbol": "Tb", "name": "Terbium", "atomic_mass": 158.93, "category": "lanthanide", "group": 0, "period": 6},
        {"number": 66, "symbol": "Dy", "name": "Dysprosium", "atomic_mass": 162.50, "category": "lanthanide", "group": 0, "period": 6},
        {"number": 67, "symbol": "Ho", "name": "Holmium", "atomic_mass": 164.93, "category": "lanthanide", "group": 0, "period": 6},
        {"number": 68, "symbol": "Er", "name": "Erbium", "atomic_mass": 167.26, "category": "lanthanide", "group": 0, "period": 6},
        {"number": 69, "symbol": "Tm", "name": "Thulium", "atomic_mass": 168.93, "category": "lanthanide", "group": 0, "period": 6},
        {"number": 70, "symbol": "Yb", "name": "Ytterbium", "atomic_mass": 173.05, "category": "lanthanide", "group": 0, "period": 6},
        {"number": 71, "symbol": "Lu", "name": "Lutetium", "atomic_mass": 174.97, "category": "lanthanide", "group": 0, "period": 6},
        {"number": 72, "symbol": "Hf", "name": "Hafnium", "atomic_mass": 178.49, "category": "transition-metal", "group": 4, "period": 6},
        {"number": 73, "symbol": "Ta", "name": "Tantalum", "atomic_mass": 180.95, "category": "transition-metal", "group": 5, "period": 6},
        {"number": 74, "symbol": "W", "name": "Tungsten", "atomic_mass": 183.84, "category": "transition-metal", "group": 6, "period": 6},
        {"number": 75, "symbol": "Re", "name": "Rhenium", "atomic_mass": 186.21, "category": "transition-metal", "group": 7, "period": 6},
        {"number": 76, "symbol": "Os", "name": "Osmium", "atomic_mass": 190.23, "category": "transition-metal", "group": 8, "period": 6},
        {"number": 77, "symbol": "Ir", "name": "Iridium", "atomic_mass": 192.22, "category": "transition-metal", "group": 9, "period": 6},
        {"number": 78, "symbol": "Pt", "name": "Platinum", "atomic_mass": 195.08, "category": "transition-metal", "group": 10, "period": 6},
        {"number": 79, "symbol": "Au", "name": "Gold", "atomic_mass": 196.97, "category": "transition-metal", "group": 11, "period": 6},
        {"number": 80, "symbol": "Hg", "name": "Mercury", "atomic_mass": 200.59, "category": "transition-metal", "group": 12, "period": 6},
        {"number": 81, "symbol": "Tl", "name": "Thallium", "atomic_mass": 204.38, "category": "post-transition-metal", "group": 13, "period": 6},
        {"number": 82, "symbol": "Pb", "name": "Lead", "atomic_mass": 207.2, "category": "post-transition-metal", "group": 14, "period": 6},
        {"number": 83, "symbol": "Bi", "name": "Bismuth", "atomic_mass": 208.98, "category": "post-transition-metal", "group": 15, "period": 6},
        {"number": 84, "symbol": "Po", "name": "Polonium", "atomic_mass": 209, "category": "post-transition-metal", "group": 16, "period": 6},
        {"number": 85, "symbol": "At", "name": "Astatine", "atomic_mass": 210, "category": "halogen", "group": 17, "period": 6},
        {"number": 86, "symbol": "Rn", "name": "Radon", "atomic_mass": 222, "category": "noble-gas", "group": 18, "period": 6},
        {"number": 87, "symbol": "Fr", "name": "Francium", "atomic_mass": 223, "category": "alkali-metal", "group": 1, "period": 7},
        {"number": 88, "symbol": "Ra", "name": "Radium", "atomic_mass": 226, "category": "alkaline-earth-metal", "group": 2, "period": 7},
        {"number": 89, "symbol": "Ac", "name": "Actinium", "atomic_mass": 227, "category": "actinide", "group": 0, "period": 7},
        {"number": 90, "symbol": "Th", "name": "Thorium", "atomic_mass": 232.04, "category": "actinide", "group": 0, "period": 7},
        {"number": 91, "symbol": "Pa", "name": "Protactinium", "atomic_mass": 231.04, "category": "actinide", "group": 0, "period": 7},
        {"number": 92, "symbol": "U", "name": "Uranium", "atomic_mass": 238.03, "category": "actinide", "group": 0, "period": 7},
        {"number": 93, "symbol": "Np", "name": "Neptunium", "atomic_mass": 237, "category": "actinide", "group": 0, "period": 7},
        {"number": 94, "symbol": "Pu", "name": "Plutonium", "atomic_mass": 244, "category": "actinide", "group": 0, "period": 7},
        {"number": 95, "symbol": "Am", "name": "Americium", "atomic_mass": 243, "category": "actinide", "group": 0, "period": 7},
        {"number": 96, "symbol": "Cm", "name": "Curium", "atomic_mass": 247, "category": "actinide", "group": 0, "period": 7},
        {"number": 97, "symbol": "Bk", "name": "Berkelium", "atomic_mass": 247, "category": "actinide", "group": 0, "period": 7},
        {"number": 98, "symbol": "Cf", "name": "Californium", "atomic_mass": 251, "category": "actinide", "group": 0, "period": 7},
        {"number": 99, "symbol": "Es", "name": "Einsteinium", "atomic_mass": 252, "category": "actinide", "group": 0, "period": 7},
        {"number": 100, "symbol": "Fm", "name": "Fermium", "atomic_mass": 257, "category": "actinide", "group": 0, "period": 7},
        {"number": 101, "symbol": "Md", "name": "Mendelevium", "atomic_mass": 258, "category": "actinide", "group": 0, "period": 7},
        {"number": 102, "symbol": "No", "name": "Nobelium", "atomic_mass": 259, "category": "actinide", "group": 0, "period": 7},
        {"number": 103, "symbol": "Lr", "name": "Lawrencium", "atomic_mass": 262, "category": "actinide", "group": 0, "period": 7},
        {"number": 104, "symbol": "Rf", "name": "Rutherfordium", "atomic_mass": 267, "category": "transition-metal", "group": 4, "period": 7},
        {"number": 105, "symbol": "Db", "name": "Dubnium", "atomic_mass": 270, "category": "transition-metal", "group": 5, "period": 7},
        {"number": 106, "symbol": "Sg", "name": "Seaborgium", "atomic_mass": 271, "category": "transition-metal", "group": 6, "period": 7},
        {"number": 107, "symbol": "Bh", "name": "Bohrium", "atomic_mass": 270, "category": "transition-metal", "group": 7, "period": 7},
        {"number": 108, "symbol": "Hs", "name": "Hassium", "atomic_mass": 277, "category": "transition-metal", "group": 8, "period": 7},
        {"number": 109, "symbol": "Mt", "name": "Meitnerium", "atomic_mass": 276, "category": "transition-metal", "group": 9, "period": 7},
        {"number": 110, "symbol": "Ds", "name": "Darmstadtium", "atomic_mass": 281, "category": "transition-metal", "group": 10, "period": 7},
        {"number": 111, "symbol": "Rg", "name": "Roentgenium", "atomic_mass": 280, "category": "transition-metal", "group": 11, "period": 7},
        {"number": 112, "symbol": "Cn", "name": "Copernicium", "atomic_mass": 285, "category": "transition-metal", "group": 12, "period": 7},
        {"number": 113, "symbol": "Nh", "name": "Nihonium", "atomic_mass": 284, "category": "post-transition-metal", "group": 13, "period": 7},
        {"number": 114, "symbol": "Fl", "name": "Flerovium", "atomic_mass": 289, "category": "post-transition-metal", "group": 14, "period": 7},
        {"number": 115, "symbol": "Mc", "name": "Moscovium", "atomic_mass": 288, "category": "post-transition-metal", "group": 15, "period": 7},
        {"number": 116, "symbol": "Lv", "name": "Livermorium", "atomic_mass": 293, "category": "post-transition-metal", "group": 16, "period": 7},
        {"number": 117, "symbol": "Ts", "name": "Tennessine", "atomic_mass": 294, "category": "halogen", "group": 17, "period": 7},
        {"number": 118, "symbol": "Og", "name": "Oganesson", "atomic_mass": 294, "category": "noble-gas", "group": 18, "period": 7},
    ]
    
    # Merge additional elements with main elements
    elements.extend(additional_elements)
    return elements

@lru_cache(maxsize=1)
def load_compounds():
    """Load comprehensive chemical compounds database"""
    return [
        # Common Molecular Compounds
        {"formula": "H2O", "name": "Water", "molecular_weight": 18.015, "category": "molecular", "description": "Essential for all life on Earth", "uses": ["Drinking", "Cleaning", "Industrial solvent"], "state": "liquid", "common_name": "Water", "hazards": ["None at normal conditions"]},
        {"formula": "CO2", "name": "Carbon Dioxide", "molecular_weight": 44.010, "category": "molecular", "description": "Greenhouse gas produced by respiration and combustion", "uses": ["Carbonated drinks", "Fire extinguisher", "Dry ice"], "state": "gas", "common_name": "Carbon dioxide", "hazards": ["Asphyxiant in high concentrations"]},
        {"formula": "O2", "name": "Oxygen", "molecular_weight": 31.998, "category": "molecular", "description": "Essential gas for respiration", "uses": ["Breathing", "Combustion", "Medical treatment"], "state": "gas", "common_name": "Oxygen", "hazards": ["Supports combustion"]},
        {"formula": "N2", "name": "Nitrogen", "molecular_weight": 28.014, "category": "molecular", "description": "Makes up 78% of Earth's atmosphere", "uses": ["Inert atmosphere", "Fertilizer production", "Food packaging"], "state": "gas", "common_name": "Nitrogen", "hazards": ["Asphyxiant in high concentrations"]},
        {"formula": "NH3", "name": "Ammonia", "molecular_weight": 17.031, "category": "molecular", "description": "Pungent gas used in cleaning and fertilizers", "uses": ["Cleaning products", "Fertilizer production", "Refrigerant"], "state": "gas", "common_name": "Ammonia", "hazards": ["Corrosive", "Toxic"]},
        {"formula": "H2O2", "name": "Hydrogen Peroxide", "molecular_weight": 34.015, "category": "molecular", "description": "Bleaching and disinfecting agent", "uses": ["Disinfectant", "Bleaching", "Rocket fuel"], "state": "liquid", "common_name": "Hydrogen peroxide", "hazards": ["Oxidizer", "Skin irritant"]},
        {"formula": "NO", "name": "Nitric Oxide", "molecular_weight": 30.006, "category": "molecular", "description": "Important signaling molecule in biology", "uses": ["Medical gas", "Chemical intermediate"], "state": "gas", "common_name": "Nitric oxide", "hazards": ["Toxic"]},
        {"formula": "NO2", "name": "Nitrogen Dioxide", "molecular_weight": 46.006, "category": "molecular", "description": "Brown gas, air pollutant", "uses": ["Chemical production"], "state": "gas", "common_name": "Nitrogen dioxide", "hazards": ["Toxic", "Corrosive"]},
        {"formula": "SO2", "name": "Sulfur Dioxide", "molecular_weight": 64.066, "category": "molecular", "description": "Preservative and bleaching agent", "uses": ["Food preservative", "Wine production"], "state": "gas", "common_name": "Sulfur dioxide", "hazards": ["Toxic", "Respiratory irritant"]},
        {"formula": "SO3", "name": "Sulfur Trioxide", "molecular_weight": 80.066, "category": "molecular", "description": "Used to make sulfuric acid", "uses": ["Sulfuric acid production"], "state": "liquid", "common_name": "Sulfur trioxide", "hazards": ["Highly corrosive"]},
        
        # Organic Compounds
        {"formula": "CH4", "name": "Methane", "molecular_weight": 16.043, "category": "organic", "description": "Simplest hydrocarbon and major component of natural gas", "uses": ["Fuel", "Heating", "Chemical feedstock"], "state": "gas", "common_name": "Natural gas", "hazards": ["Flammable", "Asphyxiant"]},
        {"formula": "C2H4", "name": "Ethylene", "molecular_weight": 28.054, "category": "organic", "description": "Plant hormone and polymer precursor", "uses": ["Plastic production", "Fruit ripening"], "state": "gas", "common_name": "Ethylene", "hazards": ["Flammable"]},
        {"formula": "C2H6", "name": "Ethane", "molecular_weight": 30.070, "category": "organic", "description": "Component of natural gas", "uses": ["Fuel", "Chemical feedstock"], "state": "gas", "common_name": "Ethane", "hazards": ["Flammable"]},
        {"formula": "C2H2", "name": "Acetylene", "molecular_weight": 26.038, "category": "organic", "description": "Fuel gas for welding", "uses": ["Welding", "Cutting"], "state": "gas", "common_name": "Acetylene", "hazards": ["Highly flammable", "Explosive"]},
        {"formula": "C3H8", "name": "Propane", "molecular_weight": 44.096, "category": "organic", "description": "Gas used for heating and cooking", "uses": ["Fuel", "Refrigerant", "Aerosol propellant"], "state": "gas", "common_name": "Propane", "hazards": ["Flammable"]},
        {"formula": "C4H10", "name": "Butane", "molecular_weight": 58.122, "category": "organic", "description": "Gas used in lighters", "uses": ["Lighter fuel", "Aerosol propellant", "Refrigerant"], "state": "gas", "common_name": "Butane", "hazards": ["Flammable"]},
        {"formula": "C6H6", "name": "Benzene", "molecular_weight": 78.114, "category": "organic", "description": "Aromatic hydrocarbon, important industrial chemical", "uses": ["Chemical production", "Solvent"], "state": "liquid", "common_name": "Benzene", "hazards": ["Carcinogenic", "Flammable"]},
        {"formula": "C8H18", "name": "Octane", "molecular_weight": 114.232, "category": "organic", "description": "Component of gasoline", "uses": ["Fuel", "Solvent"], "state": "liquid", "common_name": "Octane", "hazards": ["Flammable"]},
        {"formula": "C2H5OH", "name": "Ethanol", "molecular_weight": 46.068, "category": "organic", "description": "Alcohol found in alcoholic beverages", "uses": ["Beverages", "Fuel additive", "Solvent"], "state": "liquid", "common_name": "Alcohol", "hazards": ["Flammable", "Intoxicating"]},
        {"formula": "CH3OH", "name": "Methanol", "molecular_weight": 32.042, "category": "organic", "description": "Simple alcohol, toxic", "uses": ["Fuel", "Solvent", "Antifreeze"], "state": "liquid", "common_name": "Methanol", "hazards": ["Toxic", "Flammable"]},
        {"formula": "CH3COOH", "name": "Acetic Acid", "molecular_weight": 60.052, "category": "organic", "description": "Main component of vinegar", "uses": ["Food preservative", "Chemical production"], "state": "liquid", "common_name": "Vinegar", "hazards": ["Corrosive"]},
        {"formula": "HCHO", "name": "Formaldehyde", "molecular_weight": 30.026, "category": "organic", "description": "Preservative and disinfectant", "uses": ["Preservative", "Disinfectant"], "state": "gas", "common_name": "Formaldehyde", "hazards": ["Carcinogenic", "Toxic"]},
        
        # Sugars and Biological Compounds
        {"formula": "C6H12O6", "name": "Glucose", "molecular_weight": 180.156, "category": "organic", "description": "Simple sugar and primary energy source for cells", "uses": ["Energy production", "Food sweetener", "Medical treatment"], "state": "solid", "common_name": "Blood sugar", "hazards": ["None"]},
        {"formula": "C12H22O11", "name": "Sucrose", "molecular_weight": 342.297, "category": "organic", "description": "Common table sugar", "uses": ["Food sweetener", "Preservative", "Energy source"], "state": "solid", "common_name": "Table sugar", "hazards": ["None"]},
        {"formula": "C6H8O7", "name": "Citric Acid", "molecular_weight": 192.124, "category": "organic", "description": "Natural acid found in citrus fruits", "uses": ["Food flavoring", "Preservative", "Cleaning agent"], "state": "solid", "common_name": "Citric acid", "hazards": ["Mild irritant"]},
        {"formula": "C8H10N4O2", "name": "Caffeine", "molecular_weight": 194.191, "category": "organic", "description": "Stimulant found in coffee and tea", "uses": ["Beverages", "Medications", "Cosmetics"], "state": "solid", "common_name": "Caffeine", "hazards": ["Stimulant"]},
        
        # Ionic Compounds - Salts
        {"formula": "NaCl", "name": "Sodium Chloride", "molecular_weight": 58.443, "category": "ionic", "description": "Common table salt", "uses": ["Food seasoning", "De-icing roads", "Chemical production"], "state": "solid", "common_name": "Table salt", "hazards": ["None at normal usage"]},
        {"formula": "KCl", "name": "Potassium Chloride", "molecular_weight": 74.551, "category": "ionic", "description": "Salt substitute and fertilizer", "uses": ["Fertilizer", "Food additive", "Medical treatment"], "state": "solid", "common_name": "Potassium chloride", "hazards": ["None at normal usage"]},
        {"formula": "CaCl2", "name": "Calcium Chloride", "molecular_weight": 110.984, "category": "ionic", "description": "De-icing agent and desiccant", "uses": ["De-icing", "Drying agent", "Food additive"], "state": "solid", "common_name": "Calcium chloride", "hazards": ["Hygroscopic"]},
        {"formula": "MgCl2", "name": "Magnesium Chloride", "molecular_weight": 95.211, "category": "ionic", "description": "De-icing agent", "uses": ["De-icing", "Dust control"], "state": "solid", "common_name": "Magnesium chloride", "hazards": ["Mild irritant"]},
        {"formula": "NaHCO3", "name": "Sodium Bicarbonate", "molecular_weight": 84.007, "category": "ionic", "description": "Baking soda", "uses": ["Baking", "Antacid", "Cleaning"], "state": "solid", "common_name": "Baking soda", "hazards": ["None"]},
        {"formula": "Na2CO3", "name": "Sodium Carbonate", "molecular_weight": 105.988, "category": "ionic", "description": "Washing soda", "uses": ["Cleaning", "Glass production"], "state": "solid", "common_name": "Washing soda", "hazards": ["Alkaline"]},
        
        # Oxides
        {"formula": "CaCO3", "name": "Calcium Carbonate", "molecular_weight": 100.087, "category": "ionic", "description": "Main component of limestone and marble", "uses": ["Construction material", "Paper production", "Antacid"], "state": "solid", "common_name": "Limestone", "hazards": ["None"]},
        {"formula": "CaO", "name": "Calcium Oxide", "molecular_weight": 56.077, "category": "ionic", "description": "Also known as quicklime", "uses": ["Cement production", "Steel making", "Water treatment"], "state": "solid", "common_name": "Quicklime", "hazards": ["Caustic"]},
        {"formula": "MgO", "name": "Magnesium Oxide", "molecular_weight": 40.304, "category": "ionic", "description": "Refractory material", "uses": ["Refractory lining", "Antacid", "Supplements"], "state": "solid", "common_name": "Magnesia", "hazards": ["None"]},
        {"formula": "Al2O3", "name": "Aluminum Oxide", "molecular_weight": 101.961, "category": "ionic", "description": "Very hard compound used as abrasive", "uses": ["Abrasive", "Refractory material", "Catalyst support"], "state": "solid", "common_name": "Alumina", "hazards": ["None"]},
        {"formula": "Fe2O3", "name": "Iron(III) Oxide", "molecular_weight": 159.688, "category": "ionic", "description": "Common rust compound", "uses": ["Pigment", "Polishing compound", "Magnetic material"], "state": "solid", "common_name": "Rust", "hazards": ["None"]},
        {"formula": "SiO2", "name": "Silicon Dioxide", "molecular_weight": 60.084, "category": "covalent", "description": "Main component of sand and glass", "uses": ["Glass production", "Electronics", "Construction"], "state": "solid", "common_name": "Silica", "hazards": ["Respiratory irritant when inhaled"]},
        {"formula": "TiO2", "name": "Titanium Dioxide", "molecular_weight": 79.866, "category": "ionic", "description": "White pigment", "uses": ["Paint", "Sunscreen", "Food coloring"], "state": "solid", "common_name": "Titanium white", "hazards": ["None"]},
        
        # Acids and Bases
        {"formula": "HCl", "name": "Hydrochloric Acid", "molecular_weight": 36.461, "category": "acid", "description": "Strong acid found in stomach acid", "uses": ["Stomach digestion", "Metal cleaning", "Chemical production"], "state": "gas", "common_name": "Muriatic acid", "hazards": ["Highly corrosive"]},
        {"formula": "H2SO4", "name": "Sulfuric Acid", "molecular_weight": 98.079, "category": "acid", "description": "Strong acid used in many industrial processes", "uses": ["Battery acid", "Chemical production", "Metal processing"], "state": "liquid", "common_name": "Battery acid", "hazards": ["Highly corrosive"]},
        {"formula": "HNO3", "name": "Nitric Acid", "molecular_weight": 63.012, "category": "acid", "description": "Strong oxidizing acid", "uses": ["Fertilizer production", "Explosives"], "state": "liquid", "common_name": "Nitric acid", "hazards": ["Highly corrosive", "Oxidizer"]},
        {"formula": "H3PO4", "name": "Phosphoric Acid", "molecular_weight": 97.994, "category": "acid", "description": "Used in food and fertilizers", "uses": ["Food additive", "Fertilizer production"], "state": "liquid", "common_name": "Phosphoric acid", "hazards": ["Corrosive"]},
        {"formula": "NaOH", "name": "Sodium Hydroxide", "molecular_weight": 39.997, "category": "base", "description": "Strong base, caustic soda", "uses": ["Soap making", "Drain cleaner"], "state": "solid", "common_name": "Lye", "hazards": ["Highly caustic"]},
        {"formula": "KOH", "name": "Potassium Hydroxide", "molecular_weight": 56.106, "category": "base", "description": "Strong base", "uses": ["Soap making", "Battery electrolyte"], "state": "solid", "common_name": "Caustic potash", "hazards": ["Highly caustic"]},
        {"formula": "Ca(OH)2", "name": "Calcium Hydroxide", "molecular_weight": 74.093, "category": "base", "description": "Slaked lime", "uses": ["Water treatment", "Mortar"], "state": "solid", "common_name": "Slaked lime", "hazards": ["Caustic"]},
        
        # Fertilizers
        {"formula": "NH4NO3", "name": "Ammonium Nitrate", "molecular_weight": 80.043, "category": "ionic", "description": "Common fertilizer", "uses": ["Fertilizer", "Explosives"], "state": "solid", "common_name": "Ammonium nitrate", "hazards": ["Oxidizer", "Explosive when contaminated"]},
        {"formula": "(NH4)2SO4", "name": "Ammonium Sulfate", "molecular_weight": 132.140, "category": "ionic", "description": "Nitrogen fertilizer", "uses": ["Fertilizer"], "state": "solid", "common_name": "Ammonium sulfate", "hazards": ["None"]},
        {"formula": "Ca(H2PO4)2", "name": "Monocalcium Phosphate", "molecular_weight": 234.052, "category": "ionic", "description": "Fertilizer and baking powder ingredient", "uses": ["Fertilizer", "Baking powder"], "state": "solid", "common_name": "Monocalcium phosphate", "hazards": ["None"]},
        
        # Plastics and Polymers (monomers)
        {"formula": "C2H3Cl", "name": "Vinyl Chloride", "molecular_weight": 62.498, "category": "organic", "description": "Monomer for PVC plastic", "uses": ["PVC production"], "state": "gas", "common_name": "Vinyl chloride", "hazards": ["Carcinogenic"]},
        {"formula": "C8H8", "name": "Styrene", "molecular_weight": 104.150, "category": "organic", "description": "Monomer for polystyrene", "uses": ["Polystyrene production"], "state": "liquid", "common_name": "Styrene", "hazards": ["Possible carcinogen"]},
        
        # Pharmaceutical compounds
        {"formula": "C9H8O4", "name": "Aspirin", "molecular_weight": 180.158, "category": "organic", "description": "Pain reliever and anti-inflammatory", "uses": ["Pain relief", "Anti-inflammatory"], "state": "solid", "common_name": "Aspirin", "hazards": ["Blood thinner"]},
        {"formula": "C8H9NO2", "name": "Acetaminophen", "molecular_weight": 151.163, "category": "organic", "description": "Pain reliever and fever reducer", "uses": ["Pain relief", "Fever reduction"], "state": "solid", "common_name": "Tylenol", "hazards": ["Liver damage in high doses"]},
        
        # Environmental compounds
        {"formula": "CFC-12", "name": "Dichlorodifluoromethane", "molecular_weight": 120.913, "category": "organic", "description": "Ozone-depleting refrigerant", "uses": ["Refrigerant (banned)"], "state": "gas", "common_name": "Freon-12", "hazards": ["Ozone depletion"]},
        {"formula": "CH2Cl2", "name": "Dichloromethane", "molecular_weight": 84.933, "category": "organic", "description": "Paint stripper and solvent", "uses": ["Paint stripper", "Solvent"], "state": "liquid", "common_name": "Methylene chloride", "hazards": ["Carcinogenic"]},
    ]

# Routes
@app.route('/')
def index():
    """Homepage with complete periodic table"""
    elements = load_elements()
    return render_template('index.html', elements=elements)

@app.route('/element/<int:number>')
def element_detail(number):
    """Element detail page"""
    elements = load_elements()
    element = next((e for e in elements if e['number'] == number), None)
    if not element:
        return render_template('error.html', error_code=404), 404
    return render_template('element_detail.html', element=element)

@app.route('/search')
def search():
    """Advanced search page"""
    query = request.args.get('q', '')
    compounds = load_compounds()
    elements = load_elements()
    
    results = []
    if query:
        # Search compounds
        for compound in compounds:
            if (query.lower() in compound['name'].lower() or 
                query.lower() in compound['formula'].lower()):
                results.append({'type': 'compound', 'data': compound})
        
        # Search elements
        for element in elements:
            if (query.lower() in element['name'].lower() or 
                query.lower() in element['symbol'].lower()):
                results.append({'type': 'element', 'data': element})
    
    return render_template('search.html', query=query, results=results)

@app.route('/compound/<formula>')
def compound_detail(formula):
    """Compound detail page"""
    compounds = load_compounds()
    compound = next((c for c in compounds if c['formula'] == formula), None)
    if not compound:
        return render_template('error.html', error_code=404), 404
    return render_template('compound_detail.html', compound=compound)

@app.route('/formula-finder')
def formula_finder():
    """Advanced chemical formula finder and calculator"""
    return render_template('formula_finder.html')

@app.route('/about')
def about():
    """About ChemVista page"""
    return render_template('about.html')

@app.route('/use-cases')
def use_cases():
    """Use cases and applications page"""
    return render_template('use_cases.html')

@app.route('/scientists')
def scientists():
    """Famous chemists and scientists page"""
    return render_template('scientists.html', scientists=FAMOUS_CHEMISTS)

@app.route('/scientist/<name>')
def scientist_detail(name):
    """Individual scientist detail page"""
    scientist = next((s for s in FAMOUS_CHEMISTS if s['name'].replace(' ', '-').lower() == name.lower()), None)
    if not scientist:
        return render_template('error.html', error_code=404), 404
    return render_template('scientist_detail.html', scientist=scientist)

@app.route('/periodic-table-info')
def periodic_table_info():
    """Comprehensive periodic table information"""
    return render_template('periodic_table_info.html')

@app.route('/chemistry-concepts')
def chemistry_concepts():
    """Chemistry concepts and theories"""
    return render_template('chemistry_concepts.html', concepts=CHEMISTRY_CONCEPTS)

@app.route('/concept/<concept_title>')
def concept_detail(concept_title):
    """Individual chemistry concept detail page"""
    concept = next((c for c in CHEMISTRY_CONCEPTS if c['title'].replace(' ', '-').lower() == concept_title.lower()), None)
    if not concept:
        return render_template('error.html', error_code=404), 404
    return render_template('concept_detail.html', concept=concept)

@app.route('/resources')
def resources():
    """Educational resources and reference links"""
    return render_template('resources.html')

@app.route('/calculator')
def calculator():
    """Chemistry calculator and tools"""
    return render_template('calculator.html')

@app.route('/quiz')
def quiz():
    """Interactive chemistry quiz"""
    return render_template('quiz.html')

@app.route('/lab-safety')
def lab_safety():
    """Laboratory safety guidelines"""
    return render_template('lab_safety.html')

@app.route('/api/search')
def api_search():
    """Search API for autocomplete"""
    query = request.args.get('q', '').strip()
    limit = int(request.args.get('limit', 10))
    
    if not query:
        return jsonify([])
    
    compounds = load_compounds()
    results = []
    
    query_lower = query.lower()
    for compound in compounds:
        if (query_lower in compound['formula'].lower() or 
            query_lower in compound['name'].lower()):
            results.append({
                'formula': compound['formula'],
                'name': compound['name'],
                'molecular_weight': compound.get('molecular_weight', 0)
            })
            if len(results) >= limit:
                break
    
    return jsonify(results)

@app.route('/api/elements')
def api_elements():
    """Get all elements"""
    return jsonify(load_elements())

@app.route('/api/compounds')
def api_compounds():
    """Get all compounds"""
    return jsonify(load_compounds())

# Helper functions for formula calculations
def parse_formula(formula):
    """Parse a chemical formula and return element composition"""
    import re
    elements = {}
    
    # Simple regex to match element symbols and their counts
    pattern = r'([A-Z][a-z]?)(\d*)'
    matches = re.findall(pattern, formula)
    
    for element, count in matches:
        count = int(count) if count else 1
        elements[element] = elements.get(element, 0) + count
    
    return elements

def calculate_molecular_weight(formula, elements_data):
    """Calculate molecular weight from formula"""
    composition = parse_formula(formula)
    molecular_weight = 0
    
    element_dict = {e['symbol']: e['atomic_mass'] for e in elements_data}
    
    for element, count in composition.items():
        if element in element_dict:
            molecular_weight += element_dict[element] * count
        else:
            raise ValueError(f"Unknown element: {element}")
    
    return round(molecular_weight, 3)

def balance_chemical_equation(equation):
    """Simple chemical equation balancer (placeholder)"""
    # This is a simplified placeholder - real equation balancing is complex
    if '->' in equation:
        reactants, products = equation.split('->')
        return f"Balanced: {equation.strip()} (Note: Advanced balancing coming soon)"
    else:
        return "Invalid equation format. Use '->' to separate reactants and products."

@app.route('/api/formula-calculator', methods=['POST'])
def formula_calculator():
    """Calculate molecular properties from formula"""
    data = request.get_json()
    formula = data.get('formula', '').strip()
    
    if not formula:
        return jsonify({'error': 'No formula provided'}), 400
    
    try:
        elements = load_elements()
        molecular_weight = calculate_molecular_weight(formula, elements)
        element_composition = parse_formula(formula)
        
        return jsonify({
            'formula': formula,
            'molecular_weight': molecular_weight,
            'composition': element_composition,
            'valid': True
        })
    except Exception as e:
        return jsonify({'error': str(e), 'valid': False}), 400

@app.route('/api/calculate_molecular_weight', methods=['POST'])
def calculate_molecular_weight_api():
    """Calculate molecular weight from formula"""
    data = request.get_json()
    formula = data.get('formula', '').strip()
    
    if not formula:
        return jsonify({'error': 'No formula provided'}), 400
    
    try:
        elements = load_elements()
        molecular_weight = calculate_molecular_weight(formula, elements)
        element_composition = parse_formula(formula)
        
        # Create detailed element breakdown
        element_breakdown = []
        element_dict = {e['symbol']: e for e in elements}
        
        for symbol, count in element_composition.items():
            if symbol in element_dict:
                element_info = element_dict[symbol]
                element_breakdown.append({
                    'symbol': symbol,
                    'name': element_info['name'],
                    'count': count,
                    'mass': element_info['atomic_mass'] * count
                })
        
        return jsonify({
            'formula': formula,
            'molecular_weight': molecular_weight,
            'elements': element_breakdown,
            'valid': True
        })
    except Exception as e:
        return jsonify({'error': str(e), 'valid': False}), 400

@app.route('/api/balance-equation', methods=['POST'])
def balance_equation():
    """Balance chemical equations"""
    data = request.get_json()
    equation = data.get('equation', '').strip()
    
    if not equation:
        return jsonify({'error': 'No equation provided'}), 400
    
    try:
        balanced = balance_chemical_equation(equation)
        return jsonify({
            'original': equation,
            'balanced': balanced,
            'valid': True
        })
    except Exception as e:
        return jsonify({'error': str(e), 'valid': False}), 400

@app.route('/api/quiz/random')
def api_quiz_random():
    """Get random quiz questions"""
    elements = load_elements()
    compounds = load_compounds()
    
    import random
    questions = []
    
    # Element questions
    for i in range(3):
        element = random.choice(elements)
        wrong_answers = [random.choice(elements)['symbol'] for _ in range(3)]
        questions.append({
            'type': 'element',
            'question': f"What is the chemical symbol for {element['name']}?",
            'correct_answer': element['symbol'],
            'options': [element['symbol']] + wrong_answers,
            'explanation': f"{element['name']} has the symbol {element['symbol']} and atomic number {element['number']}"
        })
    
    # Compound questions
    for i in range(2):
        compound = random.choice(compounds)
        wrong_answers = [random.choice(compounds)['formula'] for _ in range(3)]
        questions.append({
            'type': 'compound',
            'question': f"What is the chemical formula for {compound['name']}?",
            'correct_answer': compound['formula'],
            'options': [compound['formula']] + wrong_answers,
            'explanation': f"{compound['name']} has the formula {compound['formula']}"
        })
    
    # Shuffle options for each question
    for question in questions:
        random.shuffle(question['options'])
    
    return jsonify(questions)

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', error_code=404), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('error.html', error_code=500), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
