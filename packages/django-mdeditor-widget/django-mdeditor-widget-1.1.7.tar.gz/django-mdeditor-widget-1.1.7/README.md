django-mdeditor-widget
===

A Markdown editor widget for textarea fields. 


Installation and usage
--------------------

1. Install with pip 

```
pip install django-mdeditor-widget
```

2. Add "mdeditor" to your INSATLLED_APPS setting like: 



```
INSTALLED_APPS = [
    ...
    'mdeditor',
]
```

3. In the form set the wdget to be "MDeditorWidget":

```
self.fields['text'].widget = MDeditorWidget(attrs={'rows': '30'})
```

