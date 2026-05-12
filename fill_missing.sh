#!/usr/bin/env bash
export PATH="$HOME/.npm-global/bin:$PATH"
OUT_DIR="/Users/paulina/Desktop/seeddance/MCOL_Videos"
MCOL_DIR="/Users/paulina/Desktop/seeddance/MCOL"
PROMPT='Cinematic transition. Scene starts unlit. it should Start at pitch-black night with no artificial light. Transform the video to begin in total darkness. Progressively, one by one, individual architectural and pathway lights click on, outdoor landscape lights power on sequentially from each part of the house across the property, slowly revealing the house until the entire scene matches the original video ending in a fully illuminated, cinematic nighttime exterior.'

submit_wait_download() {
  local NAME="$1"
  local FILE="$2"
  local OUT_FILE="$OUT_DIR/${NAME}.mp4"

  echo "[$NAME] Submitting..."
  JOB_JSON=$(higgsfield generate create seedance_2_0 --prompt "$PROMPT" --start-image "$FILE" --json 2>&1)
  JOB_ID=$(echo "$JOB_JSON" | python3 -c "import sys,json; ids=json.load(sys.stdin); print(ids[0])" 2>/dev/null || true)

  if [[ -z "$JOB_ID" ]]; then
    echo "[$NAME] Submit failed: $JOB_JSON"
    return 1
  fi

  echo "[$NAME] Job ID: $JOB_ID — waiting..."
  RESULT=$(higgsfield generate wait "$JOB_ID" --json --timeout 20m --interval 10s 2>&1)
  VIDEO_URL=$(echo "$RESULT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('result_url',''))" 2>/dev/null || true)

  if [[ -n "$VIDEO_URL" ]]; then
    curl -sL "$VIDEO_URL" -o "$OUT_FILE"
    echo "[$NAME] Saved: $OUT_FILE"
  else
    STATUS=$(echo "$RESULT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('status','?'), d.get('error_message',''))" 2>/dev/null || echo "$RESULT" | head -2)
    echo "[$NAME] No video URL — status: $STATUS"
  fi
  echo ""
}

submit_wait_download "250611 Ryan-20" "$MCOL_DIR/250611 Ryan-20.jpg"
submit_wait_download "250611 Ryan-45" "$MCOL_DIR/250611 Ryan-45.jpg"
submit_wait_download "Hunter-36"      "$MCOL_DIR/Hunter-36.jpg"
submit_wait_download "Hunter-38"      "$MCOL_DIR/Hunter-38.jpg"

echo "Final count: $(ls "$OUT_DIR"/*.mp4 2>/dev/null | wc -l)/25 videos"
