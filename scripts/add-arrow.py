#!/usr/bin/env python3
"""
Add arrows (connections) between elements in Excalidraw diagrams.

Usage:
    python add-arrow.py <diagram_path> <from_x> <from_y> <to_x> <to_y> [OPTIONS]

Options:
    --style {solid|dashed|dotted}    Arrow line style (default: solid)
    --color HEX                      Arrow color (default: #1e1e1e)
    --label TEXT                     Add text label on the arrow (bound via containerId)
    --from-id ID                     Bind arrow start to an existing shape element
    --to-id ID                       Bind arrow end to an existing shape element
    --use-edit-suffix                Edit via .excalidraw.edit to avoid editor overwrite issues (enabled by default; use --no-use-edit-suffix to disable)

Examples:
    # Loose arrow (not bound to shapes)
    python add-arrow.py diagram.excalidraw 300 200 500 300

    # Arrow bound to shapes — moves with them when dragged
    python add-arrow.py diagram.excalidraw 300 200 500 300 --from-id box1 --to-id box2
    python add-arrow.py diagram.excalidraw 300 200 500 300 --from-id box1 --to-id box2 --label "HTTP"
"""

import json
import sys
import uuid
from pathlib import Path


def generate_unique_id() -> str:
    """Generate a unique ID for Excalidraw elements."""
    return str(uuid.uuid4()).replace('-', '')[:16]


def compute_binding(shape, arrow_x, arrow_y, arrow_side):
    """
    Compute startBinding or endBinding for an arrow connecting to a shape.

    Determines which edge of the shape the arrow connects to and computes
    the focus (position along that edge, -1 to 1) and gap (distance from edge).

    Args:
        shape: The shape element dict
        arrow_x: Arrow endpoint X (absolute canvas coordinate)
        arrow_y: Arrow endpoint Y (absolute canvas coordinate)
        arrow_side: 'start' or 'end' (determines direction bias)
    """
    sx, sy = shape['x'], shape['y']
    sw, sh = shape.get('width', 0), shape.get('height', 0)
    cx, cy = sx + sw / 2, sy + sh / 2

    # Which side is the arrow closest to?
    dist_left = abs(arrow_x - sx)
    dist_right = abs(arrow_x - (sx + sw))
    dist_top = abs(arrow_y - sy)
    dist_bottom = abs(arrow_y - (sy + sh))

    # Determine the primary edge by direction from shape center
    dx = arrow_x - cx
    dy = arrow_y - cy

    if abs(dx) > abs(dy):
        # Horizontal: left or right edge
        if dx > 0:
            focus = (arrow_y - sy) / sh * 2 - 1
            gap = abs(arrow_x - (sx + sw))
        else:
            focus = (arrow_y - sy) / sh * 2 - 1
            gap = abs(arrow_x - sx)
    else:
        # Vertical: top or bottom edge
        if dy > 0:
            focus = (arrow_x - sx) / sw * 2 - 1
            gap = abs(arrow_y - (sy + sh))
        else:
            focus = (arrow_x - sx) / sw * 2 - 1
            gap = abs(arrow_y - sy)

    return {
        "elementId": shape['id'],
        "focus": round(focus, 4),
        "gap": max(1, round(gap, 0))
    }


def prepare_edit_path(diagram_path, use_edit_suffix):
    """Prepare safe edit path to avoid editor overwrite issues."""
    if not use_edit_suffix:
        return diagram_path, None
    if diagram_path.suffix != ".excalidraw":
        return diagram_path, None

    edit_path = diagram_path.with_suffix(diagram_path.suffix + ".edit")
    if diagram_path.exists():
        if edit_path.exists():
            raise FileExistsError(f"Edit file already exists: {edit_path}")
        diagram_path.rename(edit_path)
    return edit_path, diagram_path


def finalize_edit_path(work_path, final_path):
    """Rename .edit back to .excalidraw if needed."""
    if final_path is None:
        return
    if final_path.exists():
        final_path.unlink()
    work_path.rename(final_path)


