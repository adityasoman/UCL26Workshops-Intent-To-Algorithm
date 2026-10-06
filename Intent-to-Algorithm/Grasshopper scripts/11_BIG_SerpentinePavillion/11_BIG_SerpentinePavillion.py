#! python3
"""BIG Serpentine Pavilion-inspired visual model, Rhino 8 Python 3 Script mode.

Inputs, all Item Access:
    base_a, base_b: optional Curve inputs; connect both or neither.
    height, depth, module_width, module_height, opening_width: float.
Optional float inputs: length, thickness, gap, profile_power.

Outputs: meshes, colours, base_profiles, ridge, centres, module_planes,
         row_ids, side_ids, info.
Keep the special console output named out. Rename the regular output a to
meshes, then add colours and the other regular outputs. Never rename out.

Depth is BOX extrusion depth. Opening width is the maximum sampled nominal
ground-level clear gap, not entrance width. See the matching Markdown guide.
"""

import math

import Rhino
import Rhino.Geometry as rg
from System.Drawing import Color


def number_input(name, default, minimum=None, maximum=None):
    value = globals().get(name)
    if value is None:
        value = default
    if value is None:
        return None
    try:
        result = float(value)
    except (TypeError, ValueError, OverflowError):
        raise ValueError("{} must be a number.".format(name))
    if not math.isfinite(result):
        raise ValueError("{} must be finite.".format(name))
    if minimum is not None and result < minimum:
        raise ValueError("{} must be at least {}.".format(name, minimum))
    if maximum is not None and result > maximum:
        raise ValueError("{} must be at most {}.".format(name, maximum))
    return result


def generated_curves(plan_length):
    lower_points = []
    upper_points = []
    for index in range(129):
        fraction = index / 128.0
        station = plan_length * fraction
        sway = -0.55 * math.sin(2.0 * math.pi * fraction)
        half_gap = 0.65 + 0.20 * math.sin(math.pi * fraction)
        lower_points.append(rg.Point3d(station, plan_length * (sway - half_gap) / 4.0, 0))
        upper_points.append(rg.Point3d(station, plan_length * (sway + half_gap) / 4.0, 0))
    return rg.PolylineCurve(lower_points), rg.PolylineCurve(upper_points)


def prepare_curve(value, name, tolerance, messages):
    if not isinstance(value, rg.Curve) or not value.IsValid:
        raise ValueError("{} must have a Curve type hint and contain a valid curve.".format(name))
    if value.IsClosed:
        raise ValueError("{} must be an open plan curve, not a closed loop.".format(name))
    result = value.DuplicateCurve()
    bounds = result.GetBoundingBox(True)
    if max(abs(bounds.Min.Z), abs(bounds.Max.Z)) > tolerance:
        messages.append("{} was projected to World XY; input elevations were ignored.".format(name))
    if not result.Transform(rg.Transform.PlanarProjection(rg.Plane.WorldXY)):
        raise ValueError("Could not project {} to World XY.".format(name))
    if result.GetLength() <= tolerance:
        raise ValueError("{} is too short after projection.".format(name))
    return result


def align_curves(first, second, tolerance):
    direct = (first.PointAtStart.DistanceTo(second.PointAtStart)
              + first.PointAtEnd.DistanceTo(second.PointAtEnd))
    reversed_cost = (first.PointAtStart.DistanceTo(second.PointAtEnd)
                     + first.PointAtEnd.DistanceTo(second.PointAtStart))
    if reversed_cost < direct:
        if not second.Reverse():
            raise ValueError("Could not reverse base_b to align the curve directions.")
    start = rg.Point3d(
        (first.PointAtStart.X + second.PointAtStart.X) / 2.0,
        (first.PointAtStart.Y + second.PointAtStart.Y) / 2.0, 0)
    end = rg.Point3d(
        (first.PointAtEnd.X + second.PointAtEnd.X) / 2.0,
        (first.PointAtEnd.Y + second.PointAtEnd.Y) / 2.0, 0)
    direction = end - start
    if direction.Length <= tolerance or not direction.Unitize():
        raise ValueError("Base curves need distinct common start and end regions.")
    transverse = rg.Vector3d(-direction.Y, direction.X, 0)
    plane = rg.Plane(start, direction, transverse)
    to_local = rg.Transform.PlaneToPlane(plane, rg.Plane.WorldXY)
    for name, curve in (("base_a", first), ("base_b", second)):
        if not curve.Transform(to_local):
            raise ValueError("Could not transform {} into the pavilion frame.".format(name))
        parameters = curve.DivideByCount(128, True)
        if parameters is None:
            raise ValueError("Could not sample {}.".format(name))
        coordinates = [curve.PointAt(parameter).X for parameter in parameters]
        if any(after < before - tolerance for before, after in zip(coordinates, coordinates[1:])):
            raise ValueError("{} doubles back along the pavilion axis. Use a single-valued plan curve.".format(name))
    start_station = max(first.PointAtStart.X, second.PointAtStart.X)
    end_station = min(first.PointAtEnd.X, second.PointAtEnd.X)
    if end_station - start_station <= tolerance:
        raise ValueError("The two curves have no shared length along the pavilion axis.")
    return first, second, plane, start_station, end_station


