#!/usr/bin/env python3
"""
Add Interactive Glossary Tooltips to Course Materials
Scans HTML files and wraps glossary terms with tooltips and links
"""

from bs4 import BeautifulSoup
from pathlib import Path
import re
import json

# Import glossary terms from create_glossary.py
# For now, we'll define the key terms here
GLOSSARY_TERMS = {
    "Virtualization": "The creation of virtual versions of physical computing resources",
    "Hypervisor": "Software that creates and manages virtual machines",
    "Type 1 Hypervisor": "A bare-metal hypervisor that runs directly on hardware",
    "Type 2 Hypervisor": "A hosted hypervisor that runs on a host OS",
    "Virtual Machine": "A software-based emulation of a physical computer",
    "VM": "Virtual Machine - A software-based emulation of a physical computer",
    "Guest OS": "The operating system running inside a virtual machine",
    "Host OS": "The primary OS running on physical hardware",
    "KVM": "Kernel-based Virtual Machine - A Type 1 hypervisor",
    "QEMU": "Quick Emulator - Works with KVM for virtualization",
    "Proxmox": "Open-source virtualization platform combining KVM and LXC",
    "vCPU": "Virtual CPU - Portion of physical CPU allocated to a VM",
    "Virtual Disk": "A file that appears as a physical disk to a VM",
    "qcow2": "QEMU Copy-On-Write disk image format",
    "Snapshot": "Point-in-time copy of VM state for rollback",
    "Live Migration": "Moving a running VM between hosts without downtime",
    "Template": "Pre-configured VM image for quick deployment",
    "Clone": "An exact copy of a virtual machine",
    "Virtual Network": "Software-defined network for VM communication",
    "Bridge": "Network device connecting network segments",
    "VLAN": "Virtual LAN - Logical network segmentation",
    "NAT": "Network Address Translation - Maps private to public IPs",
    "SDN": "Software-Defined Networking - Software-based network control",
    "DHCP": "Dynamic Host Configuration Protocol - Assigns IP addresses",
    "DNS": "Domain Name System - Translates domain names to IPs",
    "Storage Pool": "Collection of storage resources for VMs",
    "ZFS": "Advanced file system with volume management",
    "LVM": "Logical Volume Manager - Flexible disk management",
    "NFS": "Network File System - Remote file access protocol",
    "iSCSI": "Internet SCSI - Block storage over IP networks",
    "Ceph": "Distributed storage system for object/block/file storage",
    "Container": "Lightweight package with application code and dependencies",
    "Docker": "Platform for developing and running containers",
    "Docker Image": "Template for creating Docker containers",
    "Dockerfile": "Instructions for building a Docker image",
    "LXC": "Linux Containers - OS-level virtualization",
    "Kubernetes": "Container orchestration platform",
    "Pod": "Smallest deployable unit in Kubernetes",
    "High Availability": "System design for minimal downtime (99.9%+ uptime)",
    "HA": "High Availability - System design for minimal downtime",
    "Cluster": "Group of servers working together",
    "Quorum": "Minimum nodes needed for cluster to function",
    "Corosync": "Cluster engine for group communication",
    "Failover": "Automatic transfer to backup on failure",
    "Fencing": "Safety mechanism to isolate failed cluster nodes",
    "Cloud Computing": "Computing services delivered over the internet",
    "IaaS": "Infrastructure as a Service - Virtualized computing resources",
    "PaaS": "Platform as a Service - Development platform",
    "SaaS": "Software as a Service - Software over the internet",
    "OpenStack": "Open-source cloud computing platform",
    "Nova": "OpenStack compute service for VMs",
    "Neutron": "OpenStack networking service",
    "Cinder": "OpenStack block storage service",
    "Glance": "OpenStack image service",
    "Keystone": "OpenStack identity/authentication service",
    "Horizon": "OpenStack web dashboard",
    "Multi-tenancy": "Single instance serving multiple customers",
    "Tenant": "Grouping of users and resources (also called Project)",
    "Flavor": "VM template defining vCPUs, RAM, and disk",
    "API": "Application Programming Interface",
    "REST API": "RESTful web services using HTTP methods",
    "JSON": "JavaScript Object Notation - Data format",
    "CLI": "Command Line Interface",
    "Ansible": "Automation tool for configuration management",
    "Infrastructure as Code": "Managing infrastructure through code",
    "IaC": "Infrastructure as Code",
    "Orchestration": "Automated coordination of systems"
}

