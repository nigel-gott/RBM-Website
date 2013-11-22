var layerCount = 0;
$(document).ready( function () {
    layerCount = parseInt($("[name=layer_count]").val());

    $("#add-layer").click(function() {
        input = $('<input type="text">');
        input.attr('name', 'layer_' + layerCount);
        input.attr('id', 'id_layer_' + layerCount);

        label = $('<label></label> ');
        label.attr('for', 'id_layer_' + layerCount);
        label.text("Layer " + layerCount + ":");

        div = $('<div class="fieldWrapper"></div>');

        div.append(label);
        div.append(' ');
        div.append(input);
        div.hide().appendTo('#layers').fadeIn(400);

        layerCount ++;
        $("[name=layer_count]").val(layerCount);
    });

    $("#delete-layer").click(function() {
        if (layerCount > 0) {
            layerCount --;
            $("[name=layer_count]").val(layerCount);

            layerWrapper = $("#id_layer_" + layerCount).parent(".fieldWrapper");
            layerWrapper.fadeOut(300, function() { $(this).remove(); });
        };
    });

    $("#preview").click( function() {
        preview();
        setInterval ("preview()", 1000);funcName, delay
    });
});

function preview() {
    $("#previewCanvas").remove();
    var topology = getTopology();
    drawTopology(topology);
}

function getTopology() {
    var topology = new Array();
    topology[0] = $("#id_visible").val();
    for (var i = 0; i < layerCount; i++) {
        topology[1 + i] = $("#id_layer_" + i).val();
    };
    topology[layerCount + 1] = $("#id_labels").val();
    return topology;
}

function drawTopology(topology) {
    var height = 60;
    var gap = 40;
    var textOffset = height + 15;
    var perHeight = height + gap;
    var canvasHeight = perHeight * (layerCount + 2);
    var canvasWidth = 300;
    var canvas = $('<canvas />').attr({
        id: "previewCanvas",
        width: canvasWidth,
        height: canvasHeight
    });
    canvas.appendTo('#canvasContainer');

    var ctx = $("#previewCanvas")[0].getContext("2d");
    ctx.clearRect(0,0,canvasWidth,canvasHeight);
    ctx.fillStyle = "#000000";
    ctx.font = '8pt Helvetica';
    ctx.textAlign = 'left';
    var max = Math.max.apply(Math, topology);
    var ratio = canvasWidth/max;
    var widths = $.map(topology, function(n) {
        return Math.round(ratio*n);
    });

    var currentHeight = canvasHeight - perHeight;
    for (var i = 0; i < layerCount + 2; i++) {
        fillRandomPixels(ctx, (canvasWidth/2) - widths[i]/2, currentHeight, widths[i], height);
        if (i == 0) {
            ctx.fillText("Input Data: " + topology[0] + " nodes", 0, currentHeight + textOffset);
        } else if (i == layerCount + 1) {
            ctx.fillText("Classifier: " + topology[layerCount + 1] + " nodes", 0, currentHeight + textOffset);
        } else {
            ctx.fillText(("Layer " + (i-1)) + ": " + topology[i] + " nodes", 0, currentHeight + textOffset);
        };
        currentHeight = currentHeight - perHeight;
    };
}

function fillRandomPixels(ctx,xcoord,ycoord,width,height, pixels) {
    for (var x = 0; x < width; x++) {
        for (var y = 0; y < height; y++) {
            var prob = Math.floor(Math.random()*2);
            if (prob == 1) {
                ctx.fillRect(xcoord + x, ycoord + y, 1, 1);
            };
        };
    };
}

