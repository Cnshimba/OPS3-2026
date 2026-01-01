#!/usr/bin/env python3
"""
Add AI Chatbot to Glossary Page
Enhances the glossary with an interactive AI assistant sidebar
"""

from pathlib import Path
import re

def add_chatbot_to_glossary(glossary_path):
    """Add AI chatbot sidebar to the glossary HTML"""
    
    with open(glossary_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Find the insertion point - after the header styles
    style_insertion = html_content.find('        @media (max-width: 768px) {')
    
    chatbot_styles = """
        /* AI Chat Assistant Styles */
        .chat-container {
            position: fixed;
            bottom: 100px;
            right: 30px;
            width: 350px;
            max-height: 600px;
            background: linear-gradient(135deg, #1e3a5f 0%, #142a46 100%);
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
            border: 2px solid #c9984a;
            display: flex;
            flex-direction: column;
            z-index: 1000;
            transition: all 0.3s;
        }
        
        .chat-container.minimized {
            max-height: 60px;
        }
        
        .chat-header {
            background: #c9984a;
            color: #1e3a5f;
            padding: 15px;
            border-radius: 13px 13px 0 0;
            font-weight: bold;
            display: flex;
            justify-content: space-between;
            align-items: center;
            cursor: pointer;
        }
        
        .chat-header h3 {
            margin: 0;
            font-size: 1.1em;
        }
        
        .chat-toggle {
            background: none;
            border: none;
            color: #1e3a5f;
            font-size: 1.2em;
            cursor: pointer;
            padding: 0 5px;
        }
        
        .chat-messages {
            flex: 1;
            overflow-y: auto;
            padding: 15px;
            display: flex;
            flex-direction: column;
            gap: 10px;
            max-height: 400px;
        }
        
        .chat-message {
            padding: 10px 12px;
            border-radius: 10px;
            max-width: 85%;
            word-wrap: break-word;
        }
        
        .chat-message.user {
            background: rgba(201, 152, 74, 0.3);
            align-self: flex-end;
            border: 1px solid #c9984a;
            color: #ffffff;
        }
        
        .chat-message.bot {
            background: rgba(30, 58, 95, 0.8);
            align-self: flex-start;
            border: 1px solid rgba(201, 152, 74, 0.5);
            color: #ffffff;
        }
        
        .chat-message.bot strong {
            color: #c9984a;
        }
        
        .chat-input-container {
            padding: 15px;
            border-top: 1px solid rgba(201, 152, 74, 0.3);
        }
        
        .chat-input {
            width: 100%;
            padding: 10px;
            border: 2px solid #c9984a;
            border-radius: 8px;
            background: rgba(255, 255, 255, 0.1);
            color: #ffffff;
            font-size: 0.9em;
        }
        
        .chat-input::placeholder {
            color: #c8c8c8;
        }
        
        .chat-send-btn {
            width: 100%;
            margin-top: 10px;
            padding: 10px;
            background: #c9984a;
            color: #1e3a5f;
            border: none;
            border-radius: 8px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .chat-send-btn:hover {
            background: #ffffff;
            transform: scale(1.02);
        }
        
        .chat-suggestions {
            display: flex;
            flex-wrap: wrap;
            gap: 5px;
            padding: 10px;
            border-top: 1px solid rgba(201, 152, 74, 0.2);
        }
        
        .suggestion-btn {
            padding: 6px 12px;
            background: rgba(201, 152, 74, 0.2);
            border: 1px solid #c9984a;
            border-radius: 15px;
            color: #c9984a;
            font-size: 0.85em;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .suggestion-btn:hover {
            background: #c9984a;
            color: #1e3a5f;
        }
        
        .typing-indicator {
            display: none;
            align-self: flex-start;
            padding: 10px;
        }
        
        .typing-indicator.active {
            display: block;
        }
        
        .typing-dot {
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #c9984a;
            margin: 0 2px;
            animation: typing 1.4s infinite;
        }
        
        .typing-dot:nth-child(2) {
            animation-delay: 0.2s;
        }
        
        .typing-dot:nth-child(3) {
            animation-delay: 0.4s;
        }
        
        @keyframes typing {
            0%, 60%, 100% {
                transform: translateY(0);
            }
            30% {
                transform: translateY(-10px);
            }
        }
        
"""
    
    # Insert chatbot styles before media query
    html_content = html_content[:style_insertion] + chatbot_styles + html_content[style_insertion:]
    
    # Add chatbot HTML before closing body tag
    chatbot_html = """
    <!-- AI Chat Assistant -->
    <div class="chat-container" id="chatContainer">
        <div class="chat-header" onclick="toggleChat()">
            <h3>🤖 AI Study Assistant</h3>
            <button class="chat-toggle" id="chatToggle">−</button>
        </div>
        <div class="chat-messages" id="chatMessages">
            <div class="chat-message bot">
                <strong>Hi there!</strong> I'm your AI study assistant for OPS3. Ask me anything about virtualization, cloud computing, containers, or any course topic!
            </div>
        </div>
        <div class="chat-suggestions">
            <button class="suggestion-btn" onclick="askQuestion('What is the difference between Type 1 and Type 2 hypervisors?')">Hypervisor Types?</button>
            <button class="suggestion-btn" onclick="askQuestion('Explain containers vs VMs')">Containers vs VMs?</button>
            <button class="suggestion-btn" onclick="askQuestion('What is OpenStack?')">OpenStack?</button>
        </div>
        <div class="chat-input-container">
            <input type="text" class="chat-input" id="chatInput" placeholder="Ask a question..." onkeypress="if(event.key==='Enter') sendMessage()">
            <button class="chat-send-btn" onclick="sendMessage()">Send Question</button>
        </div>
        <div class="typing-indicator" id="typingIndicator">
            <span class="typing-dot"></span>
            <span class="typing-dot"></span>
            <span class="typing-dot"></span>
        </div>
    </div>
    
    <script>
        // Chat functionality
        let chatMinimized = false;
        
        function toggleChat() {
            const container = document.getElementById('chatContainer');
            const toggle = document.getElementById('chatToggle');
            chatMinimized = !chatMinimized;
            
            if (chatMinimized) {
                container.classList.add('minimized');
                toggle.textContent = '+';
            } else {
                container.classList.remove('minimized');
                toggle.textContent = '−';
            }
        }
        
        function addMessage(text, isUser) {
            const messagesDiv = document.getElementById('chatMessages');
            const messageDiv = document.createElement('div');
            messageDiv.className = `chat-message ${isUser ? 'user' : 'bot'}`;
            messageDiv.innerHTML = text;
            messagesDiv.appendChild(messageDiv);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }
        
        function showTyping() {
            document.getElementById('typingIndicator').classList.add('active');
        }
        
        function hideTyping() {
            document.getElementById('typingIndicator').classList.remove('active');
        }
        
        function askQuestion(question) {
            document.getElementById('chatInput').value = question;
            sendMessage();
        }
        
        async function sendMessage() {
            const input = document.getElementById('chatInput');
            const question = input.value.trim();
            
            if (!question) return;
            
            // Add user message
            addMessage(question, true);
            input.value = '';
            
            // Show typing indicator
            showTyping();
            
            // Simulate AI response (you can replace this with actual API call)
            setTimeout(() => {
                hideTyping();
                const response = getAIResponse(question);
                addMessage(response, false);
            }, 1500);
        }
        
        function getAIResponse(question) {
            const lowerQ = question.toLowerCase();
            
            // Simple pattern matching for demo - you can integrate real AI API here
            if (lowerQ.includes('hypervisor')) {
                return `<strong>Hypervisors:</strong><br>
                    <strong>Type 1 (Bare-metal):</strong> Runs directly on hardware without a host OS. Examples: KVM, VMware ESXi, Proxmox VE. More efficient and better for production.<br><br>
                    <strong>Type 2 (Hosted):</strong> Runs on top of a host OS. Examples: VirtualBox, VMware Workstation. Easier to set up but less efficient.`;
            }
            
            if (lowerQ.includes('container') && lowerQ.includes('vm')) {
                return `<strong>Containers vs Virtual Machines:</strong><br>
                    <strong>Containers:</strong> Share the host OS kernel, lightweight, start in seconds, less overhead. Good for microservices.<br><br>
                    <strong>VMs:</strong> Have their own OS, more isolated, heavier, start in minutes. Better for running different OSes or complete isolation.`;
            }
            
            if (lowerQ.includes('openstack')) {
                return `<strong>OpenStack:</strong> An open-source cloud computing platform for building IaaS clouds.<br><br>
                    <strong>Key Components:</strong><br>
                    • <strong>Nova:</strong> Compute (VMs)<br>
                    • <strong>Neutron:</strong> Networking<br>
                    • <strong>Cinder:</strong> Block Storage<br>
                    • <strong>Glance:</strong> Images<br>
                    • <strong>Keystone:</strong> Authentication<br>
                    • <strong>Horizon:</strong> Web Dashboard`;
            }
            
            if (lowerQ.includes('kvm')) {
                return `<strong>KVM (Kernel-based Virtual Machine):</strong> A Type 1 hypervisor built into the Linux kernel. Works with QEMU for full virtualization. Used by Proxmox VE and many cloud providers.`;
            }
            
            if (lowerQ.includes('docker')) {
                return `<strong>Docker:</strong> A platform for building, shipping, and running containers.<br><br>
                    • <strong>Images:</strong> Templates for containers<br>
                    • <strong>Containers:</strong> Running instances<br>
                    • <strong>Dockerfile:</strong> Instructions to build images<br>
                    • <strong>Docker Hub:</strong> Image registry`;
            }
            
            if (lowerQ.includes('proxmox')) {
                return `<strong>Proxmox VE:</strong> Open-source virtualization platform combining KVM (for VMs) and LXC (for containers). Features web-based management, clustering, and high availability.`;
            }
            
            if (lowerQ.includes('high availability') || lowerQ.includes(' ha ')) {
                return `<strong>High Availability:</strong> System design to ensure minimal downtime (99.9%+ uptime).<br><br>
                    <strong>Key Concepts:</strong><br>
                    • <strong>Clustering:</strong> Multiple servers working together<br>
                    • <strong>Failover:</strong> Automatic switch to backup<br>
                    • <strong>Quorum:</strong> Minimum nodes needed<br>
                    • <strong>Fencing:</strong> Isolating failed nodes`;
            }
            
            if (lowerQ.includes('cloud') && lowerQ.includes('service')) {
                return `<strong>Cloud Service Models:</strong><br>
                    <strong>IaaS:</strong> Infrastructure (servers, storage, networks). Example: OpenStack, AWS EC2<br><br>
                    <strong>PaaS:</strong> Platform for development. Example: Google App Engine <br><br>
                    <strong>SaaS:</strong> Software applications. Example: Gmail, Office 365`;
            }
            
            // Default response
            return `<strong>Great question!</strong> I can help with topics like:<br>
                • Virtualization (hypervisors, VMs, KVM, Proxmox)<br>
                • Containers (Docker, Kubernetes, LXC)<br>
                • Cloud Computing (OpenStack, IaaS/PaaS/SaaS)<br>
                • Networking (VLANs, SDN, bridges)<br>
                • Storage (ZFS, Ceph, LVM)<br>
                • High Availability (clusters, failover)<br><br>
                Try asking about specific terms from the glossary, or check the term definitions above! 📚`;
        }
    </script>
"""
    
    # Insert before closing body tag
    body_close = html_content.rfind('</body>')
    html_content = html_content[:body_close] + chatbot_html + html_content[body_close:]
    
    # Write back
    with open(glossary_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Added AI chatbot to glossary")

def main():
    """Main function"""
    base_dir = Path(__file__).parent.parent
    glossary_path = base_dir / "glossary.html"
    
    print("=" * 70)
    print("Adding AI Chatbot to Glossary")
    print("=" * 70)
    print()
    
    add_chatbot_to_glossary(glossary_path)
    
    print()
    print("=" * 70)
    print(" Glossary now has an interactive AI assistant!")
    print("=" * 70)

if __name__ == "__main__":
    main()
