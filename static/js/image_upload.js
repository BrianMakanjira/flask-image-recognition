/*  ==========================================
    SHOW UPLOADED VIDEO
* ========================================== */

$(function () {
  $("#upload").on("change", function () {
    $("#video_result").attr("src", URL.createObjectURL(input.files[0]));
    $("#video_player").load();
  });
});

/*  ==========================================
    SHOW UPLOADED VIDEO NAME
* ========================================== */
var input = document.getElementById("upload");
var infoArea = document.getElementById("upload-label");

input.addEventListener("change", showFileName);
function showFileName(event) {
  var input = event.srcElement;
  var fileName = input.files[0].name;
  infoArea.textContent = "File name: " + fileName;
}

/* =================================================
    SETTING THE FILE UPLOAD LIMIT
*/
input.addEventListener("change", setFileLimit);
function setFileLimit(event) {
  var input = event.srcElement;
  if (input.files[0].size > 2097152) {
    alert("File is too big!");
  }
}

$(document).ready(function () {
  $(".search_select_box select").selectpicker();
});

/* =================================================================
 *
 */
const imageSelect = document.getElementById("image_select");
const selectedImage = document.getElementById("selected_image");
const imageFilenames = JSON.parse("{{ predictions|tojson }}");
let selectedFilename = imageFilenames[0]["name"];

imageSelect.addEventListener("change", function () {
  selectedFilename = imageSelect.value;
  selectedImage.setAttribute(
    "src",
    "{{ url_for('serve_image', filename=selectedFilename) }}"
  );
});
