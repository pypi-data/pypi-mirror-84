(function () {
    function mdEditor(textarea) {
        var id = textarea.id;
        var editor = ace.edit("markdown-editor-" + id);

        var editor_tab = $('#editor-tab-' + id);
        var preview_tab = $('#preview-tab-' + id);

        var toolbar = $('#editor-toolbar-' + id);

        var preview = $('#md-preview-' + id);

        /* Configuration editeur */
        editor.setOptions({
            mode: "ace/mode/markdown",
            maxLines: textarea.getAttribute('rows'),
            minLines: textarea.getAttribute('rows'),
            autoScrollEditorIntoView: true,
        });

        editor.setFontSize("14px");
        editor.session.setUseWrapMode(true);

        /* setup editor */
        editor.getSession().setValue(textarea.textContent);
        preview.html(md.render(editor.getSession().getValue()));
        editor.focus();

        /* Logique des onglets */
        var tabs = $('#editor-list-' + id + ' a'); 
        tabs.on('click', function (e) {
            e.preventDefault()
            $(this).tab('show')
        })

        editor_tab.click(function () {
            editor.focus();
        });

        editor.getSession().on('change', function () {
            var dirty = md.render(editor.getSession().getValue());
            var config = {
                ADD_TAGS: ['iframe'],
                SAFE_FOR_JQUERY: true
            };
            var clean = DOMPurify.sanitize(dirty, config);
            preview.html(clean);
            MathJax.typeset()

            /* set textarea value  */
            textarea.textContent = editor.getSession().getValue();
        });

        /* toolbar logic */
        toolbar.find('#btn-bold').click(function () {
            editor.insert("**text**");
            editor.find('text', {
                backwards: true,
                caseSensitive: true,
                wholeWord: true,
            });
            editor.focus();
        });

        toolbar.find('#btn-italic').click(function () {
            editor.insert("*text*");
            editor.find('text', {
                backwards: true,
                caseSensitive: true,
                wholeWord: true,
            });
            editor.focus();
        });

        toolbar.find('#btn-underline').click(function () {
            editor.insert("__text__");
            editor.find('text', {
                backwards: true,
                caseSensitive: true,
                wholeWord: true,
            });
            editor.focus();
        });

        toolbar.find('#btn-strike').click(function () {
            editor.insert("~~text~~");
            editor.find('text', {
                backwards: true,
                caseSensitive: true,
                wholeWord: true,
            });
            editor.focus();
        });

        toolbar.find('#btn-header').click(function () {
            editor.insert("#");
            editor.focus();
        });

        toolbar.find('#btn-line').click(function () {
            editor.insert("\n***\n");
            editor.focus();
        });

        toolbar.find('#btn-list').click(function () {
            editor.insert("* ");
            editor.focus();
        });

        toolbar.find('#btn-num-list').click(function () {
            editor.insert("1. ");
            editor.focus();
        });

        toolbar.find('#btn-table').click(function () {
            editor.insert("| Column 1 | Column 2 | Column 3 |\n| -------- |:-------------:| -----:|\n| col 1 is | right-aligned | $1600 |\n| col 2 is | centered      |   $12 |\n| col 3 is | left-aligned  |    $1 |\n ");

            editor.find('Column 1', {
                backwards: true,
                caseSensitive: true,
                wholeWord: true,
            });
        });

        toolbar.find('#btn-math').click(function () {
            editor.insert("$$\nmath\n$$\n");
            editor.find('math', {
                backwards: true,
                caseSensitive: true,
                wholeWord: true,
            });
            editor.focus();
        });

        toolbar.find('#btn-code').click(function () {
            editor.insert("```\ncode\n```");
            editor.find('code', {
                backwards: true,
                caseSensitive: true,
                wholeWord: true,
            });
            editor.focus();
        });

        toolbar.find('#btn-quote').click(function () {
            editor.insert("> ");
            editor.focus();
        });

        toolbar.find($('#btn-link')).click(function () {
            editor.insert("[link](https://www.)");
            editor.find('link', {
                backwards: true,
                caseSensitive: true,
                wholeWord: true,
            });
        });

        toolbar.find('#btn-image').click(function () {
            editor.insert("![image](src)");
            editor.find('image', {
                backwards: true,
                caseSensitive: true,
                wholeWord: true,
            });
        });

        toolbar.find('#btn-undo').click(function () {
            editor.undo();
        });

        toolbar.find('#btn-redo').click(function () {
            editor.redo();
        });

        /* emoji logic */
        var smiley = toolbar.find('#btn-smile');

        preview_tab.click(function () {
            smiley.popover('hide');
        });

        smiley.popover({
            html: true,
            title: ' ',
            position: 'bottom',
            content: toolbar.find('#emoji-popover-content').html(),
        });

        var first_time = true; 
        smiley.on('shown.bs.popover', function () {
            if (first_time) {
                var this_pop = $(this).data('bs.popover').tip.id;
                $('#'+this_pop).emojiPickerContainer({
                    twemoji: true,
                    width: 235,
                    closeOnSelect: false,
                    onSelect: function (emoji) {
                        editor.insert(':' + emoji.name + ':');
                    }
                });
                first_time = false;
            }            
        });
    }

    document.addEventListener('DOMContentLoaded', function (e) {
        [].forEach.call(document.querySelectorAll('textarea.mdeditor'), mdEditor);
    });
})();

/* enable tooltip in the toolbar */
$(function () {
    $('[data-toggle="tooltip"]').tooltip()
});
