"""Build the three fixture repos under exec/fixtures/. Deterministic, offline, stdlib only."""
import os, random, shutil, struct, subprocess, sys, zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent / "fixtures"
FONT_SRC = Path("/System/Library/Fonts/Supplemental/Georgia.ttf")


def write(base: Path, rel: str, data):
    p = base / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(data if isinstance(data, bytes) else data.encode())


def commit(base: Path):
    env = {**os.environ, "GIT_AUTHOR_DATE": "2026-10-01T00:00:00Z", "GIT_COMMITTER_DATE": "2026-10-01T00:00:00Z"}
    for cmd in (["git", "init", "-q", "-b", "main"], ["git", "config", "core.autocrlf", "false"], ["git", "add", "-A"],
                ["git", "-c", "user.name=fixture", "-c", "user.email=fixture@example.invalid",
                 "-c", "core.autocrlf=false", "commit", "-q", "-m", "initial"]):
        subprocess.run(cmd, cwd=base, check=True, env=env)


def fixture_ts(base: Path):
    write(base, "package.json", """{
  "name": "label-kit",
  "version": "1.0.0",
  "private": true,
  "type": "module",
  "scripts": {
    "test": "node --test",
    "typecheck": "tsc --noEmit"
  }
}
""")
    write(base, "tsconfig.json", """{
  "compilerOptions": {
    "target": "es2022",
    "module": "nodenext",
    "moduleResolution": "nodenext",
    "strict": true,
    "strictNullChecks": false,
    "noEmit": true,
    "allowImportingTsExtensions": true,
    "erasableSyntaxOnly": true,
    "types": []
  },
  "include": ["src"]
}
""")
    write(base, "README.md", "# label-kit\n\nSmall label helpers. `npm test` runs the tests (Node 24, no dependencies). `npm run typecheck` runs tsc.\n")
    write(base, ".gitignore", "node_modules/\n")
    write(base, "src/formatLabel.ts", "export function formatLabel(value: string | null) { return value.trim(); }\n")
    write(base, "src/productCard.ts", """import { formatLabel } from "./formatLabel.ts";

export interface Product {
  name: string;
  category: string | null;
}

export function productCardTitle(product: Product): string {
  return `${formatLabel(product.name)} (${formatLabel(product.category)})`;
}
""")
    write(base, "src/invoiceRow.ts", """import { formatLabel } from "./formatLabel.ts";

export function invoiceRow(description: string | null, amount: number): string {
  return `${formatLabel(description)}\\t${amount.toFixed(2)}`;
}
""")
    write(base, "src/index.ts", """export { formatLabel } from "./formatLabel.ts";
export { productCardTitle } from "./productCard.ts";
export { invoiceRow } from "./invoiceRow.ts";
""")
    write(base, "test/formatLabel.test.ts", """import { test } from "node:test";
import assert from "node:assert/strict";
import { formatLabel } from "../src/formatLabel.ts";

test("trims surrounding spaces", () => {
  assert.equal(formatLabel("  Flour  "), "Flour");
});

test("keeps inner spaces", () => {
  assert.equal(formatLabel(" Brown sugar "), "Brown sugar");
});

test("returns an unpadded string unchanged", () => {
  assert.equal(formatLabel("Salt"), "Salt");
});
""")


def fixture_readme(base: Path):
    lines = [
        b"# Widget Kit\r\n",
        b"\r\n",
        b"A tiny toolkit for widgets.\r\n",
        b"\r\n",
        b"## Setup  \n",
        b"\n",
        b"Run npm install in the project root.\r\n",
        b"If that fails, run npm instal again with --verbose.\n",
        b"\n",
        b"```sh\n",
        b"npm installl widget-kit\n",
        b"```\n",
        b"\n",
        b"## Update\r\n",
        b"\r\n",
        b"Use npm install widget-kit@latest to update.\r\n",
        b"\r\n",
        b"Licensed MIT.",
    ]
    data = b"".join(lines)
    assert data.count(b"npm instal") == 4 and data.count(b"npm installl") == 1
    assert data.count(b"npm install") == 3  # 2 real + the installl prefix
    write(base, "README.md", data)


