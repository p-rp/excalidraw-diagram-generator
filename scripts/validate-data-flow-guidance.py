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
        "logical-customer",
        "logical-collect-order",
        "logical-validate-order",
        "logical-order-store",
        "logical-fulfillment-team",
        "physical-web-app",
        "physical-api-service",
        "physical-database",
        "physical-analytics",
    }
    missing = required_ids - set(by_id)
    if missing:
        fail(f"data-flow template missing required logical/physical nodes: {sorted(missing)}")

    expected_types = {
        "logical-customer": "rectangle",
        "logical-collect-order": "ellipse",
        "logical-validate-order": "ellipse",
        "logical-order-store": "rectangle",
        "logical-fulfillment-team": "rectangle",
        "physical-web-app": "rectangle",
        "physical-api-service": "ellipse",
        "physical-database": "rectangle",
        "physical-analytics": "rectangle",
    }
    for element_id, expected_type in expected_types.items():
        actual_type = by_id[element_id]["type"]
        if actual_type != expected_type:
            fail(f"{element_id} must be {expected_type}, got {actual_type}")

    arrows = [element for element in elements if element["type"] == "arrow"]
    if len(arrows) < 8:
        fail("data-flow template must include at least 8 labeled data-flow arrows")

    for element in elements:
        if element["type"] not in {"rectangle", "ellipse", "diamond", "arrow"}:
            continue

        bound_text_ids = [
            item["id"]
            for item in element.get("boundElements", [])
            if item.get("type") == "text"
        ]

        if element["type"] in {"rectangle", "ellipse", "diamond"} and not bound_text_ids:
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

    process_ids = [element["id"] for element in elements if element["type"] == "ellipse"]
    data_store_ids = [
        element["id"]
        for element in elements
        if element["type"] in {"rectangle", "ellipse", "diamond"}
        and ("store" in element["id"] or "database" in element["id"])
    ]
    for node_id in process_ids + data_store_ids:
        inbound = [arrow for arrow in arrows if arrow.get("endBinding", {}).get("elementId") == node_id]
        outbound = [arrow for arrow in arrows if arrow.get("startBinding", {}).get("elementId") == node_id]
        if not inbound:
            fail(f"DFD node {node_id} must have at least one input flow")
        if not outbound:
            fail(f"DFD node {node_id} must have at least one output flow")

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
