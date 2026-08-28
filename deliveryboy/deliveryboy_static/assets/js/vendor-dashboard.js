function showTab(t) {
        $('.tab-content').addClass('d-none'); $('#tab-'+t).removeClass('d-none');
        $('.sidebar-link').removeClass('active'); $('#link-'+t).addClass('active');
    }

    function previewProductImg(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function(e) {
                $('#img-preview').attr('src', e.target.result).show();
                $('#upload-icon').hide();
            }
            reader.readAsDataURL(input.files[0]);
        }
    }

    function addProduct() {
        const name = $('#prod-name').val();
        const price = $('#prod-price').val();
        const imgSrc = $('#img-preview').attr('src');
        if(name && price && imgSrc) {
            const newRow = `<tr>
                <td><img src="${imgSrc}" class="product-img-sm"></td>
                <td>${name}</td><td>$${price}</td><td><span class="badge bg-success">In Stock</span></td>
                <td><button class="btn btn-sm btn-outline-danger" onclick="$(this).closest('tr').remove()"><i class="fas fa-trash"></i></button></td>
            </tr>`;
            $('#product-table tbody').prepend(newRow);
            bootstrap.Modal.getInstance($('#addProductModal')).hide();
            $('#prod-name, #prod-price, #prod-img').val('');
            $('#img-preview').hide(); $('#upload-icon').show();
        } else { alert("Please complete all fields!"); }
    }

    function saveVendorProfile() {
        $('#disp-name').text($('#edit-name').val());
        $('#disp-contact').text($('#edit-contact').val());
        $('#disp-address').text($('#edit-address').val());
        const imgInput = document.getElementById('edit-img');
        if (imgInput.files && imgInput.files[0]) {
            const reader = new FileReader();
            reader.onload = (e) => $('#main-profile-img').attr('src', e.target.result);
            reader.readAsDataURL(imgInput.files[0]);
        }
        bootstrap.Modal.getInstance($('#editVendorModal')).hide();
    }

    function updateOrderStatus(id, val) {
        const badge = $('#status-' + id);
        badge.text(val).removeClass('badge-pending badge-shipped badge-delivered').addClass('badge-' + val.toLowerCase());
    }