def add_glossary_tooltips(html_content, output_path):
    """Add tooltips to glossary terms in HTML content"""
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Add glossary CSS and JavaScript to head
    head = soup.find('head')
    if head:
        # Add tooltip styles
        style_tag = soup.new_tag('style')
        style_tag.string = """
        /* Glossary Tooltip Styles */
        .glossary-term {
            color: #c9984a;
            border-bottom: 2px dotted #c9984a;
            cursor: help;
            position: relative;
            text-decoration: none;
            transition: all 0.3s;
        }
        
        .glossary-term:hover {
            color: #ffffff;
            border-bottom-color: #ffffff;
        }
        
        .glossary-tooltip {
            visibility: hidden;
            opacity: 0;
            position: absolute;
            z-index: 1000;
            background: linear-gradient(135deg, #1e3a5f 0%, #142a46 100%);
            color: #ffffff;
            padding: 12px 16px;
            border-radius: 8px;
            border: 2px solid #c9984a;
            font-size: 14px;
            line-height: 1.5;
            max-width: 300px;
            width: max-content;
            bottom: 125%;
            left: 50%;
            transform: translateX(-50%);
            transition: opacity 0.3s, visibility 0.3s;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        }
        
        .glossary-tooltip::after {
            content: "";
            position: absolute;
            top: 100%;
            left: 50%;
            margin-left: -8px;
            border-width: 8px;
            border-style: solid;
            border-color: #c9984a transparent transparent transparent;
        }
        
        .glossary-term:hover .glossary-tooltip {
            visibility: visible;
            opacity: 1;
        }
        """
        head.append(style_tag)
    
    # Find all text nodes and replace terms
    article = soup.find('article') or soup.find('body')
    if article:
        # Sort terms by length (longest first) to match longer phrases first
        sorted_terms = sorted(GLOSSARY_TERMS.items(), key=lambda x: len(x[0]), reverse=True)
        
        # Identify "Objective" or "Intro" section elements
        elements_to_process = []
        
        # Iterate through direct children of article
        for child in article.children:
            # Stop if we hit a major section header or horizontal rule
            if child.name in ['h2', 'hr']:
                break
                
            # If it's a content block (p, blockquote, ul, ol, div), add to list
            if child.name in ['p', 'blockquote', 'ul', 'ol', 'div']:
                elements_to_process.append(child)
                
        # Process text content in selected elements
        for parent_element in elements_to_process:
            for element in parent_element.find_all(text=True):
                # Skip headings/scripts/style/etc
                if element.parent.name in ['script', 'style', 'code', 'pre', 'a', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                    continue  # Skip these elements
                
                text = str(element)
                modified_text = text
                
                for term, definition in sorted_terms:
                    # Use word boundary regex to match whole words/phrases
                    pattern = r'\b' + re.escape(term) + r'\b'
                    matches = list(re.finditer(pattern, modified_text, re.IGNORECASE))
                    
                    # Replace matches (in reverse to maintain positions)
                    for match in reversed(matches):
                        matched_text = match.group()
                        # Create clean tooltip HTML without icons
                        tooltip_html = f'<a href="glossary.html#{term.replace(" ", "-")}" class="glossary-term">{matched_text}<span class="glossary-tooltip">{definition}</span></a>'
                        
                        # Replace in text
                        modified_text = modified_text[:match.start()] + tooltip_html + modified_text[match.end():]
                
                # Replace the text node with modified HTML if changed
                if modified_text != text:
                    new_soup = BeautifulSoup(modified_text, 'html.parser')
                    element.replace_with(new_soup)
    
    return str(soup)

def process_html_files(base_dir):
    """Process all HTML files to add glossary tooltips"""
    processed = 0
    
    # Find all student notes HTML files
    for week_dir in base_dir.glob("Week *"):
        if week_dir.is_dir():
            notes_files = list(week_dir.glob("*Student_Notes.html"))
            
            for html_file in notes_files:
                print(f"Processing: {html_file.name}")
                
                with open(html_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Add tooltips
                modified_content = add_glossary_tooltips(content, html_file)
                
                # Write back
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(modified_content)
                
                processed += 1
                print(f"  ✅ Added glossary tooltips (Header section only)")
    
    return processed

def main():
    """Main function"""
    base_dir = Path(__file__).parent.parent
    
    print("=" * 70)
    print("Adding Interactive Glossary Tooltips to Course Materials")
    print("=" * 70)
    print()
    
    processed = process_html_files(base_dir)
    
    print()
    print("=" * 70)
    print(f"✅ Processed {processed} HTML files")
    print(f"   Terms will now show tooltips on hover")
    print(f"   Click terms to jump to glossary")
    print("=" * 70)

if __name__ == "__main__":
    main()
