/**
 * Bridge Producer
 * 
 * Creates signed bundles for secure transfer across trust boundaries.
 */

import { createHmac, createHash } from 'crypto';
import { writeFileSync, mkdirSync } from 'fs';
import { join } from 'path';
import { v4 as uuidv4 } from 'uuid';

interface Bundle {
  bundleId: string;
  createdAt: string;
  producer: string;
  payload: Record<string, unknown>;
  signature: string;
  checksum: string;
}

const SECRET_KEY = process.env.BRIDGE_SECRET || 'demo-secret-key';
const STAGING_DIR = process.env.STAGING_DIR || '../../staging';
const PRODUCER_ID = process.env.PRODUCER_ID || 'ts-producer-001';

function computeChecksum(data: string): string {
  return createHash('sha256').update(data).digest('hex');
}

function signPayload(payload: string): string {
  return createHmac('sha256', SECRET_KEY).update(payload).digest('base64');
}

function createBundle(payload: Record<string, unknown>): Bundle {
  const payloadStr = JSON.stringify(payload);
  
  return {
    bundleId: uuidv4(),
    createdAt: new Date().toISOString(),
    producer: PRODUCER_ID,
    payload,
    signature: signPayload(payloadStr),
    checksum: computeChecksum(payloadStr),
  };
}

function saveBundle(bundle: Bundle): string {
  const filename = `bundle-${bundle.bundleId}.json`;
  const filepath = join(STAGING_DIR, filename);
  
  mkdirSync(STAGING_DIR, { recursive: true });
  writeFileSync(filepath, JSON.stringify(bundle, null, 2));
  
  return filepath;
}

// Demo: Create sample bundles
function main() {
  console.log('🔧 Bridge Producer starting...');
  console.log(`   Producer ID: ${PRODUCER_ID}`);
  console.log(`   Staging dir: ${STAGING_DIR}`);
  console.log('');

  const samplePayloads = [
    { type: 'metrics', values: [1, 2, 3, 4, 5], timestamp: Date.now() },
    { type: 'event', name: 'user_action', userId: 'user-123' },
    { type: 'config', settings: { feature_x: true, threshold: 0.75 } },
  ];

  for (const payload of samplePayloads) {
    const bundle = createBundle(payload);
    const path = saveBundle(bundle);
    console.log(`✅ Created: ${path}`);
  }

  console.log('');
  console.log(`📦 ${samplePayloads.length} bundles created`);
}

main();

export { createBundle, saveBundle, computeChecksum, signPayload };
