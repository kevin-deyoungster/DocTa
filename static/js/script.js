let ALL_FILES = [];
const FILE_LIST = document.getElementById('dropped-files');
const COUNT_VIEW = document.getElementById('count');
const FORM = document.getElementById('form');
const FILE_INPUT = document.getElementById('file');
const SUBMIT_BUTTON = document.getElementById('submitButton');
const CLEAR_LIST_BUTTON = document.getElementById('clearList');

function renderDocs() {
	FILE_LIST.innerHTML = '';
	COUNT_VIEW.innerText = ALL_FILES.length + ' Documents';

	ALL_FILES.forEach(file => {
		let li = document.createElement('li');
		li.className = 'dropped-file';
		li.innerText = file.name;
		let span = document.createElement('span');
		span.innerText = 'x';
		span.className = 'dropped-file-close';
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
	'change',
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
		formData.append('file[]', file);
	}

	SUBMIT_BUTTON.value = 'Converting...';
	axios({
		method: 'post',
		url: '/upload',
		data: formData,
		responseType: 'arraybuffer',
		config: { headers: { 'Content-Type': 'multipart/form-data' } }
	}).then(response => {
		filename = response.headers['content-disposition'].split('=')[1];
		downloadFile(response.data, filename);
		SUBMIT_BUTTON.value = 'Convert';
	});
	return false;
};

function downloadFile(data, filename) {
	const url = window.URL.createObjectURL(new Blob([data]));
	const link = document.createElement('a');
	link.href = url;
	link.setAttribute('download', filename);
	document.body.appendChild(link);
	link.click();
}

function clearFiles() {
	ALL_FILES = [];
}

function resetInput() {
	FILE_INPUT.value = '';
}
