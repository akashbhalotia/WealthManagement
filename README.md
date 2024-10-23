# WealthManagement

A Django application that allows 


## TODO

### Productionization Ideas
- Deploy to a Cloud Provider (eg. AWS).
- Replace SQLite DB with production grade DB like PostgreSQL or MySQL.
- Set up DB backups.
- Set up alerting and monitoring.
- Serve static and media files via a CDN or object storage like AWS S3.
- Store media files separately (e.g., AWS S3, Azure Blob Storage).
- Use a load balancer (e.g., AWS ELB) if needed for scaling horizontally.
- Implement caching with Redis or Memcached for improved performance.
- Set up automated testing (unit, integration, load tests).

### Functionality
- Option to re-generate assets/expenditures/income of a given transcript. Currently this can be done by re-uploading the same file again (PUT operation).
  Provide separate API endpoint for it. Frontend can have a refresh button which calls this to re-generate the extracted financial data. Useful when
  LLM hallucinates or encounters errors.

- Intgerate users functionality. Each user has their own set of uploaded transcripts. A user can access only their own uploaded transcripts and associated
  extracted financial data. Admin can access the data of all users through admin panel.

- Improve data extraction logic. Make it more sophisticated. Currently we use a simple prompt to do it. Use AI Agents to examine the transcript and
  select the best suited prompt for it from among multiple stored prompts. For example, prompt might be different for a client who is looking for
  personal finance expertise vs a client looking for financial advice related to their small business and so on.

- APIs to enable higher level of customization, such as selecting timeout duration. Selecting LLM model. Setting temperature, etc.

- Allow editing of extracted financial data. Useful to include additional notes.

- Improve project name and app name.

- Handle timeout better. Can use a library (example celery) to continue extraction of financial data as a background task, instead of timing out.
