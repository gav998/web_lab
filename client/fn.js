// Инициализация API функции получения списка тестов
async function get_test_list() {
	let url = new URL(server + "test_list/");

	let response = await fetch(url);
	if (response.ok) { // если HTTP-статус в диапазоне 200-299
		// получаем тело ответа
		let json = await response.json();
		console.log(decodeURI(url.href), '\n', json);
		return json;
	} else {
		console.log(url.href, '\n', decodeURI(url.href), '\n', "Ошибка HTTP: " + response.status);
		alert("Ошибка HTTP: " + response.status);
	}
}

// Инициализация API функции получения UUID теста send_choice_and_get_uuid(test) по адр get_uuid и редирект на тест
async function send_choice_and_get_uuid(test, name, num, letter) {
	let url = new URL(server + "get_uuid/");
	url.searchParams.set('test', test);
	url.searchParams.set('name', name);
	url.searchParams.set('num', num);
	url.searchParams.set('letter', letter);

	let response = await fetch(url);
	if (response.ok) { // если HTTP-статус в диапазоне 200-299
		// получаем тело ответа
		let json = await response.json();
		console.log(decodeURI(url.href), '\n', json);
		return json;
	} else {
		console.log(url.href, '\n', decodeURI(url.href), '\n', "Ошибка HTTP: " + response.status);
		alert("Ошибка HTTP: " + response.status);
	}
}



async function get_task(UUID, task) {
	let url = new URL(server + "get_test/");
	url.searchParams.set('UUID', UUID);
	url.searchParams.set('task', task);
	let response = await fetch(url);
	if (response.ok) { // если HTTP-статус в диапазоне 200-299
		// получаем тело ответа
		let json = await response.json();
		console.log(decodeURI(url.href), '\n', json);
		return json;
	} else {
		console.log(url.href, '\n', decodeURI(url.href), '\n', "Ошибка HTTP: " + response.status);
		alert("Ошибка HTTP: " + response.status);
	}
}

async function set_answ(UUID, task, answ) {
	let url = new URL(server + "set_answ/");
	url.searchParams.set('UUID', UUID);
	url.searchParams.set('task', task);
	url.searchParams.set('answ', answ);
	let response = await fetch(url);
	if (response.ok) { // если HTTP-статус в диапазоне 200-299
		// получаем тело ответа
		let json = await response.json();
		console.log(decodeURI(url.href), '\n', json);
		return json;
	} else {
		console.log(url.href, '\n', decodeURI(url.href), '\n', "Ошибка HTTP: " + response.status);
		alert("Ошибка HTTP: " + response.status);
	}
}

async function set_answ_file(UUID, task, answFile) {
	let url = new URL(server + "upload_file/");
	
	// Create a FormData object to send the file
    let formData = new FormData();
    formData.append('UUID', UUID);
    formData.append('task', task);
    formData.append('answ', answFile);

	let response = await fetch(url, {
            method: 'POST',
            body: formData,
        });
	if (response.ok) { // если HTTP-статус в диапазоне 200-299
		// получаем тело ответа
		let json = await response.json();
		console.log(decodeURI(url.href), '\n', json);
		return json;
	} else {
		console.log(url.href, '\n', decodeURI(url.href), '\n', "Ошибка HTTP: " + response.status);
		alert("Ошибка HTTP: " + response.status);
	}
}

// Инициализация API функции получения инфо и текста задания get_test() используя UUID, task по адр get_test
async function get_full_test_and_lock(UUID) {
	let url = new URL(server + "get_full_test_and_lock/");
	url.searchParams.set('UUID', UUID);
	let response = await fetch(url);
	if (response.ok) { // если HTTP-статус в диапазоне 200-299
		// получаем тело ответа
		let json = await response.json();
		console.log(decodeURI(url.href), '\n', json);
		return json;
	} else {
		console.log(url.href, '\n', decodeURI(url.href), '\n', "Ошибка HTTP: " + response.status);
		alert("Ошибка HTTP: " + response.status);
	}
}



async function get_headers(KEY) {
	let url = new URL(server + "get_headers/");
	url.searchParams.set('KEY', KEY);
	let response = await fetch(url);
	if (response.ok) { // если HTTP-статус в диапазоне 200-299
		// получаем тело ответа
		let json = await response.json();
		console.log(decodeURI(url.href), '\n', json);
		return json;
	} else {
		console.log(url.href, '\n', decodeURI(url.href), '\n', "Ошибка HTTP: " + response.status);
		alert("Ошибка HTTP: " + response.status);
	}
}


async function get_results(KEY, TIME_START, NUM, LETTER, TEST) {
	let url = new URL(server + "get_results/");
	url.searchParams.set('KEY', KEY);
	url.searchParams.set('TIME_START', TIME_START);
	url.searchParams.set('NUM', NUM);
	url.searchParams.set('LETTER', LETTER);
	url.searchParams.set('TEST', TEST);
	let response = await fetch(url);
	if (response.ok) { // если HTTP-статус в диапазоне 200-299
		// получаем тело ответа
		let json = await response.json();
		console.log(decodeURI(url.href), '\n', json);
		return json;
	} else {
		console.log(url.href, '\n', decodeURI(url.href), '\n', "Ошибка HTTP: " + response.status);
		alert("Ошибка HTTP: " + response.status);
	}
}



function read_GET_values() {
	console.log("Чтение GET параметров");
	let p_url = location.search.substring(1);
	let parametr = p_url.split("&");
	let values = new Array();
	for (let i = 0; i < parametr.length; i++) {
		j = parametr[i].split("=");
		values[j[0]] = unescape(j[1]);
	}
	console.log(values);
	return values
}
