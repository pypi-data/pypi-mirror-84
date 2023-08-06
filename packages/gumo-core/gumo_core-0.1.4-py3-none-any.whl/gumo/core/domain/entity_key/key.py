import dataclasses
from typing import List
from typing import Union
from typing import Optional


@dataclasses.dataclass(frozen=True)
class KeyPair:
    kind: str
    name: Union[str, int]

    def __post_init__(self):
        if not isinstance(self.kind, str):
            raise ValueError(
                f'kind must be an instance of str, but received: {type(self.kind)} (value: {self.kind})'
            )

        if not (isinstance(self.name, str) or isinstance(self.name, int)):
            raise ValueError(
                f'name must be an instance of str or int, but received: {type(self.name)} (value: {self.name})'
            )

        if self.kind.find("'") >= 0 or self.kind.find('"') >= 0:
            raise ValueError(f'Invalid kind of "{self.kind}", do not include quotes in kind')

        if isinstance(self.name, str):
            if self.name.find("'") >= 0 or self.name.find('"') >= 0:
                raise ValueError(f'Invalid name of "{self.name}", do not include quotes in name')

    @classmethod
    def build(cls, kind: str, name: Union[str, int], implicit_id_str: bool = True):
        if implicit_id_str:
            if isinstance(name, str) and name.isdecimal():
                name = int(name)

        return cls(kind=kind, name=name)

    @classmethod
    def build_from_dict(cls, doc: dict):
        if 'kind' not in doc:
            raise ValueError(f'dictionary must have "kind" item, but received doc={doc}')
        if 'name' not in doc and 'id' not in doc:
            raise ValueError(f'dictionary must have "name" or "id" item, but received doc={doc}')

        return cls(doc.get('kind'), doc.get('name', doc.get('id')))

    def is_name(self) -> bool:
        return isinstance(self.name, str)

    def is_id(self) -> bool:
        return isinstance(self.name, int)

    def key_pair_literal(self) -> str:
        if self.is_name():
            return f"'{self.kind}', '{self.name}'"
        else:
            return f"'{self.kind}', {self.name}"


class _BaseKey:
    def parent(self):
        raise NotImplementedError()

    def has_parent(self) -> bool:
        raise NotImplementedError()

    def pairs(self) -> List[KeyPair]:
        return []

    def flat_pairs(self) -> List[Union[str, int]]:
        return []

    def kind(self) -> str:
        raise NotImplementedError()

    def name(self) -> Union[str, int]:
        raise NotImplementedError()

    def key_literal(self) -> str:
        raise NotImplementedError()

    def key_path(self) -> str:
        raise NotImplementedError()

    def key_path_urlsafe(self) -> str:
        raise NotImplementedError()


class NoneKey(_BaseKey):
    _root = None

    @classmethod
    def get_instance(cls):
        if cls._root:
            return cls._root
        cls._root = cls()
        return cls._root

    def parent(self):
        return self

    def has_parent(self) -> bool:
        return False

    def pairs(self):
        return []

    def flat_pairs(self):
        return []

    def kind(self):
        return None

    def name(self):
        return None

    def __repr__(self):
        return "NoneKey(kind='None', name='none')"

    def __eq__(self, other):
        return isinstance(other, self.__class__)

    def key_literal(self):
        return None

    def key_path(self):
        return None

    def key_path_urlsafe(self):
        return None


@dataclasses.dataclass(frozen=True)
class EntityKey(_BaseKey):
    _kind: str
    _name: Union[str, int]
    _parent: object  # type: EntityKey

    def __post_init__(self):
        if not isinstance(self._kind, str):
            raise ValueError(
                f'kind must be an instance of str, but received: {type(self._kind)} (value: {self._kind})'
            )

        if not (isinstance(self._name, str) or isinstance(self._name, int)):
            raise ValueError(
                f'name must be an instance of str or int, but received: {type(self._name)} (value: {self._name})'
            )

        if self._kind.find("'") >= 0 or self._kind.find('"') >= 0:
            raise ValueError(f'Invalid kind of "{self._kind}", do not include quotes in kind')

        if isinstance(self._name, str):
            if self._name.find("'") >= 0 or self._name.find('"') >= 0:
                raise ValueError(f'Invalid name of "{self._name}", do not include quotes in name')

    def is_name(self) -> bool:
        return isinstance(self._name, str)

    def is_id(self) -> bool:
        return isinstance(self._name, int)

    def has_parent(self) -> bool:
        return self._parent is not None

    def parent(self):
        """
        :rtype: EntityKey
        """
        if self.has_parent():
            return self._parent
        else:
            return NoneKey.get_instance()

    def pairs(self):
        pairs = []
        if self.has_parent():
            pairs.extend(self.parent().pairs())
        pairs.append(KeyPair(
            kind=self._kind,
            name=self._name,
        ))
        return pairs

    def flat_pairs(self):
        flat_pairs = []
        for pair in self.pairs():
            flat_pairs.append(pair.kind)
            flat_pairs.append(pair.name)

        return flat_pairs

    def kind(self):
        return self._kind

    def name(self):
        return self._name

    def key_literal(self) -> str:
        return 'Key({})'.format(', '.join([
            pair.key_pair_literal() for pair in self.pairs()
        ]))

    def key_path(self) -> str:
        """
        Returns a structured key separated by `/`
        The kind and name are separated by `:`
        """
        pairs = []
        for pair in self.pairs():
            pairs.append(f'{pair.kind}:{pair.name}')
        return '/'.join(pairs)

    def key_url(self) -> str:
        """
        Returns a structured key separated by / between kind and name.
        This format is suitable for expressing in a form embedded in a URL.
        """
        return '/'.join([
            f'{pair.kind}/{pair.name}' for pair in self.pairs()
        ])

    def key_path_urlsafe(self) -> str:
        return self.key_path().replace('/', '%2F').replace(':', '%3A')


@dataclasses.dataclass(frozen=True)
class IncompleteKey:
    kind: str
    parent: Optional[EntityKey] = None

    def __post_init__(self):
        if not isinstance(self.kind, str):
            raise ValueError(f'kind must be an instance of str, but received {type(self.kind)} (value: {self.kind})')

        if not (self.parent is None or isinstance(self.parent, EntityKey)):
            raise ValueError(
                f'parent must be an instance of EntityKey, but received {type(self.parent)} (value: {self.parent}'
            )

    def flat_pairs(self):
        flat_pairs = self.parent.flat_pairs() if self.parent else []
        flat_pairs.append(self.kind)

        return flat_pairs

    def key_literal(self) -> str:
        if self.parent:
            return 'IncompleteKey({}, {})'.format(
                ', '.join([pair.key_pair_literal() for pair in self.parent.pairs()]),
                self.kind
            )
        return 'IncompleteKey({})'.format(self.kind)
