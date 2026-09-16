# Telegrinder pixel mark as a slab of optical glass, rendered with Cycles.
#
#   blender -b -P grinder.py -- <out_dir> [--fast] [--turn N] [--size PX]
#
# The silhouette comes straight from docs/assets/logo-black.png (20 px cells).
# Body and output strands are separate 4-connected pieces, so corner-touching
# pixels never share a vertex and the bevel stays clean.

import math
import sys

import bmesh
import bpy
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
FAST = "--fast" in argv
TURN = 0
SIZE = 1400
OUT = "/tmp/grinder"
rest = []
i = 0
while i < len(argv):
    a = argv[i]
    if a in ("--fast", "--clear", "--frost"):
        pass
    elif a == "--turn":
        TURN = int(argv[i + 1])
        i += 1
    elif a == "--size":
        SIZE = int(argv[i + 1])
        i += 1
    else:
        rest.append(a)
    i += 1
if rest:
    OUT = rest[0]

GRID = """
.........#############...............
.........#############...............
...........#########.................
.............#####...................
.............#####...................
.............#####............#.#.#.#
.............#####....####....#.#.#.#
........##################...#..#.#.#
......####################..#..#..#.#
...##.####################....#..#..#
...#######################..##..#..#.
.#########################.....#..#..
.#########################..###..#...
.#########################......#....
...####.##################..####.....
...####.##################...........
...####......#####....####...........
....#####....#####...................
.....####....#####...................
......###....#####...................
......###....#####...................
....#####....#####...................
#########....#####...................
#########....#####...................
....#####.##.#####.##................
..........###########................
........###############..............
........###############..............
""".strip().splitlines()

ROWS, COLS = len(GRID), len(GRID[0])
CELL = 0.2
DEPTH = 0.8
STRAND_COL = 26


def components():
    seen = set()
    out = []
    for r in range(ROWS):
        for c in range(COLS):
            if GRID[r][c] != "#" or (r, c) in seen:
                continue
            stack, comp = [(r, c)], []
            seen.add((r, c))
            while stack:
                y, x = stack.pop()
                comp.append((y, x))
                for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < ROWS and 0 <= nx < COLS and GRID[ny][nx] == "#" and (ny, nx) not in seen:
                        seen.add((ny, nx))
                        stack.append((ny, nx))
            out.append(comp)
    return out