def ordinate_at(curve, station, tolerance):
    section_plane = rg.Plane(rg.Point3d(station, 0, 0), rg.Vector3d.XAxis)
    events = rg.Intersect.Intersection.CurvePlane(curve, section_plane, tolerance)
    ordinates = []
    if events is not None:
        for event in events:
            if event.IsOverlap:
                raise ValueError("A base curve overlaps a cross-section. Remove transverse segments or folds.")
            if event.IsPoint:
                ordinate = event.PointA.Y
                if not any(abs(ordinate - existing) <= tolerance for existing in ordinates):
                    ordinates.append(ordinate)
    if len(ordinates) != 1:
        raise ValueError(
            "Each base curve must cross every section once; found {} intersections at {:.3f}."
            .format(len(ordinates), station))
    return ordinates[0]


def fit_modules(span, requested_size, joint):
    count = max(1, int(math.ceil((span + joint) / (requested_size + joint))))
    actual_size = (span - (count - 1) * joint) / count
    return count, actual_size


def tube_mesh(width, height, depth, wall_thickness, colour):
    result = rg.Mesh()
    for front_back in (-1.0, 1.0):
        for inset in (0.0, wall_thickness):
            half_width = width / 2.0 - inset
            half_height = height / 2.0 - inset
            for horizontal, vertical in (
                    (-half_width, -half_height), (half_width, -half_height),
                    (half_width, half_height), (-half_width, half_height)):
                result.Vertices.Add(horizontal, front_back * depth / 2.0, vertical)
    for corner in range(4):
        following = (corner + 1) % 4
        result.Faces.AddFace(corner, following, following + 4, corner + 4)
        result.Faces.AddFace(corner + 8, corner + 12, following + 12, following + 8)
        result.Faces.AddFace(corner, corner + 8, following + 8, following)
        result.Faces.AddFace(corner + 4, following + 4, following + 12, corner + 12)
    result.Normals.ComputeNormals()
    result.Unweld(0.0, True)
    result.Normals.ComputeNormals()
    result.VertexColors.CreateMonotoneMesh(colour)
    result.Compact()
    if not result.IsValid:
        raise ValueError("The module mesh is invalid; check module dimensions and thickness.")
    return result


meshes, colours, centres, module_planes, row_ids, side_ids = [], [], [], [], [], []
base_profiles = []
ridge = None
info = ""
warnings = []

document = Rhino.RhinoDoc.ActiveDoc
tolerance = max(document.ModelAbsoluteTolerance if document is not None else 0.01, 1e-9)
positive_minimum = 2.0 * tolerance
pavilion_height = number_input("height", 14000.0, positive_minimum)
box_depth = number_input("depth", 1000.0, positive_minimum)
requested_width = number_input("module_width", 500.0, positive_minimum)
requested_height = number_input("module_height", 400.0, positive_minimum)
requested_opening = number_input("opening_width", None, 0.0)
default_length = number_input("length", 28000.0, positive_minimum)
wall_thickness = number_input("thickness", 12.0, positive_minimum)
joint = number_input("gap", 0.0, 0.0)
profile_exponent = number_input("profile_power", 1.7, 0.2, 5.0)
input_a = globals().get("base_a")
input_b = globals().get("base_b")
if (input_a is None) != (input_b is None):
    raise ValueError("Connect both base_a and base_b, or leave both absent/optional for the built-in curves.")
using_defaults = input_a is None
if using_defaults:
    input_a, input_b = generated_curves(default_length)
    if requested_opening is None:
        requested_opening = 10000.0

curve_a = prepare_curve(input_a, "base_a", tolerance, warnings)
curve_b = prepare_curve(input_b, "base_b", tolerance, warnings)
curve_a, curve_b, axis_plane, first_station, last_station = align_curves(curve_a, curve_b, tolerance)
pavilion_length = last_station - first_station
column_count, actual_width = fit_modules(pavilion_length, requested_width, joint)
row_count, actual_height = fit_modules(pavilion_height, requested_height, joint)
if column_count * row_count > 12000:
    raise ValueError("More than 12,000 modules requested. Increase module sizes or reduce the pavilion size.")
if min(actual_width, actual_height) <= 2.0 * wall_thickness + tolerance:
    raise ValueError("Fitted module width and height must exceed twice thickness. Reduce thickness or gap.")
if row_count < 2:
    warnings.append("One course cannot form an unzipped enclosure; increase height or reduce module_height.")

