Module mip.widgets.dialogs
==========================

Classes
-------

`PopupRetrieval(**kwargs)`
:   Popup class. See module documentation for more information.
    
    :Events:
        `on_open`:
            Fired when the Popup is opened.
        `on_dismiss`:
            Fired when the Popup is closed. If the callback returns True, the
            dismiss will be canceled.

    ### Ancestors (in MRO)

    * kivy.uix.popup.Popup
    * kivy.uix.modalview.ModalView
    * kivy.uix.anchorlayout.AnchorLayout
    * kivy.uix.layout.Layout
    * kivy.uix.widget.Widget
    * kivy.uix.widget.WidgetBase
    * kivy._event.EventDispatcher
    * kivy._event.ObjectWithUid

    ### Descendants

    * mip.widgets.dialogs.SampleRateDialog

    ### Instance variables

    `retrieval_label`
    :   ObjectProperty(defaultvalue=None, rebind=False, **kw)
        Property that represents a Python object.
        
            :Parameters:
                `defaultvalue`: object type
                    Specifies the default value of the property.
                `rebind`: bool, defaults to False
                    Whether kv rules using this object as an intermediate attribute
                    in a kv rule, will update the bound property when this object
                    changes.
        
                    That is the standard behavior is that if there's a kv rule
                    ``text: self.a.b.c.d``, where ``a``, ``b``, and ``c`` are
                    properties with ``rebind`` ``False`` and ``d`` is a
                    :class:`StringProperty`. Then when the rule is applied, ``text``
                    becomes bound only to ``d``. If ``a``, ``b``, or ``c`` change,
                    ``text`` still remains bound to ``d``. Furthermore, if any of them
                    were ``None`` when the rule was initially evaluated, e.g. ``b`` was
                    ``None``; then ``text`` is bound to ``b`` and will not become bound
                    to ``d`` even when ``b`` is changed to not be ``None``.
        
                    By setting ``rebind`` to ``True``, however, the rule will be
                    re-evaluated and all the properties rebound when that intermediate
                    property changes. E.g. in the example above, whenever ``b`` changes
                    or becomes not ``None`` if it was ``None`` before, ``text`` is
                    evaluated again and becomes rebound to ``d``. The overall result is
                    that ``text`` is now bound to all the properties among ``a``,
                    ``b``, or ``c`` that have ``rebind`` set to ``True``.
                `\*\*kwargs`: a list of keyword arguments
                    `baseclass`
                        If kwargs includes a `baseclass` argument, this value will be
                        used for validation: `isinstance(value, kwargs['baseclass'])`.
        
            .. warning::
        
                To mark the property as changed, you must reassign a new python object.
        
            .. versionchanged:: 1.9.0
                `rebind` has been introduced.
        
            .. versionchanged:: 1.7.0
        
                `baseclass` parameter added.

    ### Methods

    `on_retrieval_label(self, instance, value)`
    :

    `retrieval_completed(self, dt)`
    :

    `update_progress_bar(self, dt)`
    :

`SDCardDialog(**kwargs)`
:   

    ### Ancestors (in MRO)

    * kivy.uix.popup.Popup
    * kivy.uix.modalview.ModalView
    * kivy.uix.anchorlayout.AnchorLayout
    * kivy.uix.layout.Layout
    * kivy.uix.widget.Widget
    * kivy.uix.widget.WidgetBase
    * kivy._event.EventDispatcher
    * kivy._event.ObjectWithUid

    ### Methods

    `update(self)`
    :

