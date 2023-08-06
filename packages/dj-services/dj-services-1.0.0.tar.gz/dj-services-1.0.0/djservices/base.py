"""This module includes base services classes

Notes
-----
To use services you need to create `services.py` module in your app and
create `BaseService` subclasses in it. Services must have `model` attribute
and `strategy_class` if it's not setted in service class and if you want
to use strategies in your service

"""

from __future__ import annotations
from typing import Any

from django.forms import Form

from .strategies import FormsCRUDStrategy


class BaseService:

    """Base services class

    Attributes
    ----------
    strategy_class : BaseStrategy subclass
        A BaseStrategy subclass with mutable functionality
    model : Model
        A model using in service logic
    self.strategy : `strategy_class` instance
        A BaseStrategy instance created in constructor using
        `strategy_class`

    Examples
    --------
    To use this service you need to subclass it and set `model`
    and `strategy_class` attributes if you want to use strategies in
    your service, and add some methods:

    >>> class MyService(BaseService):
    ...     model = MyModel
    ...     strategy_class = MyStrategy
    ...
    ...     def do_some_logic(self, *args, **kwargs):
    ...         return self.strategy.do_some_logic(*args, **kwargs)
    ...

    If arguments other than `model` must be passed to the constructor
    of your strategy you can add them to the `_get_strategy_args()` method:

    >>> class MyService(BaseService):
    ...     model = MyModel
    ...     strategy_class = MyStrategy
    ...     another_attribute = Something
    ...
    ...     def _get_strategy_args(self):
    ...         args = (self.another_attribute,)
    ...         return super()._get_strategy_args() + args
    ...

    Or if you want to use service without strategy you can just define
    `model` attribute:

    >>> class MyService(BaseService):
    ...     model = MyModel
    ...
    ...     def do_some_logic(self):
    ...         pass

    """

    strategy_class = None
    model = None

    def __init__(self) -> None:
        if not self.model:
            raise AttributeError("You need to set `model` attribute")

        if self.strategy_class:
            self.strategy = self.strategy_class(*self._get_strategy_args())

    def _get_strategy_args(self) -> tuple:
        """Returns tuple with arguments for strategy constructor

        Returns
        -------
        Tuple with `model` attribute value. It's default behavior

        """
        return (self.model,)


class BaseCRUDService(BaseService):

    """Base class for CRUD services

    Attributes
    ----------
    Each CRUD service must define the following attributes:

    strategy_class : BaseCRUDStrategy subclass
        Strategy class with CRUD functionality realization
    model : Model
        Django model service works with

    Methods
    -------
    All these methods are default for CRUD strategies. In this service
    all these methods delegate control to strategy methods

    get_all()
        Returns all model entries
    get_concrete()
        Returns a concrete model entry
    create()
        Creates a new model entry
    change()
        Changes a concrete model entry
    delete()
        Deletes a concrete model entry

    Examples
    --------
    If your CRUD strategy doesn't have other then default 5 methods
    you can just subclass this class and define `strategy_class` and
    `model` attributes:

    >>> class MyCRUDService(BaseCRUDService):
    ...     strategy_class = MyCRUDStrategy
    ...     model = MyModel
    ...

    But if your CRUD strategy has other than default methods you need to
    define non-default methods in your service and delegate control to
    strategy in them

    >>> class MyCRUDService(BaseCRUDService):
    ...     strategy_class = MyCRUDStrategy
    ...     model = MyModel
    ...
    ...     def do_some_logic(self, *args, **kwargs):
    ...         return self.strategy.do_some_logic(*args, **kwargs)

    """

    strategy_class = None
    model = None

    def __init__(self) -> None:
        if not self.strategy_class:
            raise AttributeError(
                "You need to set `strategy_class` attribute"
            )

        super().__init__()

    def get_all(self, *args, **kwargs) -> Any:
        return self.strategy.get_all(*args, **kwargs)

    def get_concrete(self, *args, **kwargs) -> Any:
        return self.strategy.get_concrete(*args, **kwargs)

    def create(self, *args, **kwargs) -> Any:
        return self.strategy.create(*args, **kwargs)

    def change(self, *args, **kwargs) -> Any:
        return self.strategy.change(*args, **kwargs)

    def delete(self, *args, **kwargs) -> Any:
        return self.strategy.delete(*args, **kwargs)


class CRUDService(BaseCRUDService):

    """Service with CRUD functionality using `FormsCRUDStrategy`

    Attributes
    ----------
    strategy_class : FormsCRUDStrategy
        Strategy with CRUD functionality
    form : |Form|
        A form using in strategy logic for validating data

    Methods
    -------
    get_create_form(*args, **kwargs)
        Returns form for creating a new model entry
    get_change_form(*args, **kwargs)
        Returns form with entry data for changing that entry

    Examples
    --------
    To use this services you need to subclass it and set `model` and `form`
    attributes:

    >>> class MyService(CRUDService):
    ...     model = MyModel
    ...     form = MyModelForm
    ...

    After that you can use this service in Django views. For example,
    you can make Django's ListView analog:

    >>> def list_view(request):
    ...     service = MyService()
    ...     entries = service.get_all()
    ...     return render(request, 'entries.html', {'entries': entries})
    ...

    """

    strategy_class = FormsCRUDStrategy
    form = None

    def __init__(self) -> None:
        if not self.form:
            raise AttributeError("You need to set `form` attribute")

        super().__init__()

    def _get_strategy_args(self) -> tuple:
        """Returns tuple with default attributes and `form` because `form`
        attribute is necessary for CRUD strategies
        """
        args = (self.form,)
        return super()._get_strategy_args() + args

    def get_create_form(self, *args, **kwargs) -> Form:
        """Returns form for creating a new model entry calling
        `get_create_form` strategy method
        """
        return self.strategy.get_create_form(*args, **kwargs)

    def get_change_form(self, *args, **kwargs) -> Form:
        """Returns form with entry data for changing that entry
        calling `get_change_form` strategy method
        """
        return self.strategy.get_change_form(*args, **kwargs)
