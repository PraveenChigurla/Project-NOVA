"""
NOVA SDK CLI Entrypoint.
Usage: python -m nova.sdk.cli [command]
"""
import sys
import argparse
import logging
from nova.sdk.generator import ProjectGenerator
from nova.sdk.validator import ExtensionValidator
from nova.sdk.simulator import ExtensionSimulator
from nova.sdk.packager import ExtensionPackager

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("nova.sdk")

def main():
    parser = argparse.ArgumentParser(description="NOVA Extension SDK CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # new
    parser_new = subparsers.add_parser("new", help="Create a new extension")
    parser_new.add_argument("type", choices=["skill", "provider", "capability"])
    parser_new.add_argument("name", help="Name of the extension")
    
    # validate
    parser_validate = subparsers.add_parser("validate", help="Validate an extension")
    parser_validate.add_argument("dir", help="Directory of the extension")
    
    # simulate
    parser_simulate = subparsers.add_parser("simulate", help="Simulate an extension")
    parser_simulate.add_argument("dir", help="Directory of the extension")
    
    # package
    parser_package = subparsers.add_parser("package", help="Package an extension")
    parser_package.add_argument("dir", help="Directory of the extension")
    
    args = parser.parse_args()
    
    if args.command == "new":
        generator = ProjectGenerator()
        generator.generate(args.type, args.name)
        
    elif args.command == "validate":
        validator = ExtensionValidator()
        if not validator.validate(args.dir):
            sys.exit(1)
            
    elif args.command == "simulate":
        simulator = ExtensionSimulator()
        simulator.simulate(args.dir)
        
    elif args.command == "package":
        packager = ExtensionPackager()
        packager.package(args.dir)

if __name__ == "__main__":
    main()
