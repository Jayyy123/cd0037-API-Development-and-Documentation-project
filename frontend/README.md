# Frontend - Trivia API

## WELCOME TO MY TRIVIA GAME:
 This project was inspired and given to me by ALX in collaboration with Udacity. To get started read the following information and to
 find out how to use the endpoints properly please refer to the api documentation below!


## Getting Setup

> _tip_: this frontend is designed to work with [Flask-based Backend](../backend) so it will not load successfully if the backend is not working or not connected. We recommend that you **stand up the backend first**, test using Postman or curl, update the endpoints in the frontend, and then the frontend should integrate smoothly.

### Installing Dependencies

1. **Installing Node and NPM**
   This project depends on Nodejs and Node Package Manager (NPM). Before continuing, you must download and install Node (the download includes NPM) from [https://nodejs.com/en/download](https://nodejs.org/en/download/).

2. **Installing project dependencies**
   This project uses NPM to manage software dependencies. NPM Relies on the package.json file located in the `frontend` directory of this repository. After cloning, open your terminal and run:

```bash
npm install
```

> _tip_: `npm i`is shorthand for `npm install``


### Expected endpoints and behaviors

##### API  DOUCMENTATION by JOSEPH OFILI

`GET '/categories'`

- Fetches a dictionary which either contains
  - on success :
    - the categories which is a dictionary which contain keys of id and type and their values.
    - the success i.e True or False
    - and the status code of either 200

    # SUCCESS

    ```json
    {
      "categories": {
        "id" :1, 
        "type":"Science",
        "id" :2, 
        "type":"Art",
        "id" :3, 
        "type":"Geography",
        "id" :4, 
        "type":"History",
        "id" :5, 
        "type":"Entertainment",
        "id" :6, 
        "type":"Sports"
      },
      "success":True,
      "total_categories": "total number",
      "status_code":200
    }
    ```

  - on  failure :
      - A 404 not found error with the error code, a message and the success set to False.
    # FAILURE

    ```json
      {
        "success": False, 
        "error code": 404,
        "message": " resource was Not found!"
      }
    ```

- Request Arguments: None
- Returns: An object with a single key, categories, that contains an object of id: category_string key:value pairs.




---

`GET '/questions?page=${integer}'`

- Fetches a dictionary which either contains
  - on success :
    - Fetches a paginated set of questions, a total number of questions, all the categories which is a dictionary which contain keys of id and type and their values and current category string.
    - Request Arguments: `page` - integer
    - Returns: An object with 10 paginated questions, total questions, object including all categories, and current category string

    # SUCCESS

    ```json
      {
        "questions": [
          {
            "id": 1,
            "question": "This is a question",
            "answer": "This is an answer",
            "difficulty": 5,
            "category": 2
          }
        ],
        "totalQuestions": 100,
        "categories": {
          "id" :1, 
          "type":"Science",
          "id" :2, 
          "type":"Art",
          "id" :3, 
          "type":"Geography",
          "id" :4, 
          "type":"History",
          "id" :5, 
          "type":"Entertainment",
          "id" :6, 
          "type":"Sports"
        },
        "currentCategory": "ALL"
      }
    ```

  - on  failure :
      - A 404 not found error with the error code, a message and the success set to False.
    # FAILURE

    ```json
      {
        "success": False, 
        "error code": 404,
        "message": " resource was Not found!"
      }
    ```

---

`GET '/categories/${id}/questions'`

- Fetches a dictionary which either contains
  - on success :
    - Fetches questions for a cateogry specified by id request argument
    - Request Arguments: `id` - integer
    - Returns: An object with questions for the specified category, total questions, and current category string

    # SUCCESS

    ```json
      {
        "questions": [
          {
            "id": 1,
            "question": "This is a question",
            "answer": "This is an answer",
            "difficulty": 5,
            "category": 2
          }
        ],
        "totalQuestions": 100,
        "categories": {
          "id" :1, 
          "type":"Science",
          "id" :2, 
          "type":"Art",
          "id" :3, 
          "type":"Geography",
          "id" :4, 
          "type":"History",
          "id" :5, 
          "type":"Entertainment",
          "id" :6, 
          "type":"Sports"
        },
        "currentCategory": "Entertainment"
      }
    ```

  - on  failure :
      - A 404 not found error with the error code, a message and the success set to False.
    # FAILURE

    ```json
      {
        "success": False, 
        "error code": 404,
        "message": " resource was Not found!"
      }
    ```

---

`DELETE '/questions/${id}'`

- Deletes a specified question using the id of the question
- Request Arguments: `id` - integer
- Returns: 
  # ON SUCCESS
    ```json
        {
          "success": True,
          "message": "question with {question_id} has been successfully deleted from the database!"
        }
    ```
  # ON FAILURE
      ```json
      {
        "success": False, 
        "error code": 404,
        "message": " resource was Not found!"
      }
    ```

---

`POST '/quizzes'`

- Sends a post request in order to get the next question
- Request Body:

  ```json
  {
      "previous_questions": [1, 4, 20, 15],
      "quiz_category": "current category"
  }
  ```

- Returns: a single new question object
    # ON SUCCESS
      ```json
          {
            "category": "History",
            "question": {
                  "id": 1,
                  "question": "This is a question",
                  "answer": "This is an answer",
                  "difficulty": 5,
                  "category": 2
                },
            "difficulty": 4
          }
      ```
    # ON FAILURE
    ```json
      {
        "success": False, 
        "error code": 422,
        "message": " resource was unprocessable!"
      }
    ```

---

`POST '/questions/create'`

- Sends a post request in order to add a new question
- Request Body:

```json
{
  "question": "Heres a new question string",
  "answer": "Heres a new answer string",
  "difficulty": 1,
  "category": 3
}
```

- Returns:
  # ON SUCCESS
      ```json
          {
            "status": 200,
            "message": "New Question has been inserted successfully"
          }
      ```
    # ON FAILURE
        ```json
        {
          "status": False, 
          "error code": 422,
          "message": " resource was unprocessable!"
        }
    ```

---

`POST '/questions/search'`

- Sends a post request in order to search for a specific question by search term
- Request Body:

      ```json
      {
        "searchTerm": "this is the term the user is looking for"
      }
      ```
      

- Returns: 
    # ON SUCCESS
    -any array of questions, a number of totalQuestions that met the search term and the current category string
    ```json
      {

          "success":True,
          "questions":[
                        {
                          "id": 1,
                          "question": "This is a question",
                          "answer": "This is an answer",
                          "difficulty": 5,
                          "category": 5
                        }
                      ],
          "total_questions": 1,
          "current_category": "history"
      }
    ```

