if (typeof jQuery !== 'undefined') {
    (function($, win) {
        'use strict';


        var settings = {};

        $.fn.lsxEmojiPicker = function(options) {

            // Overriding default options
            settings = $.extend({
                width: 220,
                height: 200,
                twemoji: false,
                closeOnSelect: true,
                onSelect: function(em) {}
            }, options);

            var appender = $('<div></div>')
                .addClass('emojipicker-appender');
            var container = $('<div></div>')
                .addClass('emojipicker-container')
                .css({
                    'top': -(settings.height + 70)
                });
            var wrapper = $('<div></div>')
                .addClass('emojipicker-wrapper');

            var spinnerContainer = $('<div></div>')
                .addClass('spinner-container');
            var spinner = $('<div></div>')
                .addClass('loader');
            spinnerContainer.append(spinner);

            var emojiPeopleContainer = $('<div></div>')
                .addClass('emojipicker-emoji emoji-tab emoji-people')
                .css({ 'width': settings.width, 'height': settings.height });
            var emojiNatureContainer = $('<div></div>')
                .addClass('emojipicker-emoji emoji-tab emoji-nature hidden')
                .css({ 'width': settings.width, 'height': settings.height });
            var emojiPlaceContainer = $('<div></div>')
                .addClass('emojipicker-emoji emoji-tab emoji-place hidden')
                .css({ 'width': settings.width, 'height': settings.height });
            var emojiObjectContainer = $('<div></div>')
                .addClass('emojipicker-emoji emoji-tab emoji-object hidden')
                .css({ 'width': settings.width, 'height': settings.height });

            var tabs = $('<ul></ul>')
                .addClass('emojipicker-tabs');

            var peopleEmoji = $('<li></li>')
                .addClass('selected')
                .html(emoji['people'][1].value)
                .click(function(e) {
                    e.preventDefault();
                    $('ul.emojipicker-tabs li').removeClass('selected');
                    $(this).addClass('selected');
                    $('.emoji-tab').addClass('hidden');
                    emojiPeopleContainer.removeClass('hidden');
                });
            var natureEmoji = $('<li></li>')
                .html(emoji['nature'][0].value)
                .click(function(e) {
                    e.preventDefault();
                    $('ul.emojipicker-tabs li').removeClass('selected');
                    $(this).addClass('selected');
                    $('.emoji-tab').addClass('hidden');
                    emojiNatureContainer.removeClass('hidden');
                });
            var placeEmoji = $('<li></li>')
                .html(emoji['place'][38].value)
                .click(function(e) {
                    e.preventDefault();
                    $('ul.emojipicker-tabs li').removeClass('selected');
                    $(this).addClass('selected');
                    $('.emoji-tab').addClass('hidden');
                    emojiPlaceContainer.removeClass('hidden');
                });
            var objectEmoji = $('<li></li>')
                .html(emoji['object'][4].value)
                .click(function(e) {
                    e.preventDefault();
                    $('ul.emojipicker-tabs li').removeClass('selected');
                    $(this).addClass('selected');
                    $('.emoji-tab').addClass('hidden');
                    emojiObjectContainer.removeClass('hidden');
                });

            tabs.append(peopleEmoji)
                .append(natureEmoji)
                .append(placeEmoji)
                .append(objectEmoji);

            createEmojiTab('people', emojiPeopleContainer, container);
            createEmojiTab('nature', emojiNatureContainer, container);
            createEmojiTab('place', emojiPlaceContainer, container);
            createEmojiTab('object', emojiObjectContainer, container);

            //wrapper.append(spinnerContainer);
            wrapper.append(emojiPeopleContainer)
                .append(emojiNatureContainer)
                .append(emojiPlaceContainer)
                .append(emojiObjectContainer);
            wrapper.append(tabs);
            container.append(wrapper);
            appender.append(container);
            this.append(appender);


            if (settings.twemoji) {
                twemoji.parse(emojiPeopleContainer[0], { size: 72 });
                twemoji.parse(emojiNatureContainer[0], { size: 72 });
                twemoji.parse(emojiPlaceContainer[0], { size: 72 });
                twemoji.parse(emojiObjectContainer[0], { size: 72 });
                twemoji.parse(tabs[0], { size: 72 });
            }

            this.click(function(e) {
                e.preventDefault();
                if (!$(e.target).parent().hasClass('emojipicker-tabs') &&
                    !$(e.target).parent().parent().hasClass('emojipicker-tabs') &&
                    !$(e.target).parent().hasClass('emoji-tab') &&
                    !$(e.target).parent().parent().hasClass('emoji-tab')) {
                    if (container.is(':visible')) {
                        container.hide();
                    } else {
                        container.fadeIn();
                    }
                }
            });

            // Apply the plugin to the selected elements
            return this;
        }

        $.fn.emojiPickerContainer = function(options) {

            // Overriding default options
            settings = $.extend({
                width: 220,
                height: 200,
                twemoji: false,
                closeOnSelect: true,
                onSelect: function(em) {}
            }, options);

            /*
            var appender = $('<div></div>')
                .addClass('emojipicker-appender');
            var container = $('<div></div>')
                .addClass('emojipicker-container')
                .css({
                    'top': -(settings.height + 70)
                });
            */
            var wrapper = $('<div></div>')
                .addClass('emojipicker-wrapper');

            var emojiPeopleContainer = $('<div></div>')
                .addClass('emojipicker-emoji emoji-tab emoji-people')
                .css({ 'width': settings.width, 'height': settings.height });
            var emojiNatureContainer = $('<div></div>')
                .addClass('emojipicker-emoji emoji-tab emoji-nature hidden')
                .css({ 'width': settings.width, 'height': settings.height });
            var emojiPlaceContainer = $('<div></div>')
                .addClass('emojipicker-emoji emoji-tab emoji-place hidden')
                .css({ 'width': settings.width, 'height': settings.height });
            var emojiObjectContainer = $('<div></div>')
                .addClass('emojipicker-emoji emoji-tab emoji-object hidden')
                .css({ 'width': settings.width, 'height': settings.height });

            var tabs = $('<ul></ul>')
                .addClass('emojipicker-tabs');

            var peopleEmoji = $('<li></li>')
                .addClass('selected')
                .html(emoji['people'][1].value)
                .click(function(e) {
                    e.preventDefault();
                    $('ul.emojipicker-tabs li').removeClass('selected');
                    $(this).addClass('selected');
                    $('.emoji-tab').addClass('hidden');
                    emojiPeopleContainer.removeClass('hidden');
                });
            var natureEmoji = $('<li></li>')
                .html(emoji['nature'][0].value)
                .click(function(e) {
                    e.preventDefault();
                    $('ul.emojipicker-tabs li').removeClass('selected');
                    $(this).addClass('selected');
                    $('.emoji-tab').addClass('hidden');
                    emojiNatureContainer.removeClass('hidden');
                });
            var placeEmoji = $('<li></li>')
                .html(emoji['place'][38].value)
                .click(function(e) {
                    e.preventDefault();
                    $('ul.emojipicker-tabs li').removeClass('selected');
                    $(this).addClass('selected');
                    $('.emoji-tab').addClass('hidden');
                    emojiPlaceContainer.removeClass('hidden');
                });
            var objectEmoji = $('<li></li>')
                .html(emoji['object'][4].value)
                .click(function(e) {
                    e.preventDefault();
                    $('ul.emojipicker-tabs li').removeClass('selected');
                    $(this).addClass('selected');
                    $('.emoji-tab').addClass('hidden');
                    emojiObjectContainer.removeClass('hidden');
                });

            tabs.append(peopleEmoji)
                .append(natureEmoji)
                .append(placeEmoji)
                .append(objectEmoji);

            createEmojiTab('people', emojiPeopleContainer, this);
            createEmojiTab('nature', emojiNatureContainer, this);
            createEmojiTab('place', emojiPlaceContainer, this);
            createEmojiTab('object', emojiObjectContainer, this);

            //wrapper.append(spinnerContainer);
            wrapper.append(emojiPeopleContainer)
                .append(emojiNatureContainer)
                .append(emojiPlaceContainer)
                .append(emojiObjectContainer);
            wrapper.append(tabs);
            /*
            container.append(wrapper);
            appender.append(container);
            this.append(appender);
            */
            this.append(wrapper);

            if (settings.twemoji) {
                twemoji.parse(emojiPeopleContainer[0], { size: 72 });
                twemoji.parse(emojiNatureContainer[0], { size: 72 });
                twemoji.parse(emojiPlaceContainer[0], { size: 72 });
                twemoji.parse(emojiObjectContainer[0], { size: 72 });
                twemoji.parse(tabs[0], { size: 72 });
            }
            /*
            this.click(function(e) {
                e.preventDefault();
                if (!$(e.target).parent().hasClass('emojipicker-tabs') &&
                    !$(e.target).parent().parent().hasClass('emojipicker-tabs') &&
                    !$(e.target).parent().hasClass('emoji-tab') &&
                    !$(e.target).parent().parent().hasClass('emoji-tab')) {
                    if (container.is(':visible')) {
                        container.hide();
                    } else {
                        container.fadeIn();
                    }
                }
            });
            */

            // Apply the plugin to the selected elements
            return this;
        };

        function createEmojiTab(type, container, wrapper) {
            for (var i = 0; i < emoji[type].length; i++) {
                var selectedEmoji = emoji[type][i];
                var emoticon = $('<span></span>')
                    .data('value', selectedEmoji.value)
                    .attr('title', selectedEmoji.name)
                    .html(selectedEmoji.value);

                emoticon.click(function(e) {
                    e.preventDefault();
                    settings.onSelect({
                        'name': $(this).attr('title'),
                        'value': $(this).data('value')
                    });
                    if (settings.closeOnSelect) {
                        wrapper.hide();
                    }
                });
                container.append(emoticon);
            }
        }
    }(jQuery, window));
}