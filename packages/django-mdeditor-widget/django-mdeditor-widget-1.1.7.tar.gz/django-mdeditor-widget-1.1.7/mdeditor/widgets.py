from django import forms
from django.template.loader import get_template

class MDeditorWidget(forms.widgets.Textarea):

    def render(self, name, value, attrs=None, renderer=None, **kwargs): 
        template = get_template('mdeditor/editor.html')

        if 'class' in attrs:
            attrs['class'] += ' mdeditor'
        else:
            attrs['class'] = 'mdeditor'
  
        final_attrs = {
            'rows': 30, 
            'hidden': '',
        }

        final_attrs.update(attrs)
        final_attrs.update(self.attrs)

        widget   = super(MDeditorWidget, self).render(name, value, attrs=final_attrs)
        
        return template.render({
            # 'field_name': name,
            'field_id':   attrs['id'], 
            'field':      widget, 
        })

    class Media:
        css = {
            'all': (
                'mdeditor/css/mdeditor.css',
            )
        }
    
        js = (
            'https://cdnjs.cloudflare.com/ajax/libs/ace/1.4.11/ace.min.js',
            'https://cdnjs.cloudflare.com/ajax/libs/ace/1.4.11/mode-markdown.min.js',
            'mdeditor/js/emoji.js',
            'mdeditor/js/emoji-picker.js',
            'mdeditor/js/mdeditor.js',
        )
