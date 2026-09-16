# Renders the glass twin of every pixel icon in src/render/icons.json with Cycles.
#
#   blender -b -P design/icons.py -- <out_dir> [name ...] [--fast]
#
# Same material and light rig as the logo (design/grinder.py): '#' cells are frosted glass,
# '+' cells are blue glass. Every icon uses one camera, so the 16×16 grid always lands on the
# same 80 % square of the frame and the web morph can line pixels up with the render.

import json
import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
FAST = "--fast" in argv
args = [a for a in argv if not a.startswith("--")]
OUT = args[0] if args else "/tmp/telegrinder-icons"
ONLY = set(args[1:])

HERE = os.path.dirname(os.path.abspath(__file__))
ICONS = {k: v for k, v in json.load(open(os.path.join(HERE, "../src/render/icons.json"))).items() if k != "_"}

CELL = 0.2
SIZE = 640
GRID = 16


def set_input(node, names, value):
    for name in names if isinstance(names, (list, tuple)) else [names]:
        if name in node.inputs:
            node.inputs[name].default_value = value
            return


def glass(name, absorb, density, rough, dispersion):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    bsdf = nt.nodes.get("Principled BSDF")
    set_input(bsdf, "Base Color", (1, 1, 1, 1))
    set_input(bsdf, "Roughness", rough)
    set_input(bsdf, "IOR", 1.5)
    set_input(bsdf, ["Transmission Weight", "Transmission"], 1.0)
    set_input(bsdf, "Dispersion", dispersion)
    set_input(bsdf, ["Coat Weight", "Clearcoat"], 0.35)
    set_input(bsdf, ["Coat Roughness", "Clearcoat Roughness"], 0.02)
    vol = nt.nodes.new("ShaderNodeVolumeAbsorption")
    vol.inputs["Color"].default_value = (*absorb, 1)
    vol.inputs["Density"].default_value = density
    nt.links.new(vol.outputs["Volume"], nt.nodes["Material Output"].inputs["Volume"])
    return m


def components(rows, symbol):
    seen, out = set(), []
    for r in range(GRID):
        for c in range(GRID):
            if rows[r][c] != symbol or (r, c) in seen:
                continue
            stack, comp = [(r, c)], []
            seen.add((r, c))
            while stack:
                y, x = stack.pop()
                comp.append((y, x))
                for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < GRID and 0 <= nx < GRID and rows[ny][nx] == symbol and (ny, nx) not in seen:
                        seen.add((ny, nx))
                        stack.append((ny, nx))
            out.append(comp)
    return out


def slab(name, cells, depth, mat, bevel):
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    verts = {}

    def v(y, x):
        if (y, x) not in verts:
            verts[(y, x)] = bm.verts.new(((x - GRID / 2) * CELL, -depth / 2, (GRID / 2 - y) * CELL))
        return verts[(y, x)]

    for (y, x) in cells:
        bm.faces.new((v(y, x), v(y + 1, x), v(y + 1, x + 1), v(y, x + 1)))
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
    mod.segments = 6
    mod.limit_method = "ANGLE"
    mod.angle_limit = math.radians(40)
    mod.harden_normals = True
    mod.miter_outer = "MITER_ARC"
    for p in obj.data.polygons:
        p.use_smooth = True
    obj.data.materials.append(mat)
    return obj


