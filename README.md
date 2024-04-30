
# LLM expenses bot

This project uses FastAPI and Langchain to manage incoming request from a TelegramBot, understand the message and in case that the message was an expense, persist it in database.




## Installation

Clone the project

```bash
  git clone https://github.com/erebodino/fast_bot.git
```

### Install python dependencies

Using requeriments.txt
```bash
  pip install -r requirements.txt
```

Using pipenv
```bash
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
    cd fast_bot
    pipenv shell
    uvicorn main:app --reload
```





    