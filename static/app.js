document.addEventListener('DOMContentLoaded', (event) => {
    let score = 0;

    document.getElementById("checkwordbtn").addEventListener("click", function(e){
        e.preventDefault();
        
        word = $('#word').val();
        if (word.length === 0 ){
            alert("Enter a word please");
        } else {
            sendWordToServer(word);
        }
        $('#word').val('');
    });

    async function sendWordToServer(word){
        let resp = await axios.get("/wordcheck", { params: { word: word }});
        console.log("got", resp);
        if (resp.data === "not-word"){
            showMsg(`The word ${word} is not found in the application's dictionary.`, "err");
        } else if (resp.data === "not-on-board"){
            showMsg(`The word ${word} was not found on current board.`, "warn");
        } else {
            showMsg(`Success! The word ${word} was found.`, "ok");
            score += word.length;
            $(".score").text(score);
        }
    }

    function showMsg(msg, lvl){
        let msgDiv = document.getElementById("msgdiv");
        $("#msgdiv").empty();
        let newP = document.createElement("p");
        newP.classList.add("msg", `${lvl}`);
        newP.textContent = msg;
        msgDiv.appendChild(newP);
        
        //$(".msg").text(msg).removeClass().addClass(`msg ${lvl}`);
    }

    async function sendScoreToSever(score){
        let resp = await axios.post("/score")
    }
});