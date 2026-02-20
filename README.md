# Dania Beach Crowd Checker

Production-ready full-stack app for estimating Dania Beach crowd levels from the public pier webcam stream.

## Stack
- Backend: FastAPI + OpenCV + pHash scene classification + SQLite
- Frontend: Next.js 14 + Recharts + Tailwind
- Deployment: Docker Compose

## Quick start
```bash
docker-compose up --build
```
- Frontend: http://localhost:3000
- Backend docs: http://localhost:8000/docs

## API
- `GET /api/crowd/current`
- `GET /api/crowd/history?hours=12`
- `GET /api/crowd/best-times`
- `GET /api/health`

## Calibration CLI
```bash
python -m calibration.capture_references --duration 120 --output calibration/refs/
python -m calibration.label_scenes --input calibration/refs/
python -m calibration.draw_rois --scenes config/scenes.yaml
python -m calibration.validate --duration 300 --verbose
python -m calibration.export_config --output config/scenes.yaml
```

## Privacy
- Frames are processed in memory only.
- No frame/snapshot endpoints are exposed.
- Only aggregate counts are persisted.

## Deployment
Use a 2vCPU/4GB VM, reverse proxy with TLS, and monitor `/api/health`.
