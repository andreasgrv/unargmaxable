import os
import datetime

from collections import defaultdict
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event, select, func
from sqlalchemy.ext.hybrid import hybrid_property

from stollen.server.utils import Hasher


db = SQLAlchemy()
hasher = Hasher(salt=None)


def compute_hexid(mapper, connection, target):
    # Since we want to use hexid to check for duplicates
    # we only encode attributes we assume flag duplicates
    kwargs = {k: getattr(target, k) for k in target.core_attrs}
    target.hexid = hasher.hash_as_hex(**kwargs)


class Experiment(db.Model):
    """Represents a run of the stollen detection algorithm on a model"""

    __tablename__ = 'experiment'

    id = db.Column(db.Integer,
                   db.Sequence('experiment_id_seq'),
                   primary_key=True)

    hexid = db.Column(db.String(16), index=True, nullable=False)
    algorithm = db.Column(db.String, nullable=False)
    started = db.Column(db.DateTime, index=True, nullable=False)
    finished = db.Column(db.DateTime, index=True, nullable=True)
    patience = db.Column(db.Integer, index=True, nullable=True)
    num_bounded = db.Column(db.Integer, index=True, nullable=True)
    misc = db.Column(db.JSON)

    model = db.relationship('Model', uselist=False,
                            back_populates='experiment')
    results = db.relationship('Result',
                              back_populates='experiment',
                              passive_deletes='all')

    core_attrs = ['algorithm', 'patience', 'model_id']

    def __init__(self,
                 algorithm=None,
                 started=None,
                 finished=None,
                 patience=None,
                 num_bounded=None,
                 model=None,
                 results=None,
                 **kwargs):
        super().__init__()
        self.algorithm = algorithm
        self.started = started
        self.finished = finished
        self.patience = patience
        self.num_bounded = num_bounded
        self.model = model
        self.results = results
        self.misc = kwargs

    @property
    def model_id(self):
        return self.model.id

    def as_dict(self):
        return dict(id=self.id,
                    hexid=self.hexid,
                    algorithm=self.algorithm,
                    started=self.started,
                    finished=self.finished,
                    patience=self.patience,
                    model=self.model.as_dict(),
                    num_bounded=self.num_bounded,
                    misc=self.misc)


class Model(db.Model):
    """Represents a model being evaluated for stolen probability"""

    __tablename__ = 'model'

    id = db.Column(db.Integer,
                   db.Sequence('model_id_seq'),
                   primary_key=True)

    hexid = db.Column(db.String(16), index=True, nullable=False)
    name = db.Column(db.String, index=True, nullable=False)
    task = db.Column(db.String, nullable=False)
    vocab_size = db.Column(db.Integer, index=True, nullable=True)
    embed_dim = db.Column(db.Integer, index=True, nullable=True)
    has_bias = db.Column(db.Boolean, nullable=False, default=True)
    url = db.Column(db.String, nullable=True)
    misc = db.Column(db.JSON)

    experiment_id = db.Column(db.Integer,
                              db.ForeignKey('experiment.id'),
                              index=True,
                              nullable=False)
    experiment = db.relationship('Experiment', uselist=False,
                                 back_populates='model')

    core_attrs = ['name', 'task', 'vocab_size', 'embed_dim', 'has_bias']

    def __init__(self, name=None, task=None, vocab_size=None, embed_dim=None,
                 has_bias=None, url=None, **kwargs):
        super().__init__()
        self.name = name
        self.task = task
        self.vocab_size = vocab_size
        self.embed_dim = embed_dim
        self.has_bias = has_bias
        self.url = url
        self.misc = kwargs

    def as_dict(self):
        return dict(id=self.id,
                    hexid=self.hexid,
                    name=self.name,
                    task=self.task,
                    vocab_size=self.vocab_size,
                    embed_dim=self.embed_dim,
                    has_bias=self.has_bias,
                    url=self.url,
                    misc=self.misc)


class Result(db.Model):
    """Represents an evaluation of stolen probability for a vocabulary token.
    A detection algorithm is run on a model using a specific set of settings"""

    __tablename__ = 'result'

    id = db.Column(db.Integer,
                   db.Sequence('result_id_seq'),
                   primary_key=True)

    index = db.Column(db.Integer, index=True, nullable=False)
    token = db.Column(db.String, index=True, nullable=False)
    is_bounded = db.Column(db.Boolean, nullable=False, default=True)
    iterations = db.Column(db.Integer, nullable=True)
    misc = db.Column(db.JSON)

    experiment_id = db.Column(db.Integer,
                              db.ForeignKey('experiment.id', ondelete='CASCADE'),
                              index=True,
                              nullable=False)
    experiment = db.relationship('Experiment', back_populates='results')

    time_taken = db.Column(db.Float, nullable=True)

    solution = db.relationship('Solution', uselist=False, back_populates='result')

    def __init__(self,
                 index=None,
                 token=None,
                 is_bounded=None,
                 iterations=None,
                 time_taken=None,
                 solution=None,
                 **kwargs):
        super().__init__()
        self.index = index
        self.token = token
        self.is_bounded = is_bounded
        self.iterations = iterations
        self.time_taken = time_taken
        self.solution = solution
        self.misc = kwargs

    def as_dict(self, include_solution=False):
        if include_solution:
            solution = None
        else:
            solution = None
        return dict(id=self.id,
                    index=self.index,
                    token=self.token,
                    is_bounded=self.is_bounded,
                    iterations=self.iterations,
                    time_taken=self.time_taken,
                    solution=None,
                    misc=self.misc)


class Solution(db.Model):
    """Represents a solution for a particular result"""

    __tablename__ = 'solution'

    id = db.Column(db.Integer,
                   db.Sequence('solution_id_seq'),
                   primary_key=True)

    point = db.Column(db.PickleType, nullable=True)
    misc = db.Column(db.JSON)

    result_id = db.Column(db.Integer,
                          db.ForeignKey('result.id'),
                          index=True,
                          nullable=False)
    result = db.relationship('Result', uselist=False,
                             back_populates='solution')

    def __init__(self,
                 point=None,
                 **kwargs):
        super().__init__()
        self.point = point

event.listen(Experiment, 'before_insert', compute_hexid)
event.listen(Experiment, 'before_update', compute_hexid)
event.listen(Model, 'before_insert', compute_hexid)
event.listen(Model, 'before_update', compute_hexid)
