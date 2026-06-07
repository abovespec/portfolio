---
title: "Roughness vs Glossiness: Understanding Surface Finish in PBR"
description: "Learn the difference between roughness and glossiness workflows in physically-based rendering and how they affect your textures."
publishDate: "2026-04-24"
category: "pbr"
heroImage: "/blog/roughness-glossiness.png"
draft: false
---

If you have worked with PBR materials, you have probably noticed that some tools use **roughness** and others use **glossiness**. They are essentially the same information expressed in opposite directions. If you are new to PBR, start with our [What Is a PBR Texture](/blog/what-is-pbr-texture/) guide.

## The Core Concept

Both roughness and glossiness describe how light scatters off a surface at the micro level. The difference is just the scale:

- **Roughness** goes from 0 (perfectly smooth/mirror) to 1 (fully rough/diffuse)
- **Glossiness** goes from 0 (fully rough/diffuse) to 1 (perfectly smooth/mirror)

In other words, **glossiness = 1 - roughness**.

## Why Two Workflows?

The roughness workflow is the modern standard, used by Unity, Unreal Engine 4 and 5, Blender, Substance Painter, and most contemporary tools. The glossiness workflow was used in older engines and software like 3ds Max and early versions of Marmoset.

For more on this topic, see [*How to Use PBR Textures in Unity: A Practical Guide*](/blog/pbr-textures-in-unity).

The reason roughness won is that it maps more naturally to how we think about surfaces. A rough surface has high roughness, which is intuitive.

## Practical Tips

- **Most texture sites use roughness maps** -- the darker the pixel, the smoother the surface. A pure black pixel means mirror-smooth; pure white means fully matte. Our textures on [FreePBRTextures](/) use roughness maps, so you can plug them directly into any modern engine.

- **If a tool expects glossiness**, you can invert the roughness map. In Photoshop: Image > Adjustments > Invert (Ctrl+I). In Blender: add an Invert node to the texture socket. See our [Blender PBR guide](/blog/pbr-textures-in-blender/) for the full setup.

- **Our textures on FreePBRTextures use roughness maps** -- you can plug them directly into Unity, Unreal, Blender, and other modern PBR workflows without conversion.

## Common Mistakes

The most frequent error is accidentally using a glossiness map where roughness is expected (or vice versa). The result is surfaces that look the opposite of intended -- matte areas appear glossy and vice versa. If your material looks wrong, check which workflow your tool expects and whether the map needs inverting.

## Summary

Roughness and glossiness are the same data flipped. Modern PBR uses roughness, so you will see it everywhere. Just remember: dark is smooth, white is rough.
