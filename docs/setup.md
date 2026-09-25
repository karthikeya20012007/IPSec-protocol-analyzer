# Development Setup Guide

Complete setup instructions for the IPSec Protocol Analyzer on Ubuntu / WSL2.

---

## 1. Clone the Repository

**SSH (recommended for development):**

```bash
git clone git@github.com:<USERNAME>/IPSec-protocol-analyzer.git
cd IPSec-protocol-analyzer
```

**HTTPS (alternative):**

```bash
git clone https://github.com/<USERNAME>/IPSec-protocol-analyzer.git
cd IPSec-protocol-analyzer
```

Replace `<USERNAME>` with the GitHub account that hosts the repository.

SSH is recommended because it avoids repeated password prompts and integrates with standard SSH key authentication.

---

## 2. Python Virtual Environment

Create a project-local virtual environment to isolate Python dependencies from the system Python:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
```

`.venv/` is listed in `.gitignore` and must **never** be committed to Git. Each developer creates their own local venv.

To re-activate in a new terminal session:

```bash
source .venv/bin/activate
```

---

## 3. Verify Python Tooling

After activating the venv, confirm the expected versions:

```bash
python --version
python -m pytest --version
```

Expected output (versions may differ):

```text
Python 3.14.4
pytest 9.1.1
```

---

## 4. Required System Packages

The following system-level packages are required for the IPsec testbed and packet analysis. These are **not** Python packages and must be installed via `apt`:

```bash
sudo apt-get update
sudo apt-get install -y \
    strongswan \
    strongswan-swanctl \
    charon-systemd \
    tshark \
    iproute2 \
    tcpdump \
    hping3 \
    iperf3
```

| Package              | Purpose                                      |
|----------------------|----------------------------------------------|
| `strongswan`         | IPsec metapackage (libraries and plugins)    |
| `strongswan-swanctl` | Modern swanctl CLI and VICI plugin           |
| `charon-systemd`     | IKE daemon (`/usr/sbin/charon-systemd`)      |
| `tshark`             | Command-line packet analyzer (Wireshark CLI) |
| `iproute2`           | `ip` command for namespaces, links, routes   |
| `tcpdump`            | Raw packet capture                           |
| `hping3`             | Flexible traffic generation                  |
| `iperf3`             | Bandwidth/throughput testing                 |

`iproute2`, `tcpdump`, and basic networking tools are typically pre-installed on Ubuntu. The others may need explicit installation.

> **Note:** Do NOT install Scapy or ML/API dependencies yet. Dependencies are added incrementally as each project phase requires them.

---

## 5. Git Configuration

Configure your Git identity (used for commit authorship):

```bash
git config --global user.name "<YOUR_NAME>"
git config --global user.email "<YOUR_EMAIL>"
```

Replace the placeholders with your actual name and email. These values are stored in `~/.gitconfig` and are not project-specific.

---

## 6. Identify an Existing SSH Key

Check if you already have an SSH key pair:

```bash
ls -la ~/.ssh
```

Look for files named `id_ed25519` and `id_ed25519.pub`. If they exist, display the **public** key:

```bash
cat ~/.ssh/id_ed25519.pub
```

The `.pub` file is the **public key** and is safe to share. It can be added to GitHub.

> **WARNING:** Never share, copy, or commit `~/.ssh/id_ed25519` (without the `.pub` extension). That is your **private key**.

---

## 7. Generate an SSH Key (If Needed)

If no SSH key exists, generate one:

```bash
ssh-keygen -t ed25519 -C "<YOUR_GITHUB_EMAIL>"
```

When prompted:
- **File location:** Press Enter to accept the default (`~/.ssh/id_ed25519`).
- **Passphrase:** Enter a strong passphrase (recommended) or press Enter for none.

This creates two files:
- `~/.ssh/id_ed25519` — private key (keep secret)
- `~/.ssh/id_ed25519.pub` — public key (share with GitHub)

---

## 8. GitHub SSH Setup

1. Go to [GitHub Settings → SSH and GPG keys](https://github.com/settings/keys).
2. Click **New SSH key**.
3. Set **Title** to something identifying your machine (e.g., `WSL2 Ubuntu`).
4. Set **Key type** to **Authentication Key**.
5. Copy the output of:

   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```

