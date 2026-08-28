function showTab(t) {
        $('.tab-content').addClass('d-none'); $('#tab-'+t).removeClass('d-none');
        $('.sidebar-link').removeClass('active'); $('#link-'+t).addClass('active');
    }

    function updateTask(id) {
        const btn = $('#btn-' + id);
        const status = $('#status-' + id);

        if (btn.text() === "Start Delivery") {
            status.text("Out for Delivery").removeClass('badge-pickup').addClass('badge-shipping');
            btn.text("Mark Delivered").removeClass('btn-brand').addClass('btn-success');
            alert("Order Status Updated: Out for Delivery!");
        } else {
            status.text("Delivered").removeClass('badge-shipping').addClass('badge-success');
            btn.remove();
            alert("Order Delivered Successfully! Table XII Updated.");
        }
    }

    function saveAgentProfile() {
        $('#disp-name').text($('#edit-name').val());
        $('#disp-contact').text($('#edit-contact').val());
        const imgInput = document.getElementById('edit-img');
        if (imgInput.files && imgInput.files[0]) {
            const reader = new FileReader();
            reader.onload = (e) => $('#main-profile-img').attr('src', e.target.result);
            reader.readAsDataURL(imgInput.files[0]);
        }
        bootstrap.Modal.getInstance($('#editAgentModal')).hide();
    }