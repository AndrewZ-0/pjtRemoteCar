class ControllerClient {
    constructor() {
        this.socket = io.connect("http://raspberrypi.local:10000");
        this.socket.on("connect", () => {
            console.log("Connected to server");
            this.startControlling();
        });
    }

    startControlling() {
        console.log("Now controlling");
        const buttons = document.querySelectorAll(".button");
        const sendInterval = 200; // random number. replace later for tuning ...

        buttons.forEach(button => {
            let intervalId;

            const sendDirection = () => {
                var direction = button.classList[0];
                console.log("Sending:", direction);
                this.socket.emit("message", direction);
            };

            const startSending = () => {
                sendDirection();
                intervalId = setInterval(sendDirection, sendInterval);
            };

            const stopSending = () => {
                clearInterval(intervalId);
            };

            button.addEventListener("mousedown", startSending);
            button.addEventListener("touchstart", startSending);

            button.addEventListener("mouseup", stopSending);
            button.addEventListener("touchend", stopSending);

            button.addEventListener("mouseleave", stopSending);
            button.addEventListener("touchcancel", stopSending);
        });
    }
}

const cc = new ControllerClient();
