# mock_rates

git clone https://github.com/mockgokberk/mock_rates.git


cd mock_rates


docker-compose build


docker-compose up

or 

git pull origin master

pip install -r requirements.txt

cd mock_rates

python manage.py test

python manage.py runserver


# api endpoints

http://127.0.0.1:8000/api/exchange_rate?provider=exchangerate_mock1

http://127.0.0.1:8000/api/best_rate

http://127.0.0.1:8000/api/best_rate?currency=usd

http://127.0.0.1:8000/api/best_rate_last_24?currency=eur
