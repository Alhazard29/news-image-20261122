// news-image-20261122 — "The World Today" front page for 22 November 2026.
// Copies entry.png (rendered by gen_poster.py) to $MAKEFUN_OUTPUT_DIR.
// Stdlib only, no network, deterministic, exit 0 on success, silent on success.

import { readFileSync, writeFileSync, mkdirSync, chmodSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const HERE = dirname(fileURLToPath(import.meta.url));
const OUT_DIR = process.env.MAKEFUN_OUTPUT_DIR;

if (!OUT_DIR) {
  process.stderr.write("MAKEFUN_OUTPUT_DIR is not set\n");
  process.exit(1);
}

const src = join(HERE, "entry.png");
const buf = readFileSync(src);

// Validate PNG magic.
const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (buf.length < 33 || !buf.subarray(0, 8).equals(PNG_MAGIC)) {
  process.stderr.write("entry.png is not a PNG\n");
  process.exit(1);
}

// Validate size and dimensions (IHDR: width at bytes 16-19, height at 20-23).
if (buf.length > 1024 * 1024) {
  process.stderr.write("entry.png exceeds 1 MiB\n");
  process.exit(1);
}
const width = buf.readUInt32BE(16);
const height = buf.readUInt32BE(20);
if (width > 1024 || height > 1024) {
  process.stderr.write("entry.png exceeds 1024x1024\n");
  process.exit(1);
}

mkdirSync(OUT_DIR, { recursive: true });
const out = join(OUT_DIR, "entry.png");
writeFileSync(out, buf);
chmodSync(out, 0o644);
