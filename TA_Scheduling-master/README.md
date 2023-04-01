# TA Backend

## Developing Environment

\*\*NOTE: current environment config works on Python 3.8

1. Set up, then start virtual environment:

   - python3 -m venv venv
   - source venv/bin/activate

2. Install all dependencies:
   - pip3 install --upgrade pip : perform this step to make sure your pip is up-to-date
   - pip3 install -r requirements.txt

3. Start the server:
   - uvicorn src.main:app --reload
   - python3 -m uvicorn src.main:app --host 127.0.0.1 --port <port_number> : use this command if you want to run on a specific port
4. View interactive documentation in browesr:
   - http://127.0.0.1:8000/docs

---

Set up Qualtrics:

- Make changes to .env file at the top level of this project. Here are some notes on each
variable (all of these information can be found on the Account Settings page on Qualtrics. 
Go to Account Settings, then choose Qualtrics IDs tab).

  - TOKEN: you may need to generate a new Token every once in a while and update the environment variable.
  - USER_ID: found under 'User' tab on Qualtrics IDs
  - ORG_ID: found under 'User' tab on Qualtrics IDs
  - DATACENTER: found under 'User' tab on Qualtrics IDs
  - DEFAULT_DIR: found under 'Directories' tab on Qualtrics IDs

---

Set up MongoDB connection:

- Here are the notes on the existing environment variables:
   - CLUSTER: the connection string provided by MongoDB
   - DB_NAME: the name of the working database