def ensure_bound_elements_list(shape):
    """Ensure boundElements is a list (convert None to [])."""
    bes = shape.get('boundElements')
    if bes is None:
        shape['boundElements'] = []
    elif not isinstance(bes, list):
        shape['boundElements'] = []


def create_arrow(from_x, from_y, to_x, to_y, style="solid", color="#1e1e1e",
                 label=None, start_binding=None, end_binding=None, diagram_elements=None):
    """
    Create an arrow element with an optionally bound text label and shape bindings.

    Returns:
        List of elements (arrow and optional bound label) plus modifications to diagram
    """
    elements = []
    arrow_id = generate_unique_id()
    shape_updates = []  # list of (shape_id, arrow_id) for boundElements sync

    bound_elements = []
    if label:
        label_id = generate_unique_id()
        bound_elements.append({"id": label_id, "type": "text"})

    arrow = {
        "id": arrow_id,
        "type": "arrow",
        "x": from_x,
        "y": from_y,
        "width": to_x - from_x,
        "height": to_y - from_y,
        "angle": 0,
        "strokeColor": color,
        "backgroundColor": "transparent",
        "fillStyle": "solid",
        "strokeWidth": 2,
        "strokeStyle": style,
        "roughness": 1,
        "opacity": 100,
        "groupIds": [],
        "frameId": None,
        "index": "a0",
        "roundness": None,
        "seed": 1000000000 + hash(f"{from_x}{from_y}{to_x}{to_y}") % 1000000000,
        "version": 1,
        "versionNonce": 2000000000 + hash(f"{from_x}{from_y}{to_x}{to_y}") % 1000000000,
        "isDeleted": False,
        "boundElements": bound_elements,
        "updated": 1738195200000,
        "link": None,
        "locked": False,
        "points": [[0, 0], [to_x - from_x, to_y - from_y]],
        "startBinding": start_binding,
        "endBinding": end_binding,
        "startArrowhead": None,
        "endArrowhead": "arrow",
        "lastCommittedPoint": None
    }
    elements.append(arrow)

    if label:
        mid_x = (from_x + to_x) / 2
        mid_y = (from_y + to_y) / 2 - 12

        label_element = {
            "id": label_id,
            "type": "text",
            "x": mid_x,
            "y": mid_y,
            "width": len(label) * 14,
            "height": 25,
            "angle": 0,
            "strokeColor": color,
            "backgroundColor": "transparent",
            "fillStyle": "solid",
            "strokeWidth": 2,
            "strokeStyle": "solid",
            "roughness": 1,
            "opacity": 100,
            "groupIds": [],
            "frameId": None,
            "index": "a0",
            "roundness": None,
            "seed": 1000000000 + hash(label) % 1000000000,
            "version": 1,
            "versionNonce": 2000000000 + hash(label) % 1000000000,
            "isDeleted": False,
            "boundElements": [],
            "updated": 1738195200000,
            "link": None,
            "locked": False,
            "text": label,
            "fontSize": 14,
            "fontFamily": 5,
            "textAlign": "center",
            "verticalAlign": "middle",
            "containerId": arrow_id,
            "originalText": label,
            "autoResize": True,
            "lineHeight": 1.25
        }
        elements.append(label_element)

    return elements


