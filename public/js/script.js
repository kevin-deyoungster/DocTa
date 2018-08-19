let ALL_FILES = [];
const FILE_LIST = document.getElementById("dropped-files");
const COUNT_VIEW = document.getElementById("count");
const FORM = document.getElementById("form");
const FILE_INPUT = document.getElementById("file");
const SUBMIT_BUTTON_TEXT = document.getElementById("submitButtonText");
const CLEAR_LIST_BUTTON = document.getElementById("clearList");

function renderDocs() {
  FILE_LIST.innerHTML = "";
  COUNT_VIEW.innerText = ALL_FILES.length + " Documents";

  ALL_FILES.forEach(file => {
    let li = document.createElement("li");
    li.className = "dropped-file";
    li.innerText = file.name;
    let span = document.createElement("span");
    let i = document.createElement("i");
    i.className = "fa fa-times";
    span.appendChild(i);
    // span.innerText = "X";
    span.className = "dropped-file-close";
    span.onclick = () => {
      ALL_FILES.splice(ALL_FILES.indexOf(file), 1);
      resetInput();
      renderDocs();
    };
    li.appendChild(span);
    FILE_LIST.appendChild(li);
  });
}

FILE_INPUT.addEventListener(
  "change",
  function() {
    ALL_FILES = Array.from(this.files).concat(Array.from(ALL_FILES));
    renderDocs();
  },
  false
);

CLEAR_LIST_BUTTON.onclick = () => {
  clearFiles();
  resetInput();
  renderDocs();
};

FORM.onsubmit = function(event) {
  event.preventDefault();

  let formData = new FormData();
  for (let file of ALL_FILES) {
    formData.append("file[]", file);
  }

  SUBMIT_BUTTON_TEXT.innerText = "Converting...";
  CONVERT_ICON = document.querySelector(".fa-recycle");
  CONVERT_ICON.className = "fa fa-refresh";

  axios({
    method: "post",
    url: "/convert",
    data: formData,
    responseType: "arraybuffer",
    config: { headers: { "Content-Type": "multipart/form-data" } }
  })
    .then(response => {
      filename = response.headers["content-disposition"].split("=")[1];
      downloadFile(response.data, filename);
      SUBMIT_BUTTON_TEXT.innerText = "Convert";
      CONVERT_ICON.className = "fa fa-recycle";
      clearFiles();
      resetInput();
      renderDocs();
    })
    .catch(err => {
      SUBMIT_BUTTON_TEXT.innerText = "Convert";
      CONVERT_ICON.className = "fa fa-recycle";
      alert(err);
    });
  return false;
};

function downloadFile(data, filename) {
  const url = window.URL.createObjectURL(new Blob([data]));
  const link = document.createElement("a");
  link.href = url;
  link.setAttribute("download", filename);
  document.body.appendChild(link);
  link.click();
}

function clearFiles() {
  ALL_FILES = [];
}

function resetInput() {
  FILE_INPUT.value = "";
}
