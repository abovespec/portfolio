---
title: "PBR Workflow Explained: From Texture to Final Render"
description: "A complete walkthrough of the PBR material workflow — creating textures, setting up materials in Blender/Unity/Unreal, and best practices for realistic rendering."
publishDate: 2026-04-24
author: "Editorial Team"
tags: ["PBR workflow", "3D texturing", "material creation", "game dev", "archviz"]
draft: false
---

The PBR (Physically Based Rendering) workflow is the modern standard for 3D materials. It replaces the old "diffuse + specular + manually painted lighting" approach with a unified, physics-based system that looks correct under any lighting.

This guide walks through the complete PBR workflow — from understanding the texture maps to applying them in your 3D software.

For more on this topic, see [*How to Use PBR Textures in Unity: A Practical Guide*](/blog/pbr-textures-in-unity).

---

## Step 1: Understand the Map Types

Before you start texturing, you need to understand what each PBR map does and how they interact:

### Albedo (Base Color)
The surface color under white light. No lighting or shadow information.

### Normal Map
Surface detail encoded as RGB direction vectors. Creates the illusion of depth.

### Roughness Map
Controls micro-surface smoothness. Black = mirror, White = matte.

### Metallic Map
Separates metal from non-metal. Black = dielectric, White = conductor.

### Ambient Occlusion (Optional)
Pre-calculated shadowing in crevices and corners.

[Learn more about each map type in our PBR textures guide](/blog/what-is-pbr-texture/).

## Step 2: Source or Create Your Textures

You need each PBR map for your material. Sources:

- **Download full PBR sets** — [FreePBRTextures](/textures/) offers complete 4K PBR sets with albedo, normal, roughness, and metallic maps
- **Generate procedurally** — tools like Substance Designer or procedural generators
- **Generate with AI** — modern models like ERNIE-Image can create photorealistic textures from prompts
- **Convert photos** — using tools like Materialize or Photoshop to extract PBR maps from source images

## Step 3: Set Up Your Material

The setup differs per engine, but the logic is the same everywhere:

### In Blender (Principled BSDF)

1. Select your object and create a new material
2. Add the Principled BSDF shader (it's the default)
3. Connect your textures:
   - Albedo → Base Color
   - Normal Map → Normal (with a Normal Map node in between)
   - Roughness → Roughness
   - Metallic → Metallic
4. Set Color Space:
   - Albedo: sRGB
   - Normal: Non-Color
   - Roughness: Non-Color
   - Metallic: Non-Color

> **Pro tip:** In Blender 4.0+, you can drag and drop image textures directly into the shader editor — it automatically creates the Image Texture nodes and connects them.

### In Unity (Built-in RP or URP)

1. Import your textures into the Assets folder
2. Set texture import settings:
   - Albedo: sRGB
   - Normal: Texture Type = Normal Map
   - Roughness + Metallic: sRGB = off
3. Create a new Material
4. Select the Lit or Universal Render Pipeline/Lit shader
5. Assign maps to their slots

### In Unreal Engine 5

1. Import textures into the Content Browser
2. Create a Material
3. Add Texture Sample nodes for each map
4. Connect them:
   - Albedo → Base Color
   - Normal → Normal Map (with a ConstantBiasScale to remap from [0,1] to [-1,1])
   - Roughness → Roughness
   - Metallic → Metallic
5. Unreal handles the normal map decompression automatically when you set the texture to Normal Map type

## Step 4: Common PBR Pitfalls

### Wrong Color Space
This is the #1 mistake. Albedo maps should be sRGB. Normal, roughness, metallic, and height maps should be set to Non-Color/Linear. If they're wrong, your material will look washed out or glitchy.

### Normal Map Strength
Too much normal strength creates unnatural "crater" effects. Start with 1.0 and adjust based on the depth of detail. Our textures use a default strength of 2.0, which works well for most surfaces.

### Metallic Edges
Pure black/white metallic maps create harsh transitions. If your material has both metal and non-metal areas (like a rusty bolt), use a soft gradient at the transition.

### Roughness + Metallic Confusion
Metals have colored reflections (from the albedo) and no diffuse color. Non-metals have white reflections and colored diffuse. This is why mixing them up looks wrong.

## Step 5: Preview and Iterate

Always preview your material under different lighting conditions. PBR should look good in:

- Bright direct sunlight
- Diffuse overcast lighting
- Dark indoor scenes with point lights
- Dynamic time-of-day lighting (in games)

If it looks good everywhere, your PBR setup is correct.

---

## Ready-Made PBR Textures

Skip the setup and download complete 4K PBR texture sets from [FreePBRTextures](/textures/). All textures include albedo, normal, and roughness maps — ready to drop into your project. Browse categories:

For more on this topic, see [*How to Use PBR Textures in Blender: Complete Setup Guide*](/blog/pbr-textures-in-blender).

- [Seamless Wood Textures](/textures/wood/)
- [Stone & Rock Textures](/textures/stone/)
- [Brick & Masonry Textures](/textures/brick/)
- [Concrete Textures](/textures/concrete/)
- [Metal Textures](/textures/metal/)