def add_arrow_to_diagram(diagram_path, from_x, from_y, to_x, to_y,
                         style="solid", color="#1e1e1e", label=None,
                         from_id=None, to_id=None):
    """Add an arrow to an Excalidraw diagram, optionally binding to shapes."""
    print(f"Creating arrow from ({from_x}, {from_y}) to ({to_x}, {to_y})")

    # Load diagram
    print(f"Loading diagram: {diagram_path}")
    with open(diagram_path, 'r', encoding='utf-8') as f:
        diagram = json.load(f)

    if 'elements' not in diagram:
        diagram['elements'] = []

    elements = {e['id']: e for e in diagram['elements']}

    # Compute bindings
    start_binding = None
    end_binding = None

    if from_id:
        if from_id not in elements:
            print(f"Error: from-id '{from_id}' not found in diagram elements")
            sys.exit(1)
        start_binding = compute_binding(elements[from_id], from_x, from_y, 'start')
        print(f"  Binding start to '{from_id}' (focus={start_binding['focus']}, gap={start_binding['gap']})")

    if to_id:
        if to_id not in elements:
            print(f"Error: to-id '{to_id}' not found in diagram elements")
            sys.exit(1)
        end_binding = compute_binding(elements[to_id], to_x, to_y, 'end')
        print(f"  Binding end to '{to_id}' (focus={end_binding['focus']}, gap={end_binding['gap']})")

    if label:
        print(f"  With label: '{label}'")

    arrow_elements = create_arrow(from_x, from_y, to_x, to_y, style, color,
                                  label, start_binding, end_binding)

    # Extract arrow ID from first element
    arrow_id = arrow_elements[0]['id']

    # Sync boundElements on shapes — add arrow to each bound shape's list
    if from_id:
        shape = elements[from_id]
        ensure_bound_elements_list(shape)
        shape['boundElements'].append({"id": arrow_id, "type": "arrow"})

    if to_id:
        shape = elements[to_id]
        ensure_bound_elements_list(shape)
        if from_id != to_id:
            shape['boundElements'].append({"id": arrow_id, "type": "arrow"})

    # Add arrow elements
    original_count = len(diagram['elements'])
    diagram['elements'].extend(arrow_elements)
    print(f"  Added {len(arrow_elements)} elements (total: {original_count} -> {len(diagram['elements'])})")

    # Save diagram
    print("Saving diagram")
    with open(diagram_path, 'w', encoding='utf-8') as f:
        json.dump(diagram, f, indent=2, ensure_ascii=False)

    print(f"\u2713 Successfully added arrow to diagram")


def main():
    """Main entry point."""
    if len(sys.argv) < 6:
        print(__doc__)
        sys.exit(1)

    diagram_path = Path(sys.argv[1])
    from_x = float(sys.argv[2])
    from_y = float(sys.argv[3])
    to_x = float(sys.argv[4])
    to_y = float(sys.argv[5])

    style = "solid"
    color = "#1e1e1e"
    label = None
    from_id = None
    to_id = None
    use_edit_suffix = True

    i = 6
    while i < len(sys.argv):
        if sys.argv[i] == '--style':
            if i + 1 < len(sys.argv):
                style = sys.argv[i + 1]
                if style not in ('solid', 'dashed', 'dotted'):
                    print(f"Error: Invalid style '{style}'. Must be: solid, dashed, or dotted")
                    sys.exit(1)
                i += 2
            else:
                print("Error: --style requires an argument")
                sys.exit(1)
        elif sys.argv[i] == '--color':
            if i + 1 < len(sys.argv):
                color = sys.argv[i + 1]
                i += 2
            else:
                print("Error: --color requires an argument")
                sys.exit(1)
        elif sys.argv[i] == '--label':
            if i + 1 < len(sys.argv):
                label = sys.argv[i + 1]
                i += 2
            else:
                print("Error: --label requires a text argument")
                sys.exit(1)
        elif sys.argv[i] == '--from-id':
            if i + 1 < len(sys.argv):
                from_id = sys.argv[i + 1]
                i += 2
            else:
                print("Error: --from-id requires an element ID")
                sys.exit(1)
        elif sys.argv[i] == '--to-id':
            if i + 1 < len(sys.argv):
                to_id = sys.argv[i + 1]
                i += 2
            else:
                print("Error: --to-id requires an element ID")
                sys.exit(1)
        elif sys.argv[i] == '--use-edit-suffix':
            use_edit_suffix = True
            i += 1
        elif sys.argv[i] == '--no-use-edit-suffix':
            use_edit_suffix = False
            i += 1
        else:
            print(f"Error: Unknown option: {sys.argv[i]}")
            sys.exit(1)

    if not diagram_path.exists():
        print(f"Error: Diagram file not found: {diagram_path}")
        sys.exit(1)

    try:
        work_path, final_path = prepare_edit_path(diagram_path, use_edit_suffix)
        add_arrow_to_diagram(work_path, from_x, from_y, to_x, to_y, style, color,
                             label, from_id, to_id)
        finalize_edit_path(work_path, final_path)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
