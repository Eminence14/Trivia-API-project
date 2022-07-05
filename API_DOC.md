TRIVIA API

This project houses a number of questions sorted by categories for each individual to pick from as desired. It can be played alone, or with others to have more fun. Dive right in and enjoy!

# GETTING STARTED

- Base URL: Currently, this app is not deployed yet, rather it is hosted locally at http://127.0.0.1:5000 or localhost:5000 and it can also be viewed on your network via http://192.38.58.1:5000.
- Authentication: At present, this app does not require any form of authentication or API keys.

## Error Handling

Errors that occur in this API solely follow the HTTP response status codes. The 2xx generally indicate "success", the 4xx indicates "client error" while the 5xx generally indicates "server error" which is pretty much rare.

The error data is returned in a principled JSON format as follows:
{#
"success": False,
"error": 400,
"message": "bad request"
}
For a 404 Not Found error;
{
'success': False,
'error': 404,
'message': "Not Found"
}

The API will return five error types when requests fail:

- 400: Bad Request
- 404: Resource Not Found
- 405: Method Not Alllowed
- 422: Not Processable
- 500: Internal Server Error (RARE)

## Endpoints

### GET "/categories"

General: - Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category - Request Arguments: None - Returns: An object with a single key, `categories`, that contains an object of id: category_string`key: value pairs. Sample:`curl localhost:5000/categories`
Result:
json
{
"1": "Science",
"2": "Art",
"3": "Geography",
"4": "History",
"5": "Entertainment",
"6": "Sports"
}

### GET "/questions"

General: - Fetches a dictionary of categories and questions served to the client with keys of 'question', 'answer', 'category', 'difficulty' and 'id' - Returns: An object with key 'questions' with a value as the list of questions. - Results are paginated in groups of 10.
-Request Arguments: A page request argument can be added in order to view a particular page. e.g "curl localhost:5000/questions?page=2" to view the second page
Sample:
curl localhost:5000/questions
Result:
{
"categories": {
"1": "Science",
"2": "Art",
"3": "Geography",
"4": "History",
"5": "Entertainment",
"6": "Sports"
},
"questions": [
{
"answer": "Tom Cruise",
"category": 5,
"difficulty": 4,
"id": 4,
"question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
},
{
"answer": "Maya Angelou",
"category": 4,
"difficulty": 2,
"id": 5,
"question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
},
{
"answer": "Edward Scissorhands",
"category": 5,
"difficulty": 3,
"id": 6,
"question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
},
{
"answer": "Muhammad Ali",
"category": 4,
"difficulty": 1,
"id": 9,
"question": "What boxer's original name is Cassius Clay?"
},
{
"answer": "Brazil",
"category": 6,
"difficulty": 3,
"id": 10,
"question": "Which is the only team to play in every soccer World Cup tournament?"
},
{
"answer": "Uruguay",
"category": 6,
"difficulty": 4,
"id": 11,
"question": "Which country won the first ever soccer World Cup in 1930?"
},
{
"answer": "George Washington Carver",
"category": 4,
"difficulty": 2,
"id": 12,
"question": "Who invented Peanut Butter?"
},
{
"answer": "Agra",
"category": 3,
"difficulty": 2,
"id": 15,
"question": "The Taj Mahal is located in which Indian city?"
},
{
"answer": "Escher",
"category": 2,
"difficulty": 1,
"id": 16,
"question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
},
{
"answer": "Mona Lisa",
"category": 2,
"difficulty": 3,
"id": 17,
"question": "La Giaconda is better known as what?"
}
],
"success": true,
"totalQuestions": 27
}

#### DELETE "/questions/<int:question_id>"

General:

- This deletes the question with the given id if it exists. It returns the id of the deleted question, it success value and the remaining questions, which is updated on the frontend.
- Results are paginated in groups of 10.
- Request Arguments: A question id can be added in order to delete it. e.g "curl localhost:5000/questions/3" to delete the question with id 3.
  Sample:
  curl localhost:5000/questions/3
  Result:
  {
  'success': True,
  'question': 3,
  'remaining_question': [
  {
  "answer": "Tom Cruise",
  "category": 5,
  "difficulty": 4,
  "id": 4,
  "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
  },
  {
  "answer": "Maya Angelou",
  "category": 4,
  "difficulty": 2,
  "id": 5,
  "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
  },
  {
  "answer": "Edward Scissorhands",
  "category": 5,
  "difficulty": 3,
  "id": 6,
  "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
  },
  {
  "answer": "Muhammad Ali",
  "category": 4,
  "difficulty": 1,
  "id": 9,
  "question": "What boxer's original name is Cassius Clay?"
  },
  {
  "answer": "Brazil",
  "category": 6,
  "difficulty": 3,
  "id": 10,
  "question": "Which is the only team to play in every soccer World Cup tournament?"
  },
  {
  "answer": "Uruguay",
  "category": 6,
  "difficulty": 4,
  "id": 11,
  "question": "Which country won the first ever soccer World Cup in 1930?"
  },
  {
  "answer": "George Washington Carver",
  "category": 4,
  "difficulty": 2,
  "id": 12,
  "question": "Who invented Peanut Butter?"
  },
  {
  "answer": "Agra",
  "category": 3,
  "difficulty": 2,
  "id": 15,
  "question": "The Taj Mahal is located in which Indian city?"
  },
  {
  "answer": "Escher",
  "category": 2,
  "difficulty": 1,
  "id": 16,
  "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
  },
  {
  "answer": "Mona Lisa",
  "category": 2,
  "difficulty": 3,
  "id": 17,
  "question": "La Giaconda is better known as what?"
  }
  ]
  }

### POST "/questions"

General: - This method collects information such as question, category, difficulty and answer from the client, - Returns the questions with the new question added and its success value. - Results are paginated in groups of 10.
-Request Arguments: A page request argument can be added in order to view a particular page. e.g "curl localhost:5000/questions?page=2" to view the second page
Sample:
curl localhost:5000/questions -X POST -H "Content-Type: application/json" -d "{'question': 'what is the full meaning of AMOLED', 'category':'1', 'difficulty':'4', 'answer': 'Active Matrix Organic Light Emiting Diode'}"
Result:
{
"questions": [
'question': 'what is the full meaning of AMOLED',
'answer': 'Active Matrix Organic Light Emiting Diode',
'category':'1',
'difficulty':'4'
]
'success': True
}

### POST GET "/questions"

General: - This takes input from the client in the form of phrases or words and filters through the question to find similar questions. - Returns questions which the search term is a substring of the question, the success value and the length of the related questions - Results are paginated in groups of 10.
-Request Arguments: The search term must be added in order to filter throught the question.
Sample:
curl localhost:5000/questions?search=cass -X POST -H "Content-Type: application/json"
Result:
related_questions: {
"answer": "Muhammad Ali",
"category": 4,
"difficulty": 1,
"id": 9,
"question": "What boxer's original name is Cassius Clay?"
},
'success': True,
'length_related_question': 1

### GET "/categories/<int:category_id>/questions"

General: - Gets all questions in a particular category. - Returns questions that are in the chosen category and its success value. - Results are paginated in groups of 10.
-Request Arguments: none.
Sample:
curl localhost:5000/categories/1/questions
Result:
{
"category_question": [
{
"answer": "The Liver",
"category": 1,
"difficulty": 4,
"id": 20,
"question": "What is the heaviest organ in the human body?"
},
{
"answer": "Alexander Fleming",
"category": 1,
"difficulty": 3,
"id": 21,
"question": "Who discovered penicillin?"
},
{
"answer": "Blood",
"category": 1,
"difficulty": 4,
"id": 22,
"question": "Hematology is a branch of medicine involving the study of what?"
},
{
"answer": "28-31 days",
"category": 1,
"difficulty": 3,
"id": 30,
"question": "How many days is the incubation period of an hen?"
}
],
"success": true,
"category_id": 1
}

### POST "/quizzes/<int:cat>"

General: - Enters a quiz mode where the client is served one question at a time taking into account the previous questions and their category. - Returns a random question within the chosen category - Questions are diplayed one at a time.
-Request Arguments: none.
Sample:
curl localhost:5000/quizzes/2
Result:
{
"question": [
{
"answer": "Escher",
"category": 2,
"difficulty": 1,
"id": 16,
"question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
}
],
"success": true
}

## Authors

Udacity, Victor.

## Acknowledgements

Udacity as a whole, thanks for the support to bring out this better version of myself.
To my coach, Coach Caryn, much love from here.
