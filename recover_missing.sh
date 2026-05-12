#!/usr/bin/env bash
export PATH="$HOME/.npm-global/bin:$PATH"
OUT_DIR="/Users/paulina/Desktop/seeddance/MCOL_Videos"
MCOL_DIR="/Users/paulina/Desktop/seeddance/MCOL"
PROMPT='Cinematic transition. Scene starts unlit. it should Start at pitch-black night with no artificial light. Transform the video to begin in total darkness. Progressively, one by one, individual architectural and pathway lights click on, outdoor landscape lights power on sequentially from each part of the house across the property, slowly revealing the house until the entire scene matches the original video ending in a fully illuminated, cinematic nighttime exterior.'

wait_and_download() {
  local NAME="$1"
  local JOB_ID="$2"
  local OUT_FILE="$OUT_DIR/${NAME}.mp4"
  echo "Waiting on job $JOB_ID for: $NAME"
  RESULT=$(higgsfield generate wait "$JOB_ID" --json --timeout 20m --interval 10s 2>&1)
  STATUS=$(echo "$RESULT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('status','?'))" 2>/dev/null || echo "parse_error")
  VIDEO_URL=$(echo "$RESULT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('result_url',''))" 2>/dev/null || true)
  echo "  Status: $STATUS"
  if [[ -n "$VIDEO_URL" ]]; then
    curl -sL "$VIDEO_URL" -o "$OUT_FILE"
    echo "  Saved: $OUT_FILE"
  else
    echo "  FAILED — will re-submit"
    return 1
  fi
}

submit_and_download() {
  local NAME="$1"
  local FILE="$2"
  echo "Re-submitting: $NAME"
  JOB_JSON=$(higgsfield generate create seedance_2_0 --prompt "$PROMPT" --start-image "$FILE" --json 2>&1)
  JOB_ID=$(echo "$JOB_JSON" | python3 -c "import sys,json; ids=json.load(sys.stdin); print(ids[0])" 2>/dev/null || true)
  if [[ -z "$JOB_ID" ]]; then
    echo "  Submit failed: $JOB_JSON"
    return 1
  fi
  echo "  Job ID: $JOB_ID"
  wait_and_download "$NAME" "$JOB_ID"
}

# Try existing job IDs first; re-submit if they failed/expired
wait_and_download "231006 LLP-114" "c9e79090-4a2f-4a47-b313-e98a440dc428" \
  || submit_and_download "231006 LLP-114" "$MCOL_DIR/231006 LLP-114.jpg"

wait_and_download "250611 Ryan-20" "a21fc0df-66ed-40a8-ac98-b0fd643ff3c6" \
  || submit_and_download "250611 Ryan-20" "$MCOL_DIR/250611 Ryan-20.jpg"

wait_and_download "250611 Ryan-45" "3add3799-01b7-4877-9663-daa835b8bf21" \
  || submit_and_download "250611 Ryan-45" "$MCOL_DIR/250611 Ryan-45.jpg"

wait_and_download "Hunter-36" "91c0e108-d124-4cb3-8859-66dc22d0de01" \
  || submit_and_download "Hunter-36" "$MCOL_DIR/Hunter-36.jpg"

wait_and_download "Hunter-38" "972e5b81-fda7-4620-a63a-2c9ae4cb418c" \
  || submit_and_download "Hunter-38" "$MCOL_DIR/Hunter-38.jpg"

echo ""
echo "Final count: $(ls "$OUT_DIR"/*.mp4 2>/dev/null | wc -l) videos"
ls -lh "$OUT_DIR"
