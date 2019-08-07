# Flask-fyle-deploy
Fyle Assignment:
This flask utility displays bank information on the basis of the following attributes:
1) Get all banks
2) By IFSC code
3) By name and/or city
4) By list of cities

All the above queries can be executed along with limit and offset parameters.

The data is stored in PostgreSQL. The app is deployed using Heroku and is accesible on the following URL:
https://fyle-assignment101.herokuapp.com/

The following Curl statements can be used to fetch the data as per requirement:

1) Login curl request (Mandatory process which generates a JWT token which is valid for 5 days)
curl -X POST \
  https://fyle-assignment101.herokuapp.com/login \
  -H 'Content-Type: application/json' \
  -d '{
	"username" : "admin",
	"password" : "admin"
}'

2) Curl request to execute the above 4 queries:
curl -X GET \
  'https://fyle-assignment101.herokuapp.com/get?name=ABHYUDAYA%20COOPERATIVE%20BANK%20LIMITED&city=mumbai&limit=5' \
  -H 'Authorization: Bearer 
  ${TOKEN_GENERATED_IN_THE_PREVIOUS_STEP}' 
  
  
  
