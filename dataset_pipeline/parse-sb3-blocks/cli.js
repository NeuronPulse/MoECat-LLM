#!/usr/bin/env node

import { readFileSync, writeFileSync } from 'fs';
import { toScratchblocks } from './dist/parse-sb3-blocks.cjs';

const HAT_BLOCKS = [
    'event_whenflagclicked',
    'event_whenkeypressed',
    'event_whengreaterthan',
    'event_whenthisspriteclicked',
    'event_whenstageclicked',
    'event_whenbackdropswitchesto',
    'event_whenbroadcastreceived',
    'control_start_as_clone',
    'procedures_definition',
    'boost_whenColor',
    'boost_whenTilted',
    'ev3_whenButtonPressed',
    'ev3_whenDistanceLessThan',
    'ev3_whenBrightnessLessThan',
    'gdxfor_whenGesture',
    'gdxfor_whenForcePushedOrPulled',
    'gdxfor_whenTilted',
    'makeymakey_whenMakeyKeyPressed',
    'makeymakey_whenCodePressed',
    'microbit_whenButtonPressed',
    'microbit_whenGesture',
    'microbit_whenTilted',
    'microbit_whenPinConnected',
    'wedo2_whenDistance',
    'wedo2_whenTilted',
];

const args = process.argv.slice(2);
if (args.length < 1) {
    console.error('Usage: node cli.js <project.json> [output.scratchblocks] [locale]');
    process.exit(1);
}

const inputPath = args[0];
const outputPath = args[1] || inputPath.replace(/\.json$/, '.scratchblocks');
const locale = args[2] || 'en';

let projectData;
try {
    projectData = JSON.parse(readFileSync(inputPath, 'utf-8'));
} catch (e) {
    console.error(`Failed to read or parse ${inputPath}: ${e.message}`);
    process.exit(1);
}

const opts = { tab: ' '.repeat(4), variableStyle: 'as-needed' };
const sections = [];

for (const target of projectData.targets) {
    const targetName = target.isStage ? 'Stage' : target.name;
    const blocks = target.blocks;
    if (!blocks) continue;

    const hatBlockIds = Object.keys(blocks).filter(key => {
        const block = blocks[key];
        return block.topLevel && HAT_BLOCKS.includes(block.opcode);
    });

    if (hatBlockIds.length === 0) continue;

    const scripts = hatBlockIds
        .map(id => toScratchblocks(id, blocks, locale, opts))
        .filter(s => s.length > 0);

    if (scripts.length === 0) continue;

    sections.push(`~~~ ${targetName} ~~~\n\n${scripts.join('\n\n')}`);
}

const result = sections.join('\n\n');
writeFileSync(outputPath, result, 'utf-8');
console.log(`Done! Output: ${outputPath}`);
