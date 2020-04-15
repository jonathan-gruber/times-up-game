

$(document).ready(function () {

    // GIVE ME A NEW WORD FROM THE LIST
    let currentword = document.getElementById("new-word").value;
    if (currentword == "") {
        currentword = "empty"
    }

    document.getElementById("new-word-button").addEventListener("click", function (e) {
        e.preventDefault()
        $.ajax({
            url: 'https://abc.execute-api.us-east-1.amazonaws.com/default/next-word?word=' + currentword + "&remove=no&team=noteamselected",
            type: 'get',
            success: function (data1) {
                console.log("ask for new word");
                console.log(data1);
                if (data1.Items.length == 0) {
                    document.getElementById("new-word").value = "no more words"
                } else {
                    var randomword = Math.floor(Math.random() * data1.Count);
                    document.getElementById("new-word").value = data1.Items[randomword].word;
                    document.getElementById("words-left").innerText = data1.Count + " words left";

                }
            }
        })
    })


    document.getElementById("stats-button").addEventListener("click", function (e) {
        e.preventDefault()
        $.ajax({
            url: 'https://abc.execute-api.us-east-1.amazonaws.com/default/timesup-getscore',
            type: 'get',
            success: function (data1) {
                console.log(data1);
                //   document.getElementById("printscores").innerText = "team A: "+ data1.Items[0].score + "   |   team B: " + data1.Items[2].score;

                var legend = [];
                var scores = [];
                data1.Items.forEach(function (item) {
                    if (item.score != 0) {
                        if (item.team == "teama") {
                            legend.push("Team A");
                        } else if (item.team == "teamb") {
                            legend.push("Team B");
                        } else if (item.team == "teamc") {
                            legend.push("Team C");
                        } else {
                            legend.push(item.team);
                        }
                        scores.push(item.score);
                    }
                });

                console.log(legend)
                console.log(scores)
                // UPDATE GRAPH

                // Bar chart
                new Chart(document.getElementById("score-graph"), {
                    type: 'bar',
                    data: {
                        labels: legend,
                        datasets: [
                            {
                                label: "teams",
                                backgroundColor: ["#c45850", "#8e5ea2", "#3cba9f", "#e8c3b9"],
                                data: scores
                            }
                        ]
                    },
                    options: {
                        legend: { display: false },
                        title: {
                            display: true,
                            text: 'team score'
                        },
                        scales: {
                            yAxes: [{
                                ticks: {
                                    beginAtZero: true
                                }
                            }]
                        }
                    }
                });


            }
        })
    })

    document.getElementById("reset-button").addEventListener("click", function (e) {
        e.preventDefault()
        $.ajax({

            url: 'https://abc.execute-api.us-east-1.amazonaws.com/default/reset-timesup',
            type: 'get',
            success: function (data1) {
                console.log("Reset Words for Next Phase");
                console.log(data1);
                document.getElementById("reset-words").innerText = "list of words has been successfully cleared for next phase"

            }
        })
    })

    document.getElementById("clear-button").addEventListener("click", function () {
        console.log("clear words");
        document.getElementById("new-word").value = "";
    });


    document.getElementById("found-button").addEventListener("click", function (e) {
        e.preventDefault()
        if (document.getElementById("new-word").value == "") {
            alert("You need to have a word to be guessed to click on Found")
        } else {
            $.ajax({
                url: 'https://abc.execute-api.us-east-1.amazonaws.com/default/next-word?remove=yes&team=' + document.getElementById("selected-team").value + '&word=' + document.getElementById("new-word").value,
                type: 'get',
                success: function (data1) {
                    console.log("ask for new word");
                    console.log(data1);
                    if (data1.Items.length == 0) {
                        document.getElementById("new-word").value = "no more words"
                        document.getElementById("words-left").innerText = "0 words left";

                    } else {
                        var randomword = Math.floor(Math.random() * data1.Count);
                        document.getElementById("new-word").value = data1.Items[randomword].word;
                        document.getElementById("words-left").innerText = data1.Count + " words left";

                    }
                }
            })
        }
    })
})



