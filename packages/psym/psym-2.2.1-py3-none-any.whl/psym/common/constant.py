#!/usr/bin/env python3
# Copyright (c) 2004-present Facebook All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

__version__ = "2.2.1"

SCHEMA_FILE_NAME = "survey_schema.json"
SIMPLE_QUESTION_TYPE_TO_REQUIRED_PROPERTY_NAME = {
    "DATE": "dateData",
    "BOOL": "boolData",
    "EMAIL": "emailData",
    "TEXT": "textData",
    "FLOAT": "floatData",
    "INTEGER": "intData",
    "PHONE": "phoneData",
}

EQUIPMENTS_TO_SEARCH = 10
LOCATIONS_TO_SEARCH = 5
PAGINATION_STEP = 1000
USER_ROLE = 0
SUPERUSER_ROLE = 3

GET_FEATURES_URL = "/features/async/"
SET_FEATURE_URL = "/features/async/{}"
