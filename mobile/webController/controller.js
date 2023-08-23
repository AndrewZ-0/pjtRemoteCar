class ControllerClient {
    constructor() {
        this.socket = io.connect("http://raspberrypi.local:10000");
        //this.socket = io.connect("http://localhost:10000");
        this.socket.on("connect", () => {
            console.log("Connected to server");
            this.updateConnectionStatus(true);
            this.startControlling();
        });
        this.socket.on("disconnect", () => {
            console.log("Disconnected from server");
            this.updateConnectionStatus(false);
        });
    }

    startControlling() {
        console.log("Now controlling");
        const buttons = document.querySelectorAll(".button");

        buttons.forEach(button => {
            const sendDirection = (action) => {
                const message = `${action}_${button.dataset.direction}`;
                console.log("Sending:", message);
                this.socket.emit("message", message);
            };

            // pc
            button.addEventListener("mousedown", () => {
                sendDirection("START");
            });
            button.addEventListener("mouseup", () => {
                sendDirection("STOP");
            });
            button.addEventListener("mouseleave", () => {
                sendDirection("STOP");
            });

            // mobile
            button.addEventListener("touchstart", () => {
                sendDirection("START");
            });
            button.addEventListener("touchend", () => {
                sendDirection("STOP");
            });
            button.addEventListener("touchcancel", () => {
                sendDirection("STOP");
            });
        });
    }

    updateConnectionStatus(connected) {
        const connectionStatus = document.querySelector(".connection-status");
        connectionStatus.classList.toggle("connected", connected);
    }
}

const cc = new ControllerClient();