"""
NOVA SDK Packager.
Compiles a validated extension directory into a portable .nova archive.
"""
import os
import zipfile
import logging

logger = logging.getLogger(__name__)

class ExtensionPackager:
    """Packages an extension for distribution."""
    
    def package(self, project_dir: str, output_dir: str = ".") -> str:
        """Zips the project directory into a .nova file."""
        logger.info(f"Packaging extension at '{project_dir}'...")
        
        ext_name = os.path.basename(os.path.normpath(project_dir))
        nova_file_path = os.path.join(output_dir, f"{ext_name}.nova")
        
        with zipfile.ZipFile(nova_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(project_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, project_dir)
                    zipf.write(file_path, arcname)
                    
        logger.info(f"Successfully created package: {nova_file_path}")
        return nova_file_path
