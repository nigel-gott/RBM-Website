function PixelDrawer(container, width, height, mode) {
    var canvas_object = new Canvas(width, height);
    var canvas = canvas_object.canvas;
    canvas_object.addCheckerboard();
    container.append(canvas);

    var currentlyDrawing = false;
    var blank = true;
    var tools = {PEN: 0, ERASER: 1};
    var currentTool = tools.PEN;

    var clear = appendButton('Clear');
    var pen = appendButton('Pen');
    var eraser = appendButton('Eraser');

    var download;
    var className;
    if (mode == "train") {
        download = appendButton('Add Class');
        className = appendClassNameInput();
    } else if (mode == "classify") {
        download = appendButton('Classify');
    } else {
        download = appendButton('Classify');
    }

    function appendClassNameInput() {
        var inputBox = $('<input id="className" type="text"/>');
        container.append(inputBox);
        return inputBox;
    }

    function appendButton(name){
        var button = $('<button />', {
            class : 'btn',
            id: name.toLowerCase(),
            text: name,
            type: 'button'
        });

        container.append(button);
        return button;
    }

    pen.attr("disabled", true);
    clear.attr("disabled", true);

    clear.click(function() {
        clearCanvas();
    });

    pen.click(function() {
        currentTool = tools.PEN;
        pen.attr("disabled", true);
        eraser.attr("disabled", false);
    });

    eraser.click(function() {
        currentTool = tools.ERASER;
        eraser.attr("disabled", true);
        pen.attr("disabled", false);
    });

    download.click(function() {
        if (mode == "train") {
            addClass();
        } else if (mode == "classify") {
            classify();
        } else {
            classify();
        }
    });

    function addClass() {
        previewCanvas = canvas_object.generatePreview();
        imageURL = previewCanvas.toDataURL("image/png");
        imageID = className.val();

        if (imageID === "") {
            alert("Please enter a class name before adding a class!");
        } else {
            image = $('<img id="' + imageID + '" src="' +  imageURL + '" alt="this is a failure">');
            deleteButton = $('<input type="button" value="-" />');
            deleteButton.click(function() {
                $(this).parent().fadeOut(300, function() { $(this).remove(); });
            });
            div = $('<div class="imageClass"></div>');

            div.append(deleteButton);
            div.append('  ');
            div.append(image);
            div.append(' - ' + imageID);
            clearCanvas();
            className.val('');
            div.hide().appendTo('#imageClasses').fadeIn(400);
        }
    }

    function classify() {
        alert('Classifying not adding');
    }

    canvas.mousedown(draw);

    canvas.mousemove( function (e) {
        if (currentlyDrawing) {
            draw(e);
        }
    });

    function clearCanvas() {
        canvas_object.addCheckerboard();
        blank = true;
        clear.attr("disabled", true);
    }

    function draw(e){
        var offset = canvas.offset();
        x = Math.floor((e.pageX - offset.left) / canvas_object.aspRatio);
        y = Math.floor((e.pageY - offset.top) / canvas_object.aspRatio);

        switch(currentTool) {
            case tools.PEN:
                canvas_object.draw(x, y);
                if (blank) {
                    clear.attr("disabled", false);
                }
                blank = false;
                break;
            case tools.ERASER:
                canvas_object.erase(x, y);
                break;
        }

        currentlyDrawing = true;
    }

    canvas.mouseup( function (event) {
        currentlyDrawing = false;
    });

    canvas.mouseleave( function (event) {
        currentlyDrawing = false;
    });
}

function Canvas(pixelWidth, pixelHeight){
    var aspRatio = 10;
    this.aspRatio = aspRatio;

    var colours = {GREY: "#DEDDDC", BLACK: "#000000", WHITE:"#FFFFFF"};

    var canvasWidth = aspRatio * pixelWidth;
    var canvasHeight = aspRatio * pixelHeight;

    this.canvas = createCanvas(canvasWidth, canvasHeight);

    var context = this.canvas[0].getContext("2d");

    /* Public Functions */
    this.draw = function(x, y) {
        fillPixel(colours.BLACK, x, y);
    };

    this.erase = function(x, y) {
        fillCheckerboardPiece(x, y);
    };

    this.generatePreview = function() {
        previewCanvas = createCanvas(pixelWidth, pixelHeight);

        var previewContext = previewCanvas[0].getContext("2d");
        for (var row = 0; row < pixelWidth; row++) {
            for (var col = 0; col < pixelHeight; col++) {
                var pixData = context.getImageData(row*aspRatio, col*aspRatio, 1, 1);
                if (pixData.data[0] === 0) {
                    previewContext.fillStyle = colours.BLACK;
                } else {
                    previewContext.fillStyle = colours.WHITE;
                }
                previewContext.fillRect(row, col, 1, 1);
            }
        }
        return previewCanvas[0];
    };

    this.addCheckerboard = function() {
        for (var row = 0; row < pixelHeight; row++) {
            for (var col = 0; col < pixelHeight; col++) {
                fillCheckerboardPiece(row, col);
            }
        }
    };

    /* Private Functions */
    function createCanvas(canvasWidth, canvasHeight){
        var canvas = $('<canvas/>', {
            'style' : 'position: relative; border: 1px solid;',
            'width' : canvasWidth,
            'height' : canvasHeight
        });
        canvas[0].width = canvasWidth;
        canvas[0].height= canvasHeight;
        return canvas;
    }

    function fillPixel(colour, x, y) {
        context.fillStyle = colour;
        context.fillRect(x*aspRatio, y*aspRatio, aspRatio, aspRatio);
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

}
