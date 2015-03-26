$(function(){
  $( "#bmi" ).submit(function( event ) {
   
    // Stop form from submitting normally
    event.preventDefault();
   
    // Get some values from elements on the page:
    var $form = $( this ),
      ht = $form.find( "input[name='height']" ).val(),
      wt = $form.find( "input[name='weight']" ).val(),
      url = $form.attr( "action" );
    
    // Send the data using post
    var posting = $.post( url, { height: ht, weight: wt } );
   
    // Put the results in a div
    posting.done(function( data ) {
      console.log(data);
      // Append the results to the result div
      $( "#result" ).empty().append( "<h4>" + "Percentile: " + data.percentile + "</h4><br/>" + "<h4>BMI: " + data.bmi + "</h4>"  );
      // Clear out the input fields
      $form.find( "input[name='weight']" ).val("");
      $form.find( "input[name='height']" ).val("");
    });
    return false
  });
});