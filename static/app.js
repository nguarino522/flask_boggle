document.addEventListener('DOMContentLoaded', (event) => {
    let score = 0;
    let time = 15;
    let words = new Set();

    document.getElementById("checkwordbtn").addEventListener("click", function (e) {
        e.preventDefault();

        word = $('#word').val();
        if (word.length === 0) {
            showMsg("Enter a word please in the input box.", "warn");
        } else {
            sendWordToServer(word);
        }
        $('#word').val('');
    });

    async function sendWordToServer(word) {
        let resp = await axios.get("/wordcheck", { params: { word: word } });
        console.log("got", resp);
        if (resp.data.result === "not-word") {
            showMsg(`The word "${word}" is not found in the application's dictionary.`, "err");
        } else if (resp.data.result === "not-on-board") {
            showMsg(`The word "${word}" was not found on current board.`, "warn");
        } else if (words.has(word)) {
            showMsg(`Already found the word "${word}" and scored.`, "warn");
        } else {
            showMsg(`Success! The word "${word}" was found. You earned ${word.length} points.`, "ok");
            score += word.length;
            $(".score").text(score);
            words.add(word);
            showWord(word);
        }
    }

    function showMsg(msg, lvl) {
        let msgDiv = document.getElementById("msgdiv");
        $("#msgdiv").empty();
        let newP = document.createElement("p");
        newP.classList.add("msg", `${lvl}`);
        newP.textContent = msg;
        msgDiv.appendChild(newP);
    }

    async function sendScoreToSever(score) {
        let resp = await axios.post("/score", { score: score });
        if (resp.data.brokeRecord) {
            showMsg(`New record score of ${score}, congrats!`, "ok");
            $("#highscore").text(`${score}`)
        }
    }

    function timer() {
        if (time !== 0) {
            $('.timer').text(time--);
        } else {
            $('.timer').text("0");
            clearInterval(myInterval);
            alert(`Time up! your score was: ${score}`);
            $("#word").prop("disabled", true);
            $("#checkwordbtn").prop("disabled", true);
            sendScoreToSever(score)

        };
    }

    document.getElementById("beginbtn").addEventListener("click", function (e) {
        e.preventDefault();
        myInterval = setInterval(timer, 1000);
        $("#word").prop("disabled", false);
        $("#checkwordbtn").prop("disabled", false);
        $("#beginbtn").prop("disabled", true);
        $("#tempboard").prop("hidden", true);
        $("#mainboard").prop("hidden", false);

    });

    function showWord(word){
        $(".usedwords").append($(`<li>${word} +${word.length}</li>`));
    };

});