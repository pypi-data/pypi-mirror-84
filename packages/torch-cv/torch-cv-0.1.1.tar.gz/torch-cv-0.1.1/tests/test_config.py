import pytest

from torchcv.config import read_config
from .data.create_configs import *

CONFIG_DIR = "/tmp/torch-cv-test/config/"


@pytest.mark.run(order=3)
class TestConfig:
    """Config Readers"""

    @pytest.mark.xfail
    def test_raise_exception_when_file_is_empty(self):
        """Should Fail when config file is empty"""
        read_config(os.path.join(CONFIG_DIR, "empty.yml"))

    def test_none_constructor(self):
        """Field should be None if !none is passed"""
        config = read_config(os.path.join(CONFIG_DIR, "none.yml"))
        assert config.field0 is None

    def test_join_constructor(self):
        """Array should join if used with !join constructor"""
        config = read_config(os.path.join(CONFIG_DIR, "join.yml"))
        assert config.field0 == 'a/b/c'
