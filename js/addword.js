/*LOAD STATISTCS AT PAGE LOAD*/

/*FUNCTION 1: Add a word*/
/*FUNCTION 2: Give random word from words left*/
/*FUNCTION 3: suceess > add a score and remove word from the list*/
/*FUNCTION 4: failure > remove display and don t update the points*/
/*FUNCTION 3: reset*/


/*DATBASE 1: score
team - point
DATABASE 2: remaining words
word - used yes-no
*/

$(document).ready(function () {

    
        // GIVE ME A NEW WORD FROM THE LIST
        document.getElementById("new-word-button").addEventListener("click", function (e) {
            e.preventDefault()
            $.ajax({
                url: 'https://mt886qkbt9.execute-api.us-east-1.amazonaws.com/default/next-word',
                type: 'get',
                success: function (data1) {
                    console.log("ask for new word");
                    console.log(data1);
                    document.getElementById("new-word").placeholder = data1.Item.word;
                }
            })
        })
    
    
        // CLEAR WORD


    })
    
  