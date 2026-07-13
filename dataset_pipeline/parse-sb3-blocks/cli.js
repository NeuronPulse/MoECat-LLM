#!/usr/bin/env node

import { readFileSync, writeFileSync, readdirSync, existsSync, statSync } from 'fs';
import { join } from 'path';

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

let toScratchblocks;

async function loadModule() {
    const mod = await import('./dist/parse-sb3-blocks.module.js');
    toScratchblocks = mod.toScratchblocks;
}

async function extractProjectJsonFromSb3(sb3Path) {
    const { default: AdmZip } = await import('adm-zip');
    const zip = new AdmZip(sb3Path);
    const entry = zip.getEntry('project.json');
    if (!entry) throw new Error('No project.json found in sb3');
    return JSON.parse(entry.getData().toString('utf-8'));
}

async function convertSingle(inputPath, outputPath, locale = 'en') {
    let projectData;
    try {
        const raw = readFileSync(inputPath, 'utf-8');
        projectData = JSON.parse(raw);
    } catch (e) {
        if (inputPath.endsWith('.sb3')) {
            projectData = await extractProjectJsonFromSb3(inputPath);
        } else {
            throw e;
        }
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
    return result;
}

async function scanFolder(folderPath, locale = 'en') {
    if (!existsSync(folderPath)) {
        console.error(`Folder not found: ${folderPath}`);
        process.exit(1);
    }

    const entries = readdirSync(folderPath);
    let converted = 0;
    let skipped = 0;

    for (const entry of entries) {
        const entryPath = join(folderPath, entry);
        if (!statSync(entryPath).isDirectory() || !entry.match(/^\d+$/)) continue;

        const sb3Path = join(entryPath, 'project.sb3');
        const outputPath = join(entryPath, 'project.scratchblocks');

        if (!existsSync(sb3Path)) {
            skipped++;
            continue;
        }

        if (existsSync(outputPath)) {
            skipped++;
            continue;
        }

        try {
            await convertSingle(sb3Path, outputPath, locale);
            converted++;
            console.log(`[OK] ${entry}`);
        } catch (e) {
            console.error(`[FAIL] ${entry}: ${e.message}`);
            skipped++;
        }
    }

    console.log(`\nDone. Converted: ${converted}, Skipped: ${skipped}`);
}

await loadModule();

const args = process.argv.slice(2);
if (args.length < 1) {
    console.error('Usage:');
    console.error('  node cli.js <input.json|input.sb3> [output.scratchblocks] [locale]');
    console.error('  node cli.js --scan <folder> [locale]');
    process.exit(1);
}

if (args[0] === '--scan') {
    const folder = args[1];
    const locale = args[2] || 'en';
    await scanFolder(folder, locale);
} else {
    const inputPath = args[0];
    const outputPath = args[1] || inputPath.replace(/\.(json|sb3)$/, '.scratchblocks');
    const locale = args[2] || 'en';
    await convertSingle(inputPath, outputPath, locale);
    console.log(`Done! Output: ${outputPath}`);
}
