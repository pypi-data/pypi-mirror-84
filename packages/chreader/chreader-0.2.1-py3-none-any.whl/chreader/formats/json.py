# -*- coding: utf-8 -*-
import json

from overrides import overrides

from .format import Format


class JsonFormat(Format):
    @overrides
    def decode(self, data: str) -> dict:
        return json.loads(data)
