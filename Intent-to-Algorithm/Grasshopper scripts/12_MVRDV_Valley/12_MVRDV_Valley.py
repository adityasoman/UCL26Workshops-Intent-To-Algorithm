#! python3
"""Valley-inspired floor-by-floor visual model for Rhino 8 Python 3 Script mode.

Main inputs, all Item Access:
    height_a, floors_a, height_b, floors_b, height_c, floors_c,
    max_setbacks, window_width, window_height.
Optional inputs:
    footprint_width, footprint_depth, tower_gap, setback_depth, seed,
    window_spacing, window_sill, window_margin, garden_inset.

Minimum regular outputs: meshes, colours, info.
Other outputs: floor_blocks, windows, gardens, block_colours, window_colours,
    garden_colours, floor_outlines, tower_ids, floor_ids, window_block_ids,
    garden_block_ids, storey_heights, cut_counts.
Keep the special console output named out. Rename regular output a to meshes.
Never rename out to meshes: out captures printed text, not geometry.

Dimensions default to millimetre-scale model units. See 12_MVRDV_Valley.md.
Windows are dark panels, not holes. Gardens are exposed terrace/roof overlays.
"""

import math
import random

import Rhino
import Rhino.Geometry as rg
from System.Drawing import Color


def number_input(name, default, minimum=None, maximum=None, integer=False):
    value = globals().get(name)
    if value is None:
        value = default
    try:
        result = float(value)
    except (TypeError, ValueError, OverflowError):
        raise ValueError("{} must be a number.".format(name))
    if not math.isfinite(result):
        raise ValueError("{} must be finite.".format(name))
    if integer and result != math.floor(result):
        raise ValueError("{} must be a whole number.".format(name))
    if minimum is not None and result < minimum:
        raise ValueError("{} must be at least {}.".format(name, minimum))
    if maximum is not None and result > maximum:
        raise ValueError("{} must be at most {}.".format(name, maximum))
    return int(result) if integer else result


def polygon_area(polygon):
    if len(polygon) < 3:
        return 0.0
    return 0.5 * sum(
        point[0] * polygon[(index + 1) % len(polygon)][1]
        - point[1] * polygon[(index + 1) % len(polygon)][0]
        for index, point in enumerate(polygon)
    )


def clean_polygon(polygon, tolerance):
    cleaned = []
    for point in polygon:
        if not cleaned or math.hypot(point[0] - cleaned[-1][0], point[1] - cleaned[-1][1]) > tolerance:
            cleaned.append(point)
    if len(cleaned) > 1 and math.hypot(cleaned[0][0] - cleaned[-1][0], cleaned[0][1] - cleaned[-1][1]) <= tolerance:
        cleaned.pop()
    changed = True
    while changed and len(cleaned) >= 3:
        changed = False
        for index, point in enumerate(cleaned):
            previous = cleaned[index - 1]
            following = cleaned[(index + 1) % len(cleaned)]
            span = math.hypot(following[0] - previous[0], following[1] - previous[1])
            cross = ((point[0] - previous[0]) * (following[1] - previous[1])
                     - (point[1] - previous[1]) * (following[0] - previous[0]))
            if abs(cross) <= tolerance * span:
                del cleaned[index]
                changed = True
                break
    return cleaned if len(cleaned) >= 3 and polygon_area(cleaned) > tolerance ** 2 else []


def clip_polygon(polygon, normal_x, normal_y, limit, tolerance):
    if not polygon:
        return []
    result = []
    previous = polygon[-1]
    previous_distance = normal_x * previous[0] + normal_y * previous[1] - limit
    previous_inside = previous_distance <= tolerance
    for current in polygon:
        current_distance = normal_x * current[0] + normal_y * current[1] - limit
        current_inside = current_distance <= tolerance
        if current_inside != previous_inside:
            denominator = previous_distance - current_distance
            if abs(denominator) > 1e-15:
                fraction = max(0.0, min(1.0, previous_distance / denominator))
                result.append((previous[0] + fraction * (current[0] - previous[0]),
                               previous[1] + fraction * (current[1] - previous[1])))
        if current_inside:
            result.append(current)
        previous = current
        previous_distance = current_distance
        previous_inside = current_inside
    return clean_polygon(result, tolerance)


