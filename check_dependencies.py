#!/usr/bin/env python3
"""
Dependency checker for AWSLogs
Tests if all required dependencies are available and meet version requirements
"""

import importlib
import sys
from packaging import version

# Define required dependencies and their version constraints
DEPENDENCIES = {
    'boto3': {
        'min_version': '1.33.13',
        'max_version': '1.34.0',
        'required': True
    },
    'jmespath': {
        'min_version': '1.0.1',
        'max_version': None,
        'required': True
    },
    'termcolor': {
        'min_version': '1.1.0',
        'max_version': '2.0.0',
        'required': True
    },
    'dateutil': {
        'import_name': 'dateutil',
        'package_name': 'python-dateutil',
        'min_version': '2.8.2',
        'max_version': None,
        'required': True
    }
}

def check_dependencies():
    """Check if all required dependencies are available with correct versions"""
    all_passed = True
    missing_deps = []
    version_issues = []
    
    print("Checking dependencies...\n")
    
    for dep_name, dep_info in DEPENDENCIES.items():
        import_name = dep_info.get('import_name', dep_name)
        package_name = dep_info.get('package_name', dep_name)
        required = dep_info.get('required', True)
        min_version_str = dep_info.get('min_version')
        max_version_str = dep_info.get('max_version')
        
        try:
            # Try to import the module
            module = importlib.import_module(import_name)
            
            # Get the installed version
            if hasattr(module, '__version__'):
                installed_version_str = module.__version__
            elif hasattr(module, 'VERSION'):
                installed_version_str = module.VERSION
            else:
                # Handle special cases or use alternative method
                if import_name == 'dateutil':
                    # For dateutil, we need to get the version differently
                    installed_version_str = importlib.import_module('dateutil.version').__version__
                else:
                    installed_version_str = "Unknown"
            
            installed_version = version.parse(installed_version_str) if installed_version_str != "Unknown" else None
            
            version_ok = True
            version_message = ""
            
            # Check minimum version constraint
            if min_version_str and installed_version:
                min_version = version.parse(min_version_str)
                if installed_version < min_version:
                    version_ok = False
                    version_message = f"too old (minimum: {min_version_str})"
            
            # Check maximum version constraint
            if max_version_str and installed_version:
                max_version = version.parse(max_version_str)
                if installed_version >= max_version:
                    version_ok = False
                    version_message = f"too new (maximum: <{max_version_str})"
            
            if version_ok:
                status = "✅ PASS"
            else:
                status = "❌ FAIL"
                all_passed = False
                version_issues.append(f"{package_name}: {installed_version_str} is {version_message}")
            
            print(f"{status} {package_name}: {installed_version_str}")
            
        except ImportError:
            status = "❌ MISSING" if required else "⚠️ OPTIONAL"
            if required:
                all_passed = False
                missing_deps.append(package_name)
            print(f"{status} {package_name}")
    
    print("\nSummary:")
    if all_passed:
        print("✅ All dependencies are installed and meet version requirements!")
    else:
        if missing_deps:
            print("❌ Missing required dependencies:")
            for dep in missing_deps:
                print(f"   - {dep}")
        
        if version_issues:
            print("❌ Version requirements not met:")
            for issue in version_issues:
                print(f"   - {issue}")
        
        print("\nTo install required dependencies, run:")
        print("pip install boto3>=1.33.13,<1.34.0 jmespath>=1.0.1 termcolor>=1.1.0,<2.0.0 python-dateutil>=2.8.2")
    
    return all_passed

if __name__ == "__main__":
    success = check_dependencies()
    sys.exit(0 if success else 1)