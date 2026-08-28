function switchPay(type) {
            $('.pay-tab').removeClass('active');
            if(type === 'card') {
                $('.pay-tab').eq(0).addClass('active');
                $('#card-form').stop().show(); $('#upi-form').hide();
            } else {
                $('.pay-tab').eq(1).addClass('active');
                $('#card-form').hide(); $('#upi-form').stop().show();
            }
        }

        $(document).ready(function() {
            // Fetch appointment data from memory (from reservation.html)
            const pending = JSON.parse(localStorage.getItem('pending_appointment'));
            
            // Logic to calculate fees based on your Revenue Model 
            const baseFee = 1500; // From Vet_Table example [cite: 931]
            const platFee = 50;   // Your platform commission charge
            const total = baseFee + platFee;

            $('#vet-fee').text('$' + baseFee.toFixed(2));
            $('#platform-fee').text('$' + platFee.toFixed(2));
            $('#total-amount').text('$' + total.toFixed(2));

            $('#paymentForm').on('submit', function(e) {
                e.preventDefault();

                // Fulfilling Table XIII requirements 
                const paymentData = {
                    app_payment_id: "PAY-" + Math.floor(Math.random() * 10000),
                    appointment_id: pending ? pending.vet_id : "501",
                    payment_mode: "Online",
                    amount: total,
                    payment_status: 1, // Success
                    payment_token: "TOK-" + Math.random().toString(36).substr(2, 9).toUpperCase(),
                    payment_date: new Date().toISOString().split('T')[0],
                    payment_time: new Date().toLocaleTimeString()
                };

                console.log("Final Database Payload (Table XIII):", paymentData);
                alert("Wag-tastic! 🐾 Your Appointment Payment is Successful.\nTransaction ID: " + paymentData.payment_token);
                
                // Clear pending data and return home
                localStorage.removeItem('pending_appointment');
                window.location.href = "index.html";
            });
        });