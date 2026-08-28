$(document).ready(function() {
        // 1. Sync Header Cart Badge
        const savedQty = localStorage.getItem('petpal_cart_qty') || 0;
        if (parseInt(savedQty) > 0) {
            $('#header-cart-count').text(savedQty).show();
        } else {
            $('#header-cart-count').hide();
        }

        // 2. Form Submit Logic strictly following Data Dictionary Table V
        $('#appointmentForm').on('submit', function(e) {
            e.preventDefault();
            
            // Capture data according to Table V: APPOINTMENT TABLE
            const appointmentData = {
                cust_id: $('#cust_id').val(),           // Foreign Key from Table I
                vet_id: $('#vet_id').val(),             // Foreign Key from Table II
                description: $('#description').val(),   // Symptoms/Notes
                appointment_date: $('#appointment_date').val(), // DATETIME format
                appointment_status: $('#appointment_status').val() // Default 0 (Pending)
            };

            // Save pending appointment to memory for the payment page
            localStorage.setItem('pending_appointment', JSON.stringify(appointmentData));

            // Log for project debug requirement
            console.log("Appointment stored. Proceeding to Payment Sequence...");

            // Alert user of status before redirection
            alert("Appointment Request Received! 🐾 Proceeding to Secure Payment.");
            
            // REDIRECT TO PAYMENT PAGE per Table XIII
            window.location.href = "appointment-payment.html"; 
        });
    });