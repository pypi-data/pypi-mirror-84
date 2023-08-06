# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['botocove']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.16.12,<2.0.0']

setup_kwargs = {
    'name': 'botocove',
    'version': '0.1.3',
    'description': 'A simple decorator to run functions against all AWS accounts in an organization',
    'long_description': '# botocove\n\nThis is a simple decorator for functions to run them against all AWS accounts in an organization. Wrap a function in `@cove` and inject a session from every AWS account in\nyour org!\n\nCredential requirements are:\nIn the calling account:\n* IAM permissions `sts:assumerole`, `sts:get-caller-identity` and `organizations:list-accounts`\n* From an account that is trusted by other account roles: primarily, an AWS organization master account.\nIn the organization accounts:\n* A trust relationship to the calling account\n* Whatever IAM permisisons your wrapped function is using.\n\n## Quickstart\nWrapping a function that is usually passed a boto3 `session` can now be called with\na `session` from every account required in your AWS organization, assuming a role in\neach account.\n\nFor example:\n\nThis function takes a boto3 `session` and gets the IAM users from an AWS account\n\n```\nimport boto3\n\n\ndef get_iam_users(session):\n    iam = session.client("iam", region_name="eu-west-1")\n    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_users\n    all_users = iam.get_paginator("list_users").paginate().build_full_result()\n\n    return all_users\n\ndef main():\n    session = boto3.session.Session(profile_name="my_dev_account")\n    users = get_iam_users(session)\n    print(users) # A single account\'s IAM users\n```\n\nThis decorated function is not called with a `session` from `main()` and instead has a `session` injected by the decorator for every account your credentials can assume a role in to. It returns a list of every account that can be accessed and their IAM users.\n\n```\nimport boto3\nfrom botocove import cove\n\n# Only required if credentials in the boto3 chain are not suitable\nsession = boto3.session.Session(profile_name="my_org_master")\n\n\n@cove(org_session=session)\ndef get_iam_users(session):\n    iam = session.client("iam", region_name="eu-west-1")\n    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_users\n    all_users = iam.get_paginator("list_users").paginate().build_full_result()\n\n    return all_users\n\ndef main():\n    all_users = get_iam_users()\n    print(all_users) # A list of all responses from IAM\'s list_users API for every account in the AWS organization\n```\n\n## Arguments\n\n`@cove`: Uses boto3 credential chain to get every AWS account within the organization.\nEquivialent to:\n`@cove(target_ids=None, ignore_ids=None, rolename=None, org_session=None)`\n\n`target_ids`: Optional[List[str]]\nA list of AWS accounts as strings to attempt to assume role in to. As\ndefault, attempts to use every available account ID in an AWS organization.\n\n`ignore_ids`: Optional[List[str]]\nA list of AWS account ID\'s that will not attempt assumption in to. Allows IDs to be\nignored. Works with or without `target_ids`.\n\n`rolename`: Optional[str]\nAn IAM role name that will be attempted to assume in all target accounts. Defaults to\nthe AWS default, `OrganizationAccountAccessRole`\n\n`org_session`: Optional[Session]\nA Boto3 `Session` object. If not provided, defaults to standard boto3 credential chain.\n\n### botocove?\n\nIt turns out that the Amazon\'s Boto dolphins are soliditary or small-group animals,\nunlike the large pods of dolphins in the oceans. This killed my "large group of boto"\nidea, so the next best idea was where might they all shelter together... a cove!',
    'author': 'Dave Connell',
    'author_email': 'daveconn41@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/connelldave/botocove',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