`SampleRateDialog(**kwargs)`
:   Popup class. See module documentation for more information.
    
    :Events:
        `on_open`:
            Fired when the Popup is opened.
        `on_dismiss`:
            Fired when the Popup is closed. If the callback returns True, the
            dismiss will be canceled.

    ### Ancestors (in MRO)

    * mip.widgets.dialogs.PopupRetrieval
    * kivy.uix.popup.Popup
    * kivy.uix.modalview.ModalView
    * kivy.uix.anchorlayout.AnchorLayout
    * kivy.uix.layout.Layout
    * kivy.uix.widget.Widget
    * kivy.uix.widget.WidgetBase
    * kivy._event.EventDispatcher
    * kivy._event.ObjectWithUid

    ### Instance variables

    `pb_update`
    :   ObjectProperty(defaultvalue=None, rebind=False, **kw)
        Property that represents a Python object.
        
            :Parameters:
                `defaultvalue`: object type
                    Specifies the default value of the property.
                `rebind`: bool, defaults to False
                    Whether kv rules using this object as an intermediate attribute
                    in a kv rule, will update the bound property when this object
                    changes.
        
                    That is the standard behavior is that if there's a kv rule
                    ``text: self.a.b.c.d``, where ``a``, ``b``, and ``c`` are
                    properties with ``rebind`` ``False`` and ``d`` is a
                    :class:`StringProperty`. Then when the rule is applied, ``text``
                    becomes bound only to ``d``. If ``a``, ``b``, or ``c`` change,
                    ``text`` still remains bound to ``d``. Furthermore, if any of them
                    were ``None`` when the rule was initially evaluated, e.g. ``b`` was
                    ``None``; then ``text`` is bound to ``b`` and will not become bound
                    to ``d`` even when ``b`` is changed to not be ``None``.
        
                    By setting ``rebind`` to ``True``, however, the rule will be
                    re-evaluated and all the properties rebound when that intermediate
                    property changes. E.g. in the example above, whenever ``b`` changes
                    or becomes not ``None`` if it was ``None`` before, ``text`` is
                    evaluated again and becomes rebound to ``d``. The overall result is
                    that ``text`` is now bound to all the properties among ``a``,
                    ``b``, or ``c`` that have ``rebind`` set to ``True``.
                `\*\*kwargs`: a list of keyword arguments
                    `baseclass`
                        If kwargs includes a `baseclass` argument, this value will be
                        used for validation: `isinstance(value, kwargs['baseclass'])`.
        
            .. warning::
        
                To mark the property as changed, you must reassign a new python object.
        
            .. versionchanged:: 1.9.0
                `rebind` has been introduced.
        
            .. versionchanged:: 1.7.0
        
                `baseclass` parameter added.

    `update_widget`
    :   ObjectProperty(defaultvalue=None, rebind=False, **kw)
        Property that represents a Python object.
        
            :Parameters:
                `defaultvalue`: object type
                    Specifies the default value of the property.
                `rebind`: bool, defaults to False
                    Whether kv rules using this object as an intermediate attribute
                    in a kv rule, will update the bound property when this object
                    changes.
        
                    That is the standard behavior is that if there's a kv rule
                    ``text: self.a.b.c.d``, where ``a``, ``b``, and ``c`` are
                    properties with ``rebind`` ``False`` and ``d`` is a
                    :class:`StringProperty`. Then when the rule is applied, ``text``
                    becomes bound only to ``d``. If ``a``, ``b``, or ``c`` change,
                    ``text`` still remains bound to ``d``. Furthermore, if any of them
                    were ``None`` when the rule was initially evaluated, e.g. ``b`` was
                    ``None``; then ``text`` is bound to ``b`` and will not become bound
                    to ``d`` even when ``b`` is changed to not be ``None``.
        
                    By setting ``rebind`` to ``True``, however, the rule will be
                    re-evaluated and all the properties rebound when that intermediate
                    property changes. E.g. in the example above, whenever ``b`` changes
                    or becomes not ``None`` if it was ``None`` before, ``text`` is
                    evaluated again and becomes rebound to ``d``. The overall result is
                    that ``text`` is now bound to all the properties among ``a``,
                    ``b``, or ``c`` that have ``rebind`` set to ``True``.
                `\*\*kwargs`: a list of keyword arguments
                    `baseclass`
                        If kwargs includes a `baseclass` argument, this value will be
                        used for validation: `isinstance(value, kwargs['baseclass'])`.
        
            .. warning::
        
                To mark the property as changed, you must reassign a new python object.
        
            .. versionchanged:: 1.9.0
                `rebind` has been introduced.
        
            .. versionchanged:: 1.7.0
        
                `baseclass` parameter added.

    ### Methods

    `on_retrieval_label(self, instance, value)`
    :

    `retrieval_completed(self, dt)`
    :

    `update(self, instance)`
    :