def polygon_edges(polygon):
    for index, start in enumerate(polygon):
        end = polygon[(index + 1) % len(polygon)]
        edge_length = math.hypot(end[0] - start[0], end[1] - start[1])
        yield start, end, edge_length, (end[1] - start[1]) / edge_length, -(end[0] - start[0]) / edge_length


def exposed_pieces(lower, upper, tolerance):
    if not upper:
        return [list(lower)]
    remaining = list(lower)
    pieces = []
    for start, end, edge_length, normal_x, normal_y in polygon_edges(upper):
        limit = normal_x * start[0] + normal_y * start[1]
        outside = clip_polygon(remaining, -normal_x, -normal_y, -limit, tolerance)
        if outside:
            pieces.append(outside)
        remaining = clip_polygon(remaining, normal_x, normal_y, limit, tolerance)
        if not remaining:
            break
    return pieces


def inset_polygon(polygon, distance, tolerance):
    if distance == 0.0:
        return list(polygon)
    result = list(polygon)
    for start, end, edge_length, normal_x, normal_y in polygon_edges(polygon):
        limit = normal_x * start[0] + normal_y * start[1] - distance
        result = clip_polygon(result, normal_x, normal_y, limit, tolerance)
        if not result:
            break
    return result


def world_polygon(polygon, centre, angle):
    cosine = math.cos(angle)
    sine = math.sin(angle)
    return [(centre[0] + point[0] * cosine - point[1] * sine,
             centre[1] + point[0] * sine + point[1] * cosine)
            for point in polygon]


def make_floor_polygons(width, depth, floor_count, maximum_cuts, cut_depth,
                        inward_angle, random_seed, tolerance):
    source = random.Random(random_seed)
    event_count = min(maximum_cuts, floor_count - 1)
    event_levels = sorted(source.sample(range(1, floor_count), event_count))
    events = {
        level: (inward_angle + math.radians(source.uniform(-78.0, 78.0)),
                cut_depth * source.uniform(0.5, 1.0))
        for level in event_levels
    }
    polygon = [(-width / 2, -depth / 2), (width / 2, -depth / 2),
               (width / 2, depth / 2), (-width / 2, depth / 2)]
    footprints = []
    actual_cuts = 0
    for floor_index in range(floor_count):
        if floor_index in events:
            angle, requested_depth = events[floor_index]
            normal_x, normal_y = math.cos(angle), math.sin(angle)
            support = max(normal_x * point[0] + normal_y * point[1] for point in polygon)
            core_support = 0.22 * (width * abs(normal_x) + depth * abs(normal_y))
            available = max(0.0, support - core_support)
            removed_depth = min(requested_depth, 0.5 * available)
            if removed_depth > tolerance:
                clipped = clip_polygon(polygon, normal_x, normal_y, support - removed_depth, tolerance)
                if not clipped:
                    raise ValueError("A setback removed an entire floor; reduce setback_depth.")
                if polygon_area(polygon) - polygon_area(clipped) > tolerance ** 2:
                    polygon = clipped
                    actual_cuts += 1
        footprints.append(list(polygon))
    return footprints, actual_cuts


def finish_mesh(mesh, colour, sharp=False):
    mesh.Normals.ComputeNormals()
    if sharp:
        mesh.Unweld(0.0, True)
        mesh.Normals.ComputeNormals()
    mesh.VertexColors.CreateMonotoneMesh(colour)
    mesh.Compact()
    if not mesh.IsValid:
        raise ValueError("A mesh is invalid; check dimensions and Rhino document tolerance.")
    return mesh


def floor_mesh(polygon, bottom, top, colour):
    mesh = rg.Mesh()
    count = len(polygon)
    for elevation in (bottom, top):
        for horizontal, vertical in polygon:
            mesh.Vertices.Add(horizontal, vertical, elevation)
    for index in range(1, count - 1):
        mesh.Faces.AddFace(0, index + 1, index)
        mesh.Faces.AddFace(count, count + index, count + index + 1)
    for index in range(count):
        following = (index + 1) % count
        mesh.Faces.AddFace(index, following, following + count, index + count)
    return finish_mesh(mesh, colour, sharp=True)


def horizontal_mesh(polygon, elevation, colour):
    mesh = rg.Mesh()
    for horizontal, vertical in polygon:
        mesh.Vertices.Add(horizontal, vertical, elevation)
    for index in range(1, len(polygon) - 1):
        mesh.Faces.AddFace(0, index, index + 1)
    return finish_mesh(mesh, colour)


