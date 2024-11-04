import unittest
from main import convert_input


class TestExample(unittest.TestCase):

    def test_convert_input(self):
        test_input = convert_input("rpm")
        assert test_input == \
          '[{"type": "rpm", "options": {"ssl": {"client_key": null, "client_cert": null, "ca_bundle": null, "verify": 1}}}]'

        test_input = convert_input("gomod")
        assert test_input == '[{"type": "gomod"}]'

        test_input = convert_input("gomod")
        assert test_input == '[{"type": "gomod"}]'

        test_input = convert_input('{"type": "rpm", "options": {"ssl": {"verify": 0 }}}')
        assert test_input == '[{"type": "rpm", "options": {"ssl": {"client_key": null, "client_cert": null, "ca_bundle": null, "verify": 0}}}]'

        test_input = convert_input('{"type": "rpm", "options": {"dnf_options": {"foo": "bar" }}}')
        assert test_input == '[{"type": "rpm", "options": {"dnf_options": {"foo": "bar"}, "ssl": {"client_key": null, "client_cert": null, "ca_bundle": null, "verify": 1}}}]'

        input1 = '{"type": "rpm", "options": {"ssl": {"verify": 0 }}}'
        input2 = '{"type": "rpm"}'

        test_input = convert_input("[%s, %s]" % (input1, input2))
        assert test_input == '[{"type": "rpm", "options": {"ssl": {"client_key": null, "client_cert": null, "ca_bundle": null, "verify": 0}}}, {"type": "rpm", "options": {"ssl": {"client_key": null, "client_cert": null, "ca_bundle": null, "verify": 1}}}]'

        test_input = convert_input('[{"type": "rpm"},{"type": "gomod"}]')
        assert test_input == '[{"type": "rpm", "options": {"ssl": {"client_key": null, "client_cert": null, "ca_bundle": null, "verify": 1}}}, {"type": "gomod"}]'
