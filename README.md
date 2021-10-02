# FastAPI + SQLModel + Alembic

Test project that uses FastAPI, async SQLAlchemy, SQLModel, Postgres, Alembic, and Docker. <br>
First realisation with django + celery at the link [https://github.com/trulander/exchange-rates](https://github.com/trulander/exchange-rates)

The project based on the task:
```team foundation
1)  Servise goes by API ones in 5-10-15 minutes (set via .env) and gets the data about 
    cryptocurrency BTC (for example curl -H "X-CMC_PRO_API_KEY: d61bca4c-e9d3-40b9-8d82-abf9b057ffbd" -H "Accept: application/json" -d "id=1" -G https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest)
    and save the data to the databases, the exchange rate, the time the data was received, and whatever else you whant.
2) Service that show informarion from the database about exchange rate(last and list)
    *   if it possible, if i want to get the latest exchange rate, i go by a special endpoint and worker gets the latest data
    *   Wrap everythink in a Docker + docker-compose
3)  share on the Github
    *   And the best if it async(if not django)
```

## Commands to set up the project

```sh
    git clone https://github.com/trulander/exchange-rates-async.git
    cd exchange-rates
    docker-compose up -d --build
    docker-compose exec web alembic upgrade head
```

After that you'll get a working project out of the box

Sanity check: [http://localhost:8000/docs](http://localhost:8000/docs) <br>
At this link you can see documentation about the project API in swagger format


# Some userfull commands:
### migration:
```sh
  alembic revision --autogenerate -m "name_of_migration"
  alembic upgrade head

```

### start application as local:
(each command runs in a new console. it must be three different applications)

```shell
 uvicorn app.main:app --reload --workers 1 --host 0.0.0.0 --port 8000
 celery -A app.worker worker -l info --pool=solo
 celery -A app.tasks beat --loglevel=info

```