def windows_on_edge(edge_length, width, spacing, margin):
    usable = edge_length - 2.0 * margin
    return max(0, int(math.floor((usable + spacing) / (width + spacing))))


def window_mesh(polygon, bottom, width, height, spacing, sill, margin, offset, colour):
    mesh = rg.Mesh()
    panel_count = 0
    for start, end, edge_length, normal_x, normal_y in polygon_edges(polygon):
        count = windows_on_edge(edge_length, width, spacing, margin)
        if count == 0:
            continue
        direction_x = (end[0] - start[0]) / edge_length
        direction_y = (end[1] - start[1]) / edge_length
        border = (edge_length - count * width - (count - 1) * spacing) / 2.0
        for panel_index in range(count):
            along = border + panel_index * (width + spacing)
            left_x = start[0] + along * direction_x + offset * normal_x
            left_y = start[1] + along * direction_y + offset * normal_y
            right_x = left_x + width * direction_x
            right_y = left_y + width * direction_y
            first_vertex = mesh.Vertices.Count
            mesh.Vertices.Add(left_x, left_y, bottom + sill)
            mesh.Vertices.Add(right_x, right_y, bottom + sill)
            mesh.Vertices.Add(right_x, right_y, bottom + sill + height)
            mesh.Vertices.Add(left_x, left_y, bottom + sill + height)
            mesh.Faces.AddFace(first_vertex, first_vertex + 1, first_vertex + 2, first_vertex + 3)
            panel_count += 1
    return (finish_mesh(mesh, colour), panel_count) if panel_count else (None, 0)


meshes, colours, floor_blocks, windows, gardens = [], [], [], [], []
block_colours, window_colours, garden_colours = [], [], []
floor_outlines, tower_ids, floor_ids, window_block_ids, garden_block_ids = [], [], [], [], []
storey_heights, cut_counts = [], []
info = ""

document = Rhino.RhinoDoc.ActiveDoc
tolerance = max(document.ModelAbsoluteTolerance if document is not None else 0.01, 1e-9)
positive_minimum = 4.0 * tolerance
tower_heights = [number_input("height_a", 100000.0, positive_minimum),
                 number_input("height_b", 81000.0, positive_minimum),
                 number_input("height_c", 67000.0, positive_minimum)]
floor_counts = [number_input("floors_a", 26, 1, 150, integer=True),
                number_input("floors_b", 23, 1, 150, integer=True),
                number_input("floors_c", 20, 1, 150, integer=True)]
maximum_setbacks = number_input("max_setbacks", 12, 0, 40, integer=True)
panel_width = number_input("window_width", 1600.0, positive_minimum)
panel_height = number_input("window_height", 2200.0, positive_minimum)
base_width = number_input("footprint_width", 30000.0, positive_minimum)
base_depth = number_input("footprint_depth", 26000.0, positive_minimum)
layout_gap = number_input("tower_gap", 8000.0, 0.0)
maximum_cut_depth = number_input("setback_depth", 4500.0, 0.0)
random_seed = number_input("seed", 17, 0, 2147483647, integer=True)
panel_spacing = number_input("window_spacing", 750.0, 0.0)
panel_sill = number_input("window_sill", 800.0, 0.0)
panel_margin = number_input("window_margin", 250.0, positive_minimum)
planting_inset = number_input("garden_inset", 200.0, 0.0)
if sum(floor_counts) > 360:
    raise ValueError("Use at most 360 floors in total to keep the Grasshopper model responsive.")
storey_heights = [height / count for height, count in zip(tower_heights, floor_counts)]
for tower_index, storey_height in enumerate(storey_heights):
    if panel_sill + panel_height + panel_margin > storey_height:
        raise ValueError(
            "Tower {}: window_sill + window_height + window_margin exceeds height / floors ({:.2f}). "
            "Reduce window height/sill, increase tower height, or reduce its floor count."
            .format("ABC"[tower_index], storey_height))

centre_spacing = math.hypot(base_width, base_depth) + layout_gap
tower_centres = [(-centre_spacing / 2.0, -math.sqrt(3.0) * centre_spacing / 6.0),
                 (centre_spacing / 2.0, -math.sqrt(3.0) * centre_spacing / 6.0),
                 (0.0, math.sqrt(3.0) * centre_spacing / 3.0)]
