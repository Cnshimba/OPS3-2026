# Quiz questions for Weeks 3-12
# Comprehensive question bank for OPS3 course

WEEKS_3_12_QUESTIONS = {
    3: {  # Week 3 - Virtual Networking
        "scenario": [
            {
                "question": "Your company needs VMs on the same host to communicate with external networks and appear as if they're on the same LAN. Which networking mode should you configure?",
                "options": ["NAT", "Host-only", "Bridged", "Internal"],
                "answer": "Bridged",
                "explanation": "Bridged networking connects VMs directly to the physical network, making them appear as physical devices on the LAN."
            },
            {
                "question": "You're setting up a development environment where VMs need to communicate with each other but NOT access external networks. What's the best network configuration?",
                "options": ["Bridged", "NAT", "Internal/Host-only", "VLAN"],
                "answer": "Internal/Host-only",
                "explanation": "Internal or host-only networks isolate VMs from external access while allowing inter-VM communication."
            },
            {
                "question": "A network administrator wants to segment network traffic logically without adding physical switches. Which technology should they implement?",
                "options": ["NAT", "DHCP", "VLAN", "DNS"],
                "answer": "VLAN",
                "explanation": "VLANs (Virtual LANs) provide logical network segmentation without requiring physical hardware changes."
            }
        ],
        "fill_blank": [
            {
                "question": "A _______ connects two or more network segments, allowing VMs to appear on the same network as the physical host.",
                "answer": "bridge",
                "alternatives": ["Bridge", "network bridge"],
                "explanation": "A bridge is a network device that connects different network segments at the data link layer."
            },
            {
                "question": "_______ automatically assigns IP addresses and network configuration to devices on a network.",
                "answer": "DHCP",
                "alternatives": ["dhcp", "Dynamic Host Configuration Protocol"],
                "explanation": "DHCP (Dynamic Host Configuration Protocol) automates IP address assignment."
            },
            {
                "question": "_______ translates human-readable domain names into IP addresses.",
                "answer": "DNS",
                "alternatives": ["dns", "Domain Name System"],
                "explanation": "DNS provides the name-to-IP resolution service for networks."
            }
        ],
        "command": [
            {
                "question": "Complete the command to create a Linux bridge named vmbr0:",
                "prompt": "ip link add name _______ type bridge",
                "answer": "vmbr0",
                "explanation": "The bridge name follows the 'name' parameter in the ip link add command."
            },
            {
                "question": "Complete the command to check network interface status:",
                "prompt": "ip _______ show",
                "answer": "link",
                "alternatives": ["addr", "a"],
                "explanation": "'ip link show' displays network interface information and status."
            }
        ]
    },
    4: {  # Week 4 - Storage
        "scenario": [
            {
                "question": "You need a storage solution that supports snapshots, compression, and self-healing from data corruption. Which filesystem should you use?",
                "options": ["ext4", "NTFS", "ZFS", "FAT32"],
                "answer": "ZFS",
                "explanation": "ZFS is an advanced filesystem offering snapshots, compression, RAID, and data integrity verification."
            },
            {
                "question": "A company requires network-accessible block storage for their virtualization cluster. Which protocol is most suitable?",
                "options": ["NFS", "SMB", "iSCSI", "FTP"],
                "answer": "iSCSI",
                "explanation": "iSCSI provides block-level storage access over IP networks, ideal for virtualization."
            },
            {
                "question": "You need to resize partitions dynamically without downtime. What technology should you implement?",
                "options": ["Standard partitions", "LVM", "RAID", "ZFS pools"],
                "answer": "LVM",
                "explanation": "LVM (Logical Volume Manager) allows dynamic volume resizing without unmounting."
            }
        ],
        "fill_blank": [
            {
                "question": "A _______ pool is a collection of storage resources that can be allocated to virtual machines.",
                "answer": "storage",
                "alternatives": ["Storage"],
                "explanation": "Storage pools aggregate physical storage into a managed resource pool for VMs."
            },
            {
                "question": "_______ provides distributed object, block, and file storage in a unified platform.",
                "answer": "Ceph",
                "alternatives": ["ceph"],
                "explanation": "Ceph is a highly scalable distributed storage system."
            }
        ],
        "command": [
            {
                "question": "Complete the command to create a ZFS pool named 'tank':",
                "prompt": "zpool create _______ /dev/sda /dev/sdb",
                "answer": "tank",
                "explanation": "The pool name comes immediately after 'zpool create'."
            },
            {
                "question": "Complete the command to display LVM volume groups:",
                "prompt": "_______ display",
                "answer": "vgdisplay",
                "alternatives": ["vgs"],
                "explanation": "'vgdisplay' shows detailed information about volume groups."
            }
        ]
    },
    5: {  # Week 5 - Containers
        "scenario": [
            {
                "question": "Your application needs to run the same way across development, testing, and production environments. What solution provides this consistency?",
                "options": ["Virtual Machines", "Physical servers", "Docker containers", "Cloud Functions"],
                "answer": "Docker containers",
                "explanation": "Containers package applications with all dependencies, ensuring consistency across environments."
            },
            {
                "question": "You need to deploy and scale 100 microservices containers across multiple hosts automatically. What tool should you use?",
                "options": ["Docker", "LXC", "Kubernetes", "Proxmox"],
                "answer": "Kubernetes",
                "explanation": "Kubernetes orchestrates container deployment, scaling, and management across cluster nodes."
            },
            {
                "question": "What's the main difference between containers and VMs regarding resource usage?",
                "options": ["Containers use more RAM", "Containers share the host OS kernel", "VMs start faster", "Containers require hypervisors"],
                "answer": "Containers share the host OS kernel",
                "explanation": "Containers share the host kernel, making them lighter than VMs which run full OS instances."
            }
        ],
        "fill_blank": [
            {
                "question": "A _______ is a read-only template containing application code and dependencies for creating Docker containers.",
                "answer": "image",
                "alternatives": ["Image", "Docker image", "docker image"],
                "explanation": "Docker images are the blueprint for creating container instances."
            },
            {
                "question": "_______ is a text file containing instructions for building a Docker image.",
                "answer": "Dockerfile",
                "alternatives": ["dockerfile"],
                "explanation": "Dockerfiles define the steps to create a container image."
            },
            {
                "question": "In Kubernetes, a _______ is the smallest deployable unit that can contain one or more containers.",
                "answer": "pod",
                "alternatives": ["Pod"],
                "explanation": "Pods are the basic execution unit in Kubernetes."
            }
        ],
        "command": [
            {
                "question": "Complete the command to build a Docker image from a Dockerfile:",
                "prompt": "docker build -t myapp:v1 _______",
                "answer": ".",
                "alternatives": ["./"],
                "explanation": "The dot (.) specifies the current directory as the build context."
            },
            {
                "question": "Complete the command to run a container from an image:",
                "prompt": "docker _______ -d nginx",
                "answer": "run",
                "explanation": "'docker run' creates and starts a container from an image."
            },
            {
                "question": "Complete the command to list running containers:",
                "prompt": "docker _______ ls",
                "answer": "container",
                "alternatives": ["ps"],
                "explanation": "'docker container ls' or 'docker ps' lists running containers."
            }
        ]
    },
    6: {  # Week 6 - High Availability
        "scenario": [
            {
                "question": "A node in your Proxmox cluster fails. How does the cluster determine which nodes can make decisions about failover?",
                "options": ["All nodes vote equally", "Through quorum mechanism", "The oldest node decides", "Manually by admin"],
                "answer": "Through quorum mechanism",
                "explanation": "Quorum ensures a majority of nodes agree before making cluster decisions, preventing split-brain."
            },
            {
                "question": "You want to prevent a failed node from damaging shared storage. What mechanism should be configured?",
                "options": ["Backup", "Snapshot", "Fencing/STONITH", "Replication"],
                "answer": "Fencing/STONITH",
                "explanation": "Fencing (STONITH - Shoot The Other Node In The Head) isolates failed nodes to protect data integrity."
            },
            {
                "question": "What's the minimum number of nodes required for a proper quorum in a Proxmox cluster?",
                "options": ["1", "2", "3", "5"],
                "answer": "3",
                "explanation": "Three nodes provide proper quorum (majority voting), while 2 nodes can lead to split-brain scenarios."
            }
        ],
        "fill_blank": [
            {
                "question": "_______ is the cluster membership and communication layer in Proxmox.",
                "answer": "Corosync",
                "alternatives": ["corosync"],
                "explanation": "Corosync provides cluster communication and quorum services."
            },
            {
                "question": "_______ is the automatic transfer of operations from a failed component to a backup.",
                "answer": "failover",
                "alternatives": ["Failover"],
                "explanation": "Failover maintains service availability when primary systems fail."
            }
        ],
        "command": [
            {
                "question": "Complete the command to check cluster status in Proxmox:",              
                "prompt": "pvecm _______",
                "answer": "status",
                "explanation": "'pvecm status' displays the current cluster state and quorum information."
            },
            {
                "question": "Complete the command to create a Proxmox cluster named 'production':",
                "prompt": "pvecm create _______",
                "answer": "production",
                "explanation": "The cluster name follows the 'pvecm create' command."
            }
        ]
    },
    7: {  # Week 7 - Cloud Computing Concepts
        "scenario": [
            {
                "question": "A startup wants to deploy applications without managing servers or infrastructure. Which cloud service model should they use?",
                "options": ["IaaS", "PaaS", "SaaS", "DaaS"],
                "answer": "PaaS",
                "explanation": "PaaS (Platform as a Service) provides development platforms without infrastructure management."
            },
            {
                "question": "Your organization needs full control over VMs, storage, and networks in the cloud. What service model fits this requirement?",
                "options": ["SaaS", "PaaS", "IaaS", "FaaS"],
                "answer": "IaaS",
                "explanation": "IaaS (Infrastructure as a Service) provides virtualized computing resources with full control."
            },
            {
                "question": "Which deployment model keeps infrastructure on-premises while using cloud services for backup?",
                "options": ["Public cloud", "Private cloud", "Hybrid cloud", "Community cloud"],
                "answer": "Hybrid cloud",
                "explanation": "Hybrid cloud combines on-premises infrastructure with public cloud services."
            }
        ],
        "fill_blank": [
            {
                "question": "_______ as a Service provides complete software applications delivered over the internet.",
                "answer": "Software",
                "alternatives": ["SaaS"],
                "explanation": "SaaS delivers fully functional applications to end users via the internet."
            },
            {
                "question": "_______ computing delivers IT services over the internet on-demand with pay-as-you-go pricing.",
                "answer": "Cloud",
                "alternatives": ["cloud"],
                "explanation": "Cloud computing provides scalable resources accessible over the internet."
            }
        ],
        "command": [
            {
                "question": "Complete the OpenStack command to list available services:",
                "prompt": "openstack _______ list",
                "answer": "service",
                "alternatives": ["catalog"],
                "explanation": "'openstack service list' shows all OpenStack services in the deployment."
            }
        ]
    },
    8: {  # Week 8 - OpenStack Foundation
        "scenario": [
            {
                "question": "Users need to authenticate before accessing OpenStack services. Which component handles this?",
                "options": ["Nova", "Neutron", "Keystone", "Horizon"],
                "answer": "Keystone",
                "explanation": "Keystone is OpenStack's identity service, providing authentication and authorization."
            },
            {
                "question": "Administrators want a web-based GUI to manage OpenStack resources. Which component provides this?",
                "options": ["Keystone", "Glance", "Horizon", "Cinder"],
                "answer": "Horizon",
                "explanation": "Horizon is the OpenStack dashboard providing web-based management interface."
            },
            {
                "question": "You need to store and manage VM images in OpenStack. Which service handles this?",
                "options": ["Nova", "Glance", "Swift", "Cinder"],
                "answer": "Glance",
                "explanation": "Glance is the image registry service for storing and retrieving VM images."
            }
        ],
        "fill_blank": [
            {
                "question": "_______ is OpenStack's compute service responsible for managing virtual machine instances.",
                "answer": "Nova",
                "alternatives": ["nova"],
                "explanation": "Nova handles VM provisioning, scheduling, and lifecycle management."
            },
            {
                "question": "In OpenStack, a _______ is a logical grouping of users and resources for isolation.",
                "answer": "project",
                "alternatives": ["Project", "tenant", "Tenant"],
                "explanation": "Projects (formerly tenants) provide resource and user isolation in OpenStack."
            },
            {
                "question": "_______ provides networking-as-a-service for OpenStack environments.",
                "answer": "Neutron",
                "alternatives": ["neutron"],
                "explanation": "Neutron manages virtual networks, routers, and firewalls in OpenStack."
            }
        ],
        "command": [
            {
                "question": "Complete the command to source OpenStack credentials:",
                "prompt": "source _______",
                "answer": "openrc",
                "alternatives": ["adminrc", "admin-openrc"],
                "explanation": "Sourcing the openrc file loads OpenStack environment variables for authentication."
            },
            {
                "question": "Complete the command to list OpenStack projects:",
                "prompt": "openstack _______ list",
                "answer": "project",
                "explanation": "'openstack project list' displays all projects in the OpenStack deployment."
            }
        ]
    },
    9: {  # Week 9 - Compute Operations
        "scenario": [
            {
                "question": "You need to create 50 VMs with specific CPU, RAM, and disk configurations. What OpenStack resource defines these specifications?",
                "options": ["Image", "Flavor", "Network", "Volume"],
                "answer": "Flavor",
                "explanation": "Flavors define the virtual hardware template (vCPUs, RAM, disk) for VM instances."
            },
            {
                "question": "A VM needs additional storage that persists even if the VM is deleted. What should you attach?",
                "options": ["Ephemeral disk", "Image", "Cinder volume", "Flavor"],
                "answer": "Cinder volume",
                "explanation": "Cinder volumes provide persistent block storage that survives VM termination."
            },
            {
                "question": "You want to quickly deploy multiple identical web servers. What's the most efficient approach?",
                "options": ["Create each manually", "Use a snapshot as base image", "Clone VMs", "Use Heat templates"],
                "answer": "Use Heat templates",
                "explanation": "Heat (Orchestration) automates deployment of multiple identical resources from templates."
            }
        ],
        "fill_blank": [
            {
                "question": "In OpenStack, a _______ defines the amount of vCPUs, RAM, and disk for a virtual machine.",
                "answer": "flavor",
                "alternatives": ["Flavor"],
                "explanation": "Flavors are VM size templates in OpenStack."
            },
            {
                "question": "A _______ IP address in OpenStack allows external access to an instance.",
                "answer": "floating",
                "alternatives": ["Floating", "public"],
                "explanation": "Floating IPs are publicly accessible addresses that can be assigned to instances."
            }
        ],
        "command": [
            {
                "question": "Complete the command to create an OpenStack instance named 'web1':",
                "prompt": "openstack server create --flavor m1.small --image ubuntu _______ web1",
                "answer": "--network",
                "alternatives": ["--nic"],
                "explanation": "The --network parameter specifies which network to connect the instance to."
            },
            {
                "question": "Complete the command to list all OpenStack instances:",
                "prompt": "openstack _______ list",
                "answer": "server",
                "explanation": "'openstack server list' shows all VM instances."
            }
        ]
    },
    10: {  # Week 10 - Storage and Persistence
        "scenario": [
            {
                "question": "A database application requires persistent storage that can be attached to different VMs. Which OpenStack service provides this?",
                "options": ["Swift", "Nova", "Cinder", "Glance"],
                "answer": "Cinder",
                "explanation": "Cinder provides block storage volumes that can be attached/detached from instances."
            },
            {
                "question": "You need object storage for millions of unstructured files like images and backups. Which service should you use?",
                "options": ["Cinder", "Swift", "Glance", "Manila"],
                "answer": "Swift",
                "explanation": "Swift provides scalable object storage for unstructured data."
            },
            {
                "question": "What's the main difference between block storage (Cinder) and object storage (Swift)?",
                "options": ["Cinder is faster", "Cinder provides file-level access", "Cinder provides block-level access like a hard drive", "Swift is more expensive"],
                "answer": "Cinder provides block-level access like a hard drive",
                "explanation": "Cinder offers block-level storage (like a raw disk), while Swift provides object-level storage (like S3)."
            }
        ],
        "fill_blank": [
            {
                "question": "_______ is OpenStack's block storage service for persistent volumes.",
                "answer": "Cinder",
                "alternatives": ["cinder"],
                "explanation": "Cinder manages creation, attachment, and snapshots of block storage volumes."
            },
            {
                "question": "_______ provides object storage for OpenStack, similar to Amazon S3.",
                "answer": "Swift",
                "alternatives": ["swift"],
                "explanation": "Swift stores objects (files) with metadata in a distributed system."
            }
        ],
        "command": [
            {
                "question": "Complete the command to create a 50GB Cinder volume:",
                "prompt": "openstack volume create --size _______ myvolume",
                "answer": "50",
                "explanation": "The size parameter specifies volume size in gigabytes."
            },
            {
                "question": "Complete the command to attach a volume to an instance:",
                "prompt": "openstack server add volume _______ myvolume",
                "answer": "web1",
                "alternatives": ["<instance-id>", "<server>"],
                "explanation": "The instance name or ID comes before the volume name in the attach command."
            }
        ]
    },
    11: {  # Week 11 - Automation and API
        "scenario": [
            {
                "question": "You need to automate deployment of 100 identical servers with specific configurations. Which tool is best for this?",
                "options": ["Manual scripting", "Ansible", "GUI", "SSH loops"],
                "answer": "Ansible",
                "explanation": "Ansible provides declarative automation for configuration management at scale."
            },
            {
                "question": "Your application needs to programmatically create VMs in OpenStack. What should you use?",
                "options": ["Horizon dashboard", "OpenStack CLI", "OpenStack API", "Manual processes"],
                "answer": "OpenStack API",
                "explanation": "APIs provide programmatic access for automation and integration."
            },
            {
                "question": "Which format is commonly used for Ansible playbooks and API responses?",
                "options": ["XML", "JSON/YAML", "CSV", "HTML"],
                "answer": "JSON/YAML",
                "explanation": "YAML is used for Ansible playbooks, while JSON is common for API data exchange."
            }
        ],
        "fill_blank": [
            {
                "question": "_______ is an automation tool that uses YAML playbooks for configuration management.",
                "answer": "Ansible",
                "alternatives": ["ansible"],
                "explanation": "Ansible automates IT infrastructure using simple, readable playbooks."
            },
            {
                "question": "_______ as Code is the practice of managing infrastructure through machine-readable files.",
                "answer": "Infrastructure",
                "alternatives": ["IaC"],
                "explanation": "IaC treats infrastructure configuration as code for version control and automation."
            },
            {
                "question": "A _______ API uses HTTP methods like GET, POST, PUT, and DELETE for operations.",
                "answer": "REST",
                "alternatives": ["rest", "RESTful"],
                "explanation": "REST (Representational State Transfer) APIs use standard HTTP methods."
            }
        ],
        "command": [
            {
                "question": "Complete the Ansible command to run a playbook:",
                "prompt": "ansible-playbook _______",
                "answer": "site.yml",
                "alternatives": ["playbook.yml", "deploy.yml"],
                "explanation": "ansible-playbook executes the specified YAML playbook file."
            },
            {
                "question": "Complete the curl command to GET data from an API:",
                "prompt": "curl -X _______ https://api.example.com/resource",
                "answer": "GET",
                "explanation": "GET is the HTTP method for retrieving data from APIs."
            }
        ]
    },
    12: {  # Week 12 - Review and Project
        "scenario": [
            {
                "question": "You're designing a high-availability web application on OpenStack. Which components are essential? (Select the BEST comprehensive answer)",
                "options": [
                    "Just multiple VMs",
                    "Load balancer, multiple VMs across availability zones, persistent storage, automated failover",
                    "Single large VM",
                    "Containers only"
                ],
                "answer": "Load balancer, multiple VMs across availability zones, persistent storage, automated failover",
                "explanation": "HA requires redundancy, load distribution, data persistence, and automatic recovery mechanisms."
            },
            {
                "question": "A project requires virtualization for VMs, container orchestration, and cloud management. Which combination provides all three?",
                "options": [
                    "Proxmox + Docker + OpenStack",
                    "Only VirtualBox",
                    "Only Kubernetes",
                    "Only OpenStack"
                ],
                "answer": "Proxmox + Docker + OpenStack",
                "explanation": "This stack provides VM management (Proxmox), containers (Docker), and cloud orchestration (OpenStack)."
            },
            {
                "question": "What's the key advantage of using Infrastructure as Code for cloud deployments?",
                "options": [
                    "It's faster to type",
                    "Reproducibility, version control, and automation",
                    "It looks professional",
                    "It's required by law"
                ],
                "answer": "Reproducibility, version control, and automation",
                "explanation": "IaC enables consistent, version-controlled, automated infrastructure deployments."
            }
        ],
        "fill_blank": [
            {
                "question": "The three main cloud service models are IaaS, PaaS, and _______.",
                "answer": "SaaS",
                "alternatives": ["saas", "Software as a Service"],
                "explanation": "IaaS, PaaS, and SaaS are the three primary cloud service delivery models."
            },
            {
                "question": "In OpenStack, _______ manages compute, _______ manages networking, and _______ manages block storage.",
                "answer": "Nova",
                "alternatives": ["nova"],
                "explanation": "Nova (compute), Neutron (networking), and Cinder (storage) are core OpenStack services."
            }
        ],
        "command": [
            {
                "question": "Complete the command to check if KVM is properly loaded:",
                "prompt": "lsmod | grep _______",
                "answer": "kvm",
                "alternatives": ["KVM"],
                "explanation": "This checks if the KVM kernel module is loaded."
            },
            {
                "question": "Complete the command to view all OpenStack endpoints:",
                "prompt": "openstack _______ list",
                "answer": "endpoint",
                "alternatives": ["catalog"],
                "explanation": "'openstack endpoint list' shows all service API endpoints."
            }
        ]
    }
}