6. Paste the public key into the **Key** field.
7. Click **Add SSH key**.

---

## 9. Test GitHub SSH Authentication

```bash
ssh -T git@github.com
```

Expected output on success:

```text
Hi <USERNAME>! You've been authenticated, but GitHub does not provide shell access.
```

If you see a permission denied error, verify that your public key was added to GitHub and that the correct key is being used.

---

## 10. Convert HTTPS Remote to SSH

If you originally cloned via HTTPS and want to switch to SSH, check the current remote:

```bash
git remote -v
```

If the URL starts with `https://`, convert it:

```bash
git remote set-url origin git@github.com:<USERNAME>/IPSec-protocol-analyzer.git
```

Verify:

```bash
git remote -v
```

Both `fetch` and `push` URLs should now show the `git@github.com:` SSH form.

---

## 11. Branch Setup

This project uses `main` as the default branch:

```bash
git branch -M main
git push -u origin main
```

For subsequent pushes after the initial setup:

```bash
git push
```

---

## 12. Run Project Tests

Activate the venv and run the test suite:

```bash
source .venv/bin/activate
pytest -v
```

### Test categories

| Category | Description | Requires |
|----------|-------------|----------|
| **Unit tests** | Safe, unprivileged tests for configuration, models, parsing | Nothing special |
| **Integration tests** | Tests marked `requires_root` and/or `requires_ipsec` | Root privileges, strongSwan |
| **Testbed verification** | Full IPsec tunnel setup/verify/cleanup cycle | Root, namespaces, strongSwan |

Normal `pytest` execution skips integration tests automatically when run without root. To run integration tests explicitly:

```bash
sudo .venv/bin/pytest -v -m requires_root
```

---

## 13. Start the Local IPsec Testbed

The testbed creates isolated Linux network namespaces with veth interfaces, configures XFRM policies and SAs, and runs isolated `charon-systemd` instances. This requires root.

```bash
sudo ./scripts/setup_testbed.sh
```

Verify the tunnel (checks IKE SA, CHILD SA, XFRM state, ESP traffic):

```bash
sudo ./scripts/verify_testbed.sh
```

Tear down the testbed (removes only project-created resources):

```bash
sudo ./scripts/cleanup_testbed.sh
```

See [docs/testbed.md](testbed.md) for the full network topology and IPsec configuration details.

---

## 14. Git Workflow

Follow this workflow for every change:

```text
implement
  ↓
add/update tests
  ↓
run pytest
  ↓
update README/docs
  ↓
inspect git diff
  ↓
commit
  ↓
push
```

Before committing, always inspect:

```bash
git status
git diff
git diff --stat
```

Use conventional commit messages:

```bash
git add <files>
git commit -m "feat: description of the change"
git push
```

Do not use automated commit/push scripts.

---

## 15. Safety Rules

- **Never** commit private SSH keys (`~/.ssh/id_ed25519` or similar).
- **Never** put GitHub tokens, passwords, or secrets in source code.
- **Never** commit `.venv/` or Python cache directories.
- **Never** commit generated PCAP files unless using an approved dataset storage mechanism (e.g., Git LFS, documented separately).
- **Do not** modify `/etc/wsl.conf` as part of normal project setup.
- **Do not** modify Windows networking, firewall, or routing tables unnecessarily.
- **Do not** run testbed scripts outside of the designated network namespaces.

---

## Quick Start (Helper Script)

A safe helper script is provided for steps 2–4:

```bash
./scripts/setup_dev.sh
```

This script:
- Checks your Python version
- Creates `.venv` if it does not exist
- Installs `requirements-dev.txt`
- Runs a basic pytest check
- Reports missing system packages

It does **not** handle SSH keys, Git configuration, GitHub authentication, or system package installation.
