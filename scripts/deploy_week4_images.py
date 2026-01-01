#!/usr/bin/env python3
"""
Deploy Week 4 Images
Moves generated images from artifacts folder to the Week 4 images directory.
"""

import shutil
from pathlib import Path
import os

def deploy_images():
    # Source: Startup artifact dir (need to find it based on known paths or assume current working dir)
    # Since script runs in CWD, we look for the known artifact path structure or accept args.
    # HARDCODED for this context based on user session info:
    artifact_dir = Path(r"C:\Users\carlos\.gemini\antigravity\brain\c1d26f20-7f52-4db0-9f6a-bd1d8d9b4764")
    
    target_dir = Path(r"d:\OneDrive - Vaal University of Technology\WORK\2026\OPS3\docs\OPS3-2026\Week 4 - Storage and Backup\images")
    
    if not target_dir.exists():
        print(f"Target directory {target_dir} does not exist!")
        return

    # Map of ImageName prefix to Destination Filename
    # We look for the most recent file matching the prefix
    image_map = {
        "linux_block_devices": "linux_block_devices.png",
        "lvm_hierarchy": "lvm_hierarchy.png",
        "zfs_cow": "zfs_cow.png",
        "zfs_healing": "zfs_healing.png",
        "disk_formats": "disk_formats.png"
    }

    print("Deploying Week 4 Images...")
    
    for prefix, dest_name in image_map.items():
        # Find matches in artifact dir
        matches = list(artifact_dir.glob(f"{prefix}*.png"))
        if not matches:
            print(f"⚠️ No image found for {prefix}")
            continue
            
        # Get latest by modification time
        latest_img = max(matches, key=os.path.getmtime)
        dest_path = target_dir / dest_name
        
        print(f"Copying {latest_img.name} -> {dest_name}")
        shutil.copy2(latest_img, dest_path)
        
    print("✅ Deployment Complete")

if __name__ == "__main__":
    deploy_images()
