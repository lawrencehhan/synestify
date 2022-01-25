import os
from pathlib import Path
from src.tasks.task_image_analysis import get_image_df

class TestImageAnalysis():

    base_path = Path(__file__).parent.parent
    img_path = os.path.join(base_path, 'assets', 'test_image_01_kyoto.jpg')

    def test_get_2d_image(self):
        twoDArray = get_image_df(self.img_path)
        # assert(twoDArray.shape, (15993586,3))
        