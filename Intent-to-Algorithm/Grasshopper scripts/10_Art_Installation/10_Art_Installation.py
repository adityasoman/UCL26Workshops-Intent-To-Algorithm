#! python3
"""Faceted paper-relief visual model for Rhino 8 Grasshopper Python 3.

Paste this entire file into a Python 3 component in Script mode.
All inputs use Item Access. Unconnected optional inputs use defaults.

Core inputs: cols, rows, cell_size, height_min, height_max,
             rotation_deg, twist_deg
Optional inputs: lean, fold, gap, flow_x, flow_y, seed, base_plane
Outputs: meshes, colours, outlines, centres, tips, angles, heights, info
Keep the special console output named out. Rename the regular output a
to meshes, then add the other regular outputs. Do not rename out to meshes.

See 10_Art_Installation.md for type hints, sliders and preview wiring.
This is an image-inspired visual approximation, not a folding pattern.
"""

import math
import random

import Rhino.Geometry as rg
from System.Drawing import Color


REFERENCE_COLOURS = """
A31A10 A91E17 A0100B 9E221B 650403 C33224 970503 B11911 910906 A91811 AF1E13 720806
780805 AD140E BD1C10 D5412A C92014 C5170D 890703 C43522 BD2915 B32015 9F1A10 961F17
BE1F10 BE0D08 D61C08 E62F20 E83B1C E02219 C41A11 F75316 C72916 A2190D C13017 A32E1D
770201 EB250D E41A0B DA1D06 EC5422 FA6342 F76238 D4411E E04924 BB2D0B B35314 903E1B
C31711 F12B17 F22C1D F8301B EC4D19 ED6024 D86805 EC702E F49123 DB7C15 E38C20 D48A36
E23828 F85E45 F43020 F12F21 DF3318 E2671D FAA412 FCB933 E1911E C76811 F19023 DA8922
DC3F30 EE7536 FC3F29 FC894A FA5E24 FB7621 FA9C2B EF9033 E97D0E FDEE69 F4C037 A86E16
F46B3E FC852C FC8335 FB7B1F FC6A2B FC8D23 FB9326 F8811F EF871A F39210 C48F18 D6A43A
E27234 F88C2D FDAB28 FEBB55 FEA241 FB8E19 F37C15 F6A01C ED9D16 EE9705 D7A321 C2AA4F
DC923E E28726 FA9124 FDB430 FDC839 FDCB2E FCB316 F0AA2B E37504 DAA30C D2A108 B98704
E4BB51 F3B840 EFAC31 FDB627 F6AB1B F0B626 E1B73A E6AF29 EDAC27 E8AA23 D1970A 9D8515
EDBD63 F8B746 F8C448 FDEC53 FDDE5E DCB66A C6A748 AD9226 B29A44 E4BF66 E3B029 9C8844
"""


def read_number(name, default, lower=None, upper=None, integer=False):
    value = globals().get(name)
    if value is None:
        value = default
    try:
        number = float(value)
    except (TypeError, ValueError, OverflowError):
        raise ValueError("{} must be a number.".format(name))
    if not math.isfinite(number):
        raise ValueError("{} must be finite.".format(name))
    if integer and number != math.floor(number):
        raise ValueError("{} must be a whole number.".format(name))
    if lower is not None and number < lower:
        raise ValueError("{} must be at least {}.".format(name, lower))
    if upper is not None and number > upper:
        raise ValueError("{} must be at most {}.".format(name, upper))
    return int(number) if integer else number


def blend(start, end, amount):
    return start + (end - start) * amount


def clamp(value, minimum=0.0, maximum=1.0):
    return max(minimum, min(maximum, value))


def decode_palette(text):
    return [
        [tuple(int(token[offset:offset + 2], 16) for offset in (0, 2, 4))
         for token in line.split()]
        for line in text.strip().splitlines()
    ]


def sample_colour(palette, horizontal, vertical):
    sample_x = clamp(horizontal) * (len(palette[0]) - 1)
    sample_y = clamp(vertical) * (len(palette) - 1)
    left = int(math.floor(sample_x))
    bottom = int(math.floor(sample_y))
    right = min(left + 1, len(palette[0]) - 1)
    top = min(bottom + 1, len(palette) - 1)
    channels = []
    for channel in range(3):
        lower = blend(palette[bottom][left][channel],
                      palette[bottom][right][channel], sample_x - left)
        upper = blend(palette[top][left][channel],
                      palette[top][right][channel], sample_x - left)
        channels.append(int(round(blend(lower, upper, sample_y - bottom))))
    return Color.FromArgb(channels[0], channels[1], channels[2])


