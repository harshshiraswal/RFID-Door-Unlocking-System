import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, Arrow
import numpy as np

# =============================================================================
# GLOBAL SETTINGS - Font and display configuration for consistent styling
# =============================================================================
plt.rcParams['font.family'] = 'system-ui'  # Use system default font for better compatibility
plt.rcParams['font.size'] = 9              # Base font size for all text
plt.rcParams['axes.titlesize'] = 13        # Larger font size for titles

def create_structural_diagram():
    """
    Creates the structural overview diagram showing component connections and system workflow.
    This diagram focuses on how components interact with each other.
    """
    # Initialize figure with specific dimensions (14x10 inches)
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(0, 14)  # Set X-axis boundaries
    ax.set_ylim(0, 10)  # Set Y-axis boundaries
    ax.set_aspect('equal')  # Maintain equal aspect ratio
    ax.axis('off')  # Hide axes for cleaner look
    
    # =========================================================================
    # TITLE SECTION
    # =========================================================================
    title_box = FancyBboxPatch((3, 9.2), 8, 0.6, boxstyle="round,pad=0.1",
                              facecolor='lightblue', edgecolor='black', linewidth=2)
    ax.add_patch(title_box)
    ax.text(7, 9.5, 'RFID DOOR SYSTEM - STRUCTURAL OVERVIEW', 
            ha='center', va='center', fontsize=12, fontweight='bold')
    
    # =========================================================================
    # COMPONENT DEFINITIONS - Positions and colors for all system components
    # Format: (x_position, y_position, width, height)
    # =========================================================================
    components = {
        'arduino': (1, 7, 2.5, 1.5),    # Main microcontroller
        'rfid': (1, 4.5, 2.5, 1.3),     # RFID reader module
        'relay': (5.5, 7, 2.5, 1.3),    # Relay switching module
        'solenoid': (5.5, 4.5, 2.5, 1.3), # Door lock solenoid
        'power': (10, 7, 2.5, 1.3),     # Power supply unit
        'rfid_card': (10, 4.5, 2, 1)    # RFID card/tag
    }
    
    # Color scheme for visual distinction of components
    colors = {
        'arduino': '#FF6B6B',    # Red shade for Arduino
        'rfid': '#4ECDC4',       # Teal for RFID reader
        'relay': '#45B7D1',      # Blue for relay
        'solenoid': '#96CEB4',   # Green for solenoid lock
        'power': '#FFEAA7',      # Yellow for power supply
        'rfid_card': '#DDA0DD'   # Purple for RFID card
    }
    
    # Draw all component boxes with rounded corners
    for comp, (x, y, w, h) in components.items():
        rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1",
                             facecolor=colors[comp], edgecolor='black', linewidth=2)
        ax.add_patch(rect)
    
    # =========================================================================
    # COMPONENT LABELS - Text labels for each component
    # =========================================================================
    component_names = {
        'arduino': 'ARDUINO\nUNO',
        'rfid': 'RFID\nREADER', 
        'relay': 'RELAY\nMODULE',
        'solenoid': 'SOLENOID\nLOCK',
        'power': 'POWER\nSUPPLY',
        'rfid_card': 'RFID\nCARD'
    }
    
    # Add centered text labels to each component box
    for comp, name in component_names.items():
        x, y, w, h = components[comp]
        lines = name.split('\n')
        for i, line in enumerate(lines):
            ax.text(x + w/2, y + h/2 - i*0.25, line, ha='center', va='center', 
                    fontweight='bold', fontsize=10)
    
    # =========================================================================
    # CONNECTION POINTS - Coordinates for line start/end points
    # Adjusted to avoid text overlap and ensure clean routing
    # =========================================================================
    conn_points = {
        'arduino_r': (3.5, 7.75),   # Right side of Arduino
        'arduino_b': (2.25, 7),     # Bottom of Arduino
        'rfid_t': (2.25, 5.8),      # Top of RFID reader
        'rfid_r': (3.5, 5.15),      # Right side of RFID reader
        'relay_l': (5.5, 7.85),     # Left side of relay (adjusted up to avoid text)
        'relay_b': (6.75, 7),       # Bottom of relay
        'solenoid_t': (6.75, 5.8),  # Top of solenoid
        'solenoid_l': (5.5, 5.15),  # Left side of solenoid
        'power_l': (10, 7.65),      # Left side of power supply
        'power_b': (11.25, 7)       # Bottom of power supply
    }
    
    # =========================================================================
    # CONNECTION LINES - Define connections between components
    # Format: (start_point, end_point, connection_label)
    # =========================================================================
    connections = [
        (conn_points['arduino_b'], conn_points['rfid_t'], '1'),  # Arduino to RFID (SPI)
        (conn_points['arduino_r'], conn_points['relay_l'], '2'), # Arduino to Relay (Digital)
        (conn_points['relay_b'], conn_points['solenoid_t'], '3'), # Relay to Solenoid (Power)
        (conn_points['power_l'], conn_points['relay_l'], '4')    # Power to Relay (Supply)
    ]
    
    # Draw connection lines with arrows and labels
    for start, end, label in connections:
        # Draw the main connection line
        ax.plot([start[0], end[0]], [start[1], end[1]], 'k-', linewidth=2.5, alpha=0.8)
        mid_x, mid_y = (start[0]+end[0])/2, (start[1]+end[1])/2  # Calculate midpoint
        dx, dy = end[0]-start[0], end[1]-start[1]  # Direction vector
        
        # Add direction arrow at midpoint
        arrow = Arrow(mid_x-dx*0.1, mid_y-dy*0.1, dx*0.2, dy*0.2, 
                     width=0.15, facecolor='red', edgecolor='darkred')
        ax.add_patch(arrow)
        
        # Add connection label with circular background
        ax.text(mid_x, mid_y+0.2, label, ha='center', va='center', 
                fontsize=9, fontweight='bold', 
                bbox=dict(boxstyle="circle,pad=0.3", facecolor='yellow', alpha=0.9))
    
    # =========================================================================
    # WIRELESS CONNECTION - Visual representation of RFID communication
    # =========================================================================
    rfid_center = (components['rfid'][0] + components['rfid'][2]/2, 
                   components['rfid'][1] + components['rfid'][3]/2)
    card_center = (components['rfid_card'][0] + components['rfid_card'][2]/2, 
                   components['rfid_card'][1] + components['rfid_card'][3]/2)
    
    # Draw concentric circles to represent wireless signal propagation
    for radius in [0.8, 1.1, 1.4]:
        circle = Circle(rfid_center, radius, fill=False, linestyle='--', 
                       linewidth=1.5, alpha=0.7, color='blue')
        ax.add_patch(circle)
    
    # =========================================================================
    # CONNECTION LEGEND - Explains what each connection number represents
    # =========================================================================
    legend_box = FancyBboxPatch((2, 2.5), 10, 1.3, boxstyle="round,pad=0.1",
                               facecolor='lightgray', edgecolor='black', alpha=0.8)
    ax.add_patch(legend_box)
    
    ax.text(7, 3.3, 'CONNECTION LEGEND', ha='center', va='center', 
            fontweight='bold', fontsize=11)
    
    # Connection descriptions with adjusted positions to fit in smaller box
    connection_descriptions = [
        (3, 2.8, "1: SPI Communication"),    # Serial communication protocol
        (5.5, 2.8, "2: Digital Control"),    # Digital signal control
        (8, 2.8, "3: Power to Lock"),        # Power delivery to solenoid
        (10.5, 2.8, "4: Power Input")        # Main power input
    ]
    
    for x, y, desc in connection_descriptions:
        ax.text(x, y, desc, ha='center', va='center', fontsize=9, fontweight='bold')
    
    # =========================================================================
    # SYSTEM WORKFLOW - Step-by-step process of door unlocking
    # =========================================================================
    workflow_title = ax.text(7, 1.7, 'SYSTEM WORKFLOW', ha='center', va='center', 
                            fontweight='bold', fontsize=11,
                            bbox=dict(boxstyle="round,pad=0.4", facecolor='orange', alpha=0.9))
    
    # Define each step in the workflow process
    workflow_steps = [
        (2, 1, "1. Tap Card", "Present RFID"),      # Step 1: User presents card
        (4.5, 1, "2. Read UID", "Scan ID"),         # Step 2: System reads card ID
        (7, 1, "3. Verify", "Check Auth"),          # Step 3: Authentication check
        (9.5, 1, "4. Activate", "Signal Relay"),    # Step 4: Activate relay
        (12, 1, "5. Unlock", "Open Door")           # Step 5: Door unlocks
    ]
    
    # Draw workflow steps with connecting arrows
    for i, (x, y, title, description) in enumerate(workflow_steps):
        # Step number circle
        circle = Circle((x, y), 0.3, facecolor='orange', edgecolor='black', linewidth=1.5)
        ax.add_patch(circle)
        ax.text(x, y, str(i+1), ha='center', va='center', 
                fontweight='bold', fontsize=10)
        
        # Step title and description
        ax.text(x, y-0.7, title, ha='center', va='top', fontsize=9, fontweight='bold')
        ax.text(x, y-1.0, description, ha='center', va='top', fontsize=8)
        
        # Connect steps with arrows (except the last step)
        if i < len(workflow_steps)-1:
            next_x = workflow_steps[i+1][0]
            ax.plot([x + 0.4, next_x - 0.4], [y, y], 'k-', linewidth=2, alpha=0.7)
            ax.arrow(x + 0.45, y, 0.3, 0, head_width=0.15, head_length=0.2, 
                    fc='k', ec='k', alpha=0.8)
    
    plt.tight_layout()  # Adjust layout to prevent element clipping
    return fig

