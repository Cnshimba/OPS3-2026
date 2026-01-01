#!/usr/bin/env python3
"""
Create Course Glossary from Student Notes
Extracts technical terms and creates a comprehensive glossary page
"""

from bs4 import BeautifulSoup
from pathlib import Path
import re
import json

# Comprehensive glossary with categorized terms
GLOSSARY_DATA = {
    # Week 1 - Virtualization Basics
    "Virtualization": {
        "definition": "The creation of virtual versions of physical computing resources, including servers, storage devices, and networks.",
        "category": "Virtualization",
        "week": 1
    },
    "Hypervisor": {
        "definition": "Software that creates and manages virtual machines by abstracting physical hardware resources. Also known as Virtual Machine Monitor (VMM).",
        "category": "Virtualization",
        "week": 1,
        "related": ["Type 1 Hypervisor", "Type 2 Hypervisor", "Virtual Machine"]
    },
    "Type 1 Hypervisor": {
        "definition": "A bare-metal hypervisor that runs directly on physical hardware without a host operating system. Examples include VMware ESXi, KVM, and Proxmox VE.",
        "category": "Virtualization",
        "week": 1,
        "related": ["Hypervisor", "KVM", "Proxmox"]
    },
    "Type 2 Hypervisor": {
        "definition": "A hosted hypervisor that runs on top of a host operating system. Examples include VMware Workstation, VirtualBox, and QEMU.",
        "category": "Virtualization",
        "week": 1,
        "related": ["Hypervisor", "VirtualBox", "QEMU"]
    },
    "Virtual Machine (VM)": {
        "definition": "A software-based emulation of a physical computer that runs an operating system and applications, isolated from the host system.",
        "category": "Virtualization",
        "week": 1,
        "related": ["Hypervisor", "Guest OS"]
    },
    "Guest OS": {
        "definition": "The operating system running inside a virtual machine, as opposed to the host operating system.",
        "category": "Virtualization",
        "week": 1
    },
    "Host OS": {
        "definition": "The primary operating system running on physical hardware that hosts virtual machines (in Type 2 hypervisors).",
        "category": "Virtualization",
        "week": 1
    },
    "KVM": {
        "definition": "Kernel-based Virtual Machine - A Type 1 hypervisor built into the Linux kernel, providing hardware-assisted virtualization.",
        "category": "Virtualization",
        "week": 1,
        "related": ["QEMU", "Proxmox", "Hypervisor"]
    },
    "QEMU": {
        "definition": "Quick Emulator - An open-source machine emulator and virtualizer that works with KVM to provide full system virtualization.",
        "category": "Virtualization",
        "week": 1,
        "related": ["KVM"]
    },
    "Proxmox VE": {
        "definition": "Proxmox Virtual Environment - An open-source virtualization platform combining KVM hypervisor and LXC containers with an integrated web-based management interface.",
        "category": "Virtualization",
        "week": 1,
        "related": ["KVM", "LXC", "Container"]
    },
    
    # Week 2 - Virtual Machines
    "vCPU": {
        "definition": "Virtual Central Processing Unit - A portion of physical CPU resources allocated to a virtual machine.",
        "category": "Virtual Machines",
        "week": 2,
        "related": ["Virtual Machine", "CPU Scheduling"]
    },
    "Virtual Disk": {
        "definition": "A file or volume that appears as a physical disk drive to a virtual machine, storing the VM's operating system and data.",
        "category": "Virtual Machines",
        "week": 2,
        "related": ["qcow2", "Raw Disk"]
    },
    "qcow2": {
        "definition": "QEMU Copy-On-Write version 2 - A disk image format that supports compression, encryption, and snapshots.",
        "category": "Storage",
        "week": 2,
        "related": ["Virtual Disk", "Snapshot"]
    },
    "Snapshot": {
        "definition": "A point-in-time copy of a virtual machine's state, including disk, memory, and configuration, allowing rollback to previous states.",
        "category": "Virtual Machines",
        "week": 2,
        "related": ["Virtual Machine", "Backup"]
    },
    "Live Migration": {
        "definition": "The process of moving a running virtual machine from one physical host to another without downtime.",
        "category": "Virtual Machines",
        "week": 2,
        "related": ["High Availability", "Cluster"]
    },
    "Template": {
        "definition": "A pre-configured virtual machine image used as a baseline for creating new VMs quickly and consistently.",
        "category": "Virtual Machines",
        "week": 2,
        "related": ["Clone", "Virtual Machine"]
    },
    "Clone": {
        "definition": "An exact copy of a virtual machine, which can be either linked (shares storage with original) or full (independent copy).",
        "category": "Virtual Machines",
        "week": 2,
        "related": ["Template", "Virtual Machine"]
    },
    
    # Week 3 - Networking
    "Virtual Network": {
        "definition": "A software-defined network that enables communication between virtual machines and external networks.",
        "category": "Networking",
        "week": 3
    },
    "Bridge": {
        "definition": "A network device that connects two or more network segments, allowing VMs to appear on the same network as the physical host.",
        "category": "Networking",
        "week": 3,
        "related": ["Virtual Network", "VLAN"]
    },
    "VLAN": {
        "definition": "Virtual Local Area Network - A logical network segment that groups devices regardless of physical location, improving security and reducing broadcast domains.",
        "category": "Networking",
        "week": 3,
        "related": ["Bridge", "Network Segmentation"]
    },
    "NAT": {
        "definition": "Network Address Translation - A method of mapping private IP addresses to public IP addresses, commonly used to allow VMs to access external networks.",
        "category": "Networking",
        "week": 3,
        "related": ["Routing", "Firewall"]
    },
    "Software-Defined Networking (SDN)": {
        "definition": "An approach to networking that uses software-based controllers to manage network traffic and behavior, separating the control plane from the data plane.",
        "category": "Networking",
        "week": 3,
        "related": ["OpenStack Neutron", "Virtual Network"]
    },
    "DHCP": {
        "definition": "Dynamic Host Configuration Protocol - A network protocol that automatically assigns IP addresses and network configuration to devices.",
        "category": "Networking",
        "week": 3
    },
    "DNS": {
        "definition": "Domain Name System - A hierarchical naming system that translates human-readable domain names to IP addresses.",
        "category": "Networking",
        "week": 3
    },
    
    # Week 4 - Storage
    "Storage Pool": {
        "definition": "A collection of storage resources aggregated together to be allocated to virtual machines as needed.",
        "category": "Storage",
        "week": 4,
        "related": ["ZFS", "LVM"]
    },
    "ZFS": {
        "definition": "Zettabyte File System - An advanced file system with built-in volume management, data integrity verification, and efficient snapshots.",
        "category": "Storage",
        "week": 4,
        "related": ["Storage Pool", "Snapshot"]
    },
    "LVM": {
        "definition": "Logical Volume Manager - A device mapper framework providing logical volume management for the Linux kernel, allowing flexible disk management.",
        "category": "Storage",
        "week": 4,
        "related": ["Storage Pool"]
    },
    "NFS": {
        "definition": "Network File System - A distributed file system protocol allowing remote file access over a network as if locally attached.",
        "category": "Storage",
        "week": 4,
        "related": ["Shared Storage", "CIFS"]
    },
    "iSCSI": {
        "definition": "Internet Small Computer System Interface - A protocol for transmitting SCSI commands over IP networks, enabling block-level storage access.",
        "category": "Storage",
        "week": 4,
        "related": ["SAN", "Block Storage"]
    },
    "Ceph": {
        "definition": "A unified, distributed storage system providing object, block, and file storage in a single platform with no single point of failure.",
        "category": "Storage",
        "week": 4,
        "related": ["Distributed Storage", "OpenStack Cinder"]
    },
    
    # Week 5 - Containers
    "Container": {
        "definition": "A lightweight, standalone executable package that includes application code, runtime, libraries, and dependencies, sharing the host OS kernel.",
        "category": "Containers",
        "week": 5,
        "related": ["Docker", "LXC"]
    },
    "Docker": {
        "definition": "A platform for developing, shipping, and running applications in containers, providing tools for container lifecycle management.",
        "category": "Containers",
        "week": 5,
        "related": ["Container", "Docker Image"]
    },
    "Docker Image": {
        "definition": "A read-only template containing application code and dependencies used to create Docker containers.",
        "category": "Containers",
        "week": 5,
        "related": ["Docker", "Container", "Dockerfile"]
    },
    "Dockerfile": {
        "definition": "A text file containing instructions for building a Docker image, defining the base image, dependencies, and configuration.",
        "category": "Containers",
        "week": 5,
        "related": ["Docker Image", "Docker"]
    },
    "LXC": {
        "definition": "Linux Containers - An operating system-level virtualization method providing isolated environments using Linux kernel features.",
        "category": "Containers",
        "week": 5,
        "related": ["Container", "Proxmox"]
    },
    "Kubernetes": {
        "definition": "An open-source container orchestration platform for automating deployment, scaling, and management of containerized applications.",
        "category": "Containers",
        "week": 5,
        "related": ["Docker", "Container Orchestration"]
    },
    "Pod": {
        "definition": "The smallest deployable unit in Kubernetes, consisting of one or more containers that share storage and network resources.",
        "category": "Containers",
        "week": 5,
        "related": ["Kubernetes", "Container"]
    },
    
    # Week 6 - High Availability
    "High Availability (HA)": {
        "definition": "A system design approach ensuring a service remains operational and accessible with minimal downtime, typically targeting 99.9% or higher uptime.",
        "category": "High Availability",
        "week": 6,
        "related": ["Cluster", "Failover"]
    },
    "Cluster": {
        "definition": "A group of interconnected servers working together to provide increased availability, scalability, and performance.",
        "category": "High Availability",
        "week": 6,
        "related": ["Proxmox Cluster", "Quorum"]
    },
    "Quorum": {
        "definition": "The minimum number of cluster nodes that must be available for the cluster to function, preventing split-brain scenarios.",
        "category": "High Availability",
        "week": 6,
        "related": ["Cluster", "Corosync"]
    },
    "Corosync": {
        "definition": "A cluster engine providing group communication and membership services for high availability clusters.",
        "category": "High Availability",
        "week": 6,
        "related": ["Cluster", "Quorum"]
    },
    "Failover": {
        "definition": "The automatic transfer of operations from a failed component to a redundant backup component to maintain service availability.",
        "category": "High Availability",
        "week": 6,
        "related": ["High Availability", "Redundancy"]
    },
    "Fencing": {
        "definition": "A safety mechanism in clusters that isolates or powers off failed nodes to prevent data corruption and split-brain scenarios.",
        "category": "High Availability",
        "week": 6,
        "related": ["Cluster", "STONITH"]
    },
    
    # Week 7-8 - Cloud Computing
    "Cloud Computing": {
        "definition": "The delivery of computing services including servers, storage, databases, networking, and software over the internet on-demand.",
        "category": "Cloud",
        "week": 7
    },
    "IaaS": {
        "definition": "Infrastructure as a Service - Cloud service model providing virtualized computing resources over the internet, including servers, storage, and networking.",
        "category": "Cloud",
        "week": 7,
        "related": ["PaaS", "SaaS", "Cloud Computing"]
    },
    "PaaS": {
        "definition": "Platform as a Service - Cloud service model providing a platform for developing, testing, and deploying applications without managing underlying infrastructure.",
        "category": "Cloud",
        "week": 7,
        "related": ["IaaS", "SaaS"]
    },
    "SaaS": {
        "definition": "Software as a Service - Cloud service model delivering software applications over the internet on a subscription basis.",
        "category": "Cloud",
        "week": 7,
        "related": ["IaaS", "PaaS"]
    },
    "OpenStack": {
        "definition": "An open-source cloud computing platform for building and managing public and private clouds, providing IaaS services.",
        "category": "Cloud",
        "week": 8,
        "related": ["Nova", "Neutron", "Cinder", "Glance"]
    },
    "Nova": {
        "definition": "OpenStack's compute service responsible for provisioning and managing virtual machine instances.",
        "category": "Cloud",
        "week": 9,
        "related": ["OpenStack", "Virtual Machine"]
    },
    "Neutron": {
        "definition": "OpenStack's networking service providing network connectivity as a service, including virtual networks, routers, and firewalls.",
        "category": "Cloud",
        "week": 8,
        "related": ["OpenStack", "Software-Defined Networking"]
    },
    "Cinder": {
        "definition": "OpenStack's block storage service providing persistent block storage volumes for virtual machines.",
        "category": "Cloud",
        "week": 10,
        "related": ["OpenStack", "Block Storage"]
    },
    "Glance": {
        "definition": "OpenStack's image service for discovering, registering, and retrieving virtual machine images.",
        "category": "Cloud",
        "week": 8,
        "related": ["OpenStack", "VM Image"]
    },
    "Keystone": {
        "definition": "OpenStack's identity service providing authentication and authorization for all OpenStack services.",
        "category": "Cloud",
        "week": 8,
        "related": ["OpenStack", "Authentication"]
    },
    "Horizon": {
        "definition": "OpenStack's web-based dashboard providing a graphical interface for managing cloud resources.",
        "category": "Cloud",
        "week": 8,
        "related": ["OpenStack"]
    },
    "Multi-tenancy": {
        "definition": "A software architecture where a single instance serves multiple customers (tenants) with isolated data and configurations.",
        "category": "Cloud",
        "week": 8,
        "related": ["Project", "Tenant"]
    },
    "Tenant": {
        "definition": "In OpenStack, a grouping of users and resources with isolated access. Also called a Project.",
        "category": "Cloud",
        "week": 8,
        "related": ["OpenStack", "Multi-tenancy"]
    },
    "Flavor": {
        "definition": "In OpenStack, a template defining virtual machine resources including vCPUs, RAM, and disk size.",
        "category": "Cloud",
        "week": 9,
        "related": ["Nova", "Virtual Machine"]
    },
    
    # Week 11 - Automation
    "API": {
        "definition": "Application Programming Interface - A set of protocols and tools for building software applications, enabling programmatic access to services.",
        "category": "Automation",
        "week": 11
    },
    "REST API": {
        "definition": "Representational State Transfer API - An architectural style for web services using HTTP methods (GET, POST, PUT, DELETE) for operations.",
        "category": "Automation",
        "week": 11,
        "related": ["API", "JSON"]
    },
    "JSON": {
        "definition": "JavaScript Object Notation - A lightweight data interchange format that is easy for humans to read and write and for machines to parse.",
        "category": "Automation",
        "week": 11,
        "related": ["API", "REST API"]
    },
    "CLI": {
        "definition": "Command Line Interface - A text-based interface for interacting with software and operating systems through commands.",
        "category": "Automation",
        "week": 11,
        "related": ["OpenStack CLI"]
    },
    "Ansible": {
        "definition": "An open-source automation tool for configuration management, application deployment, and task automation using declarative YAML playbooks.",
        "category": "Automation",
        "week": 11,
        "related": ["Infrastructure as Code"]
    },
    "Infrastructure as Code (IaC)": {
        "definition": "The practice of managing and provisioning infrastructure through machine-readable definition files rather than manual processes.",
        "category": "Automation",
        "week": 11,
        "related": ["Ansible", "Terraform"]
    },
    "Orchestration": {
        "definition": "The automated configuration, coordination, and management of computer systems and software, especially in cloud environments.",
        "category": "Automation",
        "week": 11,
        "related": ["Kubernetes", "OpenStack Heat"]
    }
}

