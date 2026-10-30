# A complete combined devcontainer example

## Complete `devcontainer.json` Example

```json
{
  "name": "my-project",
  "image": "ghcr.io/owner/repo-devcontainer:main@sha256:abc123...",
  "secrets": {
    "TERRAFORM_TOKEN": {
      "description": "Token to access Terraform Cloud."
    },
    "BWS_ACCESS_TOKEN": {
      "description": "Token to access Bitwarden Secrets Manager API."
    },
    "GITHUB_TOKEN": {
      "description": "Personal access token for GitHub API."
    },
    "WG_PRIVATE_KEY": {
      "description": "WireGuard client private key."
    },
    "WG_ENDPOINT": {
      "description": "WireGuard server endpoint host:port."
    }
  },
  "runArgs": [
    "--env-file", ".devcontainer/devcontainer.env",
    "--cap-add=NET_ADMIN",
    "--device=/dev/net/tun"
  ],
  "initializeCommand": "test -f .devcontainer/devcontainer.env || cp .devcontainer/devcontainer.env.sample .devcontainer/devcontainer.env",
  "onCreateCommand": "bash .devcontainer/scripts/onCreateCommand.sh ${containerWorkspaceFolder}",
  "remoteUser": "vscode",
  "containerUser": "vscode"
}
```

---
