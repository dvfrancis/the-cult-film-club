"""
This module sets default environment variables for the application.

Environment variables include:
- Database connection URL
- Secret key for application security
- Email credentials for sending emails
- Cloudinary credentials for media storage

"""

import os

os.environ.setdefault(
    "DATABASE_URL",
    (
        "postgresql://neondb_owner:rASipIC0jQu4@ep-winter-flower-a2o0rro6."
        "eu-central-1.aws.neon.tech/item_yarns_rabid_491916"
    ))

os.environ.setdefault(
    "SECRET_KEY", (
        "q(lrvsx@(^ffg*i$7e5jvq52ls=p$@y-a)w5vzm-a(@qy#(5tz"
    ))

os.environ.setdefault(
    "EMAIL_USER", (
        "dvfrancis@fastmail.com"
    ))

os.environ.setdefault(
    "EMAIL_PASSWORD", (
        "4w898l7c9l5k7m3t"
    ))

os.environ.setdefault(
    "CLOUDINARY_URL", (
        "cloudinary://928529136165633:"
        "My6UYZMSTUZATqazEddc_r1ZAGs@dvzs9gve0"
    ))

os.environ.setdefault(
    "CLOUDINARY_CLOUD_NAME", (
        "dvzs9gve0"
    ))

os.environ.setdefault(
    "CLOUDINARY_API_KEY", (
        "928529136165633"
    ))

os.environ.setdefault(
    "CLOUDINARY_API_SECRET", (
        "My6UYZMSTUZATqazEddc_r1ZAGs"
    ))
