function topBar(message, delay, type) {
    var classType = type + 'Bar';
    $("<div />", { class: classType, text: message }).hide().prependTo("#message-container")
      .slideDown('fast').delay(delay).slideUp(function() { $(this).remove(); });
}