#!/usr/bin/env bash

export PATH="$HOME/.npm-global/bin:$PATH"

MCOL_DIR="/Users/paulina/Desktop/seeddance/MCOL"
OUT_DIR="/Users/paulina/Desktop/seeddance/MCOL_Videos"
PROMPT='Cinematic transition. Scene starts unlit. it should Start at pitch-black night with no artificial light. Transform the video to begin in total darkness. Progressively, one by one, individual architectural and pathway lights click on, outdoor landscape lights power on sequentially from each part of the house across the property, slowly revealing the house until the entire scene matches the original video ending in a fully illuminated, cinematic nighttime exterior.'

mkdir -p "$OUT_DIR"
TMPDIR_CONV="/tmp/mcol_converted"
mkdir -p "$TMPDIR_CONV"

shopt -s nullglob
FILES=("$MCOL_DIR"/*.jpg "$MCOL_DIR"/*.jpeg "$MCOL_DIR"/*.JPG "$MCOL_DIR"/*.JPEG "$MCOL_DIR"/*.png "$MCOL_DIR"/*.PNG "$MCOL_DIR"/*.HEIC "$MCOL_DIR"/*.heic)

TOTAL=${#FILES[@]}
echo "Found $TOTAL images to process."
echo ""

# Image 1 already submitted as a test — recover it
RECOVERED_JOB="4bd45cd8-7745-473d-9419-83b40df19f2a"
RECOVERED_FILE="${FILES[0]}"
RECOVERED_NAME=$(basename "$RECOVERED_FILE")
RECOVERED_STEM="${RECOVERED_NAME%.*}"

echo "[RECOVER] Downloading already-submitted job for: $RECOVERED_NAME"
RESULT=$(higgsfield generate wait "$RECOVERED_JOB" --json 2>&1)
VIDEO_URL=$(echo "$RESULT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('result_url',''))" 2>/dev/null || true)
if [[ -n "$VIDEO_URL" ]]; then
  curl -sL "$VIDEO_URL" -o "$OUT_DIR/${RECOVERED_STEM}.mp4"
  echo "  -> Saved: $OUT_DIR/${RECOVERED_STEM}.mp4"
else
  echo "  !! Could not recover URL. Raw: $RESULT"
fi
echo ""

# Process remaining images (index 1 onward)
for i in "${!FILES[@]}"; do
  [[ $i -eq 0 ]] && continue  # skip first (already done above)

  FILE="${FILES[$i]}"
  BASENAME=$(basename "$FILE")
  NAME="${BASENAME%.*}"
  EXT="${BASENAME##*.}"
  NUM=$((i + 1))

  echo "[$NUM/$TOTAL] Processing: $BASENAME"

  # Skip if already downloaded
  if [[ -f "$OUT_DIR/${NAME}.mp4" ]]; then
    echo "  -> Already exists, skipping."
    echo ""
    continue
  fi

  # Convert HEIC to JPG for upload
  UPLOAD_FILE="$FILE"
  if [[ "$(echo "$EXT" | tr '[:upper:]' '[:lower:]')" == "heic" ]]; then
    CONVERTED="$TMPDIR_CONV/${NAME}.jpg"
    echo "  -> Converting HEIC to JPG..."
    sips -s format jpeg "$FILE" --out "$CONVERTED" > /dev/null 2>&1
    UPLOAD_FILE="$CONVERTED"
  fi

  echo "  -> Submitting job..."
  JOB_JSON=$(higgsfield generate create seedance_2_0 \
    --prompt "$PROMPT" \
    --start-image "$UPLOAD_FILE" \
    --json 2>&1)

  JOB_ID=$(echo "$JOB_JSON" | python3 -c "import sys,json; ids=json.load(sys.stdin); print(ids[0])" 2>/dev/null || true)

  if [[ -z "$JOB_ID" ]]; then
    echo "  !! Failed to get job ID. Output: $JOB_JSON"
    echo "  -> Skipping."
    echo ""
    continue
  fi

  echo "  -> Job ID: $JOB_ID — waiting for completion..."

  RESULT=$(higgsfield generate wait "$JOB_ID" --json --wait-timeout 20m --wait-interval 10s 2>&1)
  VIDEO_URL=$(echo "$RESULT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('result_url',''))" 2>/dev/null || true)

  if [[ -z "$VIDEO_URL" ]]; then
    echo "  !! Could not parse result_url. Raw output:"
    echo "$RESULT" | head -20
    echo ""
    continue
  fi

  OUT_FILE="$OUT_DIR/${NAME}.mp4"
  echo "  -> Downloading: $VIDEO_URL"
  curl -sL "$VIDEO_URL" -o "$OUT_FILE"
  echo "  -> Saved: $OUT_FILE"
  echo ""
done

echo "=============================="
echo "All done! Videos saved to:"
echo "$OUT_DIR"
echo ""
ls -lh "$OUT_DIR"
