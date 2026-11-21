# Adding or changing mods

The pack lives in `pack/` and is managed with [packwiz](https://packwiz.infra.link/). Every mod is a small
`.pw.toml` file that points at its download, so pull requests stay tiny and nobody commits jars.

1. Install packwiz (`go install github.com/packwiz/packwiz@latest`, or a binary from its releases).
2. `cd pack`
3. Add a mod for Minecraft **26.3, Fabric**:
   - Modrinth: `packwiz modrinth add <slug-or-url>` (preferred)
   - CurseForge: `packwiz curseforge add <slug-or-url>`
   - Remove: `packwiz remove <name>`; update one: `packwiz update <name>`
4. `packwiz refresh` (the PR check fails if `index.toml` is out of date).
5. Test it: point a Prism instance at your branch's `pack.toml` (see the README) and launch once.
6. Open a pull request saying what the mod adds and that it boots.

Rules of thumb: vanilla-plus, Fabric 26.3 builds only, no duplicate systems (one minimap, one recipe viewer), and
performance mods must be stable releases. Client-only mods get `side = "client"`. Anything that adds content must also
go on the server, so mention it in the PR.

The challenge datapack is generated: edit `tools/gen_datapack.py`, run `python3 tools/gen_datapack.py`, then copy
`datapack/sts_challenge` to `pack/datapacks/` and refresh.
