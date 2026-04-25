---
title: "Normal Map vs Height Map: What's the Difference?"
description: "An in-depth comparison of normal maps and height (displacement) maps — how they work, when to use each, and why you might need both."
publishDate: 2026-04-24
author: "Editorial Team"
tags: ["normal maps", "height maps", "displacement maps", "PBR", "3D texturing"]
draft: false
---

If you're new to PBR texturing, normal maps and height maps can seem confusingly similar. Both add surface detail. Both are shades of blue and gray. But they work in fundamentally different ways.

Here's how they compare:

---

## Normal Map (Fake Detail)

A normal map uses RGB pixels to store surface normal directions — telling the renderer which way each pixel's surface "points." This creates the illusion of 3D detail without adding any actual geometry.

**How it works:**
- Each pixel contains a 3D vector (X, Y, Z)
- The vector tells the renderer to tilt that pixel's surface
- Lighting calculations use these tilted normals, creating shadows and highlights

**Pros:**
- Extremely cheap — performance cost is negligible
- Works at any distance (close up and far away)
- Compatible with every engine and renderer
- Adds infinite detail without increasing polygon count

**Cons:**
- Silhouette remains flat — the detail doesn't cast real shadows
- Doesn't add real geometry — on cliffs and edges, the flat contour is visible
- Can look "smeared" at extreme viewing angles

## Height Map (Real Detail)

A height map (also called a displacement map) stores actual elevation data as grayscale values. Black = lowest point, White = highest point. When applied, it actually moves vertices to create real 3D geometry.

**How it works:**
- Grayscale values encode height above the surface
- The renderer subdivides the mesh and displaces vertices
- True 3D detail that interacts with everything in the scene

**Pros:**
- Real 3D geometry — correct silhouettes, real self-shadowing
- Works with physics, collision detection
- Looks correct from every angle
- No texture stretching on edges

**Cons:**
- Expensive — requires tessellation/subdivision
- Can cause geometry artifacts if displacement is too strong
- Limited by mesh resolution
- Not suitable for real-time on low-end hardware

## Key Differences at a Glance

| Aspect | Normal Map | Height Map |
|--------|-----------|------------|
| **Type** | Color data (RGB) | Height data (grayscale) |
| **Geometry** | None (optical illusion) | Real displaced geometry |
| **Performance** | Very fast | Expensive (tessellation) |
| **Silhouette** | Flat | Accurate 3D contour |
| **Self-shadowing** | No | Yes |
| **Best for** | Small/medium surface detail | Large-scale surface features |
| **3D software** | Blender, Unity, Unreal, Godot | Blender, Unreal (tessellation) |
| **File size** | Small (color image) | Small (grayscale) |

## When to Use Each

### Use Normal Maps When:
- You need **small-to-medium surface detail** — scratches, pores, mortar lines, wood grain, fabric weave
- Performance matters — games, VR, mobile
- The detail doesn't need to cast real shadows (paint chips on a wall)
- You want maximum detail with zero geometry cost

### Use Height Maps When:
- You need **large-scale surface features** — deep cracks, raised stones, embossed text, carved surfaces
- The silhouette matters — you can see the object's edge (a cliff face, a sculpted wall)
- You're doing offline rendering or using tessellation
- The surface will be viewed at extreme angles

### Use Both When:
- You want maximum realism! Blender's Material Output node has both Normal and Displacement inputs
- The surface has both fine detail (normal) and large features (height)
- You're rendering high-end archviz or film-quality assets

## How They're Connected

In many PBR workflows, the height map comes first. You can derive a normal map from a height map using a Sobel filter or similar gradient computation. That's how many normal map generators work — they take a height map as input and bake it into a normal map.

At [FreePBRTextures](/textures/), our PBR texture sets use normal maps for surface detail (they're more widely compatible with game engines). We include height maps on many of our textures — look for sets tagged with "height: true" in the map listing.

## Practical Examples

### Example 1: Brick Wall
- **Normal map** — perfectly captures the mortar lines and brick surface texture
- **Height map** — could push the bricks out and recess the mortar for real depth
- **Best approach** — normal map for the surface grain, height map for deep mortar joints

### Example 2: Wood Floor
- **Normal map** — captures wood grain, scratches, and subtle plank bevels
- **Height map** — works for deep grooves between planks
- **Best approach** — normal map is usually sufficient for game-ready wood floors

### Example 3: Stone Path
- **Normal map** — captures stone surface texture and small cracks
- **Height map** — essential for the gaps between stones and uneven surfaces
- **Best approach** — both, especially for archviz or hero assets

## Related Reading

- [What Is a PBR Texture?](/blog/what-is-pbr-texture/)
- [Roughness vs Glossiness in PBR](/blog/roughness-vs-glossiness/)
- [Download Free PBR Texture Sets](/textures/)
