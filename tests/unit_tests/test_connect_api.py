from src.tasks.task_connect_api import sampleFunction, getTracks

class TestAPIConnection():

    def test_sample_function(self):
        output = sampleFunction(3)
        assert output == 5

    def test_get_tracks(self):
        track_list = getTracks('drake')
        assert track_list['tracks']['items'][0]['name'] == 'Way 2 Sexy (with Future & Young Thug)'
        assert len(track_list['tracks']['items']) == 20
