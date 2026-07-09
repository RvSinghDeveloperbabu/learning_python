# django-app/ — platform system of record  (Weeks 4–5)

**Premise:** the multi-tenant **system of record** for the platform, in Django + DRF. It models who evaluates what and stores every run's results: organizations, users with roles/permissions, projects, eval suites, test cases, model/provider configs, runs, and results. This is my Rails-analog showcase.

**Proves:** senior Django + DRF depth — a clean relational model with migrations, the Django admin configured for ops, a real DRF API (viewsets, nested serializers, pagination, filtering, permissions, throttling), and **ORM performance**: deliberately create then FIX N+1 with `select_related`/`prefetch_related`, plus aggregations/annotations, transactions, and custom managers/querysets.

**Ruby bridge:** Models ≈ ActiveRecord · `manage.py migrate` ≈ `rails db:migrate` · DRF ≈ Grape · Django admin = a free scaffolded ops panel · pytest ≈ RSpec.

**MVP (must-build):**
- domain models + migrations for the entities above
- DRF API with serializers/viewsets, pagination, filtering, permissions, throttling
- Django admin configured for the core models
- an N+1 you can demonstrate and then eliminate, with proof (query counts)
- pytest suite covering permissions + the ORM query behavior

**Stretch:** Celery task to trigger a run; API versioning; custom permission classes.

**I scaffold this myself** (`uv init`, `django-admin startproject`, apps). Mentor guides, doesn't author.

➡️ Full spec: [`../docs/02-real-world-projects.md`](../docs/02-real-world-projects.md) · Curriculum: [`../docs/04-curriculum-weeks-0-4.md`](../docs/04-curriculum-weeks-0-4.md)
