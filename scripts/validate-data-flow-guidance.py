#!/usr/bin/env python3
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "templates" / "data-flow-diagram-template.excalidraw"
SKILL = ROOT / "SKILL.md"


def fail(message):
    raise AssertionError(message)


def main():
    data = json.loads(TEMPLATE.read_text())
    elements = data["elements"]
    by_id = {element["id"]: element for element in elements}

    required_ids = {
        "customer-entity",
        "place-order",
        "send-confirmation",
        "process-payment",
        "order-database",
        "payment-gateway",
        "customer-divider-start",
        "customer-divider-end",
        "place-order-shadow",
        "send-confirmation-shadow",
        "process-payment-shadow",
        "order-database-shadow",
        "payment-gateway-shadow",
    }
    missing = required_ids - set(by_id)
    if missing:
        fail(f"data-flow template missing required image-style DFD nodes: {sorted(missing)}")

    expected_types = {
        "customer-entity": "rectangle",
        "place-order": "ellipse",
        "send-confirmation": "ellipse",
        "process-payment": "ellipse",
        "order-database": "rectangle",
        "payment-gateway": "rectangle",
    }
    for element_id, expected_type in expected_types.items():
        actual_type = by_id[element_id]["type"]
        if actual_type != expected_type:
            fail(f"{element_id} must be {expected_type}, got {actual_type}")

    arrows = [element for element in elements if element["type"] == "arrow"]
    if len(arrows) < 7:
        fail("data-flow template must include at least 7 labeled data-flow arrows")

    for element in elements:
        if element["type"] not in {"rectangle", "ellipse", "diamond", "arrow"}:
            continue

        bound_text_ids = [
            item["id"]
            for item in element.get("boundElements", [])
            if item.get("type") == "text"
        ]

        is_visual_support = element["id"].endswith("-shadow") or element["id"] == "dfd-frame"
        if element["type"] in {"rectangle", "ellipse", "diamond"} and not bound_text_ids and not is_visual_support:
            fail(f"shape {element['id']} has no bound text")

        if element["type"] == "arrow" and not bound_text_ids:
            fail(f"data-flow arrow {element['id']} has no bound label")

        for text_id in bound_text_ids:
            text = by_id.get(text_id)
            if not text:
                fail(f"{element['id']} references missing bound text {text_id}")
            if text.get("containerId") != element["id"]:
                fail(f"text {text_id} is not bound back to {element['id']}")
            if text.get("fontFamily") != 5:
                fail(f"text {text_id} does not use Excalifont")

            if element["type"] in {"rectangle", "ellipse", "diamond"}:
                if not (element["x"] <= text["x"] <= element["x"] + element["width"]):
                    fail(f"text {text_id} is horizontally outside {element['id']}")
                if not (element["y"] <= text["y"] <= element["y"] + element["height"]):
                    fail(f"text {text_id} is vertically outside {element['id']}")

    for arrow in arrows:
        points = arrow.get("points") or []
        for start, end in zip(points, points[1:]):
            dx = end[0] - start[0]
            dy = end[1] - start[1]
            if abs(dx) > 1e-6 and abs(dy) > 1e-6:
                fail(f"arrow {arrow['id']} uses a diagonal segment instead of an orthogonal DFD route")

        start_id = arrow.get("startBinding", {}).get("elementId")
        end_id = arrow.get("endBinding", {}).get("elementId")
        if not start_id or not end_id:
            fail(f"arrow {arrow['id']} must bind to both source and target DFD nodes")
        for shape_id in [start_id, end_id]:
            shape = by_id.get(shape_id)
            if not shape:
                fail(f"arrow {arrow['id']} binds to missing shape {shape_id}")
            if not any(item.get("id") == arrow["id"] for item in shape.get("boundElements", [])):
                fail(f"shape {shape_id} does not bind back to arrow {arrow['id']}")

    process_ids = [element["id"] for element in elements if element["type"] == "ellipse" and not element["id"].endswith("-shadow")]
    data_store_ids = [
        element["id"]
        for element in elements
        if element["type"] in {"rectangle", "ellipse", "diamond"}
        and not element["id"].endswith("-shadow")
        and ("store" in element["id"] or "database" in element["id"] or element["id"] == "payment-gateway")
    ]
    for node_id in process_ids + data_store_ids:
        inbound = [arrow for arrow in arrows if arrow.get("endBinding", {}).get("elementId") == node_id]
        outbound = [arrow for arrow in arrows if arrow.get("startBinding", {}).get("elementId") == node_id]
        if not inbound:
            fail(f"DFD node {node_id} must have at least one input flow")
        if not outbound:
            fail(f"DFD node {node_id} must have at least one output flow")

    labels = {element.get("text") for element in elements if element.get("type") == "text"}
    for required_label in ["Order information", "Payment details", "Payment\nrequest", "Payment\nresponse", "Order record", "Confirmation\ndata", "Order confirmation"]:
        if required_label not in labels:
            fail(f"data-flow template missing arrow label: {required_label}")

    skill_text = SKILL.read_text()
    required_phrases = [
        "Data flow diagrams visualize data movement, storage, and transformation, not task sequence",
        "Use consistent DFD symbols",
        "Every process and data store should have at least one input and one output",
        "Data should move through a process before entering or leaving a data store",
        "Avoid crossing data-flow arrows",
    ]
    for phrase in required_phrases:
        if phrase not in skill_text:
            fail(f"SKILL.md missing required DFD guidance: {phrase}")


if __name__ == "__main__":
    main()
