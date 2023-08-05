# Scoped Concerns Py

Scoped Concerns Py is the Python version of the Ruby's [Scoped-Concerns](https://github.com/threefunkymonkeys/scoped-concerns) gem. It is a tiny utility library to help you encapsulate responsibilities in your Python applications by providing a common interface and a common response object for the so called service classes or how we like to call them: concerns.

We've been playing around with this concept in a few applications and it was evolving until this point that we feel it reusable enough to become a separated library.

## Install

It is a Python package, you can install it with:

```
pip install scoped-concerns
```

## Usage

Define a class that inherit from `scoped.BaseConcern` and define the instance  method `execute` which will perform the scoped task you want to encapsulate, returning `self.success` with a dictionary for a successful response or `self.error` with a dictionary specifying which was the error. Then you call the __class method__ `run`

A good practice is to catch the exceptions that might happen and return an error response making a concern always respond with a `ConcernResponse` object, making it predictable.

```Python
from scoped import BaseConcern
from models import User

class CreateUser(BaseConcern):
  def execute(self):
    try:
      session = User.query.session
      user = User.run(first_name = self.first_name, last_name = self.last_name, email = self.email) 

      session.add(user)

      session.commit()

      return self.success({ "user": user })
    except Exception as e:
      return self.error({ "user": repr(e), "backtrace": traceback.format_exc })
```

Then you could use this `Concern` in a Flask app, for example:

```Python
from flask import current_app, jsonify
from users.concerns import CreateUser

@users.route("/users", methods=["POST"])
def create_user():
  params = request.json

  response = CreateUser.run(params)

  if response.is_success():
    return jsonify(response.result["user"]), 201
  else:
    current_app.logger.error("Error creating user: {}".format(response.errors))
    return { "message": "Internal Server Error", 500 }
```

## Asynchronous Concern

The library provides also the `AsyncConcern` to be used as the base class when you need to perform asyncio operations. It behaves exactly the same as the `BaseConcern` class, except that you need to `await` the `run` execution. For example:

```Python
from scoped import AsyncConcern

class FetchUsers(AsyncConcern):
  async def execute(self):
    url = "{}/users".format(SERVICE_BASE_URL)

    async with client.get(url, ssl=ssl_ctx) as resp:
      try:
        body = await resp.json()

        if resp.status == 200:
          return self.success({ "users": body })
        else:
          return self.error({ "fetch": body })
...

response = await FetchUsers.run()
```

## Response
A scoped concern should always return a `ConcernResponse` object, for this, the `BaseConcern` class provides the `success` and `error` methods that will create the right object with the `result` or `errors` attributes set accordingly.
The `ConcernResponse` class provides the `is_success()` instance utility method for readability's sake.
