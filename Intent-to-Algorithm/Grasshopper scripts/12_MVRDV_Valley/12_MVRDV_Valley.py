#! python3
"""Valley-inspired floor-by-floor visual model for Rhino 8 Python 3 Script mode.

Main inputs, all Item Access:
    height_a, floors_a, height_b, floors_b, height_c, floors_c,
    max_setbacks, window_width, window_height.
Optional inputs:
    footprint_width, footprint_depth, tower_gap, setback_depth, seed,
    window_spacing, window_sill, window_margin, garden_inset,
    podium_floors, podium_height, podium_margin, facet_tilt.

Minimum regular outputs: meshes, colours, info.
Other outputs: floor_blocks, windows, gardens, block_colours, window_colours,
    garden_colours, floor_outlines, tower_ids, floor_ids, window_block_ids,
    garden_block_ids, storey_heights, cut_counts, podium_blocks, podium_colours.
Keep the special console output named out. Rename regular output a to meshes.
Never rename out to meshes: out captures printed text, not geometry.

Dimensions default to millimetre-scale model units. See 12_MVRDV_Valley.md.
Windows are dark panels, not holes. Gardens are exposed terrace/roof overlays.
Heights and floor counts INCLUDE the shared podium; podium floors are built once.
Facets use bounded sloping cuts, not a cumulative inward taper or surveyed data.
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


FACET_BANDS = (
    (0.00, 0.22, -62.0, 1.00, -1.0),
    (0.00, 0.18, 48.0, 0.86, 1.0),
    (0.12, 0.38, 6.0, 1.15, 1.0),
    (0.25, 0.45, -48.0, 0.90, -1.0),
    (0.30, 0.58, 63.0, 1.00, 1.0),
    (0.40, 0.60, -8.0, 1.25, -1.0),
    (0.52, 0.77, -67.0, 0.90, 1.0),
    (0.57, 0.80, 32.0, 1.05, -1.0),
    (0.68, 0.90, -22.0, 1.25, 1.0),
    (0.78, 1.00, 55.0, 0.85, -1.0),
    (0.84, 1.00, -58.0, 0.95, 1.0),
    (0.88, 1.00, 3.0, 0.95, -1.0),
)


def vector_subtract(first, second):
    return tuple(first[index] - second[index] for index in range(3))


def vector_dot(first, second):
    return sum(first[index] * second[index] for index in range(3))


def vector_cross(first, second):
    return (first[1] * second[2] - first[2] * second[1],
            first[2] * second[0] - first[0] * second[2],
            first[0] * second[1] - first[1] * second[0])


def vector_unit(vector):
    length = math.sqrt(vector_dot(vector, vector))
    return tuple(value / length for value in vector) if length > 1e-15 else None


def face_normal(face):
    accumulated = [0.0, 0.0, 0.0]
    origin = face[0]
    for index in range(1, len(face) - 1):
        normal = vector_cross(vector_subtract(face[index], origin),
                              vector_subtract(face[index + 1], origin))
        for axis in range(3):
            accumulated[axis] += normal[axis]
    return vector_unit(accumulated)


def prism_faces(polygon, bottom, top):
    lower = [(point[0], point[1], bottom) for point in polygon]
    upper = [(point[0], point[1], top) for point in polygon]
    faces = [list(reversed(lower)), upper]
    for index in range(len(polygon)):
        following = (index + 1) % len(polygon)
        faces.append([lower[index], lower[following], upper[following], upper[index]])
    return faces


def clip_polyhedron(faces, normal, limit, tolerance):
    normal_length = math.sqrt(vector_dot(normal, normal))
    threshold = tolerance * normal_length
    if not any(vector_dot(normal, point) - limit > threshold for face in faces for point in face):
        return faces, False
    result = []
    intersections = {}
    for face in faces:
        clipped = []
        previous = face[-1]
        previous_distance = vector_dot(normal, previous) - limit
        for current in face:
            current_distance = vector_dot(normal, current) - limit
            if (previous_distance <= threshold) != (current_distance <= threshold):
                key = tuple(sorted((previous, current)))
                if key not in intersections:
                    fraction = max(0.0, min(1.0, previous_distance / (previous_distance - current_distance)))
                    intersections[key] = tuple(previous[axis] + fraction * (current[axis] - previous[axis])
                                               for axis in range(3))
                clipped.append(intersections[key])
            if current_distance <= threshold:
                clipped.append(current)
            previous, previous_distance = current, current_distance
        cleaned = []
        for point in clipped:
            if not cleaned or vector_dot(vector_subtract(point, cleaned[-1]),
                                         vector_subtract(point, cleaned[-1])) > tolerance ** 2:
                cleaned.append(point)
        if len(cleaned) > 1 and vector_dot(vector_subtract(cleaned[0], cleaned[-1]),
                                          vector_subtract(cleaned[0], cleaned[-1])) <= tolerance ** 2:
            cleaned.pop()
        if len(cleaned) >= 3 and face_normal(cleaned) is not None:
            result.append(cleaned)
    cap = list(dict.fromkeys(intersections.values()))
    if len(cap) >= 3:
        centre = tuple(sum(point[axis] for point in cap) / len(cap) for axis in range(3))
        unit_normal = vector_unit(normal)
        horizontal = vector_unit((-normal[1], normal[0], 0.0)) or (1.0, 0.0, 0.0)
        vertical = vector_cross(unit_normal, horizontal)
        cap.sort(key=lambda point: math.atan2(vector_dot(vector_subtract(point, centre), vertical),
                                              vector_dot(vector_subtract(point, centre), horizontal)))
        result.append(cap)
    return result, True


def convex_hull(points):
    ordered = sorted(set(points))
    def cross(origin, first, second):
        return ((first[0] - origin[0]) * (second[1] - origin[1])
                - (first[1] - origin[1]) * (second[0] - origin[0]))
    lower, upper = [], []
    for point in ordered:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], point) <= 0.0:
            lower.pop()
        lower.append(point)
    for point in reversed(ordered):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], point) <= 0.0:
            upper.pop()
        upper.append(point)
    return lower[:-1] + upper[:-1]


def facet_events(width, depth, floor_count, maximum_cuts, cut_depth,
                 inward_angle, random_seed, tower_index, tilt):
    source = random.Random(random_seed + 1009 * (tower_index + 1))
    events = []
    for event_index in range(maximum_cuts):
        start, end, angle, strength, direction = FACET_BANDS[event_index % len(FACET_BANDS)]
        variation = (tower_index - 1) * 0.015
        if random_seed != 17 or event_index >= len(FACET_BANDS):
            variation += source.uniform(-0.04, 0.04)
            angle += source.uniform(-16.0, 16.0)
            strength *= source.uniform(0.85, 1.15)
        start_level = max(0, min(floor_count - 1, int(round((start + variation) * floor_count))))
        end_level = max(start_level + 1, min(floor_count, int(round((end + variation) * floor_count))))
        orientation = inward_angle + math.radians(angle + (tower_index - 1) * 5.0)
        normal_x, normal_y = math.cos(orientation), math.sin(orientation)
        support = (width * abs(normal_x) + depth * abs(normal_y)) / 2.0
        core_support = 0.22 * (width * abs(normal_x) + depth * abs(normal_y))
        amplitude = min(cut_depth * min(1.0, strength), 0.85 * (support - core_support))
        events.append((start_level, end_level, normal_x, normal_y, support,
                       amplitude * (0.65 - direction * 0.25 * tilt),
                       amplitude * (0.65 + direction * 0.25 * tilt)))
    return events


def make_tower_levels(width, depth, floor_count, storey_height, base_elevation,
                      maximum_cuts, cut_depth, inward_angle, random_seed,
                      tower_index, tilt, centre, rotation, tolerance):
    rectangle = [(-width / 2, -depth / 2), (width / 2, -depth / 2),
                 (width / 2, depth / 2), (-width / 2, depth / 2)]
    events = facet_events(width, depth, floor_count, maximum_cuts, cut_depth,
                          inward_angle, random_seed, tower_index, tilt)
    levels = []
    used_events = set()
    for floor_index in range(floor_count):
        faces = prism_faces(rectangle, 0.0, storey_height)
        lower, upper = list(rectangle), list(rectangle)
        for event_index, event in enumerate(events):
            start, end, normal_x, normal_y, support, first_depth, last_depth = event
            if not start <= floor_index < end:
                continue
            bottom_depth = first_depth + (last_depth - first_depth) * (floor_index - start) / (end - start)
            top_depth = first_depth + (last_depth - first_depth) * (floor_index + 1 - start) / (end - start)
            slope = (top_depth - bottom_depth) / storey_height
            faces, changed = clip_polyhedron(faces, (normal_x, normal_y, slope), support - bottom_depth, tolerance)
            if changed:
                used_events.add(event_index)
            lower = clip_polygon(lower, normal_x, normal_y, support - bottom_depth, tolerance)
            upper = clip_polygon(upper, normal_x, normal_y, support - top_depth, tolerance)
        if not lower or not upper or not faces:
            raise ValueError("A facet removed a floor. Reduce setback_depth.")
        bottom = base_elevation + floor_index * storey_height
        world_faces = []
        for face in faces:
            transformed = world_polygon([(point[0], point[1]) for point in face], centre, rotation)
            world_faces.append([(point[0], point[1], bottom + face[index][2])
                                for index, point in enumerate(transformed)])
        levels.append({"faces": world_faces,
                       "lower": world_polygon(lower, centre, rotation),
                       "upper": world_polygon(upper, centre, rotation),
                       "bottom": bottom, "top": bottom + storey_height,
                       "tower": tower_index + 1, "local_floor": floor_index})
    return levels, len(used_events), world_polygon(rectangle, centre, rotation)


def exposed_regions(lower, covers, tolerance):
    pieces = [lower]
    for cover in covers:
        pieces = [remaining for piece in pieces for remaining in exposed_pieces(piece, cover, tolerance)]
    return pieces


def make_scene_levels(width, depth, gap, heights, floor_counts, podium_count,
                      podium_height, podium_margin, maximum_cuts, cut_depth,
                      random_seed, tilt, tolerance):
    spacing = math.hypot(width, depth) + gap
    centres = [(-spacing, -depth * 0.12), (0.0, depth * 0.60), (spacing, 0.0)]
    rotations = [math.radians(-8.0), math.radians(4.0), math.radians(8.0)]
    towers, envelopes, counts, storeys = [], [], [], []
    for tower_index, centre in enumerate(centres):
        upper_count = floor_counts[tower_index] - podium_count
        storey = (heights[tower_index] - podium_height) / upper_count
        inward_angle = math.atan2(-centre[1], -centre[0]) - rotations[tower_index]
        levels, cut_count, envelope = make_tower_levels(
            width, depth, upper_count, storey, podium_height, maximum_cuts,
            cut_depth, inward_angle, random_seed, tower_index, tilt,
            centre, rotations[tower_index], tolerance)
        for index, level in enumerate(levels):
            level["floor"] = podium_count + index
            level["covers"] = [levels[index + 1]["lower"]] if index + 1 < len(levels) else []
        towers.append(levels)
        envelopes.extend(envelope)
        counts.append(cut_count)
        storeys.append(storey)
    combined = []
    if podium_count:
        padded = [(point[0] + horizontal, point[1] + vertical)
                  for point in envelopes
                  for horizontal in (-podium_margin, podium_margin)
                  for vertical in (-podium_margin, podium_margin)]
        podium_polygon = convex_hull(padded)
        storey = podium_height / podium_count
        for index in range(podium_count):
            bottom, top = index * storey, (index + 1) * storey
            covers = [podium_polygon] if index + 1 < podium_count else [tower[0]["lower"] for tower in towers]
            combined.append({"faces": prism_faces(podium_polygon, bottom, top),
                             "lower": podium_polygon, "upper": podium_polygon,
                             "bottom": bottom, "top": top, "tower": 0,
                             "floor": index, "covers": covers})
    for tower in towers:
        combined.extend(tower)
    return combined, counts, storeys


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


def floor_mesh(faces, colour):
    mesh = rg.Mesh()
    vertex_ids = {}
    for face in faces:
        centre = tuple(sum(point[axis] for point in face) / len(face) for axis in range(3))
        centre_id = mesh.Vertices.Add(centre[0], centre[1], centre[2])
        indices = []
        for point in face:
            if point not in vertex_ids:
                vertex_ids[point] = mesh.Vertices.Add(point[0], point[1], point[2])
            indices.append(vertex_ids[point])
        for index, vertex_id in enumerate(indices):
            mesh.Faces.AddFace(centre_id, vertex_id, indices[(index + 1) % len(indices)])
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


def horizontal_interval(polygon, ordinate, tolerance):
    intersections = []
    for index, start in enumerate(polygon):
        end = polygon[(index + 1) % len(polygon)]
        if abs(start[1] - ordinate) <= tolerance:
            intersections.append(start[0])
        if (start[1] < ordinate < end[1]) or (end[1] < ordinate < start[1]):
            fraction = (ordinate - start[1]) / (end[1] - start[1])
            intersections.append(start[0] + fraction * (end[0] - start[0]))
    return (min(intersections), max(intersections)) if len(intersections) >= 2 else None


def face_window_layout(face, floor_bottom, width, height, spacing, sill, margin, tolerance):
    if max(point[2] for point in face) - min(point[2] for point in face) <= tolerance:
        return None
    normal = face_normal(face)
    if normal is None:
        return None
    horizontal = vector_unit((-normal[1], normal[0], 0.0))
    if horizontal is None:
        return None
    vertical = vector_cross(normal, horizontal)
    if vertical[2] <= 1e-9:
        return None
    origin = face[0]
    projected = [(vector_dot(vector_subtract(point, origin), horizontal),
                  vector_dot(vector_subtract(point, origin), vertical)) for point in face]
    lower = (floor_bottom + sill - origin[2]) / vertical[2]
    upper = (floor_bottom + sill + height - origin[2]) / vertical[2]
    lower_interval = horizontal_interval(projected, lower, tolerance)
    upper_interval = horizontal_interval(projected, upper, tolerance)
    if lower_interval is None or upper_interval is None:
        return None
    left = max(lower_interval[0], upper_interval[0])
    right = min(lower_interval[1], upper_interval[1])
    count = windows_on_edge(right - left, width, spacing, margin)
    if count == 0:
        return None
    first = left + (right - left - count * width - (count - 1) * spacing) / 2.0
    return (origin, horizontal, vertical, normal, lower, upper, first, count)


def panel_quads(layout, width, spacing, offset):
    origin, horizontal, vertical, normal, lower, upper, first, count = layout
    for panel_index in range(count):
        left = first + panel_index * (width + spacing)
        coordinates = ((left, lower), (left + width, lower), (left + width, upper), (left, upper))
        yield [tuple(origin[axis] + along * horizontal[axis] + up * vertical[axis] + offset * normal[axis]
                     for axis in range(3)) for along, up in coordinates]


def window_mesh(layouts, width, spacing, offset, colour):
    mesh = rg.Mesh()
    panel_count = 0
    for layout in layouts:
        for quad in panel_quads(layout, width, spacing, offset):
            first_vertex = mesh.Vertices.Count
            for point in quad:
                mesh.Vertices.Add(point[0], point[1], point[2])
            mesh.Faces.AddFace(first_vertex, first_vertex + 1, first_vertex + 2, first_vertex + 3)
            panel_count += 1
    return (finish_mesh(mesh, colour), panel_count) if panel_count else (None, 0)


meshes, colours, floor_blocks, windows, gardens = [], [], [], [], []
podium_blocks, podium_colours = [], []
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
maximum_cut_depth = number_input("setback_depth", 7000.0, 0.0)
facet_inclination = number_input("facet_tilt", 0.85, 0.0, 1.0)
common_floor_count = number_input("podium_floors", 4, 0, 10, integer=True)
common_height = number_input("podium_height", 14000.0, 0.0)
common_margin = number_input("podium_margin", 2000.0, 0.0)
if common_floor_count == 0:
    common_height = 0.0
random_seed = number_input("seed", 17, 0, 2147483647, integer=True)
panel_spacing = number_input("window_spacing", 750.0, 0.0)
panel_sill = number_input("window_sill", 800.0, 0.0)
panel_margin = number_input("window_margin", 250.0, positive_minimum)
planting_inset = number_input("garden_inset", 200.0, 0.0)
if sum(floor_counts) > 360:
    raise ValueError("Use at most 360 floors in total to keep the Grasshopper model responsive.")
if common_floor_count and common_height <= positive_minimum:
    raise ValueError("podium_height must be positive when podium_floors is greater than zero.")
for tower_index in range(3):
    if floor_counts[tower_index] <= common_floor_count or tower_heights[tower_index] <= common_height:
        raise ValueError("Tower {} needs at least one floor and positive height above the shared podium. "
                         "The tower height and floor count include that podium."
                         .format("ABC"[tower_index]))
storey_heights = [(height - common_height) / (count - common_floor_count)
                 for height, count in zip(tower_heights, floor_counts)]
if common_floor_count and panel_sill + panel_height + panel_margin > common_height / common_floor_count:
    raise ValueError("Windows do not fit the shared podium storey height. Increase podium_height, "
                     "reduce podium_floors, or reduce window height/sill/margin.")
for tower_index, storey_height in enumerate(storey_heights):
    if panel_sill + panel_height + panel_margin > storey_height:
        raise ValueError(
            "Tower {}: window_sill + window_height + window_margin exceeds the upper storey height ({:.2f}). "
            "Reduce window height/sill, increase tower height, or reduce its floor count."
            .format("ABC"[tower_index], storey_height))

scene_levels, cut_counts, storey_heights = make_scene_levels(
    base_width, base_depth, layout_gap, tower_heights, floor_counts,
    common_floor_count, common_height, common_margin, maximum_setbacks,
    maximum_cut_depth, random_seed, facet_inclination, tolerance)
estimated_panels = 0
for level in scene_levels:
    layouts = []
    for face in level["faces"]:
        layout = face_window_layout(face, level["bottom"], panel_width, panel_height,
                                    panel_spacing, panel_sill, panel_margin, tolerance)
        if layout is not None:
            layouts.append(layout)
            estimated_panels += layout[-1]
    level["window_layouts"] = layouts
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
for level in scene_levels:
    block_index = len(floor_blocks)
    tower_id, floor_index = level["tower"], level["floor"]
    stone_colour = stone_palette[(tower_id + floor_index) % len(stone_palette)]
    block = floor_mesh(level["faces"], stone_colour)
    floor_blocks.append(block)
    block_colours.append(stone_colour)
    if tower_id == 0:
        podium_blocks.append(block)
        podium_colours.append(stone_colour)
    tower_ids.append(tower_id)
    floor_ids.append(floor_index)
    outline_points = [rg.Point3d(point[0], point[1], level["bottom"]) for point in level["lower"]]
    floor_outlines.append(rg.PolylineCurve(outline_points + [outline_points[0]]))
    glazing, panel_count = window_mesh(level["window_layouts"], panel_width, panel_spacing,
                                      surface_offset, glass_colour)
    if glazing is not None:
        windows.append(glazing)
        window_colours.append(glass_colour)
        window_block_ids.append(block_index)
        panel_total += panel_count
    for exposed in exposed_regions(level["upper"], level["covers"], tolerance):
        planted = inset_polygon(exposed, planting_inset, tolerance)
        if not planted:
            omitted_gardens += 1
            continue
        green = green_palette[(tower_id + floor_index) % len(green_palette)]
        gardens.append(horizontal_mesh(planted, level["top"] + surface_offset, green))
        garden_colours.append(green)
        garden_block_ids.append(block_index)
        garden_area += polygon_area(planted)

meshes = floor_blocks + windows + gardens
colours = block_colours + window_colours + garden_colours
summaries = [
    "Tower {}: {} floors INCLUDING podium; total height {:.2f}; upper storey {:.2f}; {} active facet patches."
    .format("ABC"[index], floor_counts[index], tower_heights[index], storey_heights[index], cut_counts[index])
    for index in range(3)
]
info = ("Shared podium: {} connected floors, height {:.2f}; modelled ONCE.\n"
        .format(common_floor_count, common_height)) + "\n".join(summaries) + (
    "\n{} separate floor blocks; {} dark panels grouped into {} window meshes."
    "\n{} green terrace/roof patches; planted area {:.2f} square model units."
    "\n{} exposed pieces too narrow/small after garden_inset were omitted."
    "\nFacet budget: at most {} bounded sloping-cut patches per tower, not per floor."
    "\nTerrace gardens use top outlines minus the immediately adjacent floor(s); they may be partly sheltered."
    "\nAll lengths use Rhino model units. Tower heights are measured from ground to massing roof."
    "\nmeshes -> Custom Preview G; colours -> M. Keep the out socket for TEXT ONLY."
    "\nPhoto-inspired preset, NOT exact MVRDV geometry; dark panels, not holes; no structural validation."
).format(len(floor_blocks), panel_total, len(windows), len(gardens), garden_area,
         omitted_gardens, maximum_setbacks)
if len(windows) < len(floor_blocks):
    info += "\nSome floors have no panels because their edges are too short for the requested window width/margins."
print(info)
