#!/usr/bin/env bash

export PATH="$HOME/.npm-global/bin:$PATH"

OUT_DIR="/Users/paulina/Desktop/seeddance/MCOL_Videos"
MCOL_DIR="/Users/paulina/Desktop/seeddance/MCOL"
TMPDIR_CONV="/tmp/mcol_converted"
PROMPT='Cinematic transition. Scene starts unlit. it should Start at pitch-black night with no artificial light. Transform the video to begin in total darkness. Progressively, one by one, individual architectural and pathway lights click on, outdoor landscape lights power on sequentially from each part of the house across the property, slowly revealing the house until the entire scene matches the original video ending in a fully illuminated, cinematic nighttime exterior.'

mkdir -p "$OUT_DIR" "$TMPDIR_CONV"

wait_and_download() {
  local NAME="$1"
  local JOB_ID="$2"
  local OUT_FILE="$OUT_DIR/${NAME}.mp4"

  if [[ -f "$OUT_FILE" ]]; then
    echo "  -> Already downloaded: $NAME.mp4"
    return 0
  fi

  echo "  -> Waiting for job $JOB_ID ..."
  RESULT=$(higgsfield generate wait "$JOB_ID" --json --timeout 20m --interval 10s 2>&1)
  VIDEO_URL=$(echo "$RESULT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('result_url',''))" 2>/dev/null || true)

  if [[ -z "$VIDEO_URL" ]]; then
    echo "  !! Could not parse result_url for $NAME. Raw:"
    echo "$RESULT" | head -5
    return 1
  fi

  echo "  -> Downloading: $VIDEO_URL"
  curl -sL "$VIDEO_URL" -o "$OUT_FILE"
  echo "  -> Saved: $OUT_FILE"
}

submit_wait_download() {
  local NAME="$1"
  local FILE="$2"
  local EXT="${FILE##*.}"
  local UPLOAD_FILE="$FILE"

  if [[ -f "$OUT_DIR/${NAME}.mp4" ]]; then
    echo "  -> Already done: $NAME.mp4"
    return 0
  fi

  if [[ "$(echo "$EXT" | tr '[:upper:]' '[:lower:]')" == "heic" ]]; then
    UPLOAD_FILE="$TMPDIR_CONV/${NAME}.jpg"
    echo "  -> Converting HEIC..."
    sips -s format jpeg "$FILE" --out "$UPLOAD_FILE" > /dev/null 2>&1
  fi

  echo "  -> Submitting $NAME ..."
  JOB_JSON=$(higgsfield generate create seedance_2_0 \
    --prompt "$PROMPT" \
    --start-image "$UPLOAD_FILE" \
    --json 2>&1)

  JOB_ID=$(echo "$JOB_JSON" | python3 -c "import sys,json; ids=json.load(sys.stdin); print(ids[0])" 2>/dev/null || true)

  if [[ -z "$JOB_ID" ]]; then
    echo "  !! Failed to submit $NAME. Output: $JOB_JSON"
    return 1
  fi

  echo "  -> Job ID: $JOB_ID"
  wait_and_download "$NAME" "$JOB_ID"
}

# ─── PHASE 1: Recover already-submitted jobs ─────────────────────────────────
echo "=== PHASE 1: Recovering already-submitted jobs ==="
echo ""

wait_and_download "231006 LLP-100"       "76c93cab-28e9-4241-bb6b-fbf25c6d5eab"
wait_and_download "231006 LLP-114"       "c9e79090-4a2f-4a47-b313-e98a440dc428"
wait_and_download "2505 Sanfilippo-61"   "7da854cd-043b-470b-bb2a-8d6fb57475cf"
wait_and_download "250611 Ryan-20"       "a21fc0df-66ed-40a8-ac98-b0fd643ff3c6"
wait_and_download "250611 Ryan-43"       "df660e68-51f3-4d94-932b-c58122e6c944"
wait_and_download "250611 Ryan-45"       "3add3799-01b7-4877-9663-daa835b8bf21"
wait_and_download "250611 Ryan-53"       "a10862f1-e0f3-45b3-8f05-16e6d8584eff"
wait_and_download "250619 Keane-5"       "6bfbb196-da1a-42fb-ae5a-b67e3592f2cf"
wait_and_download "Hawks-42"             "42e8f60c-407b-453f-9e65-d22f81fb8cbd"
wait_and_download "Hunter-38"            "972e5b81-fda7-4620-a63a-2c9ae4cb418c"
wait_and_download "Morris-37"            "0706a14c-4dd2-4725-ad4a-b27ff2fa314a"
wait_and_download "Pitta-1"              "654ddc28-c5e9-416e-8fcd-3797a6fa990d"
wait_and_download "Pitta-4"              "d1838496-66b5-4420-aaf1-15ffdf35ba92"
wait_and_download "Pitta-8"             "e9f8bd3c-f65a-41d2-908d-d5a1ce7f694c"
wait_and_download "231006 LLP-137"       "0ad9b990-48a3-484e-b103-19fa74a796b2"

echo ""
echo "=== PHASE 2: Submitting rate-limited images (one at a time) ==="
echo ""

submit_wait_download "250619 Mulholland-21" "$MCOL_DIR/250619 Mulholland-21.jpg"
submit_wait_download "Adams Drone-6"        "$MCOL_DIR/Adams Drone-6.jpg"
submit_wait_download "Hawks-13"             "$MCOL_DIR/Hawks-13.jpg"
submit_wait_download "Hawks-30"             "$MCOL_DIR/Hawks-30.jpg"
submit_wait_download "Hodges-2"             "$MCOL_DIR/Hodges-2.jpg"
submit_wait_download "Hodges-6"             "$MCOL_DIR/Hodges-6.jpg"
submit_wait_download "Hunter-36"            "$MCOL_DIR/Hunter-36.jpg"
submit_wait_download "Pitta-24"             "$MCOL_DIR/Pitta-24.jpg"
submit_wait_download "Morris-42"            "$MCOL_DIR/Morris-42.HEIC"

echo ""
echo "=============================="
echo "ALL DONE. Final video count:"
ls "$OUT_DIR"/*.mp4 2>/dev/null | wc -l
echo ""
ls -lh "$OUT_DIR"
