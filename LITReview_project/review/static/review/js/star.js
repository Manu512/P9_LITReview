function NumberToStar() {

    let stars = document.getElementsByClassName("stars");

    for (let i = 0; i < stars.length; i++) {
        let repeat = stars[i].innerText;
        stars[i].innerText = "\u2605".repeat(parseInt(repeat));

    }

}

NumberToStar();
