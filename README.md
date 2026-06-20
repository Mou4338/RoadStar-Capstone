# RoadStar Cars Dealership

RoadStar is a responsive full-stack dealership capstone application. Visitors can browse and filter nationwide dealers, inspect dealer reviews, create an account, sign in, and submit a sentiment-tagged review. The project includes authentication, admin pages, JSON APIs, container and Kubernetes manifests, and a GitHub Actions CI workflow.

## Run locally

```bash
python server.py
```

Open `http://127.0.0.1:8000`. Demo accounts: `demo / Demo123!` and `root / root123`.

## Structure

- `server.py` — self-contained application server and JSON APIs
- `server/frontend/static/` — About and Contact pages plus styling
- `server/frontend/src/components/Register/Register.jsx` — React registration component
- `.github/workflows/ci.yml` — CI validation
- `Dockerfile` and `kubernetes/deployment.yaml` — deployment assets
- `evidence/` — terminal outputs and submission-ready evidence
- `screenshots/` — rubric-named screenshots

## API endpoints

`/djangoapp/get_dealers`, `/djangoapp/get_dealers?state=KS`, `/djangoapp/dealer/1`, `/djangoapp/reviews/dealer/1`, `/djangoapp/get_cars`, `/djangoapp/analyze/Fantastic%20services`