def slab(name, cells, depth, mat, bevel):
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    verts = {}

    def v(y, x):
        key = (y, x)
        if key not in verts:
            px = (x - COLS / 2) * CELL
            pz = (ROWS / 2 - y) * CELL
            verts[key] = bm.verts.new((px, -depth / 2, pz))
        return verts[key]

    for y, x in cells:
        bm.faces.new((v(y, x), v(y + 1, x), v(y + 1, x + 1), v(y, x + 1)))
    bm.normal_update()
    ext = bmesh.ops.extrude_face_region(bm, geom=bm.faces[:])
    moved = [e for e in ext["geom"] if isinstance(e, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, verts=moved, vec=(0, depth, 0))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    bmesh.ops.dissolve_limit(bm, angle_limit=math.radians(1), verts=bm.verts[:], edges=bm.edges[:])
    bm.to_mesh(me)
    bm.free()
    obj = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(obj)
    mod = obj.modifiers.new("bevel", "BEVEL")
    mod.width = bevel
    mod.segments = 8
    mod.limit_method = "ANGLE"
    mod.angle_limit = math.radians(40)
    mod.harden_normals = True
    mod.miter_outer = "MITER_ARC"
    tri = obj.modifiers.new("tri", "TRIANGULATE")
    tri.keep_custom_normals = True
    for p in obj.data.polygons:
        p.use_smooth = True
    obj.data.materials.append(mat)
    return obj


def set_input(node, names, value):
    for name in names if isinstance(names, (list, tuple)) else [names]:
        if name in node.inputs:
            node.inputs[name].default_value = value
            return


def glass(name, absorb, density, rough=0.0, dispersion=0.35, ior=1.5):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    bsdf = nt.nodes.get("Principled BSDF")
    set_input(bsdf, "Base Color", (1, 1, 1, 1))
    set_input(bsdf, "Roughness", rough)
    set_input(bsdf, "IOR", ior)
    set_input(bsdf, ["Transmission Weight", "Transmission"], 1.0)
    set_input(bsdf, "Dispersion", dispersion)
    set_input(bsdf, ["Coat Weight", "Clearcoat"], 0.35)
    set_input(bsdf, ["Coat Roughness", "Clearcoat Roughness"], 0.02)
    vol = nt.nodes.new("ShaderNodeVolumeAbsorption")
    vol.inputs["Color"].default_value = (*absorb, 1)
    vol.inputs["Density"].default_value = density
    nt.links.new(vol.outputs["Volume"], nt.nodes["Material Output"].inputs["Volume"])
    return m


def strip(name, loc, size, power, color=(1, 1, 1), target=(0, 0, 0)):
    data = bpy.data.lights.new(name, "AREA")
    data.shape = "RECTANGLE"
    data.size, data.size_y = size
    data.energy = power
    data.color = color
    obj = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(obj)
    obj.location = loc
    obj.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    return obj


def scene_setup():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    prefs = bpy.context.preferences.addons["cycles"].preferences
    try:
        prefs.compute_device_type = "METAL"
        prefs.get_devices()
        for d in prefs.devices:
            d.use = True
        scene.cycles.device = "GPU"
    except Exception:
        scene.cycles.device = "CPU"
    scene.cycles.samples = 64 if FAST else (384 if SIZE > 1000 else 128)
    scene.cycles.use_denoising = True
    scene.cycles.max_bounces = 24
    scene.cycles.transmission_bounces = 24
    scene.cycles.glossy_bounces = 8
    scene.cycles.volume_bounces = 2
    scene.cycles.caustics_refractive = True
    scene.render.film_transparent = True
    scene.cycles.film_transparent_glass = "--clear" in argv
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGBA"
    scene.render.image_settings.color_depth = "8"
    scene.view_settings.view_transform = "AgX"
    scene.view_settings.look = "AgX - Medium High Contrast"
    scene.view_settings.exposure = 0.0
    scene.render.resolution_x = SIZE
    scene.render.resolution_y = int(SIZE * 0.8)
    return scene


def world():
    w = bpy.data.worlds.new("room")
    bpy.context.scene.world = w
    w.use_nodes = True
    nt = w.node_tree
    nt.nodes.clear()
    coord = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    bg = nt.nodes.new("ShaderNodeBackground")
    out = nt.nodes.new("ShaderNodeOutputWorld")
    e = ramp.color_ramp.elements
    e[0].position, e[0].color = 0.40, (0.02, 0.025, 0.035, 1)
    e[1].position, e[1].color = 0.52, (1.0, 1.0, 1.0, 1)
    mid = e.new(0.47)
    mid.color = (0.35, 0.45, 0.62, 1)
    top = e.new(0.8)
    top.color = (0.55, 0.6, 0.68, 1)
    bg.inputs["Strength"].default_value = 0.7
    nt.links.new(coord.outputs["Generated"], sep.inputs[0])
    nt.links.new(sep.outputs["Z"], ramp.inputs["Fac"])
    nt.links.new(ramp.outputs["Color"], bg.inputs["Color"])
    nt.links.new(bg.outputs["Background"], out.inputs["Surface"])


def tile(name, y, x, depth, mat, gap, bevel):
    size = CELL - gap
    bpy.ops.mesh.primitive_cube_add(size=1)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = (size, depth, size)
    bpy.ops.object.transform_apply(scale=True)
    obj.location = ((x + 0.5 - COLS / 2) * CELL, 0, (ROWS / 2 - y - 0.5) * CELL)
    mod = obj.modifiers.new("bevel", "BEVEL")
    mod.width = bevel
    mod.segments = 6
    mod.harden_normals = True
    for p in obj.data.polygons:
        p.use_smooth = True
    obj.data.materials.append(mat)
    return obj


def build():
    frost = "--frost" in argv
    body = glass("body", (0.86, 0.93, 1.0), 0.45, rough=0.3 if frost else 0.0, dispersion=0.5)
    minced = glass("minced", (0.10, 0.42, 1.0), 2.6, rough=0.18 if frost else 0.02, dispersion=0.3)
    parts = []
    for n, comp in enumerate(components()):
        if min(x for _, x in comp) >= STRAND_COL:
            parts.append(slab(f"strand{n}", comp, DEPTH * 0.6, minced, 0.05))
        else:
            parts.append(slab(f"body{n}", comp, DEPTH, body, 0.09))
    root = bpy.data.objects.new("mark", None)
    bpy.context.collection.objects.link(root)
    for p in parts:
        p.parent = root
    root.rotation_euler = (math.radians(3), 0, math.radians(-16 + TURN))
    return root


scene = scene_setup()
world()
build()
# long softboxes give the bevels clean, continuous highlights
strip("top", (0, -1.5, 9), (12, 2.2), 900, (1.0, 0.99, 0.97))
strip("left", (-9, -5, 2), (1.6, 9), 1100, (0.93, 0.96, 1.0))
strip("right", (9, -3, 3), (1.2, 9), 700, (1.0, 0.95, 0.9))
strip("back", (2, 8, 4), (8, 3), 1300, (0.85, 0.92, 1.0))
strip("floor", (0, -4, -7), (10, 3), 260, (0.7, 0.8, 1.0))

cam_data = bpy.data.cameras.new("cam")
cam_data.lens = 85
cam = bpy.data.objects.new("cam", cam_data)
bpy.context.collection.objects.link(cam)
cam.location = (0, -23, 2.6)
cam.rotation_euler = (Vector((0, 0, 0.1)) - cam.location).to_track_quat("-Z", "Y").to_euler()
scene.camera = cam

scene.render.filepath = OUT
bpy.ops.render.render(write_still=True)
