"""
Demo script to showcase the Auto Test Generator
"""

import os
import sys

# Add parent directory to path to import modules
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

try:
    from generators.test_generator import TestGenerator
except ImportError:
    # Alternative import method
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "test_generator", 
        os.path.join(parent_dir, "generators", "test_generator.py")
    )
    test_generator_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(test_generator_module)
    TestGenerator = test_generator_module.TestGenerator


def demo_auto_generation():
    """Demonstrate auto test generation from problem statement"""
    
    print("TestAutothon Auto Test Generator Demo")
    print("=" * 50)
    
    # Read the example problem statement
    problem_file = os.path.join(os.path.dirname(__file__), 'testautothon2024_problem.txt')
    
    try:
        with open(problem_file, 'r', encoding='utf-8') as f:
            problem_text = f.read()
    except FileNotFoundError:
        print(f"Error: Problem file '{problem_file}' not found")
        return
    
    print("Problem Statement Loaded:")
    print("-" * 30)
    print(problem_text[:200] + "..." if len(problem_text) > 200 else problem_text)
    print()
    
    # Generate tests
    try:
        generator = TestGenerator("demo_output")
        generated_files = generator.generate_from_problem_statement(problem_text, "TestAutothon2024")
        
        print("Generated Test Files:")
        print("-" * 30)
        
        for filename, content in generated_files.items():
            print(f"\n{filename}")
            print("=" * 40)
            # Show first few lines of generated code
            lines = content.split('\n')[:15]
            for i, line in enumerate(lines, 1):
                print(f"{i:2d}: {line}")
            if len(content.split('\n')) > 15:
                print("    ... (truncated)")
        
        # Save files
        saved_files = generator.save_generated_tests(generated_files)
        
        print(f"\nSuccessfully generated {len(saved_files)} test files!")
        output_path = os.path.abspath(generator.output_dir)
        print(f"Files saved to: {output_path}")
        
        for filepath in saved_files:
            print(f"   - {os.path.basename(filepath)} ({os.path.abspath(filepath)})")
            
        # Verify files exist
        print("\nFile verification:")
        for filepath in saved_files:
            if os.path.exists(filepath):
                print(f"   [OK] {os.path.basename(filepath)} exists")
            else:
                print(f"   [ERROR] {os.path.basename(filepath)} NOT FOUND")
        
        print("\nNext Steps:")
        print("1. Review the generated test files")
        print("2. Customize as needed for your specific requirements")
        print("3. Run: pytest demo_output/ -v")
        print("4. Integrate with your existing TestAutothon2824 framework")
        
    except Exception as e:
        print(f"Error generating tests: {e}")
        return


if __name__ == "__main__":
    demo_auto_generation()