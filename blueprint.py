import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_blueprint(level_name, features):
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_aspect('equal')
    
    # Building Outer Shell (Octagonal Influence)
    outer_shell = patches.RegularPolygon((0.5, 0.5), numVertices=8, radius=0.45, 
                                         orientation=0, color='#F0E6D8', alpha=0.3, label='Main Structure')
    ax.add_patch(outer_shell)

    # Drawing specific features for each level
    for feat in features:
        if feat['type'] == 'circle':
            shape = patches.Circle(feat['pos'], feat['size'], color=feat['color'], alpha=0.6)
        elif feat['type'] == 'rect':
            shape = patches.Rectangle(feat['pos'], feat['w'], feat['h'], color=feat['color'], alpha=0.6)
        ax.add_patch(shape)

    plt.title(f"Architectural Blueprint: {level_name}", fontsize=15, fontweight='bold')
    plt.axis('off')
    plt.legend(loc='upper right')
    plt.show()

# --- LEVEL 0: GROUND FLOOR (Spirituality & Social) ---
ground_features = [
    {'type': 'circle', 'pos': (0.5, 0.5), 'size': 0.15, 'color': '#5F7740', 'label': 'Central Fountain'}, # Vert Manioc
    {'type': 'rect', 'pos': (0.35, 0.1), 'w': 0.3, 'h': 0.15, 'color': '#D2B48C', 'label': 'Prayer Hall'},
    {'type': 'rect', 'pos': (0.1, 0.4), 'w': 0.15, 'h': 0.2, 'color': '#F0E6D8', 'label': 'Discussion Wing'}
]

# --- LEVEL 1: FIRST FLOOR (Science & Theology) ---
first_features = [
    {'type': 'rect', 'pos': (0.2, 0.2), 'w': 0.2, 'h': 0.6, 'color': '#5F7740', 'label': 'Scientific Labs'},
    {'type': 'rect', 'pos': (0.6, 0.2), 'w': 0.2, 'h': 0.6, 'color': '#5F7740', 'label': 'Theological Library'},
    {'type': 'circle', 'pos': (0.5, 0.5), 'size': 0.1, 'color': '#FFFFFF', 'label': 'Atrium Void'}
]

# Generate Blueprints
draw_blueprint("Level 0 - Ground Floor (Integration)", ground_features)
draw_blueprint("Level 1 - Study & Research", first_features)