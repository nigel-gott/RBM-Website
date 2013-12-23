function preview(topology, layerCount) {
    $("#previewCanvas").remove();
    drawTopology(topology, layerCount);
}

function drawTopology(topology, noLayers) {
    var height = 60;
    var gap = 40;
    var textOffset = height + 15;
    var perHeight = height + gap;
    var canvasHeight = perHeight * (noLayers + 2);
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
    for (var i = 0; i < noLayers + 2; i++) {
        fillRandomPixels(ctx, (canvasWidth/2) - widths[i]/2, currentHeight, widths[i], height);
        if (i === 0) {
            ctx.fillText("Input Data: " + topology[0] + " nodes", 0, currentHeight + textOffset);
        } else if (i == noLayers + 1) {
            ctx.fillText("Classifier: " + topology[noLayers + 1] + " nodes", 0, currentHeight + textOffset);
        } else {
            ctx.fillText(("Layer " + (i-1)) + ": " + topology[i] + " nodes", 0, currentHeight + textOffset);
        }
        currentHeight = currentHeight - perHeight;
    }
}

function fillRandomPixels(ctx,xcoord,ycoord,width,height, pixels) {
    for (var x = 0; x < width; x++) {
        for (var y = 0; y < height; y++) {
            var prob = Math.floor(Math.random()*2);
            if (prob == 1) {
                ctx.fillRect(xcoord + x, ycoord + y, 1, 1);
            }
        }
    }
}
