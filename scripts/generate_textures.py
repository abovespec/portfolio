#!/usr/bin/env python3
"""
Procedural PBR texture generator for FreePBRTextures.
Generates seamless tileable textures using periodic noise functions.
Usage:
    python generate_textures.py --category wood --count 3 --seed oak-warm --output ./public/textures
    python generate_textures.py --generate-all --output ./public/textures
Requires: pip install numpy Pillow scipy
"""

import argparse
import json
import os
import time
import hashlib
import numpy as np
from PIL import Image
from scipy import ndimage


class PeriodicNoise:
    """Perlin-like noise with periodic boundaries for seamless tiling."""

    def __init__(self, seed=42, period=128):
        self.period = period
        rng = np.random.RandomState(seed)
        perm_size = period + 2
        self.perm_x = np.sort(rng.randint(0, 256, perm_size)) % 256
        self.perm_y = np.sort(rng.randint(0, 256, perm_size)) % 256

    def fade(self, t):
        return t * t * t * (t * (t * 6 - 15) + 10)

    def grad(self, hash_val, x, y):
        """Vectorized gradient function for numpy arrays."""
        h = np.asarray(hash_val) % 4
        dx = np.where(h < 2, x, -x)
        dy = np.where(h % 2 == 0, y, -y)
        return dx + dy

    def generate(self, shape=(4096, 4096), scale=128.0):
        """Generate periodic noise, returning array of exactly `shape`."""
        # Create grid at full resolution
        y, x = np.mgrid[0:shape[0]:float(shape[0]), 0:shape[1]:float(shape[1])]

        # Wrap to period for lookup
        xf = x % 1.0
        yf = y % 1.0
        px = (x // 1.0 % self.period).astype(int) % (self.period + 1)
        py = (y // 1.0 % self.period).astype(int) % (self.period + 1)
        px1 = (px + 1) % (self.period + 1)
        py1 = (py + 1) % (self.period + 1)

        # Scale coordinates for smoother noise
        x_scaled = x / scale
        y_scaled = y / scale
        xf = x_scaled - x_scaled.astype(int)
        yf = y_scaled - y_scaled.astype(int)
        px = (x_scaled // 1.0 % self.period).astype(int) % (self.period + 1)
        py = (y_scaled // 1.0 % self.period).astype(int) % (self.period + 1)
        px1 = (px + 1) % (self.period + 1)
        py1 = (py + 1) % (self.period + 1)

        ux = self.fade(xf)
        uy = self.fade(yf)
        h00 = self.grad((self.perm_x[px] + self.perm_y[py]) % 256, xf, yf)
        h10 = self.grad((self.perm_x[px1] + self.perm_y[py]) % 256, xf - 1, yf)
        h01 = self.grad((self.perm_x[px] + self.perm_y[py1]) % 256, xf, yf - 1)
        h11 = self.grad((self.perm_x[px1] + self.perm_y[py1]) % 256, xf - 1, yf - 1)
        x0 = h00 * (1 - ux) + h10 * ux
        x1 = h01 * (1 - ux) + h11 * ux
        result = x0 * (1 - uy) + x1 * uy
        result = (result - result.min()) / (result.max() - result.min() + 1e-8)
        return result


def fbm(noise_gen, octaves=6, lacunarity=2.0, gain=0.5, shape=(4096, 4096), scale=128.0):
    result = np.zeros(shape, dtype=np.float64)
    amplitude = 1.0
    current_scale = scale
    for _ in range(octaves):
        result += amplitude * noise_gen.generate(shape, current_scale)
        amplitude *= gain
        current_scale /= lacunarity
    result = (result - result.min()) / (result.max() - result.min() + 1e-8)
    return result


def worley_noise(shape=(4096, 4096), scale=64, seed=42):
    rng = np.random.RandomState(seed)
    grid_size = max(int(scale), 4)
    points = rng.rand(grid_size, grid_size, 2)
    # Full-resolution grid
    y, x = np.mgrid[0:shape[0]:float(shape[0]), 0:shape[1]:float(shape[1])]
    gy = (y % grid_size).astype(np.float64)
    gx = (x % grid_size).astype(np.float64)
    result = np.ones_like(x) * 10.0
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            cy = ((gy + dy) % grid_size).astype(int)
            cx = ((gx + dx) % grid_size).astype(int)
            py = points[cy, cx, 0] * grid_size + dy * grid_size - gy
            px = points[cy, cx, 1] * grid_size + dx * grid_size - gx
            d2 = (px ** 2 + py ** 2)
            result = np.minimum(result, d2)
    result = (result - result.min()) / (result.max() - result.min() + 1e-8)
    return result


def generate_wood(seed=42, shape=(4096, 4096)):
    noise1 = PeriodicNoise(seed=seed)
    noise2 = PeriodicNoise(seed=seed + 1)
    noise3 = PeriodicNoise(seed=seed + 2)
    base = fbm(noise1, octaves=6, scale=256, shape=shape)
    rings = fbm(noise2, octaves=4, scale=512, shape=shape)
    y, x = np.mgrid[0:shape[0], 0:shape[1]]
    wave = np.sin(y / shape[0] * np.pi * 8 + rings * 4) * 0.1
    height = base * 0.6 + rings * 0.3 + np.abs(wave) * 0.1
    height = (height - height.min()) / (height.max() - height.min() + 1e-8)
    variation = fbm(noise3, octaves=3, scale=128, shape=shape)
    r = np.clip((0.5 + height * 0.3 + variation * 0.1), 0, 1)
    g = np.clip((0.3 + height * 0.2 + variation * 0.08), 0, 1)
    b = np.clip((0.15 + height * 0.1 + variation * 0.05), 0, 1)
    albedo = np.stack([r, g, b], axis=-1)
    return height, albedo, {'roughness': 0.7, 'metallic': 0.0}


def generate_stone(seed=42, shape=(4096, 4096)):
    noise1 = PeriodicNoise(seed=seed)
    noise2 = PeriodicNoise(seed=seed + 1)
    noise3 = PeriodicNoise(seed=seed + 2)
    base = fbm(noise1, octaves=6, scale=128, shape=shape)
    detail = fbm(noise2, octaves=4, scale=64, shape=shape)
    height = base * 0.7 + detail * 0.3
    height = (height - height.min()) / (height.max() - height.min() + 1e-8)
    color_var = fbm(noise3, octaves=3, scale=96, shape=shape)
    base_color = 0.35 + color_var * 0.2
    albedo = np.stack([np.clip(base_color + 0.02, 0, 1),
                       np.clip(base_color, 0, 1),
                       np.clip(base_color - 0.02, 0, 1)], axis=-1)
    return height, albedo, {'roughness': 0.8, 'metallic': 0.0}


def generate_concrete(seed=42, shape=(4096, 4096)):
    noise1 = PeriodicNoise(seed=seed)
    noise2 = PeriodicNoise(seed=seed + 1)
    base = fbm(noise1, octaves=5, scale=192, shape=shape)
    grain = worley_noise(shape, scale=96, seed=seed + 2)
    height = base * 0.8 + grain * 0.2
    height = ndimage.gaussian_filter(height, sigma=1.0)
    height = (height - height.min()) / (height.max() - height.min() + 1e-8)
    base_color = 0.5 + base * 0.1
    albedo = np.stack([np.clip(base_color + 0.01, 0, 1),
                       np.clip(base_color, 0, 1),
                       np.clip(base_color - 0.01, 0, 1)], axis=-1)
    return height, albedo, {'roughness': 0.75, 'metallic': 0.0}


def generate_metal(seed=42, shape=(4096, 4096)):
    noise1 = PeriodicNoise(seed=seed)
    noise2 = PeriodicNoise(seed=seed + 1)
    y, x = np.mgrid[0:shape[0], 0:shape[1]]
    directional = np.sin(x / shape[1] * np.pi * 100) * 0.3
    base = fbm(noise1, octaves=4, scale=64, shape=shape)
    scratches = fbm(noise2, octaves=6, scale=32, shape=shape)
    height = directional + base * 0.3 + scratches * 0.2
    height = (height - height.min()) / (height.max() - height.min() + 1e-8)
    base_color = 0.6 + base * 0.15
    albedo = np.stack([np.clip(base_color - 0.02, 0, 1),
                       np.clip(base_color - 0.01, 0, 1),
                       np.clip(base_color + 0.02, 0, 1)], axis=-1)
    return height, albedo, {'roughness': 0.3, 'metallic': 1.0}


def generate_fabric(seed=42, shape=(4096, 4096)):
    noise1 = PeriodicNoise(seed=seed)
    noise2 = PeriodicNoise(seed=seed + 1)
    y, x = np.mgrid[0:shape[0], 0:shape[1]]
    weave_x = np.abs(np.sin(x / shape[1] * np.pi * 80))
    weave_y = np.abs(np.sin(y / shape[0] * np.pi * 80))
    weave = weave_x * weave_y
    noise = fbm(noise1, octaves=4, scale=48, shape=shape)
    height = weave * 0.5 + noise * 0.5
    height = (height - height.min()) / (height.max() - height.min() + 1e-8)
    color_noise = fbm(noise2, octaves=3, scale=96, shape=shape)
    base = 0.7 + color_noise * 0.15
    albedo = np.stack([np.clip(base + 0.02, 0, 1),
                       np.clip(base, 0, 1),
                       np.clip(base - 0.03, 0, 1)], axis=-1)
    return height, albedo, {'roughness': 0.9, 'metallic': 0.0}


def generate_brick(seed=42, shape=(4096, 4096)):
    noise1 = PeriodicNoise(seed=seed)
    noise2 = PeriodicNoise(seed=seed + 1)
    y, x = np.mgrid[0:shape[0], 0:shape[1]]
    brick_h, brick_w, mortar = 40, 80, 4
    row = (y // brick_h) % 2
    offset = (row * brick_w // 2) % brick_w
    brick_x = ((x + offset) % brick_w)
    brick_y = y % brick_h
    is_mortar = (brick_x < mortar) | (brick_y < mortar)
    noise = fbm(noise1, octaves=4, scale=64, shape=shape)
    mortar_noise = fbm(noise2, octaves=3, scale=48, shape=shape)
    height = np.where(is_mortar, mortar_noise * 0.5, noise * 0.8)
    height = (height - height.min()) / (height.max() - height.min() + 1e-8)
    brick_color = 0.5 + noise * 0.15
    mortar_color = 0.6 + mortar_noise * 0.05
    base = np.where(is_mortar, mortar_color, brick_color)
    albedo = np.stack([np.clip(base + 0.15, 0, 1),
                       np.clip(base - 0.1, 0, 1),
                       np.clip(base - 0.2, 0, 1)], axis=-1)
    return height, albedo, {'roughness': 0.85, 'metallic': 0.0}


def generate_marble(seed=42, shape=(4096, 4096)):
    noise1 = PeriodicNoise(seed=seed)
    noise2 = PeriodicNoise(seed=seed + 1)
    noise3 = PeriodicNoise(seed=seed + 2)
    warp_x = fbm(noise1, octaves=3, scale=256, shape=shape)
    warp_y = fbm(noise2, octaves=3, scale=256, shape=shape)
    base = fbm(noise3, octaves=5, scale=128, shape=shape)
    veins = np.abs(warp_x * 2 - 1)
    veins = (veins - veins.min()) / (veins.max() - veins.min() + 1e-8)
    height = base * 0.6 + veins * 0.4
    height = (height - height.min()) / (height.max() - height.min() + 1e-8)
    base_color = 0.85 + base * 0.1
    albedo = np.stack([np.clip(base_color, 0, 1),
                       np.clip(base_color - 0.01, 0, 1),
                       np.clip(base_color - 0.02, 0, 1)], axis=-1)
    return height, albedo, {'roughness': 0.2, 'metallic': 0.0}


def generate_leather(seed=42, shape=(4096, 4096)):
    noise1 = PeriodicNoise(seed=seed)
    noise2 = PeriodicNoise(seed=seed + 1)
    base = fbm(noise1, octaves=5, scale=96, shape=shape)
    grain = worley_noise(shape, scale=48, seed=seed + 2)
    y, x = np.mgrid[0:shape[0], 0:shape[1]]
    creases = np.abs(np.sin(y / shape[0] * np.pi * 6 + base * 3))
    height = base * 0.4 + grain * 0.3 + creases * 0.3
    height = (height - height.min()) / (height.max() - height.min() + 1e-8)
    color_var = fbm(noise2, octaves=3, scale=128, shape=shape)
    base = 0.35 + color_var * 0.15
    albedo = np.stack([np.clip(base + 0.15, 0, 1),
                       np.clip(base, 0, 1),
                       np.clip(base - 0.1, 0, 1)], axis=-1)
    return height, albedo, {'roughness': 0.65, 'metallic': 0.0}


GENERATORS = {
    'wood': generate_wood, 'stone': generate_stone, 'concrete': generate_concrete,
    'metal': generate_metal, 'fabric': generate_fabric, 'brick': generate_brick,
    'marble': generate_marble, 'leather': generate_leather,
}


def height_to_normal(height, strength=2.0):
    dx = ndimage.sobel(height, axis=1) * strength
    dy = ndimage.sobel(height, axis=0) * strength
    dx = (dx - dx.min()) / (dx.max() - dx.min() + 1e-8)
    dy = (dy - dy.min()) / (dy.max() - dy.min() + 1e-8)
    return np.stack([np.clip(dx * 2 - 1, 0, 1),
                     np.clip(dy * 2 - 1, 0, 1),
                     np.ones_like(dx) * 0.5], axis=-1)


def make_roughness_map(base, roughness_val):
    roughness = base * 0.1 + roughness_val * 0.9
    roughness = np.clip(roughness, 0, 1)
    return np.stack([roughness, roughness, roughness], axis=-1)


def generate_texture(category, seed_name, seed_val, output_base, shape=(4096, 4096)):
    generator = GENERATORS.get(category)
    if not generator:
        print(f"  Unknown category: {category}")
        return None

    print(f"  Generating {category} '{seed_name}' (seed={seed_val})...")
    t0 = time.time()

    height, albedo, params = generator(seed=seed_val, shape=shape)
    normal = height_to_normal(height)
    roughness = make_roughness_map(height, params['roughness'])

    slug = seed_name.lower().replace(' ', '-').replace('_', '-')
    output_dir = os.path.join(output_base, category, slug)
    os.makedirs(output_dir, exist_ok=True)

    Image.fromarray((albedo * 255).astype(np.uint8)).save(os.path.join(output_dir, 'albedo.png'))
    Image.fromarray((normal * 255).astype(np.uint8)).save(os.path.join(output_dir, 'normal.png'))
    Image.fromarray((roughness * 255).astype(np.uint8)).save(os.path.join(output_dir, 'roughness.png'))

    albedo_img = Image.fromarray((albedo * 255).astype(np.uint8))
    albedo_img.resize((1024, 1024), Image.LANCZOS).save(os.path.join(output_dir, 'preview.png'))
    albedo_img.resize((256, 256), Image.LANCZOS).save(os.path.join(output_dir, 'thumbnail.png'))

    elapsed = time.time() - t0
    print(f"  Saved to {output_dir} in {elapsed:.1f}s")

    metadata = {
        'title': slug.replace('-', ' ').title(),
        'description': f'Seamless 4K procedural {category} texture.',
        'category': category,
        'seed': seed_val,
        'seedName': seed_name,
        'params': params,
        'shape': list(shape),
        'generatedDate': time.strftime('%Y-%m-%d'),
    }
    with open(os.path.join(output_dir, 'metadata.json'), 'w') as f:
        json.dump(metadata, f, indent=2)

    return metadata


def main():
    parser = argparse.ArgumentParser(description='Procedural PBR texture generator')
    parser.add_argument('--category', choices=list(GENERATORS.keys()), help='Texture category')
    parser.add_argument('--count', type=int, default=3, help='Number of textures')
    parser.add_argument('--seed', type=str, default=None, help='Seed name prefix')
    parser.add_argument('--generate-all', action='store_true', help='All categories')
    parser.add_argument('--output', required=True, help='Output base directory')
    parser.add_argument('--shape', type=int, nargs=2, default=[4096, 4096], help='Dimensions')

    args = parser.parse_args()
    categories = list(GENERATORS.keys()) if args.generate_all else [args.category]
    if not categories:
        parser.error("Specify --category or --generate-all")

    for category in categories:
        seed_prefix = args.seed or category
        for i in range(args.count):
            seed_name = f"{seed_prefix}-{i+1}"
            seed_val = int(hashlib.md5(seed_name.encode()).hexdigest()[:8], 16)
            generate_texture(category, seed_name, seed_val, args.output, tuple(args.shape))

    print(f"\nDone! Generated textures in {args.output}")


if __name__ == '__main__':
    main()
