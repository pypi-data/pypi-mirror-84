import argparse
import collections
import fiddler
import json

# py.test :

# Details of a request sent by Fiddler client
RequestInfo = collections.namedtuple(
    'RequestInfo', ['url', 'token', 'data', 'json_encoder']
)


class InMemorySender:
    def __init__(self):
        self.incoming = []

    def send(self, api_endpoint, token, data, json_encoder=None):
        self.incoming.append(RequestInfo(api_endpoint, token, data, json_encoder))


def test_range_violations():
    test_col = fiddler.core_objects.Column(
        name='test_col',
        data_type=fiddler.DataType.FLOAT,
        value_range_min=-0.403104259419519,
        value_range_max=0.403104259419519,
    )
    # this should return False due to default epsilon of 10^-9
    assert not test_col.violation_of_value(-0.40310425941951944)
    # this should return True since the value is significantly smaller than min
    assert test_col.violation_of_value(-0.41310425941951944)
    # this should return False due to default epsilon of 10^-9
    assert not test_col.violation_of_value(0.40310425941951944)
    # this should return True since the value is significantly larger than max
    assert test_col.violation_of_value(0.41310425941951944)


def test_is_greater_than_max_value_r_insig_large():
    assert not fiddler.core_objects.is_greater_than_max_value(
        0.40310425941951944, 0.403104259419519
    )


def test_is_greater_than_max_value_r_sig_large():
    assert fiddler.core_objects.is_greater_than_max_value(
        0.40311425941951944, 0.403104259419519
    )


def test_is_less_than_min_value_l_insig_smaller():
    assert not fiddler.core_objects.is_less_than_min_value(
        -0.40310425941951944, -0.403104259419519
    )


def test_is_less_than_min_value_l_sig_smaller():
    assert fiddler.core_objects.is_less_than_min_value(
        -0.41310425941951944, -0.403104259419519
    )


def test_publish_event():
    test_req = RequestInfo(
        url='https://api.fiddler.ai/external_event/' 'test_org/test_project/test_model',
        token='test_token',
        data={'test_key_1': 'test_value_1'},
        json_encoder=None,
    )

    fdl = fiddler.Fiddler('test_token', 'test_org', 'test_project', 'test_model')

    sender = InMemorySender()
    fdl._sender = sender

    fdl.publish_event(test_req.data)

    assert sender.incoming[-1] == test_req


class CustomEncoder(json.JSONEncoder):
    pass


# Manual testing with real service


def manual_test(args):
    """Manual test of publish() with actual server"""
    fdl = fiddler.Fiddler(args.token, args.org, args.project, args.model)
    fdl.publish_event(json.loads(args.data))


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(description='Utility for manual tests')

    arg_parser.add_argument('--org')
    arg_parser.add_argument('--project')
    arg_parser.add_argument('--model')
    arg_parser.add_argument('--token')
    arg_parser.add_argument('--data')

    manual_test(arg_parser.parse_args())
