// barcode_scanner.js
document.addEventListener("DOMContentLoaded", function() {
    const barcodeInput = document.getElementById("barcodeInput");
    const captureButton = document.getElementById("captureButton");

    Quagga.init({
        inputStream: {
            constraints: {
                facingMode: "environment" // Use the rear camera
            }
        },
        decoder: {
            readers: ["ean_reader"] // You can add more reader types here
        }
    }, function(err) {
        if (err) {
            console.error("Quagga initialization failed:", err);
            return;
        }
        console.log("Quagga initialized successfully");
        Quagga.start();
    });

    Quagga.onDetected(function(result) {
        const barcodeResult = result.codeResult.code;
        barcodeInput.value = barcodeResult;
        Quagga.stop();
    });

    captureButton.addEventListener("click", function() {
        Quagga.start();
    });
});