def make_module(plane, centre_x, centre_y, radius, height,
                angle, lean_amount, fold_amount, colour):
    direction_x = math.cos(angle)
    direction_y = math.sin(angle)
    outer = []
    shoulder = []
    for corner in range(6):
        corner_angle = corner * math.pi / 3.0
        outer.append(plane.PointAt(
            centre_x + radius * math.cos(corner_angle),
            centre_y + radius * math.sin(corner_angle), 0.0))
        shoulder_angle = corner_angle + math.radians(16.0) * fold_amount
        shoulder_radius = radius * (0.52 + 0.06 * math.cos(shoulder_angle - angle))
        shoulder_height = height * (
            0.23 + 0.12 * fold_amount * math.cos(3.0 * corner_angle - angle))
        shoulder.append(plane.PointAt(
            centre_x + shoulder_radius * math.cos(shoulder_angle)
            + 0.10 * radius * direction_x,
            centre_y + shoulder_radius * math.sin(shoulder_angle)
            + 0.10 * radius * direction_y,
            shoulder_height))
    tip = plane.PointAt(
        centre_x + lean_amount * height * direction_x,
        centre_y + lean_amount * height * direction_y, height)
    mesh = rg.Mesh()
    for corner in range(6):
        following = (corner + 1) % 6
        triangles = (
            (outer[corner], outer[following], shoulder[following]),
            (outer[corner], shoulder[following], shoulder[corner]),
            (shoulder[corner], shoulder[following], tip),
        )
        for triangle in triangles:
            first_vertex = mesh.Vertices.Count
            for point in triangle:
                mesh.Vertices.Add(point)
                mesh.VertexColors.Add(colour)
            mesh.Faces.AddFace(first_vertex, first_vertex + 1, first_vertex + 2)
    mesh.Normals.ComputeNormals()
    mesh.Compact()
    outline = rg.PolylineCurve(outer + [outer[0]])
    return mesh, outline, tip


meshes, colours, outlines, centres, tips, angles, heights = [], [], [], [], [], [], []
info = ""

column_count = read_number("cols", 22, 1, 200, integer=True)
row_count = read_number("rows", 20, 1, 200, integer=True)
size = read_number("cell_size", 70.0, 0.001)
minimum_height = read_number("height_min", 12.0, 0.001)
maximum_height = read_number("height_max", 85.0, 0.001)
rotation = read_number("rotation_deg", 0.0)
twist = read_number("twist_deg", 100.0)
lean_amount = read_number("lean", 0.75, 0.0, 2.0)
fold_amount = read_number("fold", 0.65, 0.0, 1.0)
gap_fraction = read_number("gap", 0.025, 0.0, 0.5)
flow_horizontal = read_number("flow_x", 0.35, 0.0, 1.0)
flow_vertical = read_number("flow_y", 0.35, 0.0, 1.0)
random_seed = read_number("seed", 7, 0, 2147483647, integer=True)
plane = globals().get("base_plane")
if plane is None:
    plane = rg.Plane.WorldXY
if not isinstance(plane, rg.Plane) or not plane.IsValid:
    raise ValueError("base_plane must be a valid Rhino plane.")
if maximum_height < minimum_height:
    raise ValueError("height_max must be greater than or equal to height_min.")
if column_count * row_count > 10000:
    raise ValueError("Use at most 10,000 cells; reduce cols or rows.")

palette = decode_palette(REFERENCE_COLOURS)
random_source = random.Random(random_seed)
grid_radius = size / 2.0
module_radius = grid_radius * (1.0 - gap_fraction)
spacing_x = 1.5 * grid_radius
spacing_y = math.sqrt(3.0) * grid_radius
span_x = (column_count - 1) * spacing_x
span_y = (row_count - 1 + (0.5 if column_count > 1 else 0.0)) * spacing_y
base_width = span_x + 2.0 * module_radius
base_height = span_y + math.sqrt(3.0) * module_radius
field_scale = max(base_width, base_height)
attractor_x = (flow_horizontal - 0.5) * span_x
attractor_y = (flow_vertical - 0.5) * span_y

for row in range(row_count):
    for column in range(column_count):
        centre_x = column * spacing_x - span_x / 2.0
        centre_y = (row + 0.5 * (column % 2)) * spacing_y - span_y / 2.0
        horizontal = column / float(column_count - 1) if column_count > 1 else 0.5
        vertical = (centre_y + span_y / 2.0) / span_y if row_count > 1 else 0.5
        distance_x = (centre_x - attractor_x) / field_scale
        distance_y = (centre_y - attractor_y) / field_scale
        distance = math.hypot(distance_x, distance_y)
        tangent = math.atan2(distance_y, distance_x) + math.pi / 2.0
        angle = tangent + math.radians(rotation + twist * distance)
        ripple = math.sin(2.0 * math.pi * (1.10 * horizontal - 0.70 * vertical))
        strength = clamp(
            0.18 + 0.48 * (1.0 - vertical) + 0.22 * (0.5 + 0.5 * ripple)
            + random_source.uniform(-0.08, 0.08))
        height = blend(minimum_height, maximum_height, strength)
        colour = sample_colour(palette, horizontal, vertical)
        mesh, outline, tip = make_module(
            plane, centre_x, centre_y, module_radius, height,
            angle, lean_amount, fold_amount, colour)
        meshes.append(mesh)
        colours.append(colour)
        outlines.append(outline)
        centres.append(plane.PointAt(centre_x, centre_y, 0.0))
        tips.append(tip)
        angles.append(math.degrees(angle) % 360.0)
        heights.append(height)

info = (
    "{0} modules ({1} columns x {2} rows); {3} triangular faces.\n"
    "Base footprint: {4:.2f} x {5:.2f} model units, excluding tip overhangs.\n"
    "Actual heights: {6:.2f} to {7:.2f}; allowed range: {8:.2f} to {9:.2f}.\n"
    "Tip direction = tangent + rotation_deg + twist_deg * normalized distance.\n"
    "Custom Preview: meshes -> G, colours -> M. Turn off Python preview.\n"
    "Visual approximation only: open faceted shells, not fabrication geometry."
).format(len(meshes), column_count, row_count, len(meshes) * 18,
         base_width, base_height, min(heights), max(heights),
         minimum_height, maximum_height)
print(info)
