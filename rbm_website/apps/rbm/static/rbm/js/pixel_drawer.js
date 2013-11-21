var canvas;
var previewCanvas;
var ctx;
var aspRatio = 10;
var id = "pixelDrawer";
var pixelHeight;
var pixelWidth;
var currentlyDrawing = false;
var offset;
var blank = true;
var tools = {PEN: 0, ERASER: 1};
var currentTool = tools.PEN;
var colours = {GREY: "#DEDDDC", BLACK: "#000000", WHITE:"#FFFFFF"};
var directions = {NONE: 0, NORTH: 1, EAST: 2, SOUTH: 3, WEST: 4};

function pixelDrawerCanvas(container, width, height) {
    var canvContainer = document.getElementById(container);
    canvas = document.createElement('canvas');
    ctx = canvas.getContext("2d");
    canvas.id = id;
    canvas.width = width*aspRatio;
    canvas.height = height*aspRatio;
    pixelHeight = height;
    pixelWidth = width;
    styleCanvas();
    addCheckerboard();
    canvContainer.appendChild(canvas);
    offset = $("#" + id).offset();
    createPreviewCanvas(canvContainer);
}

function draw(event) {
    pixelX = Math.floor((event.pageX - offset.left) / aspRatio);
    pixelY = Math.floor((event.pageY - offset.top) / aspRatio);

    switch(currentTool) {
        case tools.PEN:
            fillPixel(colours.BLACK, pixelX, pixelY);
            if (blank) {
                $('#clear').attr("disabled", false);
            }
            blank = false;
            break;
        case tools.ERASER:
            fillCheckerboardPiece(pixelX, pixelY);
            break;
    }
}

function fillPixel(colour, x,y) {
    ctx.fillStyle = colour;
    ctx.fillRect(x*aspRatio, y*aspRatio, aspRatio,aspRatio);
}

function fillCheckerboardPiece(x,y) {
    if (x%2 === 0) {
        if (y%2 === 0) {
            fillPixel(colours.GREY, x, y);
        } else {
            fillPixel(colours.WHITE, x, y);
        }
    } else {
        if (y%2 == 1) {
            fillPixel(colours.GREY, x, y);
        } else {
            fillPixel(colours.WHITE, x, y);
        }
    }
}

function addCheckerboard() {
    for (var row = 0; row < pixelHeight; row++) {
        for (var col = 0; col < pixelWidth; col++) {
            fillCheckerboardPiece(row, col);
        }
    }
}

function createPreviewCanvas(container) {
    previewCanvas = document.createElement('canvas');
    previewCanvas.id = id + "Preview";
    previewCanvas.width = pixelHeight;
    previewCanvas.height = pixelWidth;
    previewCanvas.style.position = "relative";
    previewCanvas.style.border = "1px solid";
}

function generatePreview() {
    var prevCtx = previewCanvas.getContext("2d");
    for (var row = 0; row < pixelHeight; row++) {
        for (var col = 0; col < pixelWidth; col++) {
            var pixData = ctx.getImageData(row*aspRatio, col*aspRatio, 1, 1);
            if (pixData.data[0] === 0) {
                prevCtx.fillStyle = colours.BLACK;
            } else {
                prevCtx.fillStyle = colours.WHITE;
            }
            prevCtx.fillRect(row, col, 1, 1);
        }
    }
}

function styleCanvas() {
    canvas.style.position = "relative";
    canvas.style.border = "1px solid";
    canvas.style.width = pixelWidth*aspRatio;
    canvas.style.height = pixelHeight*aspRatio;
}

$(document).ready( function () {
    $('#pen').attr("disabled", true);
    $('#clear').attr("disabled", true);

    $('#clear').click(function() {
        addCheckerboard();
        blank = true;
        $('#clear').attr("disabled", true);
    });

    $('#pen').click(function() {
        currentTool = tools.PEN;
        $('#pen').attr("disabled", true);
        $('#eraser').attr("disabled", false);
    });

    $('#eraser').click(function() {
        currentTool = tools.ERASER;
        $('#eraser').attr("disabled", true);
        $('#pen').attr("disabled", false);
    });

    $('#download').click(function() {
        generatePreview();
        window.location = previewCanvas.toDataURL("image/png");
    });

    $("#" + id).mousedown( function (event) {
        draw(event);
        currentlyDrawing = true;
    });

    $("#" + id).mousemove( function (event) {
        if (currentlyDrawing) {
            draw(event);
        }
    });

    $("#" + id).mouseup( function (event) {
        currentlyDrawing = false;
    });

    $("#" + id).mouseleave( function (event) {
        currentlyDrawing = false;
    });

    $(document).keydown( function (event) {
        if (event.which == 16) {
        }
    });

    $(document).keyup( function (event) {
    });
});
