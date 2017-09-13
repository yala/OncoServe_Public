$(document).on({
    // ajaxStart: function() { $('#image').css('opacity', '1') },
    //  ajaxStop: function() { $('#image').attr('src', ""); }
});

$(document).ready(function() {
    var inputs = document.querySelectorAll( '#file' );
    Array.prototype.forEach.call( inputs, function( input )
    {
    	var label	 = input.nextElementSibling,
    		labelVal = label.innerHTML;

    	input.addEventListener( 'change', function( e )
    	{
    		var fileName = '';
    		if( this.files && this.files.length > 1 )
    			fileName = ( this.getAttribute( 'data-multiple-caption' ) || '' ).replace( '{count}', this.files.length );
    		else
    			fileName = e.target.value.split( '\\' ).pop();

    		if( fileName )
    			label.innerHTML = fileName;
    		else
    			label.innerHTML = labelVal;
    	});
    });

    $('#submit').click(function() {
        console.log("clicked");
        var fd = new FormData($('#input')[0]);
        fd.append("model", $('#model').val());
        var dir = "static/uploads/";
        $.ajax({
            type: 'POST',
            url: $SCRIPT_ROOT + '/serving',
            data: fd,
            contentType: false,
            cache: false,
            processData: false,
            async: false,
            success: function(response){
                if (response.output !== undefined){
                  $("#output").css('color', 'black');
                  $("#output").text("Result: " + response.output);
                  $('#image').attr('src', dir + response.filenames[0]);
                }
                else{
                  $("#output").css('color', 'red');
                  $("#output").text("Error: " + response.error);
                  $('#image').attr('src', "");
                }
            },
        });
    });
});
