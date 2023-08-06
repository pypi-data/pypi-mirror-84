#    Copyright 2020 Jonas Waeber
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
from typing import Dict, Any

from pywaclient.models.entity import Entity


class Article(Entity):

    def __init__(self, client: 'AragornApiClient', metadata: Dict[str, Any]):
        super().__init__(client, metadata)
        if 'full_render' in self._metadata:
            self._full_render = self._metadata['full_render']
            del self._metadata['full_render']
        else:
            self._full_render = ""

    @property
    def title(self) -> str:
        return self._metadata['title']

    @property
    def category(self) -> str:
        if 'category' in self._metadata:
            return self._metadata['category']['title']
        else:
            return 'NO_CATEGORY'

    @property
    def world_id(self) -> str:
        return self._metadata['world']['id']

    @property
    def full_render(self) -> str:
        return self._full_render

    def to_json(self, indent='    ', ensure_ascii: bool = False, include_full_render: bool = False) -> str:
        if include_full_render:
            self._metadata['full_render'] = self._full_render
        return super().to_json(indent, ensure_ascii)
