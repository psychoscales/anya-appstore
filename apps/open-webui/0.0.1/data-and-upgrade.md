# Data & Upgrade

- This app persists data via a `./data` bind mount relative to `docker-compose.yml`.
- Upgrading should not remove `./data` as long as the compose cache directory remains stable.

