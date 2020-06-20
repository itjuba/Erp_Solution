
 $(document).ready(function(){
  $('#add').click(function() {
  console.log('clicked')
	var form_idx = $('#id_form-TOTAL_FORMS').val();
//	$('#form_set').append($('#empty_form').html().replace(/__prefix__/g, form_idx));
	$('#id_form-TOTAL_FORMS').val(parseInt(form_idx) + 1);
	var x = $('#id_form-TOTAL_FORMS').val(parseInt(form_idx) + 1);
	console.log(form_idx)
	$('#book-table > tbody:last').append('<tr><td><input id="id_form-'+form_idx+'"_Prix_Unitaire class=na type=text name=form_'+form_idx+'"-Prix_Unitaire required=true"></td></tr>');
});
    });