def generate_glossary_html(output_path):
    """Generate the glossary HTML page"""
    
    # Sort terms alphabetically
    sorted_terms = sorted(GLOSSARY_DATA.items())
    
    # Get unique categories
    categories = sorted(set(term['category'] for term in GLOSSARY_DATA.values()))
    
    # Build letter index
    letters = sorted(set(term[0][0].upper() for term in sorted_terms))
    
    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Course Glossary - OPS3</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1e3a5f 0%, #142a46 100%);
            color: #ffffff;
            line-height: 1.6;
            padding: 20px;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        
        header {
            text-align: center;
            padding: 40px 20px;
            background: rgba(30, 58, 95, 0.6);
            border-radius: 15px;
            margin-bottom: 30px;
        }
        
        header h1 {
            font-size: 3em;
            color: #c9984a;
            margin-bottom: 10px;
        }
        
        header p {
            font-size: 1.2em;
            color: #c8c8c8;
        }
        
        .search-bar {
            margin: 30px 0;
            text-align: center;
        }
        
        #searchInput {
            width: 100%;
            max-width: 600px;
            padding: 15px 20px;
            font-size: 1.1em;
            border: 2px solid #c9984a;
            border-radius: 10px;
            background: rgba(255, 255, 255, 0.1);
            color: #ffffff;
        }
        
        #searchInput::placeholder {
            color: #c8c8c8;
        }
        
        .filter-bar {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            justify-content: center;
            margin: 20px 0;
        }
        
        .filter-btn {
            padding: 10px 20px;
            background: rgba(201, 152, 74, 0.2);
            border: 2px solid #c9984a;
            border-radius: 25px;
            color: #ffffff;
            cursor: pointer;
            transition: all 0.3s;
            font-size: 0.9em;
        }
        
        .filter-btn:hover,
        .filter-btn.active {
            background: #c9984a;
            color: #1e3a5f;
        }
        
        .letter-index {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            justify-content: center;
            margin: 30px 0;
            padding: 20px;
            background: rgba(30, 58, 95, 0.4);
            border-radius: 10px;
        }
        
        .letter-link {
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: rgba(201, 152, 74, 0.2);
            border: 2px solid #c9984a;
            border-radius: 50%;
            color: #c9984a;
            text-decoration: none;
            font-weight: bold;
            transition: all 0.3s;
        }
        
        .letter-link:hover {
            background: #c9984a;
            color: #1e3a5f;
            transform: scale(1.1);
        }
        
        .glossary-section {
            margin: 40px 0;
        }
        
        .letter-header {
            font-size: 2.5em;
            color: #c9984a;
            border-bottom: 3px solid #c9984a;
            padding-bottom: 10px;
            margin-bottom: 20px;
            margin-top: 40px;
        }
        
        .term-card {
            background: rgba(30, 58, 95, 0.6);
            border-left: 5px solid #c9984a;
            padding: 25px;
            margin-bottom: 20px;
            border-radius: 10px;
            transition: all 0.3s;
        }
        
        .term-card:hover {
            background: rgba(30, 58, 95, 0.8);
            transform: translateX(10px);
        }
        
        .term-title {
            font-size: 1.8em;
            color: #c9984a;
            margin-bottom: 10px;
            font-weight: bold;
        }
        
        .term-definition {
            font-size: 1.1em;
            line-height: 1.8;
            margin-bottom: 15px;
        }
        
        .term-meta {
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid rgba(201, 152, 74, 0.3);
        }
        
        .term-category,
        .term-week {
            background: rgba(201, 152, 74, 0.2);
            padding: 5px 15px;
            border-radius: 15px;
            font-size: 0.9em;
            color: #c9984a;
            text-decoration: none;
            display: inline-block;
        }
        
        .term-week {
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .term-week:hover {
            background: #c9984a;
            color: #1e3a5f;
            transform: scale(1.05);
        }
        
        .related-terms {
            margin-top: 10px;
        }
        
        .related-terms strong {
            color: #c9984a;
        }
        
        .related-link {
            color: #c8c8c8;
            text-decoration: none;
            margin-right: 10px;
            transition: color 0.3s;
        }
        
        .related-link:hover {
            color: #c9984a;
        }
        
        .back-to-top {
            position: fixed;
            bottom: 30px;
            right: 30px;
            background: #c9984a;
            color: #1e3a5f;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5em;
            text-decoration: none;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
            transition: all 0.3s;
            display: none;
        }
        
        .back-to-top:hover {
            transform: scale(1.1);
        }
        
        .home-button {
            display: inline-block;
            margin: 20px auto;
            padding: 12px 30px;
            background: #c9984a;
            color: #1e3a5f;
            text-decoration: none;
            border-radius: 25px;
            font-weight: bold;
            transition: all 0.3s;
        }
        
        .home-button:hover {
            background: #ffffff;
            transform: scale(1.05);
        }
        
        .stats {
            text-align: center;
            margin: 20px 0;
            padding: 20px;
            background: rgba(30, 58, 95, 0.4);
            border-radius: 10px;
        }
        
        .stats-item {
            display: inline-block;
            margin: 0 20px;
            font-size: 1.1em;
        }
        
        .stats-number {
            font-size: 2em;
            color: #c9984a;
            font-weight: bold;
        }
        
        @media (max-width: 768px) {
            header h1 {
                font-size: 2em;
            }
            
            .term-title {
                font-size: 1.4em;
            }
            
            .letter-index {
                gap: 5px;
            }
            
            .letter-link {
                width: 35px;
                height: 35px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📚 Course Glossary</h1>
            <p>OPS3 - Virtualization and Cloud Infrastructure</p>
            <p style="margin-top: 10px; font-size: 0.9em;">Comprehensive technical terms and definitions</p>
        </header>
        
        <div style="text-align: center;">
            <a href="index.html" class="home-button">← Back to Course Home</a>
        </div>
        
        <div class="stats">
            <div class="stats-item">
                <div class="stats-number">""" + str(len(GLOSSARY_DATA)) + """</div>
                <div>Total Terms</div>
            </div>
            <div class="stats-item">
                <div class="stats-number">""" + str(len(categories)) + """</div>
                <div>Categories</div>
            </div>
            <div class="stats-item">
                <div class="stats-number">12</div>
                <div>Weeks Covered</div>
            </div>
        </div>
        
        <div class="search-bar">
            <input type="text" id="searchInput" placeholder="🔍 Search for terms..." onkeyup="filterTerms()">
        </div>
        
        <div class="filter-bar">
            <button class="filter-btn active" onclick="filterByCategory('all')">All Categories</button>
"""
    
    for category in categories:
        html += f'            <button class="filter-btn" onclick="filterByCategory(\'{category}\')">{category}</button>\n'
    
    html += """        </div>
        
        <div class="letter-index">
"""
    
    for letter in letters:
        html += f'            <a href="#letter-{letter}" class="letter-link">{letter}</a>\n'
    
    html += """        </div>
        
        <div class="glossary-section" id="glossary-content">
"""
    
    current_letter = None
    for term, data in sorted_terms:
        first_letter = term[0].upper()
        
        if first_letter != current_letter:
            if current_letter is not None:
                html += "        </div>\n"
            html += f'        <div id="letter-{first_letter}">\n'
            html += f'            <h2 class="letter-header">{first_letter}</h2>\n'
            current_letter = first_letter
        
        html += f'            <div class="term-card" data-category="{data["category"]}">\n'
        html += f'                <div class="term-title">{term}</div>\n'
        html += f'                <div class="term-definition">{data["definition"]}</div>\n'
        html += '                <div class="term-meta">\n'
        html += f'                    <span class="term-category">📂 {data["category"]}</span>\n'
        
        # Make week badge clickable to student notes
        week_num = data["week"]
        week_folders = {
            1: "Week 1 - Introduction to Virtualization",
            2: "Week 2 - Virtual Machines",
            3: "Week 3 - Virtual Networking and Linux Networking Fundamentals",
            4: "Week 4 - Storage and Backup",
            5: "Week 5 - Containers and Resource Management",
            6: "Week 6 - Proxmox Cluster and High Availability",
            7: "Week 7 - Transition to Cloud Computing Concepts",
            8: "Week 8 - Cloud Foundation",
            9: "Week 9 - Compute Operations",
            10: "Week 10 - Storage and Persistence",
            11: "Week 11 - Automation and Cloud API",
            12: "Week 12 - Final Project and Review"
        }
        
        week_folder = week_folders.get(week_num, "")
        week_link = f"{week_folder}/Week_{week_num}_Student_Notes.html" if week_folder else "#"
        
        html += f'                    <a href="{week_link}" class="term-week" title="Jump to Week {week_num} Student Notes">📅 Week {week_num}</a>\n'
        html += '                </div>\n'
        
        if 'related' in data:
            html += '                <div class="related-terms">\n'
            html += '                    <strong>Related:</strong> '
            for related in data['related']:
                html += f'<a href="#" class="related-link" onclick="searchTerm(\'{related}\'); return false;">{related}</a>'
            html += '\n                </div>\n'
        
        html += '            </div>\n'
    
    if current_letter is not None:
        html += "        </div>\n"
    
    html += """        </div>
    </div>
    
    <a href="#" class="back-to-top" id="backToTop">↑</a>
    
    <script>
        // Search functionality
        function filterTerms() {
            const searchTerm = document.getElementById('searchInput').value.toLowerCase();
            const cards = document.querySelectorAll('.term-card');
            
            cards.forEach(card => {
                const title = card.querySelector('.term-title').textContent.toLowerCase();
                const definition = card.querySelector('.term-definition').textContent.toLowerCase();
                
                if (title.includes(searchTerm) || definition.includes(searchTerm)) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        }
        
        // Search for specific term
        function searchTerm(term) {
            document.getElementById('searchInput').value = term;
            filterTerms();
            window.scrollTo({top: 0, behavior: 'smooth'});
        }
        
        // Category filter
        let currentCategory = 'all';
        function filterByCategory(category) {
            currentCategory = category;
            const cards = document.querySelectorAll('.term-card');
            const buttons = document.querySelectorAll('.filter-btn');
            
            buttons.forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');
            
            cards.forEach(card => {
                if (category === 'all' || card.dataset.category === category) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        }
        
        // Back to top button
        window.addEventListener('scroll', () => {
            const backToTop = document.getElementById('backToTop');
            if (window.pageYOffset > 300) {
                backToTop.style.display = 'flex';
            } else {
                backToTop.style.display = 'none';
            }
        });
        
        document.getElementById('backToTop').addEventListener('click', (e) => {
            e.preventDefault();
            window.scrollTo({top: 0, behavior: 'smooth'});
        });
        
        // Smooth scrolling for letter links
        document.querySelectorAll('.letter-link').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const target = document.querySelector(link.getAttribute('href'));
                target.scrollIntoView({behavior: 'smooth', block: 'start'});
            });
        });
    </script>
</body>
</html>
"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ Glossary created with {len(GLOSSARY_DATA)} terms")
    print(f"   Categories: {', '.join(categories)}")
    print(f"   Output: {output_path}")

def main():
    """Main function"""
    base_dir = Path(__file__).parent.parent
    output_path = base_dir / "glossary.html"
    
    print("=" * 70)
    print("Creating Course Glossary")
    print("=" * 70)
    print()
    
    generate_glossary_html(output_path)
    
    print()
    print("=" * 70)
    print("✅ Glossary generation complete!")
    print("=" * 70)

if __name__ == "__main__":
    main()
