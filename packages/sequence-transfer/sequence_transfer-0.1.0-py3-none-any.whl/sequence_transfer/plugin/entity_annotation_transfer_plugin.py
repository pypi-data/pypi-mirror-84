from inspect import signature

from sequence_transfer.magic_transfer import MagicTransfer
from typing import List, Tuple, Optional, Iterator
from sequence_transfer.sequence import  SequenceContext, ContextualizedSequence
from itertools import groupby, filterfalse
from sequence_transfer.sequence_transfer import SequenceTransferPlugin
import uuid


# BILUO


class InvalidBILUOCodeException(Exception):
    def __init__(self, code: str):
        super().__init__(f"Invalid BILUO code {code}")


class InvalidBILUOAnnotationException(Exception):
    def __init__(self, annotation: str):
        super().__init__(f"Invalid BILUO {annotation}")


class InvalidBILUOAnnotationSequenceException(Exception):
    def __init__(self, line: int):
        super().__init__(f"Invalid BILUO sequence at line {line}")


class Annotation:
    def __init__(self, label, namespace):
        """
        An annotation is a label in a namespace
        :param label:
        :param namespace:
        """
        self._label = label
        self._namespace = namespace

    def get_label(self):
        return self._label
    label = property(get_label)

    def get_namespace(self):
        return self._namespace
    namespace = property(get_namespace)


class EntityAnnotationBase:
    """
    An entity is a sequence (without holes) of signs. A token is a sign, a letter is a sign.
    A sequence of two tokens could be an entity
    An annotation is a label in some namespace
    An EntityAnnotation is an annotation associated with an entity. (more exactly with the id of an entity)
    """
    def __init__(self, annotation: Annotation, entity_id: Optional[str]):
        self._annotation = annotation
        self._entity_id = entity_id

    def get_annotation(self):
        return self._annotation
    annotation = property(get_annotation)

    def get_entity_id(self):
        return self._entity_id
    entity_id = property(get_entity_id)

    def get_signature(self):
        return self._annotation.namespace + '/' + self._annotation.label + '/' + self._entity_id
    signature = property(get_signature)

    def __repr__(self):
        return self.get_signature()


class EntityAnnotation(EntityAnnotationBase):
    def __init__(self, annotation: str, entity_id: Optional[str]):
        super().__init__(Annotation(annotation, ANNOTATION_NAMESPACE_PUBLIC), entity_id)


ANNOTATION_NAMESPACE_PUBLIC = 'public'
ANNOTATION_NAMESPACE_CORE = 'core'
UNDEFINED_ANNOTATION = EntityAnnotationBase(Annotation('undefined', ANNOTATION_NAMESPACE_CORE), "")
NOT_ANNOTATED = EntityAnnotationBase(Annotation('no-annotation', ANNOTATION_NAMESPACE_CORE), "")


class AnnotationSequenceContext(SequenceContext):
    def __init__(self, context: List[EntityAnnotationBase]):
        super().__init__(context)


