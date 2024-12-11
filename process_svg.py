from lxml import etree as ET

# Mapping of text labels to numeric values
level_mapping = {
    "A1 acquis": 1.0,
    "A2 en cours d'acquisition": 1.5,
    "A2 acquis": 2.0,
    "B1 en cours d'acquisition": 2.5,
    "B1 acquis": 3.0,
    "B2 en cours d'acquisition": 3.5,
    "B2 acquis": 4.0,
    "C1 en cours d'acquisition": 4.5,
    "C1 acquis": 5.0,
    "C2 en cours d'acquisition": 5.5,
    "C2 acquis": 6.0
}

def interpolate_points(p1, p2, factor):
    """Interpolates between two points p1 and p2 by a given factor."""
    x = p1[0] + (p2[0] - p1[0]) * factor
    y = p1[1] + (p2[1] - p1[1]) * factor
    return (x, y)

def update_svg(levels):
    # Convert text labels to numeric values
    levels_numeric = {key: level_mapping[value] for key, value in levels.items()}

    # Load the SVG
    svg_file_path = 'C:/LANG/HEXA.svg'  # Input SVG file
    tree = ET.parse(svg_file_path)
    root = tree.getroot()

    # Coordinates of vertices for each proficiency level hexagon
    hexagons = [
        [(300.0, 250.0), (343.3013, 275.0), (343.3013, 325.0), (300.0, 350.0), (256.6987, 325.0), (256.6987, 275.0)],  # A1 (Smallest hexagon)
        [(300.0, 220.0), (369.282, 260.0), (369.282, 340.0), (300.0, 380.0), (230.718, 340.0), (230.718, 260.0)],    # A2
        [(300.0, 190.0), (395.2628, 245.0), (395.2628, 355.0), (300.0, 410.0), (204.7372, 355.0), (204.7372, 245.0)],  # B1
        [(300.0, 160.0), (421.2436, 230.0), (421.2436, 370.0), (300.0, 440.0), (178.7564, 370.0), (178.7564, 230.0)],  # B2
        [(300.0, 130.0), (447.2243, 215.0), (447.2243, 385.0), (300.0, 470.0), (152.7757, 385.0), (152.7757, 215.0)],  # C1
        [(300.0, 100.0), (473.2051, 200.0), (473.2051, 400.0), (300.0, 500.0), (126.7949, 400.0), (126.7949, 200.0)]   # C2 (Largest hexagon)
    ]

    points = []
    for i, level in enumerate(levels_numeric.values()):
        int_level = int(level)
        decimal_part = level - int_level

        if decimal_part == 0:  # Exact level (e.g., A1, A2, etc.)
            vertex = hexagons[int_level - 1][i]
        else:  # Intermediate level (e.g., A1.5, B2.5, etc.)
            p1 = hexagons[int_level - 1][i]
            p2 = hexagons[int_level][i]
            vertex = interpolate_points(p1, p2, decimal_part)

        points.append(vertex)

    # Close the polygon loop
    points.append(points[0])

    # Convert the points to the SVG format
    svg_points = ' '.join(f'{x},{y}' for x, y in points)

    # Create the polygon element with the correct styles
    polygon = ET.Element(
        'polygon',
        points=svg_points,
        style="fill:rgba(245, 245, 220, 0.4);stroke:orange;stroke-width:2"
    )
    root.append(polygon)

    # Add nodes (circles) at each vertex point
    for x, y in points[:-1]:  # Skip the last point because it's a duplicate of the first
        circle = ET.Element(
            'circle',
            cx=str(x),
            cy=str(y),
            r="4",  # Radius of the circles
            style="fill:orange;stroke:none"
        )
        root.append(circle)

    # Save the updated SVG
    output_svg = 'static/updated_HEXA.svg'  # Output SVG file in the static directory
    tree.write(output_svg)

    return output_svg
