function saveVetProfile() {
            const newName = document.getElementById('edit-name').value;
            const newAddr = document.getElementById('edit-address').value;
            const imgInput = document.getElementById('edit-img-input');

            document.getElementById('display-name').innerText = newName;
            document.getElementById('display-address').innerHTML = `<i class="fas fa-map-marker-alt me-2"></i>${newAddr}`;
            document.getElementById('header-id-info').innerText = `${newName} | Vet_id: 201 | Expert Surgeon`;

            if (imgInput.files && imgInput.files[0]) {
                const reader = new FileReader();
                reader.onload = (e) => document.getElementById('main-profile-img').src = e.target.result;
                reader.readAsDataURL(imgInput.files[0]);
            }
            bootstrap.Modal.getInstance(document.getElementById('editProfileModal')).hide();
            alert("Profile Synced! 🐾");
        }

        function acceptAppt() {
            alert("Request Accepted.");
            document.getElementById('btn-acc').classList.add('d-none');
            document.getElementById('btn-upl').classList.remove('d-none');
        }

        function reportUploaded() {
            alert("Report Uploaded.");
            document.getElementById('btn-upl').classList.add('d-none');
            document.getElementById('btn-clm').classList.remove('d-none');
        }

        function claimMoney() {
            alert("Payment Claim Request Sent!");
            document.getElementById('btn-clm').classList.add('d-none');
            document.getElementById('btn-done').classList.remove('d-none');
        }