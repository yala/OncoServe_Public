$(document).ready(function() {

  $(document).on("scroll", function(){
    if ($(document).scrollTop() > 10){
      $(".header").css({"fontSize": "0.7em", "height": "80px"});
    }
    else {
      $(".header").css({"fontSize": "0.8em", "height": "100px"});
    }
  });

  var inputs = document.querySelectorAll( '#file' );
  Array.prototype.forEach.call( inputs, function( input ){
  	var label	 = input.nextElementSibling,
  		  labelVal = label.innerHTML;

    input.addEventListener( 'change', function( e ){
    	var fileName = '';
    	if (this.files && this.files.length > 1){
      	fileName = (this.getAttribute( 'data-multiple-caption' ) || '').replace('{count}', this.files.length);
      }
      else{
        fileName = e.target.value.split( '\\' ).pop();
      }

    	if (fileName){
        label.innerHTML = fileName;
      }
    	else{
        label.innerHTML = labelVal;
      }
    });
  });

  $('#submit').click(function() {
    $('#loading').attr('src', 'static/logos/loading.gif');
    $('.images').empty();

    var fd = new FormData($('#input')[0]);
    fd.append('model', $('#model').val());
    fd.append('agg', $('#agg').val());

    var dir = "static/uploads/";
    $.ajax({
      type: 'POST',
      url: $SCRIPT_ROOT + '/serving',
      data: fd,
      contentType: false,
      cache: false,
      processData: false,
      async: true,
      success: function(response){
        $('#loading').attr('src', "");
        if (response.output !== undefined){
          $("#output").css('color', 'black');
          $("#output").text("Result: " + response.output);

          for (var ind in response.filenames){
            $('.images').append("<img src=" + dir + response.filenames[ind] + "/>");
            $('.images img').css({height: $('.images img').width()*0.8})
          }
        }
        else{
          $("#output").css('color', 'red');
          $("#output").text("Error: " + response.error);
        }
      },
      error: function(response){
      
      },
    });
  });
});
