---
title: "How to Use PBR Textures in Unreal Engine"
description: "Complete guide to importing PBR textures, setting up materials, and using them in Unreal Engine 4 and 5."
publishDate: "2026-04-24"
category: "workflow"
heroImage: "/blog/pbr-unreal.png"
draft: false
---

Unreal Engine 4 and 5 have excellent native support for the Metallic/Roughness PBR workflow. If you are new to PBR, check out our [What Is a PBR Texture](/blog/what-is-pbr-texture/) guide first. For other engines, see our [Blender](/blog/pbr-textures-in-blender/) and [Unity](/blog/pbr-textures-in-unity/) guides.

## Unreal Engine PBR Material Channels

Unreal uses a node-based material editor. Here is how our texture maps connect to Unreal material channels:

| Texture Map | Unreal Material Channel |
|---|---|
| Albedo / Base Color | Base Color |
| Normal map | Normal |
| Roughness map | Roughness |
| Metallic map | Metallic |
| Ambient Occlusion | Ambient Occlusion (multiplied with Lighting) |
| Emission map | Emissive Color |

## Step-by-Step Setup

### 1. Import Your Textures

Right-click in the Content Browser and select **Import to /Game/**. Select all your texture files for one material (albedo, normal, roughness, metallic, AO).

Before importing, configure the settings:

- **sRGB**: Enable for the albedo/base color texture. Disable for all data maps (normal, roughness, metallic, AO).
- **Mip Gen Settings**: Use **From Image Settings** or **No Mipmaps** for small textures. Leave default for larger textures.
- **Compression Settings**: Use **Default** for most textures. For data maps like roughness, you can set Compression Settings to **Utility - No Mipmaps** to preserve accuracy.

### 2. Create a Material

Right-click in the Content Browser and select **Material**. Name it something like `M_wood_floor`. Double-click to open the Material Editor.

### 3. Build the Material Graph

Add Texture Sample nodes for each of your maps and connect them:

- **Texture Sample (Albedo)** -> **Base Color**
- **Texture Sample (Normal)** -> **Normal** (set Coordinate Space to Tangent)
- **Texture Sample (Roughness)** -> **Roughness** (use the G or R channel depending on how the map is stored -- most standalone roughness maps use the full RGB equally)
- **Texture Sample (Metallic)** -> **Metallic** (same as roughness -- use the brightest channel)
- **Texture Sample (AO)** -> multiply with **Scene Texture Sample (AO)** or directly into the material for baked lighting

For roughness and metallic maps that are stored as grayscale, all RGB channels contain the same data. You can use any single channel (R, G, or B) or take the average.

### 4. Apply to a Mesh

Drag your material onto any Static Mesh or Actor in the viewport. The material will update in real time.

## Unreal Engine 5 Specifics

### Virtual Texturing (Virtual Textures)

UE5 supports Virtual Texturing for high-resolution textures without the memory overhead. If you are using very large texture sets (4K+), consider setting up a Virtual Texture material instead:

1. Create a **Virtual Texture Material** instead of a regular material.
2. Import your textures as **Virtual Texture** type.
3. Use the **VTM Tile Generator** to create virtual texture tiles.

### Nanite

If your meshes are Nanite-compatible, you can use much higher-poly geometry without performance cost. Nanite also supports virtual texturing out of the box, so your 4K PBR textures work seamlessly.

## Material Instances

Instead of creating a full material for every variation, create one **parent material** and use **Material Instances** for color or roughness variations:

1. Right-click your material and select **Create Material Instance**.
2. Parameterize the values you want to vary (Base Color tint, roughness, etc.) in the parent material using Material Parameters.
3. Adjust those parameters in the instance without rebuilding the shader.

## Common Issues

- **Normal map looks inverted or wrong**: Check that the normal map texture has the correct coordinate space (Tangent is standard for most PBR textures). Also verify the Y-up vs Z-up convention -- most PBR tools use DirectX (Y-up) format. If normals look flipped, negate the Y channel in the material graph. See [Normal Map vs Height Map](/blog/normal-map-vs-height-map/) for more detail.
- **Roughness values seem backwards**: Unlike Unity, Unreal uses roughness directly (white = rough, black = smooth). No inversion needed if you are using roughness maps. Read our [Roughness vs Glossiness](/blog/roughness-vs-glossiness/) guide to understand the difference.
- **Textures look pixelated at close range**: Increase the texture resolution or adjust the LOD settings on your material.
- **Colors look wrong in Lumen**: Make sure your project is using the Linear color space and that your albedo texture has sRGB enabled.

## Summary

Unreal Engine makes PBR material setup straightforward with its node-based material editor. The key things to remember are disabling sRGB on data maps, using the correct coordinate space for normal maps, and leveraging material instances for efficient variation.
