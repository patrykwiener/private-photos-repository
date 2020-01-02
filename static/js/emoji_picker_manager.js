$(function () {
    window.emojiPicker = new EmojiPicker({
        emojiable_selector: '[data-emojiable=true]',
        assetsPath: '/static/external_libs/emoji/img',
        popupButtonClasses: 'fa fa-smile-o'
    });
    window.emojiPicker.discover();
});