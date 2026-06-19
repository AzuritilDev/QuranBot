# Security Policy

## Supported Versions

Security patches are provided only for the latest stable release. Older versions will not receive retroactive security updates. 

If you find a vulnerability in an older version, please update to the latest release to verify if the issue still exists.

## Reporting a Vulnerability

Please do not report security vulnerabilities through public GitHub issues. 

To report a vulnerability, email the project maintainer **azuriteluadev@proton.me**

### What to Include
*   A clear description of the vulnerability.
*   Step-by-step instructions to reproduce the issue.
*   Potential impact (e.g., unauthorized data access, bot hijacking).

Reports are reviewed as time permits. We will update you on our progress if the vulnerability is verified.

## Critical Security Guidelines for Self-Hosting

If you are hosting this bot yourself, you must secure your environment:

### 1. Token & Credential Management
*   **Never hardcode credentials:** Keep your Discord bot token, Redis and PostgreSQL passwords out of the source code.
*   **Use Environment Variables:** Store secrets in a `.env` file and add `.env` to your `.gitignore`.
*   **Rotate Secrets:** If a token or database password is accidentally leaked, rotate it immediately in the Discord Developer Portal and your database config.

>Note: Never share Discord tokens, PostgreSQL passwords, Redis passwords, API keys, or any other secrets in bug reports, screenshots, logs, or GitHub issues. 

### 2. PostgreSQL Security
*   **Avoid the `postgres` Superuser:** Create a dedicated database user for the bot with limited privileges (only `SELECT`, `INSERT`, `UPDATE`, `DELETE` on the bot database).
*   **Restrict Network Access:** If the database is on the same machine, bind PostgreSQL to `localhost` (`127.0.0.1`). Do not expose port `5432` (or whatever port your PostgreSQL service is in) to the public internet.
*   **SQL Injection Prevention:** Our bot uses parameterized queries/an ORM. If you modify the source code, never use string concatenation to build SQL queries.

### 3. Discord Permissions
*   **Principle of Least Privilege:** Only grant the bot the specific permissions it needs to function. Avoid granting the `Administrator` permission.
*   **Privileged Intents:** Turn off Gateway Intents (like Presence or Guild Members) in the Discord Developer Portal if your custom build does not use them.

### 4. Redis Security
*   **Do Not Expose Redis Publicly:** Redis should only be accessible from trusted services (such as the bot container). Do not publish Redis port (e.g. `6379`) to the public internet unless absolutely necessary.
*   **Use Docker Internal Networking:** When using Docker Compose, allow containers to communicate through the Compose network instead of exposing Redis to the host machine.
*   **Enable Authentication if Exposed:** If Redis must be reachable outside the internal Docker network, configure authentication and appropriate network restrictions.
*   **Do Not Store Secrets in Redis:** Redis may contain cached data and temporary application state. Do not use it as a secure secret store.
Regularly Update Redis Images: Pull updated Redis container images to receive security patches and bug fixes.

### 5. Docker Security
*   **Review Port Mappings:** Only expose ports that are required for external access.
*   **Protect Environment Files:** Never commit .env files containing tokens, database passwords, or Redis credentials.
*   **Use Trusted Images:** Only use official or otherwise trusted container images.
*   **Run With Least Privilege:** Avoid running containers with unnecessary privileges, host networking, or privileged mode unless required.