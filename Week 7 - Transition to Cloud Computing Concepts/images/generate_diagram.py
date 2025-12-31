from PIL import Image, ImageDraw, ImageFont
import os

# Canvas setup
width = 800
height = 600
img = Image.new('RGB', (width, height), color='white')
d = ImageDraw.Draw(img)

# Colors
box_color = "#e1f5fe"
border_color = "#0277bd"
text_color = "black"
line_color = "black"

# Coordinates
x_center = width // 2
y_start = 50
y_step = 85
box_w = 200
box_h = 50

def draw_step(y, text, step_label=None):
    # Box
    x0 = x_center - box_w // 2
    x1 = x_center + box_w // 2
    y0 = y
    y1 = y + box_h
    d.rectangle([x0, y0, x1, y1], fill=box_color, outline=border_color, width=2)
    
    # Text in Box
    # Simple centering approximation (since font metrics are tricky without external fonts)
    d.text((x0 + 10, y0 + 15), text, fill=text_color)
    
    # Arrow from previous
    if step_label:
        prev_y = y - (y_step - box_h)
        # Line
        d.line([(x_center, prev_y), (x_center, y0)], fill=line_color, width=2)
        # Arrowhead (simple)
        d.polygon([(x_center, y0), (x_center-5, y0-10), (x_center+5, y0-10)], fill=line_color)
        # Label
        d.text((x_center + 10, y0 - 30), step_label, fill="red")

# Drawing the Flow
y = y_start

# User
draw_step(y, "User / Horizon")
y += y_step

# Keystone
draw_step(y, "Keystone (Identity)", "1. Request Token")
y += y_step

# Nova
draw_step(y, "Nova (Compute)", "2. Request VM")
y += y_step

# Sched (Decision diamond simulation)
# Just a box for simplicity in this generated script
draw_step(y, "Scheduler", "3. Select Host")
y += y_step

# Neutron
draw_step(y, "Neutron (Network)", "4. Request IP")
y += y_step

# Glance
draw_step(y, "Glance (Image)", "5. Get Image")
y += y_step

# Hypervisor
draw_step(y, "Hypervisor (KVM)", "6. Boot VM")

# Save
output_path = os.path.join(os.path.dirname(__file__), "openstack_vm_flow.png")
img.save(output_path)
print(f"Generated {output_path}")
