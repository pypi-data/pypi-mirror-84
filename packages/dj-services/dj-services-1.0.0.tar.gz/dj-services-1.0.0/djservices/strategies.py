"""This module includes base services strategies

Notes
-----
Each strategy must be a subclass of `BaseStrategy` class. Each strategy
has a `model` attribute to work with database. Strategies using in
services in `strategy` attribute

"""

from __future__ import annotations
from typing import Any

from django.db.models import Model, QuerySet
from django.forms import Form
from django.shortcuts import get_object_or_404


class BaseStrategy:

    """Base class for strategies

    Attributes
    ----------
    self.model : Model
        Model strategy works with. It's for working with DB

    Examples
    --------
    Strategies must be used in services. All you need is to create
    your strategy subclassing `BaseStrategy` and add it in `strategy_class`
    service attribute:

    >>> class MyStrategy(BaseStrategy):
    ...
    ...     def get_all(self):
    ...         return self.model.objects.all()
    ...
    ...
    ... class MyService(BaseService):
    ...     model = MyModel
    ...     strategy_class = MyStrategy
    ...
    ...     def get_all(self):
    ...         return self.strategy.get_all()
    ...

    """

    def __init__(self, model: Model) -> None:
        self.model = model


class BaseCRUDStrategy(BaseStrategy):

    """
    Base abstract class for CRUD strategies. Defines a common
    interface for CRUD strategies

    Methods
    -------
    get_all()
        This method is used in CRUD strategies to get all entries
    get_concrete()
        This method is used in CRUD strategies to get a concrete entry
    create()
        This method is used in CRUD strategies to create a new entry
    change()
        This method is used in CRUD strategies to change a concrete entry
    delete()
        This method is used in CRUD strategies to delete a concrete entry

    Notes
    -----
    Each CRUD strategy must implement 4 methods:

    - get_all()
    - get_concrete()
    - create()
    - change()
    - delete()

    These methods implement CRUD strategy

    """

    def get_all(self, **kwargs) -> Any:
        raise NotImplementedError

    def get_concrete(self, pk: Any, **kwargs) -> Any:
        raise NotImplementedError

    def create(self, data: dict, **kwargs) -> Any:
        raise NotImplementedError

    def change(self, data: dict, pk: Any) -> Any:
        raise NotImplementedError

    def delete(self, pk: Any) -> Any:
        raise NotImplementedError


class FormsCRUDStrategy(BaseCRUDStrategy):

    """Strategy with CRUD functionality using forms for realization

    Attributes
    ----------
    self.form : Form
        Form strategy works with

    Methods
    -------
    get_all(**kwargs)
        Get all model entries
    get_concrete(pk, **kwargs)
        Get a concrete model entry
    create(data, **kwargs)
        Create a new model entry
    change(data, pk)
        Cahange a concrete model entry
    delete(pk)
        Delete a concrete model entry
    get_create_form()
        Return form for creating a new entry
    get_change_form(pk)
        Return form for changing a concrete entry

    """

    def __init__(self, model: Model, form: Form) -> None:
        super().__init__(model)
        self.form = form

    def get_all(self, **kwargs) -> QuerySet:
        """Returns all model entries

        Parameters
        ----------
        kwargs : dict
            Extended parameters for fetching entries

        Examples
        --------
        >>> strategy.get_all(user=request.user)

        This code will return all entries of user

        """
        return self.model.objects.filter(**kwargs)

    def get_concrete(self, pk: Any, **kwargs) -> Model:
        """Returns a concrete model entry

        Parameters
        ----------
        pk : |Any|
            Primary key of the entry
        kwargs : dict
            Extended parameters for fetching a concrete entry

        Examples
        --------
        >>> strategy.get_concrete(pk=1, user=request.user)

        This code will return entry of user `request.user` with pk `1`.
        IF the entry with pk `1` refers to another user, this code will
        raise `Http404`

        """
        return get_object_or_404(self.model, pk=pk, **kwargs)

    def create(self, data: dict, **kwargs) -> Any[Form, Model]:
        """Creates a new model entry from `data`

        Parameters
        ----------
        data : |dict|
            Data from request.POST validating in form
        kwargs : dict
            Extended fields for creating a new entry

        Examples
        --------
        >>> strategy.create(request.POST, user=request.user)

        This code will create a new model entry with data from
        POST parameters and with `user` field `request.user`

        Returns
        -------
        If data is correct, creates an entry and returns it.
        Else returns invalid form

        """
        form = self.form(data)
        if form.is_valid():
            # Don't handle exceptions because Django raises TypeError
            # if kwargs isn't valid
            entry = self.model.objects.create(**form.cleaned_data, **kwargs)
            return entry

        return form

    def _change_entry_fields(self, data: dict, entry: Model) -> None:
        """Changes `entry` fields using `data`"""
        for field in data:
            setattr(entry, field, data[field])

    def change(self, data: dict, pk: Any) -> Any[Form, Model]:
        """Change a model entry with `pk` from `data`

        Parameters
        ----------
        data : |dict|
            Data from request.POST validating in form
        pk : |Any|
            Primary key of the model entry

        Returns
        -------
        Returns changed entry if data is valid, else form with errors

        """
        form = self.form(data)
        if form.is_valid():
            changing_entry = self.get_concrete(pk)
            self._change_entry_fields(form.cleaned_data, changing_entry)
            changing_entry.save()
            return changing_entry

        return form

    def delete(self, pk: Any) -> None:
        """Deletes a concrete model entry with `pk`

        Parameters
        ----------
        pk : |Any|
            Primary key of the model entry

        """
        entry = self.get_concrete(pk)
        entry.delete()

    def get_create_form(self) -> Form:
        """Returns a form to create a new model entry"""
        return self.form()

    def _get_form_data_from_entry(self, entry: Model) -> dict:
        """Returns dict with model entry fields and values for form"""
        fields = self.form.base_fields.keys()
        fields_values = [getattr(entry, field) for field in fields]
        return dict(zip(fields, fields_values))

    def get_change_form(self, pk: Any) -> Form:
        """Returns a form with data from model entry with `pk`

        Parameters
        ----------
        pk : |Any|
            Primary key of the model entry

        """
        changing_entry = self.get_concrete(pk)
        form_data = self._get_form_data_from_entry(changing_entry)
        return self.form(form_data)
