from pathlib import PurePath
from typing import Dict, List, Optional

from labml.internal.logger.store.indicators import Indicator
from labml.internal.logger.store.indicators.artifacts import Artifact
from labml.internal.logger.store.indicators.numeric import Scalar

from .indicators.factory import load_indicator_from_dict, create_default_indicator
from .namespace import Namespace
from ..writers import Writer
from ... import util
from ...lab import lab_singleton, LabYamlNotfoundError
from ...util import strings


class Store:
    dot_indicators: Dict[str, Indicator]
    namespaces: List[Namespace]
    indicators: Dict[str, Indicator]

    def __init__(self):
        self.indicators = {}
        self.dot_indicators = {}
        self.__indicators_file = None
        self.namespaces = []
        try:
            for ind in lab_singleton().indicators:
                self.add_indicator(load_indicator_from_dict(ind))
        except LabYamlNotfoundError:
            pass

        self.is_indicators_updated = True

    def save_indicators(self, writers: List[Writer], file: Optional[PurePath] = None):
        if not self.is_indicators_updated:
            return
        self.is_indicators_updated = False
        if file is None:
            if self.__indicators_file is None:
                return
            file = self.__indicators_file
        else:
            self.__indicators_file = file

        wildcards = {k: ind.to_dict() for k, ind in self.dot_indicators.items()}
        inds = {k: ind.to_dict() for k, ind in self.indicators.items()}
        with open(str(file), "w") as file:
            file.write(util.yaml_dump({'wildcards': wildcards,
                                       'indicators': inds}))

        for w in writers:
            w.save_indicators(self.dot_indicators, self.indicators)

    def __assert_name(self, name: str, value: any):
        if name.endswith("."):
            if name in self.dot_indicators:
                assert self.dot_indicators[name].equals(value)

        assert name not in self.indicators, f"{name} already used"

    def namespace_enter(self, ns: Namespace):
        self.namespaces.append(ns)

    def namespace_exit(self, ns: Namespace):
        if len(self.namespaces) == 0:
            raise RuntimeError("Impossible")

        if ns is not self.namespaces[-1]:
            raise RuntimeError("Impossible")

        self.namespaces.pop(-1)

    def add_indicator(self, indicator: Indicator):
        self.dot_indicators[indicator.name] = indicator
        self.is_indicators_updated = True

    def _create_indicator(self, key: str, value: any):
        if key in self.indicators:
            return

        ind_key, ind_score = strings.find_best_pattern(key, self.dot_indicators.keys())
        if ind_key is None:
            raise ValueError(f"Cannot find matching indicator for {key}")
        if ind_score == 0:
            is_print = self.dot_indicators[ind_key].is_print
            self.indicators[key] = create_default_indicator(key, value, is_print)
        else:
            self.indicators[key] = self.dot_indicators[ind_key].copy(key)
        self.is_indicators_updated = True

    def store(self, key: str, value: any):
        if key.endswith('.'):
            key = '.'.join([key[:-1]] + [ns.name for ns in self.namespaces])

        self._create_indicator(key, value)
        self.indicators[key].collect_value(value)

    def clear(self):
        for k, v in self.indicators.items():
            v.clear()

    def write(self, writer: Writer, global_step):
        return writer.write(global_step=global_step,
                            indicators=self.indicators)

    def create_namespace(self, name: str):
        return Namespace(store=self,
                         name=name)
