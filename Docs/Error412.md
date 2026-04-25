# Error 412 (Catbox) Incident Report

## Incident Summary
When setting a manga poster/banner from Telegram, the bot uploads the image to Catbox via `https://catbox.moe/user/api.php`.
On Heroku deployments, uploads can fail with HTTP **412 Precondition Failed**, and the bot surfaces this as a generic Catbox failure.

## User-facing Symptom
- Telegram flow stops at banner/poster step.
- Bot message: `✗ Catbox upload failed.`
- Heroku logs show: `Catbox error: 412`.

## Technical Trace (Code Path)
1. Poster upload is triggered from Telegram in `plugins/search.py`:
   - manual upload flow (`await_banner_upload`) calls `Catbox.upload(...)`
   - channel auto-fetch banner flow also calls `Catbox.upload(...)`
2. `services/catbox.py` performs a POST to Catbox and currently logs only status code when non-200.

## Likely Root Cause
HTTP 412 from Catbox in cloud hosts is commonly an anti-abuse / edge validation rejection (request context not accepted from certain datacenter traffic patterns). Heroku egress IP ranges are frequently shared and may be rate-limited or challenged.

In this repository, the upload function:
- sends anonymous upload (`reqtype=fileupload`) with no userhash,
- does not log response body from Catbox,
- has no retry/backoff/fallback for upload failures.

This makes transient or policy-based Catbox rejections look like a permanent app error.

## Contributing Factors in Current Implementation
- **Low observability**: only HTTP status is logged (`Catbox error: 412`), not Catbox response text.
- **No upload retry**: single attempt for uploads.
- **No provider fallback**: if Catbox rejects, workflow fails.
- **No graceful degradation**: user can only skip manually.

## Impact
- Subscription setup friction for users who want posters/banners.
- Higher setup drop-off and repeated support questions.
- Inconsistent behavior by deployment region/IP reputation.

## Recommended Remediation Plan

### Priority 1 (Immediate)
1. **Improve logging for non-200** upload responses:
   - log status + short response body from Catbox,
   - include request correlation id if available.
2. **Add upload retries** for 412/429/5xx with exponential backoff.
3. **Improve user message**:
   - explicitly mention temporary host-side rejection,
   - offer one-tap retry / skip.

### Priority 2 (Stability)
4. **Support authenticated Catbox uploads** with `userhash` (if you own an account) to reduce anonymous throttling sensitivity.
5. **Introduce fallback host** (e.g., optional alternate image host) when Catbox fails.
6. **Optional direct Telegram CDN usage** for banner storage if your architecture allows it.

### Priority 3 (Operations)
7. Track metrics:
   - Catbox upload success rate,
   - failure rate by status code and host region,
   - retry success-after-failure ratio.
8. Add runbook entry for operators with known workaround: retry once, then skip banner to complete setup.

## Heroku-specific Checks
- Verify dyno region and recent outbound network behavior.
- Test Catbox upload from same dyno via one-off run to compare with local machine.
- Ensure no proxy/middleware modifies multipart payload.
- Confirm file sizes remain below Catbox limits.

## Workaround (for production right now)
- Allow users to **Skip Banner** and complete subscription.
- If banner is required, retry later from a different deployment/IP or use fallback provider.

## Conclusion
This is most likely an upstream acceptance/policy rejection from Catbox as seen from Heroku egress, amplified by missing retries and limited diagnostics in the current upload implementation. Improving observability + retries + fallback will significantly reduce user-visible failures.
