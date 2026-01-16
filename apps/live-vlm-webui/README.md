# Live VLM WebUI

Real-time Vision Language Model (VLM) interaction with webcam streaming.

This app is based on the DGX Spark playbook: `anya-doc/refs/dgx-spark-playbooks/nvidia/live-vlm-webui/`.

Note: this AppStore entry is for distribution + metadata only. The current Anya UI does not implement install/start/stop for host apps yet.

## Verify

- Open `https://<host>:${PANEL_APP_PORT_HTTPS}` in a browser.
- You must use HTTPS for webcam access; accept the self-signed certificate warning on first visit.

## Rollback

- `pip uninstall live-vlm-webui`

