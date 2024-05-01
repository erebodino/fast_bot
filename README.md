
# LLM expenses bot

Developed in Python, this service is tasked with the analysis of incoming
messages to identify and extract expense details before persisting these details into the
database. It's the core component responsible for interpreting user inputs and converting
them into structured data for storage.


## Installation

The script uses PostgreSQL database, in the instruction below all detailed all the steps to configure the conection.

Clone the project

```bash
  git clone https://github.com/erebodino/fast_bot.git
```

### Install python dependencies

Using requeriments.txt
```bash
  cd fast_bot
  pip install -r requirements.txt
```

Using pipenv
```bash
    cd fast_bot
    pipenv install
```

### Set enviroments variables
The project manage the conection to the database and the conection to the LLM model, so the next variables are requerired:

**LLM provideer**
```bash
    export LLM_API_KEY="<your_anthropic_api_key>
```
**Database**
```bash
    export POSTGRESQL_HOST="<your_postgresql_host>"
    export POSTGRESQL_DATABASE="<your_postgresql_database>"
    export POSTGRESQL_USER="<your_postgresql_user>"
    export POSTGRESQL_PASSWORD="<your_postgresql_password>"
    export POSTGRESQL_PORT="<your_postgresql_port>"
```
### Run service
```bash
    pipenv shell
    uvicorn main:app --reload
```





    