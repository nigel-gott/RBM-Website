// General javascript code for the website

// pop down message bar
// Inspired by: http://stackoverflow.com/questions/2983899
function topBar(message, delay, type) {
    var classType = type + 'Bar';
    $("<div />", { class: classType, text: message }).hide().prependTo("#message-container")
      .slideDown('fast').delay(delay).slideUp(function() { $(this).remove(); });
}