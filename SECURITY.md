# Security Policy

## Reporting a Vulnerability

Please do not report security vulnerabilities through public GitHub issues. 

To report a vulnerability, email the project maintainer **azuriteluadev@proton.me**

### What to Include
*   A clear description of the vulnerability.
*   Step-by-step instructions to reproduce the issue.
*   Potential impact (e.g., unauthorized data access, bot hijacking).

You will receive an acknowledgment of your report within 48 hours. We will keep you updated on our progress as we work on a fix.

## Critical Security Guidelines for Self-Hosting

If you are hosting this bot yourself, you must secure your environment:

### 1. Token & Credential Management
*   **Never hardcode credentials:** Keep your Discord bot token and PostgreSQL passwords out of the source code.
*   **Use Environment Variables:** Store secrets in a `.env` file and add `.env` to your `.gitignore`.
*   **Rotate Secrets:** If a token or database password is accidentally leaked, rotate it immediately in the Discord Developer Portal and your database config.

### 2. PostgreSQL Security
*   **Avoid the `postgres` Superuser:** Create a dedicated database user for the bot with limited privileges (only `SELECT`, `INSERT`, `UPDATE`, `DELETE` on the bot database).
*   **Restrict Network Access:** If the database is on the same machine, bind PostgreSQL to `localhost` (`127.0.0.1`). Do not expose port `5432` to the public internet.
*   **SQL Injection Prevention:** Our bot uses parameterized queries/an ORM. If you modify the source code, never use string concatenation to build SQL queries.

### 3. Discord Permissions
*   **Principle of Least Privilege:** Only grant the bot the specific permissions it needs to function. Avoid granting the `Administrator` permission.
*   **Privileged Intents:** Turn off Gateway Intents (like Presence or Guild Members) in the Discord Developer Portal if your custom build does not use them.
