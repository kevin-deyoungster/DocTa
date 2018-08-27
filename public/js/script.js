let ALL_FILES = [];
const FILE_LIST = document.getElementById("dropped-files");
const COUNT_VIEW = document.getElementById("count");
const FORM = document.getElementById("form");
const FILE_INPUT = document.getElementById("file");
const SUBMIT_BUTTON_TEXT = document.getElementById("submitButtonText");
const CLEAR_LIST_BUTTON = document.getElementById("clearList");

const DROP_ICON = document.getElementById("drop-icon");

["dragenter", "dragover", "dragleave", "drop"].forEach(eventName => {
  FORM.addEventListener(eventName, preventDefault, false);
});

function preventDefault(e) {
  e.preventDefault();
  e.stopPropagation();
}

FORM.addEventListener("drop", handleDrop, false);

function handleDrop(e) {
  let dt = e.dataTransfer;
  let files = dt.files;
  handleFiles(files);
}

function handleFiles(files) {
  // Get list of names of all files
  ALL_FILES_NAMES = ALL_FILES.map(item => {
    return item.name;
  });

  ALL_FILES = Array.from(files)
    .filter(item => {
      console.log(item);
      return (
        /.docx|.pptx/.test(item.name) &
        (ALL_FILES_NAMES.includes(item.name) == false)
      );
    })
    .concat(Array.from(ALL_FILES));
  console.log(ALL_FILES);
  renderDocs();
}

function renderDocs() {
  // Clear Everything in the list
  let lis = FILE_LIST.querySelectorAll("li");
  for (let li of lis) {
    li.parentNode.removeChild(li);
  }

  COUNT_VIEW.innerText = ALL_FILES.length + " Documents";

  if (ALL_FILES.length > 0) {
    DROP_ICON.style.display = "None";
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
  } else {
    DROP_ICON.style.display = "block";
  }
}

FILE_INPUT.addEventListener(
  "change",
  function() {
    ALL_FILES = Array.from(this.files)
      .filter(item => {
        return /.docx|.pptx/.test(item.name);
      })
      .concat(Array.from(ALL_FILES));
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

  if (ALL_FILES.length > 0) {
    let formData = new FormData();
    for (let file of ALL_FILES) {
      formData.append("file[]", file);
    }

    SUBMIT_BUTTON_TEXT.innerText = "Converting...";
    CONVERT_ICON = document.querySelector(".fa-recycle");
    CONVERT_ICON.className = "fa fa-refresh fa-spin";

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
        showError(err.toString());
      });
    return false;
  }
};

function showError(error) {
  if (error.includes("Network")) {
    alert(
      "Server Not Running :( \nLooks like you need to run the server ('docta.py') again"
    );
  } else if (error.includes("500")) {
    alert(
      "Server's Messed Up :(\nLook, it's not you, it's not me, it's the server. Something probably went wrong during conversion.\n Please contact my creator"
    );
  } else {
    alert(erorr);
  }
}

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
