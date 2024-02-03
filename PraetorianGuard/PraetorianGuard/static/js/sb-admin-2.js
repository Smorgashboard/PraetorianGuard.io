(function($) {
  "use strict"; // Start of use strict

  // Toggle the side navigation
  $("#sidebarToggle, #sidebarToggleTop").on('click', function(e) {
    $("body").toggleClass("sidebar-toggled");
    $(".sidebar").toggleClass("toggled");
    if ($(".sidebar").hasClass("toggled")) {
      $('.sidebar .collapse').collapse('hide');
    };
  });

  // Close any open menu accordions when window is resized below 768px
  $(window).resize(function() {
    if ($(window).width() < 768) {
      $('.sidebar .collapse').collapse('hide');
    };
    
    // Toggle the side navigation when window is resized below 480px
    if ($(window).width() < 480 && !$(".sidebar").hasClass("toggled")) {
      $("body").addClass("sidebar-toggled");
      $(".sidebar").addClass("toggled");
      $('.sidebar .collapse').collapse('hide');
    };
  });

  // Prevent the content wrapper from scrolling when the fixed side navigation hovered over
  $('body.fixed-nav .sidebar').on('mousewheel DOMMouseScroll wheel', function(e) {
    if ($(window).width() > 768) {
      var e0 = e.originalEvent,
        delta = e0.wheelDelta || -e0.detail;
      this.scrollTop += (delta < 0 ? 1 : -1) * 30;
      e.preventDefault();
    }
  });

  // Scroll to top button appear
  $(document).on('scroll', function() {
    var scrollDistance = $(this).scrollTop();
    if (scrollDistance > 100) {
      $('.scroll-to-top').fadeIn();
    } else {
      $('.scroll-to-top').fadeOut();
    }
  });

  // Smooth scrolling using jQuery easing
  $(document).on('click', 'a.scroll-to-top', function(e) {
    var $anchor = $(this);
    $('html, body').stop().animate({
      scrollTop: ($($anchor.attr('href')).offset().top)
    }, 1000, 'easeInOutExpo');
    e.preventDefault();
  });

})(jQuery); // End of use strict

var x=2;
var check;

function addTxt()
{
  if (check){
    console.log("you hit 30")
  }else{
    var cont = document.getElementsByClassName('form-group');
    var input = document.createElement('input'); 
    input.setAttribute("type", "email");
    input.setAttribute("value", "");
    input.setAttribute("name", "email_" + x);
    input.setAttribute("id", "email_" + x);
    input.setAttribute("class", "form-control");
    input.setAttribute("maxlength", "64");
    input.required = true;
    x++;
    cont[0].appendChild(input);
    check=document.getElementById('email_30');
  }
}

function removeEmail()
{
  var y = x - 1;
  var current=document.getElementById('email_' + y);
  current.remove();
  x = x -1;

}

var forms = 0;

function addForm()
{
  var br = document.createElement("br");
  var cont = document.getElementsByClassName('form-group');
  var ele_section = document.createElement("section");
  ele_section.setAttribute("class", "bg-light py-5");
  cont[0].appendChild(ele_section);
  var container = document.createElement("div");
  container.setAttribute("class", "container");
  cont[0].appendChild(container);
  var row = document.createElement("div");
  row.setAttribute("class", "row");
  cont[0].appendChild(row);
  var div_1 = document.createElement("div");
  div_1.setAttribute("class", "col-md-6 mx-auto");
  cont[0].appendChild(div_1);
  var div_2 = document.createElement("div");
  div_2.setAttribute("class", "card");
  cont[0].appendChild(div_2);
  var div_3 = document.createElement("div");
  div_3.setAttribute("class", "card-header bg-primary text-white");
  cont[0].appendChild(div_3);
  var div_4 = document.createElement("div");
  div_4.setAttribute("class", "fas fs-user-plus");
  div_4.setAttribute("value", "Register a New Company")
  cont[0].appendChild(div_4);
  var div_5 = document.createElement("div");
  div_5.setAttribute("class", "card-body");
  cont[0].appendChild(div_5);
  if (forms < 1){
    // I hate javascript
    forms = 1;
    
    // Create an input element for Full Name
    var MSP_ID = document.createElement("input");
    MSP_ID.setAttribute("type", "text");
    MSP_ID.setAttribute("name", "msp_id");
    MSP_ID.setAttribute("placeholder", "I.T. Provider");
    MSP_ID.setAttribute("value", "");
    cont[0].appendChild(MSP_ID);
    cont[0].appendChild(br.cloneNode());

     // Create an input element for date of birth
     var company_name = document.createElement("input");
     company_name.setAttribute("type", "text");
     company_name.setAttribute("name", "company_name");
     company_name.setAttribute("placeholder", "Company Name");
     cont[0].appendChild(company_name);
     cont[0].appendChild(br.cloneNode());
 
     // Create an input element for emailID
     var company_domain = document.createElement("input");
     company_domain.setAttribute("type", "text");
     company_domain.setAttribute("name", "company_domain");
     company_domain.setAttribute("placeholder", "Company's Domain");
     cont[0].appendChild(company_domain);
     cont[0].appendChild(br.cloneNode());
 
      // Create an input element for password
      var public_ip = document.createElement("input");
      public_ip.setAttribute("type", "text");
      public_ip.setAttribute("name", "public_ip");
      public_ip.setAttribute("placeholder", "Company's Public IP");
      cont[0].appendChild(public_ip);
      cont[0].appendChild(br.cloneNode());
 
      var primary_mail_domain = document.createElement("input");
      primary_mail_domain.setAttribute("type", "text");
      primary_mail_domain.setAttribute("name", "primary_mail_domain");
      primary_mail_domain.setAttribute("placeholder", "Primary Domain used for Email");
      cont[0].appendChild(primary_mail_domain);
      cont[0].appendChild(br.cloneNode());

 
      // create a submit button
      var s = document.createElement("input");
      s.setAttribute("type", "submit");
      s.setAttribute("value", "Submit");
      cont[0].appendChild(s);
    
    }else{
    console.log("You can't have two forms.")
    para = document.createElement("p");
    node = document.createTextNode("You aleady have an open form.");
    para.appendChild(node);
    element = document.getElementById("div1");
    element.appendChild(para);
  }
}

