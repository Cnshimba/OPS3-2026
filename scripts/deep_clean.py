#!/usr/bin/env python3
"""
Deep Clean corrupted glossary artifacts from HTML files.
Targeting specific corruption where definitions leaked into text.
"""

from pathlib import Path
import re

# Definitions to strip from text
GLOSSARY_DEFINITIONS = [
    "The creation of virtual versions of physical computing resources",
    "Software that creates and manages virtual machines",
    "A bare-metal hypervisor that runs directly on hardware",
    "A hosted hypervisor that runs on a host OS",
    "A software-based emulation of a physical computer",
    "Virtual Machine - A software-based emulation of a physical computer",
    "The operating system running inside a virtual machine",
    "The primary OS running on physical hardware",
    "Kernel-based Virtual Machine - A Type 1 hypervisor",
    "Quick Emulator - Works with KVM for virtualization",
    "Open-source virtualization platform combining KVM and LXC",
    "Virtual CPU - Portion of physical CPU allocated to a VM",
    "A file that appears as a physical disk to a VM",
    "QEMU Copy-On-Write disk image format",
    "Point-in-time copy of VM state for rollback",
    "Moving a running VM between hosts without downtime",
    "Pre-configured VM image for quick deployment",
    "An exact copy of a virtual machine",
    "Software-defined network for VM communication",
    "Network device connecting network segments",
    "Virtual LAN - Logical network segmentation",
    "Network Address Translation - Maps private to public IPs",
    "Software-Defined Networking - Software-based network control",
    "Dynamic Host Configuration Protocol - Assigns IP addresses",
    "Domain Name System - Translates domain names to IPs",
    "Collection of storage resources for VMs",
    "Advanced file system with volume management",
    "Logical Volume Manager - Flexible disk management",
    "Network File System - Remote file access protocol",
    "Internet SCSI - Block storage over IP networks",
    "Distributed storage system for object/block/file storage",
    "Lightweight package with application code and dependencies",
    "Platform for developing and running containers",
    "Template for creating Docker containers",
    "Instructions for building a Docker image",
    "Linux Containers - OS-level virtualization",
    "Container orchestration platform",
    "Smallest deployable unit in Kubernetes",
    "System design for minimal downtime (99.9%+ uptime)",
    "High Availability - System design for minimal downtime",
    "Group of servers working together",
    "Minimum nodes needed for cluster to function",
    "Cluster engine for group communication",
    "Automatic transfer to backup on failure",
    "Safety mechanism to isolate failed cluster nodes",
    "Computing services delivered over the internet",
    "Infrastructure as a Service - Virtualized computing resources",
    "Platform as a Service - Development platform",
    "Software as a Service - Software over the internet",
    "OpenStack compute service for VMs",
    "OpenStack networking service",
    "OpenStack block storage service",
    "OpenStack image service",
    "OpenStack identity/authentication service",
    "OpenStack web dashboard",
    "Single instance serving multiple customers",
    "Grouping of users and resources (also called Project)",
    "VM template defining vCPUs, RAM, and disk",
    "Application Programming Interface",
    "RESTful web services using HTTP methods",
    "JavaScript Object Notation - Data format",
    "Command Line Interface",
    "Automation tool for configuration management",
    "Managing infrastructure through code",
    "Infrastructure as Code",
    "Automated coordination of systems",
    # Specific artifacts seen in logs
    " - A Hypervisor\"", 
    " - Hypervisor\"", 
    "\" Hypervisor\"",
    "state for rollback", # Duplicate artifact
]

def deep_clean(content):
    # 1. Strip Tooltip Spans (Aggressive Loop to handle nesting)
    # Remove <span class="glossary-tooltip">...</span>
    # We use a pattern that matches the opening tag, then any non-span content, then closing.
    # But for nested spans, strict regex is hard.
    # We'll use a loop: find innermost spans and remove them.
    
    # Pattern: <span class="glossary-tooltip"> (no nested spans) </span>
    pattern = r'<span class="glossary-tooltip">([^<]*(?:<[^s/][^<]*)*?)</span>'
    # This is getting complex.
    # Simplest approach: Remove the start and end tags? NO, content remains.
    
    # Let's simple remove the definition strings first!
    # If "QEMU<span...>Definition</span>", and we remove "Definition", we get "QEMU<span...></span>".
    
    for definition in GLOSSARY_DEFINITIONS:
        # Remove literal definition string
        content = content.replace(definition, "")
    
    # Now remove the empty/broken tags
    content = content.replace('<span class="glossary-tooltip"></span>', '')
    content = re.sub(r'<span class="glossary-tooltip">\s*</span>', '', content)
    
    # What if some text remains? e.g. " - "
    content = content.replace(' - </span>', '</span>')
    
    # Let's try the previous repair logic again, now that definitions are gone.
    content = re.sub(r'<span class="glossary-tooltip">.*?</span>', '', content, flags=re.DOTALL)
    
    # 2. Strip Anchor Wrappers
    content = re.sub(r'<a [^>]*class="glossary-term"[^>]*>(.*?)</a>', r'\1', content, flags=re.DOTALL)
    # Handle broken ones
    content = content.replace('class="glossary-term">', '')
    content = content.replace('</a>', '') # Risky?
    # Better: Only remove </a> if it follows our known pattern.
    # Using the regex above covers valid wrappers.
    
    # Clean up lingering artifacts
    content = content.replace(' - "', '')
    content = content.replace('""', '')
    content = content.replace('for virtualization for virtualization', 'for virtualization')
    content = content.replace('  ', ' ') # Double spaces
    
    # Clean up specific recursive mess
    content = content.replace('QEMU for virtualization', 'QEMU')
    content = content.replace('QEMU - for virtualization', 'QEMU')
    
    return content

def main():
    base_dir = Path(__file__).parent.parent
    print("=" * 70)
    print("Deep Cleaning Glossary Artifacts")
    print("=" * 70)
    
    processed = 0
    for week_dir in base_dir.glob("Week *"):
        if week_dir.is_dir():
            notes_files = list(week_dir.glob("*Student_Notes.html"))
            for html_file in notes_files:
                print(f"Cleaning: {html_file.name}")
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                cleaned = deep_clean(content)
                
                # Double pass
                cleaned = deep_clean(cleaned)
                
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(cleaned)
                processed += 1
                
    print(f"✅ Deep Cleaned {processed} files")

if __name__ == "__main__":
    main()
