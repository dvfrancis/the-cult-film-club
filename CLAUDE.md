# The Cult Film Club

Django 5.2 e-commerce site selling cult film releases. Python 3.12, PostgreSQL,
Stripe checkout, S3 and CloudFront media, Amazon SES email, deployed to EC2.

## Commands

All commands assume the virtualenv is active (`source .venv/bin/activate`) or
are prefixed with `.venv/bin/python`.

```bash
.venv/bin/python manage.py runserver
```

```bash
.venv/bin/python manage.py migrate
```

```bash
.venv/bin/python manage.py makemigrations --check --dry-run
```

```bash
.venv/bin/python manage.py test
```

Reinstall dependencies after pulling:

```bash
.venv/bin/python -m pip install -r requirements.txt
```

## Local environment

`settings.py` calls `load_dotenv()` when a `.env` exists in the repo root, so
local config lives in `.env` (gitignored). The README's instructions to use
`env.py` are stale — nothing imports that file.

`SECRET_KEY` and `DATABASE_URL` are required; the rest have defaults or fall
back to empty strings. Stripe keys are absent locally, so checkout does not
work in development. Images do render locally: they come from CloudFront over
public HTTPS, so nothing needs configuring to see them.

### The database URL must use a Unix socket

`settings.py` passes `ssl_require=True` to `dj_database_url`, which always sets
`OPTIONS["sslmode"] = "require"` and overrides any `sslmode` in the URL itself.
The local Homebrew Postgres runs with `ssl = off`, so a TCP host is refused
with *"server does not support SSL, but SSL was required"*. libpq ignores
`sslmode` over a Unix socket, so the host must be left empty:

```
DATABASE_URL=postgres://domfrancis@/the_cult_film_club   # works (socket)
DATABASE_URL=postgres://domfrancis@localhost/the_cult_film_club   # fails
```

The same clause means sqlite is not usable locally either — the `sslmode`
option is passed to any backend.

## Layout

Project package is `the_cult_film_club/`, with apps nested under
`the_cult_film_club/apps/`:

| App | URL prefix | Purpose |
| --- | --- | --- |
| `home` | `/` | Landing page, default `Site` record |
| `releases` | `/releases/` | Films, images, ratings — the catalogue |
| `cart` | `/checkout/` | Orders, discount codes, Stripe webhooks |
| `account` | `/account/` | Profiles, addresses, wishlists |
| `about` | `/about/` | Static content |
| `contact` | `/contact/` | Enquiry form, emails a notification |
| `newsletter` | `/newsletter/` | Signups and unsubscribe tokens |

Authentication is django-allauth at `/accounts/` (email or username login,
mandatory verification). Custom forms live in `apps/account/forms.py`.

The `account` app sets an explicit `label = "the_cult_film_club_account"`, so
its migrations are recorded under that name rather than `account` — relevant
when writing migration dependencies or `makemigrations <app>` commands.

Error handlers render `templates/error_pages/`. Under `DEBUG`, `/test-400/`,
`/test-403/` and `/test-500/` deliberately raise for checking those pages.

## Testing

Every `tests.py` is an untouched stub, so `manage.py test` collects zero tests.
`TESTING.md` records manual and validation testing instead. New automated tests
are worth adding alongside changes, but there is no existing suite to follow.

## Deployment

Merging to `main` triggers `.github/workflows/deploy.yml`, which assumes an
AWS role via OIDC (no stored keys) and runs the `DeployCultfilmclub` SSM
document on the apps instance in `eu-west-2`. That script pulls, installs,
migrates (snapshotting first if the schema changed), restarts and smoke-tests,
rolling back on failure. Deploys are serialised by a concurrency group.

This is no longer on Railway or Heroku, and the README no longer says it is.
`Procfile` was the last leftover from that era and was removed with issue #113;
the systemd unit invokes gunicorn directly with the same WSGI path.

Email goes through SES in production, using the EC2 instance role rather than
stored credentials, and sends from `tcfc@dominicfrancis.co.uk`. With `DEBUG`
on, the console backend prints messages to the terminal instead.

## Media

Images live in the private `the-cult-film-club` S3 bucket and are served
through CloudFront on `media.cultfilmclub.dominicfrancis.co.uk`. The four
CloudFormation stacks that build it are in `infra/`; each template's header
comment carries the command that applies it.

Three prefixes, and the split matters:

| Prefix | Holds | Written by the app |
| --- | --- | --- |
| `releases/` | Release artwork | yes |
| `profiles/` | Profile photographs | yes |
| `site/` | Holding image, placeholder, homepage banners | no |

`infra/media-permissions.yaml` grants the instance role `releases/` and
`profiles/` only, so anything touching `site/` needs admin credentials. That
is deliberate rather than an oversight: `site/` holds the holding image and
the homepage banners, which the application has no reason to overwrite.

No delete permission is granted at all. Deleting a profile photo blanks the
column and leaves the object, which is what the admin's clear tickbox already
did. Combined with bucket versioning, an overwrite is recoverable.

The stored value is the prefix plus the old Cloudinary public id, with no file
extension, so `Content-Type` is set explicitly on upload rather than inferred.

Cloudinary is gone entirely. craftr migrated on 15 August 2026 and the
shared account, cloud name `dvzs9gve0`, was deleted on 20 August along with
its SSM parameters. The `CLOUDINARY_PATH` constants in the applied
migrations stay, because those have to keep working from an empty database.

## Conventions

- Conventional commits — `feat:`, `fix:`, `ci:`, `chore:`, `refactor:`, with a
  lowercase imperative summary.
- One branch per change, named `feat/…`, `fix/…`, `ci/…` or `chore/…`, merged
  into `main` by pull request.
- PEP 8 wrapped at 79 columns. No linter is configured, so match surrounding
  style by hand.
- Non-obvious decisions are explained in comments at the point of the code —
  see the SES and `AWS_SES_AUTO_THROTTLE` notes in `settings.py`. Keep that up.

## Gotchas

- `requirements.txt` is UTF-16 LE with CRLF line endings. pip decodes it fine,
  but git treats it as binary and diffs are unreadable. Preserve the encoding
  when editing, or convert it to UTF-8 as a deliberate standalone change.
- `staticfiles/` is committed. Production uses WhiteNoise's
  `CompressedManifestStaticFilesStorage`, so `collectstatic` must be re-run
  when static assets change.
- `README.md` and `TESTING.md` are ~90KB assessment documents, not developer
  guides. Grep them rather than reading them whole.
