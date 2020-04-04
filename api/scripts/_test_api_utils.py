import _test_script_utils

def assert_response_is_not_error (response):
    assert not 'error' in response, response['error']

def assert_and_print_response (response, prefix = None):
    assert_response_is_not_error(response)
    _test_script_utils.print_obj_simple (response, prefix)