column_stations = [
    first_station + actual_width / 2.0 + column * (actual_width + joint)
    for column in range(column_count)
]
guide_stations = [first_station + pavilion_length * index / 128.0 for index in range(129)]
all_stations = sorted(set(column_stations + guide_stations))
raw_sections = {
    station: (ordinate_at(curve_a, station, tolerance), ordinate_at(curve_b, station, tolerance))
    for station in all_stations
}
differences = [upper - lower for lower, upper in raw_sections.values()]
if min(differences) < -tolerance and max(differences) > tolerance:
    raise ValueError("The base curves cross within the sampled footprint. Use two non-crossing plan curves.")
if max(differences) <= tolerance and min(differences) < -tolerance:
    raw_sections = {station: (upper, lower) for station, (lower, upper) in raw_sections.items()}
    differences = [-difference for difference in differences]
    warnings.append("Base curve sides were swapped into local left/right order.")
maximum_separation = max(differences)
if maximum_separation <= tolerance:
    raise ValueError("The base curves must be separated somewhere; coincident curves do not define a cavity.")
opening_scale = ((requested_opening + box_depth) / maximum_separation
                 if requested_opening is not None else 1.0)
sections = {}
for station, (lower, upper) in raw_sections.items():
    midpoint = (lower + upper) / 2.0
    half_separation = max(0.0, upper - lower) * opening_scale / 2.0
    sections[station] = (midpoint - half_separation, midpoint + half_separation)

nominal_clearances = [upper - lower - box_depth for lower, upper in sections.values()]
if min(nominal_clearances) < -tolerance:
    warnings.append("Some nominal base clearances are negative: box-depth envelopes overlap there.")
for side in (0, 1):
    base_profiles.append(rg.PolylineCurve([
        axis_plane.PointAt(station, sections[station][side], 0.0)
        for station in all_stations
    ]))
ridge = rg.LineCurve(axis_plane.PointAt(first_station, 0, pavilion_height),
                     axis_plane.PointAt(last_station, 0, pavilion_height))
module_colour = Color.FromArgb(225, 235, 230)
prototype = tube_mesh(actual_width, actual_height, box_depth, wall_thickness, module_colour)
minimum_ordinate = float("inf")
maximum_ordinate = float("-inf")

for row in range(row_count):
    vertical_fraction = row / float(row_count - 1) if row_count > 1 else 0.0
    spread = (1.0 - vertical_fraction) ** profile_exponent
    elevation = actual_height / 2.0 + row * (actual_height + joint)
    for column, station in enumerate(column_stations):
        side = (row + column) % 2
        ordinate = sections[station][side] * spread
        centre = axis_plane.PointAt(station, ordinate, elevation)
        module_plane = rg.Plane(centre, axis_plane.XAxis, axis_plane.YAxis)
        mesh = prototype.DuplicateMesh()
        if not mesh.Transform(rg.Transform.PlaneToPlane(rg.Plane.WorldXY, module_plane)):
            raise ValueError("Could not place a module.")
        meshes.append(mesh)
        colours.append(module_colour)
        centres.append(centre)
        module_planes.append(module_plane)
        row_ids.append(row)
        side_ids.append(-1 if row_count > 1 and row == row_count - 1 else side)
        minimum_ordinate = min(minimum_ordinate, ordinate - box_depth / 2.0)
        maximum_ordinate = max(maximum_ordinate, ordinate + box_depth / 2.0)

start_clearance = sections[first_station][1] - sections[first_station][0] - box_depth
end_clearance = sections[last_station][1] - sections[last_station][0] - box_depth
info = (
    "{0} hollow modules: {1} columns x {2} courses, checkerboard split.\n"
    "Overall height: {3:.2f}; axial length: {4:.2f}; modeled transverse extent: {5:.2f}.\n"
    "Fitted module width x height x depth: {6:.2f} x {7:.2f} x {8:.2f}; thickness: {9:.2f}.\n"
    "Nominal sampled maximum ground clear gap: {10:.2f}.\n"
    "Nominal start/end clear gaps: {11:.2f} / {12:.2f} (not guaranteed walk-through clearances).\n"
    "Opening override: {13}; all lengths in Rhino model units.\n"
    "meshes -> Custom Preview G; colours -> M. The out socket is TEXT ONLY.\n"
    "Visual model only: no connections, engineering, collision checks or fabrication detailing."
).format(len(meshes), column_count, row_count, pavilion_height, pavilion_length,
         maximum_ordinate - minimum_ordinate, actual_width, actual_height, box_depth,
         wall_thickness, max(nominal_clearances), start_clearance, end_clearance,
         "active" if requested_opening is not None else "off; input curve spacing retained")
if warnings:
    info += "\nNotes:\n- " + "\n- ".join(warnings)
print(info)
