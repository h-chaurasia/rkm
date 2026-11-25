$(document).ready(function () {
  $(".nav-tabs > li > a").hover(function () {
    $(this).tab("show");
  });

  $("#btn1").on("click", function (e) {
    e.preventDefault();
    if ($("#uhml").val().trim() == "") {
      alert("Please Enter UHML");
    } else if ($("#ui").val().trim() == "") {
      alert("Please Enter Uniformity Index");
    } else if ($("#mic").val().trim() == "") {
      alert("Please Enter Mic");
    } else if ($("#str").val().trim() == "") {
      alert("Please Enter Strength");
    } else if ($("#e").val().trim() == "") {
      alert("Please Enter Elongation");
    } else if ($("#count").val().trim() == "") {
      alert("Please Enter Count");
    } else {
      $("#all_content").hide();
      $("#loading").show();
      var fd1 = new FormData();
      fd1.append("uhml", $("#uhml").val().trim());
      fd1.append("ui", $("#ui").val().trim());
      fd1.append("mic", $("#mic").val().trim());
      fd1.append("str", $("#str").val().trim());
      fd1.append("e", $("#e").val().trim());
      fd1.append("count", $("#count").val().trim());
      $.ajax({
        type: "POST",
        url: "/first_handler",
        data: fd1,
        processData: false,
        contentType: false,
        success: function (data) {
          if (data.indexOf("successfully done") != -1) {
            window.location.href = "/output";
          } else {
            window.location.href = "/check_file";
          }
        },
      });
    }
  });

  $("#btn2").on("click", function (e) {
    e.preventDefault();
    if ($("#csv_file").val() == "") {
      alert("Please Attach CSV File");
    } else {
      $("#all_content").hide();
      $("#loading").show();
      var fd = new FormData();
      fd.append(
        "csv_file",
        $("#csv_file").prop("files")[0]
      );
      $.ajax({
        type: "POST",
        url: "/second_handler",
        data: fd,
        processData: false,
        contentType: false,
        success: function (data) {
          if (data.indexOf("successfully done") != -1) {
            window.location.href = "/output";
          } else {
            window.location.href = "/check_file";
          }
        },
      });
    }
  });
});