`SampleRateSelection(**kwargs)`
:   Grid layout class. See module documentation for more information.

    ### Ancestors (in MRO)

    * kivy.uix.gridlayout.GridLayout
    * kivy.uix.layout.Layout
    * kivy.uix.widget.Widget
    * kivy.uix.widget.WidgetBase
    * kivy._event.EventDispatcher
    * kivy._event.ObjectWithUid

    ### Instance variables

    `data_sample_rate_spinner`
    :   ObjectProperty(defaultvalue=None, rebind=False, **kw)
        Property that represents a Python object.
        
            :Parameters:
                `defaultvalue`: object type
                    Specifies the default value of the property.
                `rebind`: bool, defaults to False
                    Whether kv rules using this object as an intermediate attribute
                    in a kv rule, will update the bound property when this object
                    changes.
        
                    That is the standard behavior is that if there's a kv rule
                    ``text: self.a.b.c.d``, where ``a``, ``b``, and ``c`` are
                    properties with ``rebind`` ``False`` and ``d`` is a
                    :class:`StringProperty`. Then when the rule is applied, ``text``
                    becomes bound only to ``d``. If ``a``, ``b``, or ``c`` change,
                    ``text`` still remains bound to ``d``. Furthermore, if any of them
                    were ``None`` when the rule was initially evaluated, e.g. ``b`` was
                    ``None``; then ``text`` is bound to ``b`` and will not become bound
                    to ``d`` even when ``b`` is changed to not be ``None``.
        
                    By setting ``rebind`` to ``True``, however, the rule will be
                    re-evaluated and all the properties rebound when that intermediate
                    property changes. E.g. in the example above, whenever ``b`` changes
                    or becomes not ``None`` if it was ``None`` before, ``text`` is
                    evaluated again and becomes rebound to ``d``. The overall result is
                    that ``text`` is now bound to all the properties among ``a``,
                    ``b``, or ``c`` that have ``rebind`` set to ``True``.
                `\*\*kwargs`: a list of keyword arguments
                    `baseclass`
                        If kwargs includes a `baseclass` argument, this value will be
                        used for validation: `isinstance(value, kwargs['baseclass'])`.
        
            .. warning::
        
                To mark the property as changed, you must reassign a new python object.
        
            .. versionchanged:: 1.9.0
                `rebind` has been introduced.
        
            .. versionchanged:: 1.7.0
        
                `baseclass` parameter added.

    `dismiss_button`
    :   ObjectProperty(defaultvalue=None, rebind=False, **kw)
        Property that represents a Python object.
        
            :Parameters:
                `defaultvalue`: object type
                    Specifies the default value of the property.
                `rebind`: bool, defaults to False
                    Whether kv rules using this object as an intermediate attribute
                    in a kv rule, will update the bound property when this object
                    changes.
        
                    That is the standard behavior is that if there's a kv rule
                    ``text: self.a.b.c.d``, where ``a``, ``b``, and ``c`` are
                    properties with ``rebind`` ``False`` and ``d`` is a
                    :class:`StringProperty`. Then when the rule is applied, ``text``
                    becomes bound only to ``d``. If ``a``, ``b``, or ``c`` change,
                    ``text`` still remains bound to ``d``. Furthermore, if any of them
                    were ``None`` when the rule was initially evaluated, e.g. ``b`` was
                    ``None``; then ``text`` is bound to ``b`` and will not become bound
                    to ``d`` even when ``b`` is changed to not be ``None``.
        
                    By setting ``rebind`` to ``True``, however, the rule will be
                    re-evaluated and all the properties rebound when that intermediate
                    property changes. E.g. in the example above, whenever ``b`` changes
                    or becomes not ``None`` if it was ``None`` before, ``text`` is
                    evaluated again and becomes rebound to ``d``. The overall result is
                    that ``text`` is now bound to all the properties among ``a``,
                    ``b``, or ``c`` that have ``rebind`` set to ``True``.
                `\*\*kwargs`: a list of keyword arguments
                    `baseclass`
                        If kwargs includes a `baseclass` argument, this value will be
                        used for validation: `isinstance(value, kwargs['baseclass'])`.
        
            .. warning::
        
                To mark the property as changed, you must reassign a new python object.
        
            .. versionchanged:: 1.9.0
                `rebind` has been introduced.
        
            .. versionchanged:: 1.7.0
        
                `baseclass` parameter added.

    `update_button`
    :   ObjectProperty(defaultvalue=None, rebind=False, **kw)
        Property that represents a Python object.
        
            :Parameters:
                `defaultvalue`: object type
                    Specifies the default value of the property.
                `rebind`: bool, defaults to False
                    Whether kv rules using this object as an intermediate attribute
                    in a kv rule, will update the bound property when this object
                    changes.
        
                    That is the standard behavior is that if there's a kv rule
                    ``text: self.a.b.c.d``, where ``a``, ``b``, and ``c`` are
                    properties with ``rebind`` ``False`` and ``d`` is a
                    :class:`StringProperty`. Then when the rule is applied, ``text``
                    becomes bound only to ``d``. If ``a``, ``b``, or ``c`` change,
                    ``text`` still remains bound to ``d``. Furthermore, if any of them
                    were ``None`` when the rule was initially evaluated, e.g. ``b`` was
                    ``None``; then ``text`` is bound to ``b`` and will not become bound
                    to ``d`` even when ``b`` is changed to not be ``None``.
        
                    By setting ``rebind`` to ``True``, however, the rule will be
                    re-evaluated and all the properties rebound when that intermediate
                    property changes. E.g. in the example above, whenever ``b`` changes
                    or becomes not ``None`` if it was ``None`` before, ``text`` is
                    evaluated again and becomes rebound to ``d``. The overall result is
                    that ``text`` is now bound to all the properties among ``a``,
                    ``b``, or ``c`` that have ``rebind`` set to ``True``.
                `\*\*kwargs`: a list of keyword arguments
                    `baseclass`
                        If kwargs includes a `baseclass` argument, this value will be
                        used for validation: `isinstance(value, kwargs['baseclass'])`.
        
            .. warning::
        
                To mark the property as changed, you must reassign a new python object.
        
            .. versionchanged:: 1.9.0
                `rebind` has been introduced.
        
            .. versionchanged:: 1.7.0
        
                `baseclass` parameter added.

