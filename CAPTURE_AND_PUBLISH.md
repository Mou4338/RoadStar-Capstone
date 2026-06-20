# Capture and publish the remaining graded evidence

The local project and Tasks 2, 5, 6, 8–11, and 14–16 evidence are ready. The following items must be produced in the account where you will submit; they cannot be truthfully pre-generated offline.

## Local screenshots (Tasks 12, 13, 17–22)

Run `python server.py`, then capture these pages with the browser address bar visible:

| File name | Page/state |
|---|---|
| `admin_login.png` | Log in at `/admin` with `root / root123`; capture the administration dashboard |
| `admin_logout.png` | Click **Log out**; capture the admin login page |
| `get_dealers.png` | `/` while logged out |
| `get_dealers_loggedin.png` | Log in with `demo / Demo123!`; capture `/` with “Hi, demo” and Review dealer visible |
| `dealersbystate.png` | `/?state=KS` |
| `dealer_id_reviews.png` | `/dealer/1` |
| `dealership_review_submission.png` | `/review/1` with the prefilled review, before submission |
| `added_review.png` | Submit the review and capture `/dealer/1` showing Alex Morgan’s new review |

## GitHub evidence (Tasks 1, 3, 4, 7, 23)

Create a public GitHub repository, push this folder, replace the placeholders in `SUBMISSION.md`, and open the Actions tab. The supplied workflow runs the compile, server, API smoke test, and artifact validation steps. Copy the successful run output into `evidence/CICD.txt`.

## Deployment evidence (Tasks 24–28)

Build the supplied `Dockerfile`, deploy the container to IBM Cloud Code Engine, and save its public URL in `evidence/deploymentURL`. Capture the live application—not localhost—for the four `deployed_*.png` images required by the rubric.

