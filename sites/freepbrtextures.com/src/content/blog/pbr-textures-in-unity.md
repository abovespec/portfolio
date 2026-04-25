---
title: "How to Use PBR Textures in Unity: A Practical Guide"
description: "Step-by-step guide to importing and applying PBR textures in Unity using Standard and URP/HDRP materials."
publishDate: "2026-04-24"
category: "workflow"
heroImage: "/blog/pbr-unity.png"
draft: false
---

Unity has excellent built-in support for PBR materials. If you are new to PBR, start with our [What Is a PBR Texture](/blog/what-is-pbr-texture/) guide. For other engines, see our [Blender](/blog/pbr-textures-in-blender/) and [Unreal Engine](/blog/pbr-textures-in-unreal/) guides.

## Unity PBR Material Properties

Unity's Standard Shader (and its URP/HDRP equivalents) uses a **Metallic/Roughness** workflow. Here is how our texture maps map to Unity material properties:

| Texture Map | Unity Slot |
|---|---|
| Albedo / Diffuse / Base Color | Albedo |
| Normal map | Normal Map |
| Roughness map | Smoothness (inverted) |
| Metallic map | Metallic |
| Ambient Occlusion | Occlusion |
| Emission map | Emission |

## Step-by-Step Setup

### 1. Import Your Textures

Drag your texture files into the Unity Project window. Before applying them, check the import settings:

- **Albedo**: Import as Default texture. sRGB (Color) should be checked.
- **Normal map**: Set Texture Type to **Normal map** in the import settings. Disable sRGB.
- **Roughness / Metallic / AO**: Set Texture Type to **Default**. Disable sRGB (Color). These are data maps, not color maps.

### 2. Create a Material

Right-click in the Project window and select **Create > Material**. Name it something like `wood_floor_material`.

### 3. Assign Texture Maps

With the material selected in the Inspector:

- **Albedo**: Drag your albedo/base color texture here.
- **Normal Map**: Drag your normal map here. Adjust the Smoothness slider or use a roughness map in the next step.
- **Smoothness**: Unity uses smoothness by default (inverted roughness). If you have a roughness map, drag it into the Smoothness slot and check the **Use in Smoothness** toggle that appears, or invert the map beforehand.
- **Metallic**: If your texture has a metallic map, assign it here. For non-metal surfaces like wood or stone, leave Metallic at 0.
- **Occlusion**: Assign your AO map here if available.

### 4. Apply to a Mesh

Drag the material onto any GameObject with a Mesh Renderer component. You should see your PBR material applied immediately.

## URP and HDRP Notes

- **URP**: Uses the URP/Lit shader. The workflow is identical to the Standard shader above.
- **HDRP**: Uses the HDRP/Lit shader with additional channels. HDRP supports 8-channel texture packing where you can combine roughness, metallic, AO, and other maps into a single texture file for performance.

## Performance Tips

- Use **texture atlases** to combine multiple small textures into one larger texture and reduce draw calls.
- Set appropriate **Max Size** in import settings. 4K textures are great for hero assets but wasteful for background props -- downscale to 2K or 1K.
- Enable **compression** in the Texture Import Settings. Use DXT5 for textures with alpha and DXT1 for opaque textures.
- Use **Mipmaps** to improve performance at distance and reduce aliasing.

## Common Issues

- **Surface looks too shiny or too matte**: Check whether your roughness map is inverted. Unity's Smoothness slider expects white = smooth, while roughness maps use white = rough. See our [Roughness vs Glossiness](/blog/roughness-vs-glossiness/) guide for more detail on these workflows.
- **Normal map looks wrong**: Make sure the texture import type is set to Normal map and sRGB is disabled. Also check the tangent space vs object space setting -- most PBR normal maps are tangent space. Read more in [Normal Map vs Height Map](/blog/normal-map-vs-height-map/).
- **Colors look washed out**: Ensure your albedo map has sRGB enabled and that your project color space is set correctly (Edit > Project Settings > Player > Active Color Space). We recommend Linear for PBR workflows.

## Summary

Unity's PBR workflow is straightforward once you understand the mapping between texture maps and material slots. The key things to remember are disabling sRGB on data maps, handling the roughness/smoothness inversion, and using appropriate texture resolution for your assets.