tower_rotations = [math.radians(-8.0), math.radians(8.0), 0.0]
tower_footprints = []
estimated_panels = 0
for tower_index, centre in enumerate(tower_centres):
    rotation = tower_rotations[tower_index]
    inward_angle = math.atan2(-centre[1], -centre[0]) - rotation
    local_footprints, actual_cuts = make_floor_polygons(
        base_width, base_depth, floor_counts[tower_index], maximum_setbacks,
        maximum_cut_depth, inward_angle, random_seed + 1009 * (tower_index + 1), tolerance)
    footprints = [world_polygon(polygon, centre, rotation) for polygon in local_footprints]
    tower_footprints.append(footprints)
    cut_counts.append(actual_cuts)
    for polygon in footprints:
        estimated_panels += sum(windows_on_edge(edge_length, panel_width, panel_spacing, panel_margin)
                                for start, end, edge_length, normal_x, normal_y in polygon_edges(polygon))
if estimated_panels > 60000:
    raise ValueError("More than 60,000 window panels requested. Increase width/spacing or reduce floor counts.")

stone_palette = [Color.FromArgb(192, 178, 151), Color.FromArgb(184, 169, 141),
                 Color.FromArgb(201, 186, 158)]
green_palette = [Color.FromArgb(82, 128, 68), Color.FromArgb(103, 144, 74),
                 Color.FromArgb(67, 115, 70)]
glass_colour = Color.FromArgb(37, 55, 65)
surface_offset = max(4.0 * tolerance, min(base_width, base_depth) * 0.0001)
panel_total = 0
omitted_gardens = 0
garden_area = 0.0
for tower_index, footprints in enumerate(tower_footprints):
    storey_height = storey_heights[tower_index]
    for floor_index, polygon in enumerate(footprints):
        block_index = len(floor_blocks)
        bottom = floor_index * storey_height
        top = (floor_index + 1) * storey_height
        stone_colour = stone_palette[(tower_index + floor_index) % len(stone_palette)]
        block = floor_mesh(polygon, bottom, top, stone_colour)
        floor_blocks.append(block)
        block_colours.append(stone_colour)
        tower_ids.append(tower_index + 1)
        floor_ids.append(floor_index)
        outline_points = [rg.Point3d(point[0], point[1], bottom) for point in polygon]
        floor_outlines.append(rg.PolylineCurve(outline_points + [outline_points[0]]))
        glazing, panel_count = window_mesh(
            polygon, bottom, panel_width, panel_height, panel_spacing,
            panel_sill, panel_margin, surface_offset, glass_colour)
        if glazing is not None:
            windows.append(glazing)
            window_colours.append(glass_colour)
            window_block_ids.append(block_index)
            panel_total += panel_count
        next_polygon = footprints[floor_index + 1] if floor_index + 1 < len(footprints) else []
        for exposed in exposed_pieces(polygon, next_polygon, tolerance):
            planted = inset_polygon(exposed, planting_inset, tolerance)
            if not planted:
                omitted_gardens += 1
                continue
            green = green_palette[(tower_index + floor_index) % len(green_palette)]
            gardens.append(horizontal_mesh(planted, top + surface_offset, green))
            garden_colours.append(green)
            garden_block_ids.append(block_index)
            garden_area += polygon_area(planted)

meshes = floor_blocks + windows + gardens
colours = block_colours + window_colours + garden_colours
summaries = [
    "Tower {}: {} floors; height {:.2f}; floor-to-floor {:.2f}; {} actual angled setbacks."
    .format("ABC"[index], floor_counts[index], tower_heights[index], storey_heights[index], cut_counts[index])
    for index in range(3)
]
info = "\n".join(summaries) + (
    "\n{} separate floor blocks; {} dark panels grouped into {} window meshes."
    "\n{} green terrace/roof patches; planted area {:.2f} square model units."
    "\n{} exposed pieces too narrow/small after garden_inset were omitted."
    "\nSetback budget: at most {} unique cut events per tower, not per floor."
    "\nAll lengths use Rhino model units. Tower heights are measured from ground to massing roof."
    "\nmeshes -> Custom Preview G; colours -> M. Keep the out socket for TEXT ONLY."
    "\nVisual approximation: dark panels, not holes; no structural or fabrication validation."
).format(len(floor_blocks), panel_total, len(windows), len(gardens), garden_area,
         omitted_gardens, maximum_setbacks)
if len(windows) < len(floor_blocks):
    info += "\nSome floors have no panels because their edges are too short for the requested window width/margins."
print(info)
