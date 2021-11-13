$(document).ready(function() {
  // JQuery for Materialize Navigation Sidebar element.
  $('.sidenav').sidenav({
    edge: "right"
  });
  // JQuery for Materialize Nav Dropdown element.
  $(".dropdown-trigger").dropdown();
  // JQuery for Materialize Collapsible element.
  $('.collapsible').collapsible();
  // JQuery for Materialize form select element.
  $('select').formSelect();
});

// Validate Materialize Select Code Function used courtesy of Tim Nelson (TravelTimN)
// This code snippet is used to add green/red underlining on Materialize select dropdowns.
validateMaterializeSelect();

function validateMaterializeSelect() {
  let classValid = {
    "border-bottom": "1px solid #4caf50",
    "box-shadow": "0 1px 0 0 #4caf50"
  };
  let classInvalid = {
    "border-bottom": "1px solid #f44336",
    "box-shadow": "0 1px 0 0 #f44336"
  };
  if ($("select.validate").prop("required")) {
    $("select.validate").css({
      "display": "block",
      "height": "0",
      "padding": "0",
      "width": "0",
      "position": "absolute"
    });
  }
  $(".select-wrapper input.select-dropdown").on("focusin", function() {
    $(this).parent(".select-wrapper").on("change", function() {
      if ($(this).children("ul").children("li.selected:not(.disabled)").on("click", function() {})) {
        $(this).children("input").css(classValid);
      }
    });
  }).on("click", function() {
    if ($(this).parent(".select-wrapper").children("ul").children("li.selected:not(.disabled)").css("background-color") === "rgba(0, 0, 0, 0.03)") {
      $(this).parent(".select-wrapper").children("input").css(classValid);
    } else {
      $(".select-wrapper input.select-dropdown").on("focusout", function() {
        if ($(this).parent(".select-wrapper").children("select").prop("required")) {
          if ($(this).css("border-bottom") != "1px solid rgb(76, 175, 80)") {
            $(this).parent(".select-wrapper").children("input").css(classInvalid);
          }
        }
      });
    }
  });
}

// Code for expanding Materialize text areas automatically. testhigh
//$('#issue_comment').val('');
//M.textareaAutoResize($('#textarea1'));