
html = """
<html>
    <head>
        <title>WebSocket</title>
        <style>
            body {
                padding:1rem;
                background:lightblue;
                display:flex;
                justify-content:center;
            }
            .container, form, .form_section {
                display:flex;
                justify-content:center;
                flex-direction:column;
                gap:1rem;
                width:100%;
                max-width:800px;
            }
            .form_section {
                flex-direction:row;
                gap:0;
            }
            input {
                width:100%;
                padding:5px;
            }
            button {
                padding:1rem;
                cursor:pointer;
            }
            p.message  {
                background:white;
                padding:.5rem;
            }
        </style>
    </head>
    <body>
        <div class="container">
                <h1>API docs 
                    <a href="/docs" target="__blank">here</a>
                </h1>
                <button type="button" id="clearMessageButton">Clear messages</button>
                <form id="form" >
                        <div class="form_section"><p id="endpoint"></p></div>
                        <div class="form_section">
                            <input type="text" id="chat_id_value" value="1" maxlength="60"/>
                            <button type="button" onclick="reconnectWebSocket()">Reconnect</button>
                        </div>
                        <div class="form_section">
                            <input type="text" id="message_value" />
                            <button type="submit">Send</button>
                        </div>
                </form>
                <div id="messages_container"></div>
        </div>
        <script defer>
            
            function getURL(){
                const chatId = document.getElementById("chat_id_value").value.trim().replaceAll(" ", "");
                return `ws://${window.location.host}/chat/${chatId}`;
            }

            var ws = new WebSocket(getURL());
            const form = document.getElementById("form");
            const input = document.getElementById("message_value");
            const clearMessageButton = document.getElementById("clearMessageButton");
            const messagesContainer = document.getElementById("messages_container");
            
            var startTime = new Date().getTime();

            form.addEventListener("submit", 
                function submitHandler(e){
                    e.preventDefault();
                    startTime = new Date().getTime();
                    ws.send(input.value);
                    input.value = "";
                
            });
            function clearMessages(){
                messagesContainer.innerHTML = "";
            }

            clearMessageButton.addEventListener("click", clearMessages);

            ws.onopen = function(e){
                console.log("Connected");
            }
            ws.onclose = function(e){ 
                console.log("Close");
            }
            ws.onmessage = function(e){
                const p = document.createElement("p");
                p.classList.add("message");
                const time = new Date().getTime() - startTime;

                // const data = JSON.parse((e.data));

                // console.log(message.message);

                p.innerText = `time: ${time}ms \nMessage: ${e.data}`;
                
                messagesContainer.prepend(p);
            }
            
            function reconnectWebSocket(){
                const endpoint = document.getElementById("endpoint");
                const url = getURL();
                endpoint.innerText = url;
                location.reload();

            }
            
            window.addEventListener("load",  function (){
                document.getElementById("endpoint").innerText = getURL();
            });

        </script>
    </body>
</html>
"""