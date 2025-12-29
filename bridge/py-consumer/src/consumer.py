"""
Bridge Consumer

Validates and processes bundles from the staging directory.
"""

import hashlib
import hmac
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any

from pydantic import BaseModel


class Bundle(BaseModel):
    """Bundle model for validation."""
    bundleId: str
    createdAt: str
    producer: str
    payload: dict[str, Any]
    signature: str
    checksum: str


SECRET_KEY = os.environ.get("BRIDGE_SECRET", "demo-secret-key")
STAGING_DIR = Path(os.environ.get("STAGING_DIR", "../../staging"))
OUTPUT_DIR = Path(os.environ.get("OUTPUT_DIR", "../../output"))


def compute_checksum(data: str) -> str:
    """Compute SHA-256 checksum."""
    return hashlib.sha256(data.encode()).hexdigest()


def verify_signature(payload: str, signature: str) -> bool:
    """Verify HMAC signature."""
    expected = hmac.new(
        SECRET_KEY.encode(),
        payload.encode(),
        hashlib.sha256
    ).digest()
    import base64
    return hmac.compare_digest(base64.b64decode(signature), expected)


def process_bundle(bundle: Bundle) -> dict[str, Any]:
    """Process a validated bundle."""
    return {
        "bundleId": bundle.bundleId,
        "processedAt": datetime.utcnow().isoformat(),
        "payloadType": bundle.payload.get("type", "unknown"),
        "status": "processed"
    }


def consume_bundles():
    """Read, validate, and process all bundles in staging."""
    print("🔍 Bridge Consumer starting...")
    print(f"   Staging dir: {STAGING_DIR}")
    print(f"   Output dir: {OUTPUT_DIR}")
    print("")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    bundle_files = list(STAGING_DIR.glob("bundle-*.json"))
    
    if not bundle_files:
        print("⚠️  No bundles found in staging")
        return

    processed = 0
    failed = 0

    for bundle_file in bundle_files:
        try:
            data = json.loads(bundle_file.read_text())
            bundle = Bundle.model_validate(data)
            
            # Verify checksum
            payload_str = json.dumps(bundle.payload)
            expected_checksum = compute_checksum(payload_str)
            
            if bundle.checksum != expected_checksum:
                print(f"❌ Checksum mismatch: {bundle_file.name}")
                failed += 1
                continue
            
            # Verify signature
            if not verify_signature(payload_str, bundle.signature):
                print(f"❌ Signature invalid: {bundle_file.name}")
                failed += 1
                continue
            
            # Process
            result = process_bundle(bundle)
            output_file = OUTPUT_DIR / f"processed-{bundle.bundleId}.json"
            output_file.write_text(json.dumps(result, indent=2))
            
            print(f"✅ Processed: {bundle_file.name}")
            processed += 1
            
        except Exception as e:
            print(f"❌ Error processing {bundle_file.name}: {e}")
            failed += 1

    print("")
    print(f"📊 Results: {processed} processed, {failed} failed")


if __name__ == "__main__":
    consume_bundles()
