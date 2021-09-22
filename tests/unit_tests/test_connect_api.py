from synestify.task_connect_api.py import sampleFunction

class TestAPIConnection():

    def test_sample_function(self):
        output = sampleFunction(3)
        assert output == 5