def strip(name, loc, size, power, color):
    data = bpy.data.lights.new(name, "AREA")
    data.shape = "RECTANGLE"
    data.size, data.size_y = size
    data.energy = power
    data.color = color
    obj = bpy.data.objects.new(name, data)
    bpy.context.collection.objects.link(obj)
    obj.location = loc
    obj.rotation_euler = (Vector((0, 0, 0)) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()


def scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    prefs = bpy.context.preferences.addons["cycles"].preferences
    try:
        prefs.compute_device_type = "METAL"
        prefs.get_devices()
        for d in prefs.devices:
            d.use = True
        sc.cycles.device = "GPU"
    except Exception:
        sc.cycles.device = "CPU"
    sc.cycles.samples = 48 if FAST else 160
    sc.cycles.use_denoising = True
    sc.cycles.max_bounces = 24
    sc.cycles.transmission_bounces = 24
    sc.render.film_transparent = True
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGBA"
    sc.view_settings.view_transform = "AgX"
    sc.view_settings.look = "AgX - Medium High Contrast"
    sc.render.resolution_x = SIZE
    sc.render.resolution_y = SIZE

    w = bpy.data.worlds.new("room")
    sc.world = w
    w.use_nodes = True
    nt = w.node_tree
    nt.nodes.clear()
    coord, sep, ramp = nt.nodes.new("ShaderNodeTexCoord"), nt.nodes.new("ShaderNodeSeparateXYZ"), nt.nodes.new("ShaderNodeValToRGB")
    bg, out = nt.nodes.new("ShaderNodeBackground"), nt.nodes.new("ShaderNodeOutputWorld")
    e = ramp.color_ramp.elements
    e[0].position, e[0].color = 0.40, (0.02, 0.025, 0.035, 1)
    e[1].position, e[1].color = 0.52, (1.0, 1.0, 1.0, 1)
    e.new(0.47).color = (0.35, 0.45, 0.62, 1)
    e.new(0.8).color = (0.55, 0.6, 0.68, 1)
    bg.inputs["Strength"].default_value = 0.7
    nt.links.new(coord.outputs["Generated"], sep.inputs[0])
    nt.links.new(sep.outputs["Z"], ramp.inputs["Fac"])
    nt.links.new(ramp.outputs["Color"], bg.inputs["Color"])
    nt.links.new(bg.outputs["Background"], out.inputs["Surface"])

    strip("top", (0, -1.5, 9), (12, 2.2), 900, (1.0, 0.99, 0.97))
    strip("left", (-9, -5, 2), (1.6, 9), 1100, (0.93, 0.96, 1.0))
    strip("right", (9, -3, 3), (1.2, 9), 700, (1.0, 0.95, 0.9))
    strip("back", (2, 8, 4), (8, 3), 1300, (0.85, 0.92, 1.0))
    strip("floor", (0, -4, -7), (10, 3), 260, (0.7, 0.8, 1.0))

    cam_data = bpy.data.cameras.new("cam")
    cam_data.lens = 85
    cam = bpy.data.objects.new("cam", cam_data)
    bpy.context.collection.objects.link(cam)
    # 16 cells × 0.2 = 3.2 units should fill 80 % of the frame: 4.0 units wide at the subject.
    distance = 4.0 * cam_data.lens / cam_data.sensor_width
    cam.location = (0, -distance, distance * 0.08)
    cam.rotation_euler = (Vector((0, 0, 0)) - cam.location).to_track_quat("-Z", "Y").to_euler()
    sc.camera = cam
    return sc


def render(name, rows):
    sc = scene()
    body = glass("body", (0.86, 0.93, 1.0), 0.45, 0.3, 0.5)
    accent = glass("accent", (0.22, 0.52, 1.0), 0.9, 0.16, 0.3)
    root = bpy.data.objects.new("icon", None)
    bpy.context.collection.objects.link(root)
    for n, comp in enumerate(components(rows, "#")):
        slab(f"b{n}", comp, 0.6, body, 0.06).parent = root
    for n, comp in enumerate(components(rows, "+")):
        slab(f"a{n}", comp, 0.42, accent, 0.05).parent = root
    root.rotation_euler = (math.radians(4), 0, math.radians(-14))
    sc.render.filepath = os.path.join(OUT, f"{name}.png")
    bpy.ops.render.render(write_still=True)


os.makedirs(OUT, exist_ok=True)
for name, rows in ICONS.items():
    if not ONLY or name in ONLY:
        render(name, rows)
