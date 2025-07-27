#!/usr/bin/env python3
"""
ChemVista Test Script
Test the application functionality and data integrity
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import load_element_data, load_compounds_data

def test_elements_data():
    """Test elements data loading and completeness"""
    print("Testing Elements Data...")
    elements = load_element_data()
    
    print(f"Total elements loaded: {len(elements)}")
    
    if len(elements) != 118:
        print(f"❌ ERROR: Expected 118 elements, got {len(elements)}")
        return False
    
    # Check for required fields
    required_fields = ['atomic_number', 'symbol', 'name', 'category', 'group', 'period', 'atomic_mass']
    
    for element in elements:
        for field in required_fields:
            if field not in element:
                print(f"❌ ERROR: Element {element.get('name', 'Unknown')} missing field: {field}")
                return False
    
    # Check atomic numbers 1-118
    atomic_numbers = [el['atomic_number'] for el in elements]
    expected_numbers = list(range(1, 119))
    
    if set(atomic_numbers) != set(expected_numbers):
        missing = set(expected_numbers) - set(atomic_numbers)
        extra = set(atomic_numbers) - set(expected_numbers)
        if missing:
            print(f"❌ ERROR: Missing atomic numbers: {missing}")
        if extra:
            print(f"❌ ERROR: Extra atomic numbers: {extra}")
        return False
    
    # Check categories
    categories = set(el['category'] for el in elements)
    expected_categories = {
        'alkali-metal', 'alkaline-earth-metal', 'transition-metal', 
        'post-transition-metal', 'metalloid', 'reactive-nonmetal', 
        'halogen', 'noble-gas', 'lanthanide', 'actinide'
    }
    
    if not categories.issubset(expected_categories):
        unexpected = categories - expected_categories
        print(f"❌ ERROR: Unexpected categories: {unexpected}")
        return False
    
    print("✅ Elements data test passed!")
    return True

def test_compounds_data():
    """Test compounds data loading"""
    print("Testing Compounds Data...")
    compounds = load_compounds_data()
    
    print(f"Total compounds loaded: {len(compounds)}")
    
    if len(compounds) == 0:
        print("❌ ERROR: No compounds loaded")
        return False
    
    # Check for required fields
    required_fields = ['name', 'formula']
    
    for compound in compounds:
        for field in required_fields:
            if field not in compound:
                print(f"❌ ERROR: Compound missing field: {field}")
                return False
    
    print("✅ Compounds data test passed!")
    return True

def test_periodic_table_structure():
    """Test periodic table structure"""
    print("Testing Periodic Table Structure...")
    elements = load_element_data()
    
    # Count elements by period
    period_counts = {}
    for element in elements:
        period = element['period']
        period_counts[period] = period_counts.get(period, 0) + 1
    
    print("Elements per period:")
    for period in sorted(period_counts.keys()):
        print(f"  Period {period}: {period_counts[period]} elements")
    
    # Count elements by category
    category_counts = {}
    for element in elements:
        category = element['category']
        category_counts[category] = category_counts.get(category, 0) + 1
    
    print("Elements per category:")
    for category in sorted(category_counts.keys()):
        print(f"  {category}: {category_counts[category]} elements")
    
    print("✅ Periodic table structure test passed!")
    return True

def main():
    """Run all tests"""
    print("🧪 ChemVista Application Test Suite")
    print("=" * 50)
    
    tests = [
        test_elements_data,
        test_compounds_data,
        test_periodic_table_structure
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ ERROR: Test {test.__name__} failed with exception: {e}")
            failed += 1
        print()
    
    print("=" * 50)
    print(f"Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed! ChemVista is ready to run.")
        return True
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