def create_technical_diagram():
    """
    Creates the technical specifications diagram showing detailed component specs,
    pin configurations, and system features.
    This diagram focuses on technical details and specifications.
    """
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # =========================================================================
    # TITLE SECTION
    # =========================================================================
    title_box = FancyBboxPatch((3, 9.2), 8, 0.6, boxstyle="round,pad=0.1",
                              facecolor='lightgreen', edgecolor='black', linewidth=2)
    ax.add_patch(title_box)
    ax.text(7, 9.5, 'RFID DOOR SYSTEM - TECHNICAL SPECIFICATIONS', 
            ha='center', va='center', fontsize=12, fontweight='bold')
    
    # =========================================================================
    # COMPONENT SPECIFICATIONS GRID - Technical details for each component
    # Format: (x, y, width, height, text_content, background_color)
    # =========================================================================
    spec_grid = [
        (1, 7.5, 3, 1.3, 'ARDUINO UNO\nATmega328P\n16MHz | 32KB', '#FF9999'),
        (1, 6, 3, 1.3, 'RFID READER\n13.56MHz\n0-60mm Range', '#99FF99'),
        (5, 7.5, 3, 1.3, 'RELAY MODULE\n5V DC | 10A\nElectromechanical', '#9999FF'),
        (5, 6, 3, 1.3, 'SOLENOID LOCK\n12V DC | 500mA\nFail-Secure', '#FFFF99'),
        (9, 7.5, 3, 1.3, 'POWER SUPPLY\n12V DC | 2A\n100-240V AC', '#FF99FF'),
        (9, 6, 3, 1.3, 'RFID CARD\nMIFARE 1K\n13.56MHz', '#99FFFF')
    ]
    
    # Draw specification boxes with multi-line text
    for x, y, w, h, text, color in spec_grid:
        box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1",
                            facecolor=color, edgecolor='black', linewidth=1.5)
        ax.add_patch(box)
        lines = text.split('\n')
        for i, line in enumerate(lines):
            ax.text(x + w/2, y + h - 0.4 - i*0.3, line, 
                   ha='center', va='top', fontsize=8, fontweight='bold')
    
    # =========================================================================
    # PIN CONFIGURATION SECTION - Wiring and connection details
    # =========================================================================
    pin_title = ax.text(7, 5.5, 'PIN CONFIGURATION', ha='center', va='center',
                       fontweight='bold', fontsize=12,
                       bbox=dict(boxstyle="round,pad=0.4", facecolor='lightcoral', alpha=0.9))
    
    # Pin configuration tables for different components
    pin_tables = [
        (2, 3.7, "RFID PINS", ["SDA  → Digital 10", "SCK  → Digital 13", 
                              "MOSI → Digital 11", "MISO → Digital 12",
                              "RST  → Digital 9", "3.3V → 3.3V"]),
        (6, 3.7, "RELAY PINS", ["IN1   → Digital 7", "VCC   → 5V", 
                               "GND   → GND", "JD-VCC → 12V",
                               "COM   → 12V", "IN2    → Not Used"]),
        (10, 3.7, "POWER WIRING", ["12V → Relay JD-VCC", "12V → Solenoid +", 
                                  "GND → Common", "7-12V → Arduino"])
    ]
    
    # Draw pin configuration tables with increased height for better text fit
    for x, y, title, pins in pin_tables:
        table_box = FancyBboxPatch((x-1.0, y-0.9), 2.8, 2.2, boxstyle="round,pad=0.1",
                                  facecolor='lightgray', edgecolor='black', alpha=0.8)
        ax.add_patch(table_box)
        
        ax.text(x, y+0.9, title, ha='center', va='center', 
               fontweight='bold', fontsize=10)
        
        # Add pin descriptions with adjusted spacing
        for i, pin in enumerate(pins):
            ax.text(x, y+0.6 - i*0.3, pin, ha='center', va='center', 
                   fontsize=8, fontweight='normal')
    
    # =========================================================================
    # KEY FEATURES SECTION - Highlight main system capabilities
    # =========================================================================
    features_title = ax.text(7, 2.3, 'KEY FEATURES', ha='center', va='center',
                            fontweight='bold', fontsize=12,
                            bbox=dict(boxstyle="round,pad=0.4", facecolor='lightblue', alpha=0.9))
    
    features = [
        (2.5, 2, "UID\nAuthentication"),    # Unique ID based security
        (5.5, 2, "SPI\nCommunication"),     # Serial Peripheral Interface
        (8.5, 2, "12V DC\nPower System"),   # Power specifications
        (11.5, 2, "Wireless\nRFID")         # Wireless communication
    ]
    
    for x, y, feature in features:
        ax.text(x, y, feature, ha='center', va='center', fontsize=9, fontweight='bold',
               bbox=dict(boxstyle="round,pad=0.3", facecolor='yellow', alpha=0.8))
    
    # =========================================================================
    # PERFORMANCE METRICS - System performance and capability summary
    # =========================================================================
    metrics_box = FancyBboxPatch((1, 0.7), 12, 0.9, boxstyle="round,pad=0.1",
                                facecolor='lightyellow', edgecolor='black', alpha=0.8)
    ax.add_patch(metrics_box)
    
    metrics_lines = [
        "OPERATING RANGE: 0-60mm  |  RESPONSE TIME: <2 seconds",           # Range and speed
        "POWER: 12V DC, 2A  |  COMMUNICATION: SPI + Wireless RFID",        # Power and comms
        "SECURITY: UID-based Authentication  |  LOCK TYPE: Fail-Secure"    # Security features
    ]
    
    for i, line in enumerate(metrics_lines):
        ax.text(7, 1.3 - i*0.3, line, ha='center', va='center', 
               fontsize=8, fontweight='bold')
    
    plt.tight_layout()
    return fig

def generate_diagrams():
    """
    Main function to generate both diagrams sequentially.
    Saves high-resolution PNG files and displays them.
    """
    print("Generating Enhanced Structural Diagram...")
    fig1 = create_structural_diagram()
    # Save structural diagram with high DPI for quality
    plt.savefig('rfid_door_structural.png', dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none', transparent=False)
    plt.show()  # Display the diagram
    
    print("Generating Enhanced Technical Diagram...")
    fig2 = create_technical_diagram()
    # Save technical diagram with same quality settings
    plt.savefig('rfid_door_technical.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none', transparent=False)
    plt.show()  # Display the diagram
    
    # Success message with file information
    print("\n✅ Enhanced diagrams generated successfully!")
    print("📁 Files saved:")
    print("   - rfid_door_structural.png")
    print("   - rfid_door_technical.png")
    print("\n🎯 Structural: Component connections and system workflow")
    print("🔧 Technical: Detailed specifications and pin configurations")

# =============================================================================
# MAIN EXECUTION BLOCK
# =============================================================================
if __name__ == "__main__":
    generate_diagrams()