import pytest
from tests.data.create_configs import *
from tests.data.create_images import *


@pytest.mark.run(order=1)
class TestGenerateData:
    """Generating Data"""
    def test_generate_configs(self):
        """Generate Config Files"""
        create_preprocess_config()
        create_none_config()
        create_empty_config()
        create_join_config()

        assert os.path.exists("/tmp/torch-cv-test/config/preprocess.yml")
        assert os.path.exists("/tmp/torch-cv-test/config/empty.yml")
        assert os.path.exists("/tmp/torch-cv-test/config/join.yml")
        assert os.path.exists("/tmp/torch-cv-test/config/none.yml")

    def test_generate_images(self):
        """Generate random images"""
        create_images()

        assert os.path.exists("/tmp/torch-cv-test/original_images/")
        for i in range(5):
            for j in range(10):
                assert os.path.exists("/tmp/torch-cv-test/original_images/{0}/{0}_{1}.jpg".format(i, j))
