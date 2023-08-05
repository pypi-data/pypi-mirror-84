import unittest

from scoped import BaseConcern, ConcernResponse

class HappyConcern(BaseConcern):
    def execute(self):
        return self.success({ "status": "Success" })

class ErrorConcern(BaseConcern):
    def execute(self):
        return self.error({ "error": "This concern errored"})

class AttributesConcern(BaseConcern):
    def execute(self):
        """
        This concern tests the attribute definition.
        It requires:
            first_name
            last_name
            email
        """

        return self.success({
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email
        })


class TestConcerns(unittest.TestCase):
    def test_success_case(self):
        response = HappyConcern.run()

        self.assertEqual(ConcernResponse, type(response))

        self.assertTrue(response.is_success())
        self.assertEqual("Success", response.result["status"])

    def test_error_case(self):
        response = ErrorConcern.run()

        self.assertEqual(ConcernResponse, type(response))

        self.assertFalse(response.is_success())
        self.assertEqual("This concern errored", response.errors["error"])

    def test_attributes_dict(self):
        attrs = { "first_name": "Layne", "last_name": "Staley", "email": "layne@aic.com" }

        response = AttributesConcern.run(attrs)

        self.assertEqual(ConcernResponse, type(response))
        self.assertTrue(response.is_success())

        self.assertEqual(attrs["first_name"], response.result["first_name"])
        self.assertEqual(attrs["last_name"], response.result["last_name"])
        self.assertEqual(attrs["email"], response.result["email"])

    def test_kwargs(self):
        attrs = { "first_name": "Scott", "last_name": "Weiland", "email": "scott@stp.com" }

        response = AttributesConcern.run(
            first_name = attrs["first_name"],
            last_name  = attrs["last_name"],
            email = attrs["email"]
        )

        self.assertEqual(ConcernResponse, type(response))
        self.assertTrue(response.is_success())

        self.assertEqual(attrs["first_name"], response.result["first_name"])
        self.assertEqual(attrs["last_name"], response.result["last_name"])
        self.assertEqual(attrs["email"], response.result["email"])

if __name__ == "__main__":
    unittest.main()
