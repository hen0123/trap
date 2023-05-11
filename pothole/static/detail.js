$(document).ready(function() {
  $(".content").hide();
  //content 클래스를 가진 div를 표시/숨김(토글)
  $(".heading").click(function()
  {
    $(this).next(".content").slideToggle(500);
    $("i", this).toggleClass("fa-chevron-down fa-chevron-up");
  });
});