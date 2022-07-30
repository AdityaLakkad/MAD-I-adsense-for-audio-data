const texts = document.querySelector(".texts");

window.SpeechRecognition =
  window.SpeechRecognition || window.webkitSpeechRecognition;

const recognition = new SpeechRecognition();
recognition.interimResults = true;


recognition.addEventListener("result", (e) => {

  const text = Array.from(e.results)
    .map((result) => result[0])
    .map((result) => result.transcript)
    .join("");
  var logedinUserId = $('#my-data').data();
  console.log(logedinUserId);
  if(e.results[0].isFinal){
    text.textContent = text;
    console.log(text);
    const xhr = new XMLHttpRequest();
    xhr.open('POST', 'http://127.0.0.1:5000/api/v1/pushString');
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = () => {
      console.log('Sent');
    };
    xhr.send(JSON.stringify({
      'user_id': logedinUserId,
      'string': text
    }));
  }
  console.log(text);
});
recognition.addEventListener("end", () => {
  recognition.start();
});
recognition.start();
