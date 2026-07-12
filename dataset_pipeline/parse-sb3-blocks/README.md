# parse-sb3-blocks

Parse Scratch 3.0 block formats and convert to [scratchblocks](https://github.com/scratchblocks/scratchblocks) text.

## Usage

```bash
node cli.js <project.json> [output.scratchblocks] [locale]
```

- `project.json` — Path to the Scratch 3.0 project.json file
- `output.scratchblocks` — Output file path (default: same name as input with `.scratchblocks` extension)
- `locale` — Locale code, e.g. `en`, `zh_CN` (default: `en`)

### Extract project.json from .sb3

An `.sb3` file is a ZIP archive. To extract `project.json`:

```bash
unzip project.sb3 project.json
node cli.js project.json
```

### Output Format

Scripts are grouped by sprite/stage, separated by markers:

```
~~~ Stage ~~~

when green flag clicked
say [Hello!]

~~~ Sprite1 ~~~

when this sprite clicked
move (10) steps
```

## Building

```bash
npm install
npm run rollup
```

## Credits

- Original library by [apple502j](https://github.com/apple502j)
- [scratchblocks](https://github.com/scratchblocks/scratchblocks) by Tim Radvan (tjvr)