function getDate(){
  var myDate = document.getElementById('myDate');
  var today = new Date();
  myDate.value = today.toISOString().substring(0,19);
}

function checkDNS(param1, param2){
  console.log("running");
  console.log(param1)
  console.log(param2)
  $.ajax({
      url : "/home/checkDNS", // the endpoint
      type : "GET", // http method
      data : { param_first : param1, 
               param_second : param2 }, // data sent with the get request

      // handle a successful response
      success : function(json) {
          console.log("success"); // another sanity check
      },

      // handle a non-successful response
      error : function(xhr,errmsg,err) {
          console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
      }
  });
};

function changeForm() {
  // get the select element and the selected option
  var select = document.getElementById("scan_type");
  var option = select.options[select.selectedIndex];
  
  // get the value of the selected option
  var form_type = option.value;
  
  // get the container element for the extra fields
  var container = document.getElementById("change_me");
  
  // remove any existing fields
  while (container.firstChild) {
    container.removeChild(container.firstChild);
  }
  
  // add new fields based on the selected option
  if (form_type === "email") {
    var input1 = document.createElement("input");
    input1.type = "email";
    input1.name = "target";
    input1.placeholder = "Email";
    input1.setAttribute("class", "form-control");
    container.appendChild(input1);
    var br = document.createElement("br");
    container.appendChild(br);
    var input2 = document.createElement("input");
    input2.type = "text";
    input2.name = "scan_name";
    input2.placeholder = "Scan Name"
    input2.setAttribute("class", "form-control");
    container.appendChild(input2);
  } else if (form_type === "domain") {
    var input1 = document.createElement("input");
    input1.type = "text";
    input1.name = "target";
    input1.placeholder = "Domain";
    input1.setAttribute("class", "form-control");
    container.appendChild(input1);
    var br = document.createElement("br");
    container.appendChild(br);
    var input2 = document.createElement("input");
    input2.type = "text";
    input2.name = "scan_name";
    input2.placeholder = "Scan Name"
    input2.setAttribute("class", "form-control");
    container.appendChild(input2);
  } else if (form_type === "password") {
    var input1 = document.createElement("input");
    input1.type = "password";
    input1.name = "target";
    input1.placeholder = "Password";
    input1.setAttribute("class", "form-control");
    container.appendChild(input1);
  }
}

let scans = 0;

function addScan()
{
  if (scans < 1){
    scans = 1;
    var br = document.createElement("br");
    var cont = document.querySelector("#form-group");
    var ele_section = document.createElement("section");
    ele_section.setAttribute("class", "bg-light py-5");
    cont.appendChild(ele_section);
    var container = document.createElement("div");
    container.setAttribute("class", "container");
    ele_section.appendChild(container);
    var row = document.createElement("div");
    row.setAttribute("class", "row");
    container.appendChild(row);
    var div_1 = document.createElement("div");
    div_1.setAttribute("class", "col-md-6 mx-auto");
    row.appendChild(div_1);
    var div_2 = document.createElement("div");
    div_2.setAttribute("class", "card");
    div_1.appendChild(div_2);
    var div_3 = document.createElement("div");
    div_3.setAttribute("class", "card-header bg-primary text-white");
    div_2.appendChild(div_3);
    var div_4 = document.createElement("div");
    div_4.setAttribute("class", "fas fs-user-plus");
    div_4.setAttribute("value", "Register a New Company")
    div_3.appendChild(div_4);
    var div_5 = document.createElement("div");
    div_5.setAttribute("class", "card-body");
    div_4.appendChild(div_5);
  
    // I hate javascript

    // Create an input element for Password
    var input1 = document.createElement("input");
    input1.type = "password";
    input1.name = "target";
    input1.placeholder = "Password";
    input1.setAttribute("class", "form-control");
    div_5.appendChild(input1);
 
    // create a submit button
    var s = document.createElement("input");
    s.setAttribute("type", "submit");
    s.setAttribute("value", "Submit");
    div_5.appendChild(s);
    
  }else{
    //Def need to fix this
    console.log("You can't have two forms.")
    para = document.createElement("p");
    node = document.createTextNode("You aleady have an open form.");
    element = document.getElementsByClassName("div1");
    element[0].appendChild(para);
    element[0].appendChild(node)
  }
}
