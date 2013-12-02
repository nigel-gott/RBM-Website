// TODO: Prevent duplicate class names, use dictionary?
// CHANGE BRUSH SIZE TO JQUERY UI SLIDER
// CLEAN UP CODE
// Centre by default on submit

function PixelDrawer(drawerContainer, width, height, mode, max_labels, uploadURL, csrfToken) {
    var canvas_object = new Canvas(width, height);
    var canvas = canvas_object.canvas;
    var container;
    var buttons;
    var slider;

    var brushes = {SMALL: 1, MEDIUM: 2, LARGE: 3};

    var currentlyDrawing = false;
    var blank = true;
    var tools = {PEN: 0, ERASER: 1};
    var currentTool = tools.PEN;

    createLayout();
    createSlider();

    canvas_object.addCheckerboard();
    container.append(canvas);

    var clear = appendButton('clear', 'Clear');
    var pen = appendButton('pen', 'Pen');
    var eraser = appendButton('eraser', 'Eraser');
    var centre = appendButton('centre', 'Centre');

    var download;
    var train;
    var className;
    var classes_remaining;

    if (mode == "train") {
        classes_remaining = max_labels;
        printRemainingClasses();
        download = appendButton('addClass', 'Add Class');
        createTrainButton();
        className = appendClassNameInput();
    } else if (mode == "classify") {
        download = appendButton('classify', 'Classify');
    } else {
        download = appendButton('classify', 'Classify');
    }

    function createTrainButton() {
        train = appendButton('trainButton', 'Train DBN');
        train.attr("disabled", true);
        train.click(function() {
            var images = [];

            $('.imageClass').each(function() {
                var classImg = $(this).children("img");
                var data = {
                    'image_name': classImg.prop('id'),
                    'image_data' : classImg.prop('src')
                };
                images.push(data);
            });

            $.post(uploadURL, {classImages: images, csrfmiddlewaretoken: csrfToken}, function(data, textStatus, xhr) {
                window.location.href = '/rbm/training/';
            });
        });
    }

    function createLayout() {
        container = $('<div/>', {
            id: 'canvasContainer',
        }).appendTo(drawerContainer);
        buttons = $('<div/>', {
            id: 'buttons',
        }).appendTo(drawerContainer);
        slider = $('<div/>', {
            id: 'slider',
        }).appendTo(buttons);
    }

    function createSlider() {
        var min = brushes.SMALL;
        var max = brushes.LARGE;
        console.log('max is ' + max + ' min is ' + min);
        slider.slider({
            min: min,
            max: max,
            step: 1,
            value: 1,
            stop: function( event, ui ) {
                var value = slider.slider('value');
                console.log('value is ' + value);
                canvas_object.changeBrushSize(value);
            }
        });
    }

    function appendClassNameInput() {
        var inputBox = $('<input id="className" type="text"/>');
        buttons.append(inputBox);
        return inputBox;
    }

    function appendButton(name, value){
        var button = $('<button />', {
            class : 'btn',
            id: name,
            text: value,
            type: 'button'
        });

        buttons.append(button);
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

    centre.click(function() {
        var bounds = canvas_object.getCanvasBounds();
        var drawHeight = bounds["top"] - bounds["bottom"];
        var drawWidth = bounds["right"] - bounds["left"];
        var drawHeightCentre = bounds["bottom"] + Math.round(drawHeight/2);
        var drawWidthCentre = bounds["left"] + Math.round(drawWidth/2);
        var heightOffset = Math.round(height/2) - drawHeightCentre;
        var widthOffset = Math.round(width/2) - drawWidthCentre;
        canvas_object.shiftDrawing(heightOffset, widthOffset);
    });

    function printRemainingClasses() {
        $('#classesRemainingDisplay').empty().prepend('You have ' + classes_remaining + ' out of ' + max_labels + ' image classes remaining!');
    }

    function classify() {
        previewCanvas = canvas_object.generatePreview();
        imageURL = previewCanvas.toDataURL("image/png");

        $.post(uploadURL, {'image_data' : imageURL, csrfmiddlewaretoken : csrfToken}, function(data, textStatus, xhr) {
           alert(data.number + ' with probability ' + data.max_prob);
           console.log(data);
        });
    }

    function addClass() {
        previewCanvas = canvas_object.generatePreview();
        imageURL = previewCanvas.toDataURL("image/png");
        imageID = className.val();

        if (imageID === "") {
            alert("Please enter a class name before adding a class!");
        } else {
            image = $('<img id="' + imageID + '" src="' +  imageURL + '" >');
            deleteButton = $('<input type="button" value="-" />');
            deleteButton.click(function() {
                classes_remaining++;
                if (classes_remaining == 1) {
                    $('#trainButton').attr("disabled", true);
                    $('#addClass').attr("disabled", false);
                    $('#className').attr("disabled", false);
                }
                printRemainingClasses();
                $(this).parent().fadeOut(300, function() { $(this).remove(); });
            });
            div = $('<div class="imageClass"></div>');

            div.append(deleteButton);
            div.append('  ');
            div.append(image);
            div.append(' - ' + imageID);
            clearCanvas();
            className.val('');
            classes_remaining--;
            div.hide().appendTo('#imageClasses').fadeIn(400);
            printRemainingClasses();
            if (classes_remaining === 0) {
                $('#addClass').attr("disabled", true);
                $('#className').attr("disabled", true);
                $('#trainButton').attr("disabled", false);
            }
        }
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
    this.brushSize = 1;

    var colours = {GREY: "#DEDDDC", BLACK: "#000000", WHITE:"#FFFFFF"};
    var size = {SMALL: 1, MEDIUM: 2, LARGE: 3};

    var canvasWidth = aspRatio * pixelWidth;
    var canvasHeight = aspRatio * pixelHeight;

    this.canvas = createCanvas(canvasWidth, canvasHeight);

    var context = this.canvas[0].getContext("2d");

    /* Public Functions */
    this.draw = function(x, y) {
        if (this.brushSize >= size.SMALL) {
            fillPixel(colours.BLACK, x, y);
        }
        if (this.brushSize >= size.MEDIUM) {
            fillPixel(colours.BLACK, x+1, y);
            fillPixel(colours.BLACK, x-1, y);
            fillPixel(colours.BLACK, x, y+1);
            fillPixel(colours.BLACK, x, y-1);
        }
        if (this.brushSize >= size.LARGE) {
            fillPixel(colours.BLACK, x+1, y+1);
            fillPixel(colours.BLACK, x-1, y+1);
            fillPixel(colours.BLACK, x-1, y-1);
            fillPixel(colours.BLACK, x+1, y-1);
        }
    };

    this.erase = function(x, y) {
        fillCheckerboardPiece(x, y);
    };

    this.shiftDrawing = function(heightOffset, widthOffset) {
        var tempCanvas = createCanvas(canvasWidth, canvasHeight);
        var tempCtx = tempCanvas[0].getContext("2d");
        tempCtx.drawImage(this.canvas[0], 0, 0);
        this.addCheckerboard();

        for (var col = 0; col < pixelWidth; col++) {
            for (var row = 0; row < pixelHeight; row++) {
                var pixData = tempCtx.getImageData(col*aspRatio, row*aspRatio, 1, 1);
                if (pixData.data[0] === 0) {
                    context.fillStyle = colours.BLACK;
                    context.fillRect((col+widthOffset)*aspRatio, (row-heightOffset)*aspRatio, aspRatio, aspRatio);
                }
            }
        }
    };

    this.generatePreview = function() {
        previewCanvas = createCanvas(pixelWidth, pixelHeight);

        var previewContext = previewCanvas[0].getContext("2d");
        for (var col = 0; col < pixelWidth; col++) {
            for (var row = 0; row < pixelHeight; row++) {
                var pixData = context.getImageData(col*aspRatio, row*aspRatio, 1, 1);
                if (pixData.data[0] === 0) {
                    previewContext.fillStyle = colours.BLACK;
                } else {
                    previewContext.fillStyle = colours.WHITE;
                }
                previewContext.fillRect(col, row, 1, 1);
            }
        }
        return previewCanvas[0];
    };

    this.getCanvasBounds = function() {
        var left = pixelWidth + 1;
        var right = -1;
        var bottom = -1;
        var top = pixelHeight + 1;
        for (var col = 0; col < pixelWidth; col++) {
            for (var row = 0; row < pixelHeight; row++) {
                var pixData = context.getImageData(col*aspRatio, row*aspRatio, 1, 1);
                if (pixData.data[0] === 0) {
                    if  (col > right) {
                        right = col;
                    }
                    if (col < left) {
                        left = col;
                    }
                    if (row > bottom) {
                        bottom = row;
                    }
                    if (row < top) {
                        top = row;
                    }
                }
            }
        }
        bottom = pixelHeight - (bottom + 1);
        top = pixelHeight - (top + 1);
        return ({"left": left, "right": right, "bottom": bottom, "top": top});
    };

    this.addCheckerboard = function() {
    for (var col = 0; col < pixelWidth; col++) {
            for (var row = 0; row < pixelHeight; row++) {
                fillCheckerboardPiece(col, row);
            }
        }
    };

    this.changeBrushSize = function(newSize) {
        console.log('new size is ' + newSize);
        this.brushSize = newSize;
        console.log('end size is ' + this.brushSize);
    }

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
