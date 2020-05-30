$(function () {



  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-book .modal-content").html("");
        $("#modal-book").modal("show");
      },
      success: function (data) {
        $("#modal-book .modal-content").html(data.html_form);
      }
    });
  };

  var saveForm = function () {
    var form = $(this);

    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $("#book-table tbody").html(data.html_book_list);
          $("#modal-book").modal("hide");
          md.showNotificationSuccess('top','center','success','Caisse Created Successfully !');
          console.log("success");
        }
        else {
          console.log('error');
          md.showNotificationFail('bottom','left','warning','please enter a valid email adresse !');
          $("#modal-book .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };

   var saveFormDelete = function () {
    var form = $(this);

    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $("#book-table tbody").html(data.html_book_list);
          $("#modal-book").modal("hide");
          md.showNotificationDelete('top','center','danger','Caisse Deleted Successfully !');
          setTimeout(function() { $("#display").hide(); }, 5000);
        }
        else {
          $("#modal-book .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };

   var saveFormUpdate = function () {
    var form = $(this);

    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $("#book-table tbody").html(data.html_book_list);
          $("#modal-book").modal("hide");
          md.showNotificationUpdate('top','center','primary','Caisse Updated Successfully');
          setTimeout(function() { $("#display").hide(); }, 5000);
        }
        else {
          $("#modal-book .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };


  /* Binding */

  // Create book
  $(".js-create-book").click(loadForm);
  $("#modal-book").on("submit", ".js-book-create-form", saveForm);

  // Update book
  $("#book-table").on("click", ".js-update-book", loadForm);
  $("#modal-book").on("submit", ".js-book-update-form", saveFormUpdate);

  // Delete book
  $("#book-table").on("click", ".js-delete-book", loadForm);
  $("#modal-book").on("submit", ".js-book-delete-form", saveFormDelete);

});