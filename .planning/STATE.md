# Project State

## Active Task
- **Task**: Fix 500 Internal Server Error caused by SMTP worker timeout on unconfigured email credentials.
- **Status**: RESOLVED (16/16 tests passing)
- **Mode**: [Debug & Fix Mode]

## Root Cause
When `DEBUG=False` in cloud, `EMAIL_BACKEND` previously defaulted to `smtp.EmailBackend` without verifying that `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` were provided. Calling `send_mail` attempted to connect to `smtp.gmail.com:587`, hanging the Gunicorn worker until the 30s timeout killed the worker process with HTTP 500.

## Resolution
1. Guarded `EMAIL_BACKEND` in `config/settings.py`: defaults to `console.EmailBackend` unless both `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` are explicitly set.
2. Form submissions process instantly with zero network hanging.
3. Added `EmailBackendSafetyTestCase` to verify the setting invariant.

## Verification
- `Ran 16 tests in 28.016s - OK`
