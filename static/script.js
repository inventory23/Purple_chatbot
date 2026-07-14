const chatBox = document.getElementById("chat-box");
const input = document.getElementById("message");
const typing = document.getElementById("typing");

//------------------------------------------
// Add User Message
//------------------------------------------

function addUserMessage(message){

    const div = document.createElement("div");

    div.className = "user-message";

    div.innerText = message;

    chatBox.appendChild(div);

    scrollBottom();

}

//------------------------------------------
// Add AI Message
//------------------------------------------

function addBotMessage(message){

    const div = document.createElement("div");

    div.className = "bot-message";

    div.innerText = message;

    chatBox.appendChild(div);

    scrollBottom();

}

//------------------------------------------
// Scroll Chat
//------------------------------------------

function scrollBottom(){

    chatBox.scrollTop = chatBox.scrollHeight;

}

//------------------------------------------
// Send Message
//------------------------------------------

async function sendMessage(){

    const message = input.value.trim();

    if(message==="")
        return;

    addUserMessage(message);

    input.value="";

    typing.style.display="block";

    scrollBottom();

    try{

        const response = await fetch("/chat",{

            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify({

                message:message

            })

        });

        const data = await response.json();

        typing.style.display="none";

        if(data.status==="success"){

            addBotMessage(data.response);

        }
        else{

            addBotMessage("Error : "+data.response);

        }

    }

    catch(error){

        typing.style.display="none";

        addBotMessage("Unable to connect to Flask Server.");

    }

}

//------------------------------------------
// Press Enter
//------------------------------------------

input.addEventListener("keypress",function(e){

    if(e.key==="Enter"){

        sendMessage();

    }

});