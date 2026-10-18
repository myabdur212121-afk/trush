# Security

## Credentials are not setup inputs

Cloning this public repository, downloading the public fonts, and installing the
public packages do **not** need a GitHub token. Authentication is relevant only
to publishing changes or managing a repository.

Never commit or attach:

- personal access tokens, `token.md`, `.env` or credential files;
- secrets embedded in Git remote URLs, commands, screenshots or logs;
- private keys or authentication headers.

The ignore rules reduce accidents, but they cannot remove an already committed
secret and do not replace checking the staged content.

If a credential was exposed, **revoke it at the provider immediately**. Deleting
a file, chat message or Git commit alone does not invalidate the credential.
Review affected access/history before issuing a replacement with the smallest
necessary scope and a short lifetime.

## Installer boundaries

- Review scripts before running them. APT actions require root/sudo and change
  system packages; pip packages are isolated in per-engine virtual environments.
- Full TeX Live is an explicit, large optional installation, never a hidden fix.
- Font downloads use HTTPS and pinned SHA-256 values. A mismatch is a failure,
  not permission to silently disable verification.
- Do not run untrusted animation code merely because it is a Manim scene: it is
  Python code with the permissions of the executing user.
- Keep persistent fonts out of temporary or snapshot-excluded directories.

## Reporting

Use GitHub's private vulnerability-reporting channel if the repository offers
one. Otherwise contact the owner privately through a channel they publish before
sharing exploitable details. Do not post live credentials or sensitive logs in a
public issue. No response-time guarantee or dedicated security team is implied.
