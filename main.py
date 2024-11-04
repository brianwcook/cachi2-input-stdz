import json
import os
import sys


def string_to_json(input: str):
    if input in ["gomod", "pip", "npm", "yarn", "bundler", "rpm"]:
        input = '{"type": "%s"}' % input
        # print("json: %s" % input)
    return input


def json_to_list(input: str):
    input = json.loads(input)
    if type(input) is dict:
        input = [input]
    return json.dumps(input)


def inject_certs(input: str, rhsm_id: str):
    input = json.loads(input)
    if type(input is list):
        cert = ("/shared/rhsm/%s.pem" % rhsm_id)
        key = ("/shared/rhsm/%s-key.pem" % rhsm_id)
        ca_bundle = os.getenv("CA_BUNDLE", None)

        for pkg_man in input:
            if pkg_man["type"] == "rpm":

                # preserve verify setting
                verify = \
                    pkg_man.get("options", {}).get("ssl", {}).get("verify", 1)

                # preserve other options
                options = pkg_man.get('options', {})

                ssl_options = {
                    "client_key": key,
                    "client_cert": cert,
                    "ca_bundle": ca_bundle,
                    "ssl_verify": verify}

                options['ssl'] = ssl_options
                pkg_man["options"] = options
        return (json.dumps(input))

    else:
        # throw an error
        print("boooo!")


def convert_input(input, rhsm_id):
    input = string_to_json(input)
    input = json_to_list(input)
    input = inject_certs(input, rhsm_id)
    return input


if __name__ == '__main__':
    rhsm_id = ""
    input = ""

    try:
        f = open("/shared/RHSM_ID", "r")
        rhsm_id = f.read().strip("\n")
        print("RHSM ID is: %s" % rhsm_id)

    except:
        print("No RHSM ID found.")
        input = sys.argv[1]

    if input == "":
        input = convert_input(sys.argv[1], rhsm_id)

    print("Preprocessing result: %s" % input)
    with open('/shared/preprocessed_input', 'w') as f:
        f.write(input)
