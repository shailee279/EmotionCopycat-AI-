function check(emotion)
{  
    if (emotion.includes("Angry")) {
        alert("BINGO!!!!!!!!!!!!!!!!!!!!");
        document.getElementById("photo").src = "http://127.0.0.1:5000/static/happy-face.jpg";
        $("#photo").attr('src', "http://127.0.0.1:5000/static/happy-face.jpg");
        var emojies = document.getElementsByClassName("emoji") // this creates the array that I mentioned
        for (item in emojies) {
            emojies[item].style.visibility = 'hidden';
        }
    }
    else {
        alert("Wrong");
        var emojies = document.getElementsByClassName("emoji") // this creates the array that I mentioned
        for (item in emojies) {
            emojies[item].style.visibility = 'visible';
        }
    }
} 