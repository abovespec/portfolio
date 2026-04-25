---
title: "What Is a PBR Texture? A Complete Guide to Physically Based Rendering"
description: "Learn the fundamentals of PBR textures — albedo, normal, roughness, metallic maps, and how they work together to create realistic 3D materials."
publishDate: 2026-04-24
author: "Editorial Team"
tags: ["PBR", "physically based rendering", "3D materials", "texture maps", "game dev"]
draft: false
---

If you've worked with 3D graphics in the last decade, you've heard the term "PBR texture." It's everywhere — but what does it actually mean?

PBR stands for **Physically Based Rendering**. It's a shading model that simulates how light interacts with real-world surfaces. Instead of artists manually painting shadows and highlights, PBR uses mathematical models of light behavior to render materials that look realistic under any lighting condition.

## What Makes PBR Different from Traditional Texturing?

Before PBR, 3D artists used techniques like:

- **Diffuse + Specular maps** — two separate textures for base color and highlights
- **Hand-painted lighting** — fake shadows and highlights baked into the diffuse map
- **Fixed shaders** — each material type needed a custom shader

PBR replaced all of this with a unified approach based on real physics. The same PBR material looks correct whether it's in a sunlit outdoor scene, a dim interior, or under colored lighting. This consistency is why PBR became the standard across every major game engine and 3D tool.

## The Core PBR Texture Maps

A standard PBR texture set usually includes these maps:

### 1. Albedo (Base Color) Map
The albedo map defines the surface color — what the material looks like under pure white light. It should contain only color information, with no lighting or shadows baked in.

**Key rule:** The albedo map should never contain directional lighting or shadows. That's what the other maps handle.

Browse our [CC0 albedo textures](/albedo-textures/) to see examples.

### 2. Normal Map
A normal map encodes surface detail as RGB color values that tell the renderer which direction each pixel's surface is "facing." This creates the illusion of 3D detail (bumps, scratches, mortar lines) without adding geometry.

- **RGB channels** encode X, Y, Z surface normal directions
- Works with any lighting direction
- Saves millions of polygons compared to geometric detail

Learn more in our guide on [normal maps vs height maps](/blog/normal-map-vs-height-map/).

### 3. Roughness Map
The roughness map (grayscale) controls how rough or smooth a surface is at each point:

- **Black (0)** = perfectly smooth, mirror-like reflection
- **White (1)** = completely rough, diffuse reflection

A brushed metal surface, for example, would have a mostly dark roughness map with streaks of lighter values in the brush direction.

### 4. Metallic Map
The metallic map (grayscale) defines which areas of the surface behave like metal:

- **Black (0)** = dielectric (non-metal), like plastic, wood, stone
- **White (1)** = metallic conductor, like iron, gold, copper

Metals reflect light differently — they have colored reflections and no diffuse color. That's why the metallic map is critical for realistic rendering.

### 5. Height / Displacement Map
An optional height map adds actual geometric displacement to the surface. Unlike the normal map (which only fakes detail), a height map physically moves vertices — but it's much more expensive and typically used only for hero assets.

## The PBR Material Formula

This is the key insight: **there is no single PBR "look."** A PBR material just defines the physical properties of a surface. The final rendered look depends on the lighting environment — which is exactly how real materials work.

A wooden table looks different under a desk lamp vs. sunlight vs. candlelight. PBR captures that automatically.

Here's the rough math behind standard PBR:

1. Split the surface into metallic and dielectric areas (metallic map)
2. For dielectric areas: albedo defines the base color, roughness defines the micro-surface
3. For metallic areas: albedo defines the reflection color (metals have colored reflections), roughness defines the sharpness of reflections
4. The normal map modifies the surface direction at each pixel
5. Combine with the environment lighting using the Cook-Torrance BRDF (Bidirectional Reflectance Distribution Function)

## PBR in Different Engines

### Blender (Principled BSDF)
Blender uses the Principled BSDF shader which combines all PBR maps into a single node. Connect albedo to Base Color, normal to Normal, roughness to Roughness, and metallic to Metallic. See our [Blender PBR texture guide](/blog/pbr-textures-in-blender/).

### Unity (HDRP / URP)
Unity's Lit Shader uses the same PBR model. Set the material to use the metallic-alpha workflow and connect your maps. See our [Unity PBR textures guide](/blog/pbr-textures-in-unity/).

### Unreal Engine
Unreal's Material system is built entirely around PBR. The default Material Expression nodes (TextureSample + scalar parameters) map directly to the PBR model. See our [Unreal PBR textures guide](/blog/pbr-textures-in-unreal/).

## Where to Get Free PBR Textures

[FreePBRTextures](/) offers 4K seamless PBR texture sets — including albedo, normal, roughness, and metallic maps — under the CC0 license. Free for any use, including commercial projects. Browse our full [PBR texture collection](/textures/) to get started.

## Advanced Reading

- [PBR Workflow Explained](/blog/pbr-workflow-explained/) — a deeper dive into the production pipeline
- [Roughness vs Glossiness](/blog/roughness-vs-glossiness/) — the two PBR conventions explained
- [Normal Map vs Height Map](/blog/normal-map-vs-height-map/) — when to use each
