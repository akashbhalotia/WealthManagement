# WealthManagement

A Django application that extracts financial data from a transcript file (.txt) uploaded by the user.

The application extracts a list of facts (sentences) from the uploaded transcript, under three categories:

- **Assets**
- **Expenditures**
- **Income**

For example:

> "Martin is a partner in a law firm in London, earning an average of £15,000 per month before taxes."


## Setup Instructions (MacOS)
1. Create a virtual environment:
   ```
   python3 -m venv myvenv
   source myvenv/bin/activate
   ```
   
2. Clone the repository:
   ```
   git clone https://github.com/akashbhalotia/WealthManagement.git
   cd WealthManagement
   ```
   
3. Install dependencies from `requirements.txt`.
   ```
   pip install -r requirements.txt
   ```
   
4. Set OpenAI API Key:
   ```
   export OPENAI_API_KEY='paste your API key here'
   ```

5. Run the server:
   ```
   python manage.py runserver
   ```

6. Open your browser and enter the following url:
   ```
   http://127.0.0.1:8000/api/transcripts/
   ```

## API Use
1. Get Transcript List:
   ```
   GET http://127.0.0.1:8000/api/transcripts/
   ```
   
2. Upload a new Transcript:
   ```
   POST http://127.0.0.1:8000/api/transcripts/
   ```

3. Get Transcript Details:
   ```
   GET http://127.0.0.1:8000/api/transcripts/<id>/
   ```

4. Update Transcript Details:
   ```
   PUT http://127.0.0.1:8000/api/transcripts/<id>/
   ```

5. Delete a Transcript:
   ```
   DELETE http://127.0.0.1:8000/api/transcripts/<id>/
   ```

## Code Structure and Details:

- **financialInfoExtractor** is the the Django project.
- **transcriptDataExtractor** is the Django app.
- Uses OpenAI **gpt-4o** to extract financial data.
- Timeout is set to **10 seconds**.
- Max file size is **1000 KB**.
- Allows only **.txt files** to be uploaded.


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

### Better Functionality Ideas
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

- Add more comprehensive tests.

- Improve documentation.
