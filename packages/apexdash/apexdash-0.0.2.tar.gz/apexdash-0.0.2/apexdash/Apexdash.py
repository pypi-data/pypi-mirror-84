# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class Apexdash(Component):
    """An Apexdash component.
ExampleComponent is an example component.
It takes a property, `label`, and
displays it.
It renders an input with the property `value`
which is editable by the user.

Keyword arguments:
- id (string; default 'defaultid'): The ID used to identify this component in Dash callbacks.
- options (dict; default {
chart: {
  id: 'sparkline1',
  group: 'sparklines',
  type: 'area',
  height: 160,
  sparkline: {
    enabled: true
  },
},
stroke: {
  curve: 'straight'
},
fill: {
  opacity: 1,
},
series: [{
  name: 'Sales',
  data: [30, 40, 45, 50, 49, 60, 70, 91]
}],
labels: [...Array(8).keys()].map(n => `2018-09-0${n+1}`),
yaxis: {
  min: 0
},
xaxis: {
  type: 'datetime',
},
colors: ['#008FFB'],
title: {
  text: '$424,652',
  offsetX: 30,
  style: {
    fontSize: '24px',
    cssClass: 'apexcharts-yaxis-title'
  }
},
subtitle: {
  text: 'Sales',
  offsetX: 30,
  style: {
    fontSize: '14px',
    cssClass: 'apexcharts-yaxis-title'
  }
}
}): The value displayed in the input.
- type (string; default 'area')
- series (list; default [
  {
    name: "series-1",
    data: [30, 40, 45, 50, 49, 60, 70, 91]
  }
])
- width (string; default '200')
- height (string; default '200')"""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, options=Component.UNDEFINED, type=Component.UNDEFINED, series=Component.UNDEFINED, width=Component.UNDEFINED, height=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'options', 'type', 'series', 'width', 'height']
        self._type = 'Apexdash'
        self._namespace = 'apexdash'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'options', 'type', 'series', 'width', 'height']
        self.available_wildcard_properties =            []

        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}

        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(Apexdash, self).__init__(**args)