class EntityAnnotationSequence(ContextualizedSequence):
    BILUO = 'biluo'

    @staticmethod
    def new(annotations: List[str], annotation_sequence_format: str = BILUO):
        if annotation_sequence_format == EntityAnnotationSequence.BILUO:
            return EntityAnnotationSequence(
                0,
                len(annotations),
                AnnotationSequenceContext(
                    EntityAnnotationSequence.biluo_annotations_to_entity_annotations(annotations)))
        else:
            raise ValueError('Invalid sequence format')

    def __init__(self, start: int, stop: int, context: AnnotationSequenceContext):
        super().__init__(start, stop, context)

    def convert(self, annotation_sequence_format):
        if annotation_sequence_format == EntityAnnotationSequence.BILUO:
            return EntityAnnotationSequence.entity_annotations_to_biluo_annotations(self._context.content)
        return

    def get_annotated_entities(self) -> List["EntityAnnotationSequence"]:
        z = filterfalse(lambda signature,y :  signature != NOT_ANNOTATED.signature,
            groupby(self._context.content, key=lambda a: a.signature))
        print(z)

    @staticmethod
    def biluo_annotations_to_entity_annotations(biluo_annotations: List[str]):
        new_annotations = []
        tmp = None
        for i, annotation in enumerate(biluo_annotations):
            if annotation == 'O':
                new_annotations.append(NOT_ANNOTATED)
            else:
                try:
                    code, tag = annotation.split('-')
                except Exception:
                    raise InvalidBILUOAnnotationException(annotation)
                if code not in {'B', 'I', 'L', 'U'}:
                    raise InvalidBILUOCodeException(code)

                if code == 'B' or code == 'U':
                    if tmp is not None:
                        raise InvalidBILUOAnnotationSequenceException(i)
                    tmp = str(uuid.uuid4())

                new_annotations.append(EntityAnnotation(tag, tmp))

                if code == 'L' or code == 'U':
                    tmp = None

                # TODO raise error for an eventual missing L at the end.
                # TODO More checks... THINK
        return new_annotations

    @staticmethod
    def entity_annotations_to_biluo_annotations(annotations: List[EntityAnnotation]):
        new_annotations = []

        for signature, group in groupby(annotations, key=lambda a: a.signature):
            group = list(group)
            if signature == NOT_ANNOTATED.signature:
                for _ in group:
                    new_annotations.append('O')
            else:
                for i, annotation in enumerate(group):
                    if i == 0:
                        if len(group) == 1:
                            code = 'U'
                        else:
                            code = 'B'
                    elif i == len(group) - 1:
                        code = 'L'
                    else:
                        code = 'I'
                    new_annotations.append(code + '-' + annotation.annotation.label)

        return new_annotations


class EntityAnnotationTransferPlugin(SequenceTransferPlugin):
    def apply(self, transfer, annotation_sequence: EntityAnnotationSequence) -> EntityAnnotationSequence:
        if annotation_sequence.size != transfer.source.size:
            raise ValueError("Annotation sequence size != transfer source size")  # TODO custom exception

        source = transfer.source
        target = transfer.target
        inverse_transfer = transfer.invert()

        transferred_annotations = map(self.handle_conflicts,
                                      map(lambda s: list(zip(
                                          annotation_sequence.materialize(s),
                                          [len(source.get_text(sub)) for sub in s]
                                      )), map(inverse_transfer.apply, target)))

        z = self.handle_undefined(transferred_annotations)
        return EntityAnnotationSequence(0, len(z), AnnotationSequenceContext(z))

    @staticmethod
    def handle_conflicts(weighted_annotations: Iterator[Tuple[EntityAnnotationBase, int]]) -> EntityAnnotationBase:
        """
        Resolve conflicts between annotations. All annotations have a weight related to the text size
        TODO:  ##e->weight 3  or &amp;->5
        :param weighted_annotations:
        :return:
        """
        if not weighted_annotations:
            return UNDEFINED_ANNOTATION
        best = None
        max_score = -1
        for _, group_with_same_id in groupby(weighted_annotations,
                                             key=lambda weighted_annotation: weighted_annotation[0].signature):
            group_with_same_id = list(group_with_same_id)
            group_score = 0
            for _, weight in group_with_same_id:
                group_score += weight
            if group_score > max_score:
                best = group_with_same_id[0][0]
                max_score = group_score
        return best

    @staticmethod
    def handle_undefined(annotations: Iterator[EntityAnnotation]) -> List[EntityAnnotation]:
        """
        :param annotations:
        :return:
        """
        new_annotations = []
        undefined = 0
        for i, (signature, group) in enumerate(groupby(annotations, key=lambda a: a.signature)):
            if signature == UNDEFINED_ANNOTATION.signature:
                if i == 0:
                    # undefined at start
                    for _ in group:
                        new_annotations.append(NOT_ANNOTATED)
                else:
                    undefined = len(list(group))
            else:
                for annotation in group:
                    if undefined:
                        interpolate = new_annotations[-1].signature == annotation.signature
                        while undefined:
                            if interpolate:
                                new_annotations.append(annotation)
                            else:
                                new_annotations.append(NOT_ANNOTATED)
                            undefined -= 1
                    new_annotations.append(annotation)

        # Remaining undefined
        for i in range(undefined):
            new_annotations.append(NOT_ANNOTATED)

        return new_annotations




