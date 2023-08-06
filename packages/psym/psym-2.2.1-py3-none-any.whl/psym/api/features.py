#!/usr/bin/env python3
# Copyright (c) 2004-present Facebook All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from typing import List

from psym.client import SymphonyClient
from psym.common.constant import GET_FEATURES_URL, SET_FEATURE_URL

from ..exceptions import assert_ok


def get_enabled_features(client: SymphonyClient) -> List[str]:
    """Returns list of the enabled features that are accessible publicly

    :raises:
        AssertionError: Server error

    :return: Enabled features list
    :rtype: List[str]

    **Example**

    .. code-block:: python

        features = client.get_enabled_features()
    """
    resp = client.get(GET_FEATURES_URL)
    assert_ok(resp)
    return list(map(str, resp.json()["features"]))


def set_feature(client: SymphonyClient, feature_id: str, enabled: bool) -> None:
    """Enable or disable given feature if the feature is publicly accessible

    :param feature_id: The feature identifier to set
    :type feature_id: str
    :param enabled: Enabled or disabled flag
    :type enabled: bool

    :raises:
        AssertionError: Server error

    :return: None

    **Example**

    .. code-block:: python

        features = client.get_enabled_features()
        client.set_feature(feature[0], False)
    """
    resp = client.post(SET_FEATURE_URL.format(feature_id), {"enabled": enabled})
    assert_ok(resp)
