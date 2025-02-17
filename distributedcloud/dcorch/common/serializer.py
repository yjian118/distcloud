# Copyright 2015 Huawei Technologies Co., Ltd.
# Copyright (c) 2020-2022 Wind River Systems, Inc.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import oslo_messaging

ATTR_NOT_SPECIFIED = object()


class Mapping(object):
    def __init__(self, mapping):
        self.direct_mapping = mapping
        self.reverse_mapping = {}
        for key, value in mapping.items():
            self.reverse_mapping[value] = key

_SINGLETON_MAPPING = Mapping({
    ATTR_NOT_SPECIFIED: "@@**ATTR_NOT_SPECIFIED**@@",
})


class DCOrchSerializer(oslo_messaging.Serializer):
    def __init__(self, base=None):
        super(DCOrchSerializer, self).__init__()
        self._base = base

    def serialize_entity(self, ctxt, entity):
        if isinstance(entity, dict):
            for key, value in entity.items():
                entity[key] = self.serialize_entity(ctxt, value)

        elif isinstance(entity, list):
            for i, item in enumerate(entity):
                entity[i] = self.serialize_entity(ctxt, item)

        elif entity in _SINGLETON_MAPPING.direct_mapping:
            entity = _SINGLETON_MAPPING.direct_mapping[entity]

        if self._base is not None:
            entity = self._base.serialize_entity(ctxt, entity)

        return entity

    def deserialize_entity(self, ctxt, entity):
        if isinstance(entity, dict):
            for key, value in entity.items():
                entity[key] = self.deserialize_entity(ctxt, value)

        elif isinstance(entity, list):
            for i, item in enumerate(entity):
                entity[i] = self.deserialize_entity(ctxt, item)

        elif entity in _SINGLETON_MAPPING.reverse_mapping:
            entity = _SINGLETON_MAPPING.reverse_mapping[entity]

        if self._base is not None:
            entity = self._base.deserialize_entity(ctxt, entity)

        return entity

    def serialize_context(self, ctxt):
        if self._base is not None:
            context = self._base.serialize_context(ctxt)

        return context

    def deserialize_context(self, ctxt):
        if self._base is not None:
            context = self._base.deserialize_context(ctxt)

        return context