`TRHConfigurationDialog(**kwargs)`
:   

    ### Ancestors (in MRO)

    * kivy.uix.popup.Popup
    * kivy.uix.modalview.ModalView
    * kivy.uix.anchorlayout.AnchorLayout
    * kivy.uix.layout.Layout
    * kivy.uix.widget.Widget
    * kivy.uix.widget.WidgetBase
    * kivy._event.EventDispatcher
    * kivy._event.ObjectWithUid

    ### Instance variables

    `temperature_rep_spinner`
    :   ObjectProperty(defaultvalue=None, rebind=False, **kw)
        Property that represents a Python object.
        
            :Parameters:
                `defaultvalue`: object type
                    Specifies the default value of the property.
                `rebind`: bool, defaults to False
                    Whether kv rules using this object as an intermediate attribute
                    in a kv rule, will update the bound property when this object
                    changes.
        
                    That is the standard behavior is that if there's a kv rule
                    ``text: self.a.b.c.d``, where ``a``, ``b``, and ``c`` are
                    properties with ``rebind`` ``False`` and ``d`` is a
                    :class:`StringProperty`. Then when the rule is applied, ``text``
                    becomes bound only to ``d``. If ``a``, ``b``, or ``c`` change,
                    ``text`` still remains bound to ``d``. Furthermore, if any of them
                    were ``None`` when the rule was initially evaluated, e.g. ``b`` was
                    ``None``; then ``text`` is bound to ``b`` and will not become bound
                    to ``d`` even when ``b`` is changed to not be ``None``.
        
                    By setting ``rebind`` to ``True``, however, the rule will be
                    re-evaluated and all the properties rebound when that intermediate
                    property changes. E.g. in the example above, whenever ``b`` changes
                    or becomes not ``None`` if it was ``None`` before, ``text`` is
                    evaluated again and becomes rebound to ``d``. The overall result is
                    that ``text`` is now bound to all the properties among ``a``,
                    ``b``, or ``c`` that have ``rebind`` set to ``True``.
                `\*\*kwargs`: a list of keyword arguments
                    `baseclass`
                        If kwargs includes a `baseclass` argument, this value will be
                        used for validation: `isinstance(value, kwargs['baseclass'])`.
        
            .. warning::
        
                To mark the property as changed, you must reassign a new python object.
        
            .. versionchanged:: 1.9.0
                `rebind` has been introduced.
        
            .. versionchanged:: 1.7.0
        
                `baseclass` parameter added.

    `temperature_sample_rate_spinner`
    :   ObjectProperty(defaultvalue=None, rebind=False, **kw)
        Property that represents a Python object.
        
            :Parameters:
                `defaultvalue`: object type
                    Specifies the default value of the property.
                `rebind`: bool, defaults to False
                    Whether kv rules using this object as an intermediate attribute
                    in a kv rule, will update the bound property when this object
                    changes.
        
                    That is the standard behavior is that if there's a kv rule
                    ``text: self.a.b.c.d``, where ``a``, ``b``, and ``c`` are
                    properties with ``rebind`` ``False`` and ``d`` is a
                    :class:`StringProperty`. Then when the rule is applied, ``text``
                    becomes bound only to ``d``. If ``a``, ``b``, or ``c`` change,
                    ``text`` still remains bound to ``d``. Furthermore, if any of them
                    were ``None`` when the rule was initially evaluated, e.g. ``b`` was
                    ``None``; then ``text`` is bound to ``b`` and will not become bound
                    to ``d`` even when ``b`` is changed to not be ``None``.
        
                    By setting ``rebind`` to ``True``, however, the rule will be
                    re-evaluated and all the properties rebound when that intermediate
                    property changes. E.g. in the example above, whenever ``b`` changes
                    or becomes not ``None`` if it was ``None`` before, ``text`` is
                    evaluated again and becomes rebound to ``d``. The overall result is
                    that ``text`` is now bound to all the properties among ``a``,
                    ``b``, or ``c`` that have ``rebind`` set to ``True``.
                `\*\*kwargs`: a list of keyword arguments
                    `baseclass`
                        If kwargs includes a `baseclass` argument, this value will be
                        used for validation: `isinstance(value, kwargs['baseclass'])`.
        
            .. warning::
        
                To mark the property as changed, you must reassign a new python object.
        
            .. versionchanged:: 1.9.0
                `rebind` has been introduced.
        
            .. versionchanged:: 1.7.0
        
                `baseclass` parameter added.

    ### Methods

    `update(self)`
    :