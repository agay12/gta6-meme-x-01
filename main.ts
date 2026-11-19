// gta6-meme-x-01 — GTA 6 launch-week meme for make.fun (posted on X, entry = the post).
//
// Deterministic packager: no network, no wall clock, reads only files in this
// repository and writes the meme picture plus the X post pointer into the
// grader's output directory.
//
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join, resolve } from "node:path";

const botDir = resolve(process.env.MAKEFUN_BOT_DIR ?? ".");
const outDir = resolve(process.env.MAKEFUN_OUTPUT_DIR ?? "out");

// The entry's deliverable: where the X post lives (filled in after posting).
const post = JSON.parse(readFileSync(join(botDir, "POST.json"), "utf8"));
if (typeof post?.url !== "string" || !post.url.startsWith("https://")) {
  throw new Error("POST.json must be {\"url\": \"https://x.com/<handle>/status/<id>\"}");
}

// The meme itself (rendered by the repository's renderer from assets/):
// Vice-sunset beach scene with make.fun's ghost mascot, a neon make.fun sign,
// and the launch-week joke. Written out byte-for-byte, same bytes every run.
mkdirSync(outDir, { recursive: true });
copyFileSync(join(botDir, "POST.json"), join(outDir, "POST.json"));
writeFileSync(join(outDir, "meme.png"), readFileSync(join(botDir, "assets", "meme.png")));
writeFileSync(join(outDir, "post.txt"), readFileSync(join(botDir, "post.txt")));
