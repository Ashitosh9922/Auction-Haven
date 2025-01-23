const chatSocket = new WebSocket(
    (window.location.protocol === "https:" ? "wss://" : "ws://") + window.location.host + "/ws/auction/"
);


chatSocket.onopen = () => {
    console.log("WebSocket connection established.");
};

chatSocket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log("Message received:", data);
};

chatSocket.onclose = (event) => {
    console.error("WebSocket closed unexpectedly.");
};