def png(width: int, height: int, seed: int) -> bytes:
    rnd = random.Random(seed)
    rows = bytearray()
    for y in range(height):
        rows.append(0)
        for x in range(width):
            n = rnd.getrandbits(6)
            rows += bytes(((x * 255 // width) ^ n, (y * 255 // height) ^ n, (128 + n) & 255))
    chunk = lambda t, d: struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xFFFFFFFF)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(bytes(rows), 9)) + chunk(b"IEND", b""))


def fixture_site(base: Path):
    write(base, "index.html", """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Costo Bakery Suite - Price every recipe</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="css/style.css">
  <script src="js/vendor.js"></script>
  <script src="js/analytics.js"></script>
</head>
<body>
  <header class="site-header">
    <a class="logo" href="/">Costo</a>
    <nav><a href="/pricing">Pricing</a> <a href="/blog">Blog</a></nav>
  </header>
  <main>
    <section class="hero">
      <img class="hero-image" src="img/hero.png" alt="A baker weighing flour next to a laptop">
      <h1>Know the real cost of every recipe</h1>
      <p>Costo tracks ingredient prices and updates your margins automatically.</p>
      <a id="cta-signup" class="cta" href="/signup">Start free trial</a>
    </section>
    <section class="features">
      <article><img src="img/feature-1.png" alt="Ingredient price list"><h2>Live ingredient prices</h2><p>Update a price once, every recipe follows.</p></article>
      <article><img src="img/feature-2.png" alt="Recipe margin chart"><h2>Margins you can trust</h2><p>See labor and fixed costs in each product.</p></article>
      <article><img src="img/feature-3.png" alt="Price history timeline"><h2>Price history</h2><p>Spot volatile ingredients before they hurt.</p></article>
    </section>
  </main>
  <footer><p>&copy; 2026 Costo</p></footer>
</body>
</html>
""")
    write(base, "css/style.css", """@font-face {
  font-family: "Brand Serif";
  src: url("../fonts/brand-serif.ttf") format("truetype");
}
body { margin: 0; font-family: "Brand Serif", serif; color: #1d2a1f; }
.site-header { display: flex; justify-content: space-between; padding: 16px; }
.hero { padding: 16px; text-align: center; }
.hero-image { width: 100%; }
.hero h1 { font-size: 2rem; }
.cta { display: inline-block; padding: 12px 24px; background: #2f7d32; color: #fff; border-radius: 8px; text-decoration: none; }
.features { display: grid; gap: 16px; padding: 16px; }
.features img { width: 100%; }
""")
    rnd = random.Random(7)
    chunks = ["/* vendor bundle: ui-kit 4.2.0 + polyfills (minified) */\n", "window.VendorKit=(function(){var d=[\n"]
    size = sum(map(len, chunks))
    while size < 800_000:
        s = '"' + "".join(rnd.choice("abcdefghijklmnopqrstuvwxyz0123456789") for _ in range(70)) + '",\n'
        chunks.append(s); size += len(s)
    chunks.append('""];var h=0;for(var i=0;i<d.length;i++){for(var j=0;j<d[i].length;j++){h=(h*31+d[i].charCodeAt(j))|0;}}\n'
                  'document.addEventListener("DOMContentLoaded",function(){document.body.setAttribute("data-vendor","ready");});\n'
                  'return {hash:h,size:d.length};})();\n')
    write(base, "js/vendor.js", "".join(chunks))
    write(base, "js/analytics.js", """/* Marketing analytics tag. Owner: marketing team. */
window.dataLayer = window.dataLayer || [];
window.dataLayer.push({ event: "page_view", page: location.pathname });
document.documentElement.setAttribute("data-analytics", "loaded");
""")
    write(base, "img/hero.png", png(1150, 900, 1))
    for i in (1, 2, 3):
        write(base, f"img/feature-{i}.png", png(600, 400, 10 + i))
    write(base, "fonts/brand-serif.ttf", FONT_SRC.read_bytes())
    write(base, "README.md", "# Marketing site\n\nStatic home page. Serve locally with `python3 -m http.server 8000` and open http://localhost:8000/.\n")


def main():
    for name, build in (("fixture-ts", fixture_ts), ("fixture-readme", fixture_readme), ("fixture-site", fixture_site)):
        base = ROOT / name
        if base.exists():
            shutil.rmtree(base)
        base.mkdir(parents=True)
        build(base)
        commit(base)
        print(name, "built")


if __name__ == "__main__":
    sys.exit(main())
