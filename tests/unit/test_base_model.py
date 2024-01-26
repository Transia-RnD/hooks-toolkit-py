from unittest import TestCase

from hooks_toolkit.libs.binary_models import BaseModel, XRPAddress


class SampleModel(BaseModel):
    def __init__(self, owner: XRPAddress = None):
        self.owner = owner
        super().__init__()

    @staticmethod
    def get_metadata():
        return [{"field": "owner", "type": "xrpAddress"}]


class TestBaseModel(TestCase):
    def test_encode_decode_model(self):
        owner = "rHb9CJAWyB4rj91VRWn96DkukG4bwdtyTh"
        sample = SampleModel(owner)

        sample_encoded = sample.encode()
        sample_decoded = BaseModel.decode(sample_encoded, SampleModel)
        self.assertEqual(sample_decoded.owner, sample.owner)

    def test_get_hex_length(self):
        hex_length = BaseModel.get_hex_length(SampleModel)
        self.assertEqual(hex_length, 40)
