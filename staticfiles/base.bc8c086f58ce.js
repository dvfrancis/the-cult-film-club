// Utility function to get a cookie value by name (used for CSRF tokens)
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Main DOMContentLoaded event for all interactive features
document.addEventListener('DOMContentLoaded', function () {
    // Suppress CKEditor widget-toolbar-no-items errors
    const originalConsoleError = console.error;
    console.error = function(...args) {
        if (args[0] && args[0].includes && args[0].includes('widget-toolbar-no-items')) {
            return; // Suppress this specific error
        }
        originalConsoleError.apply(console, args);
    };

    // Also suppress CKEditor errors through the error event
    window.addEventListener('error', function(e) {
        if (e.message && e.message.includes('widget-toolbar-no-items')) {
            e.preventDefault();
            return false;
        }
    });

    // Filter dropdowns for releases page
    const allFiltersElem = document.getElementById('all-filters-data');
    if (allFiltersElem) {
        const allFilters = JSON.parse(allFiltersElem.textContent);
        const genreSelect = document.getElementById('genre-select');
        const subgenreSelect = document.getElementById('subgenre-select');
        const directorSelect = document.getElementById('director-select');
        const decadeSelect = document.getElementById('decade-select');
        const resetBtn = document.getElementById('reset-filters-btn');

        // Dynamically update dropdown options based on current selections
        function updateDropdowns() {
            const genre = genreSelect.value;
            const subgenre = subgenreSelect.value;
            const director = directorSelect.value;
            const decade = decadeSelect.value;
            // Populate genres
            const genres = [...new Set(
                allFilters.filter(f =>
                    (!subgenre || f.subgenre === subgenre) &&
                    (!director || f.director === director) &&
                    (!decade || String(f.decade) === decade)
                ).map(f => f.genre).filter(Boolean)
            )].sort();
            genreSelect.innerHTML = '<option value="">All Genres</option>' +
                genres.map(g => `<option value="${g}"${g === genre ? ' selected' : ''}>${g}</option>`).join('');
            if (genres.length === 1) {
                genreSelect.value = genres[0];
            }
            // Populate subgenres
            const subgenres = [...new Set(
                allFilters.filter(f =>
                    (!genre || f.genre === genre) &&
                    (!director || f.director === director) &&
                    (!decade || String(f.decade) === decade)
                ).map(f => f.subgenre).filter(Boolean)
            )].sort();
            subgenreSelect.innerHTML = '<option value="">All Subgenres</option>' +
                subgenres.map(s => `<option value="${s}"${s === subgenre ? ' selected' : ''}>${s}</option>`).join('');
            if (subgenres.length === 1) {
                subgenreSelect.value = subgenres[0];
            }
            // Populate directors
            const directors = [...new Set(
                allFilters.filter(f =>
                    (!genre || f.genre === genre) &&
                    (!subgenre || f.subgenre === subgenre) &&
                    (!decade || String(f.decade) === decade)
                ).map(f => f.director).filter(Boolean)
            )].sort();
            directorSelect.innerHTML = '<option value="">All Directors</option>' +
                directors.map(d => `<option value="${d}"${d === director ? ' selected' : ''}>${d}</option>`).join('');
            if (directors.length === 1) {
                directorSelect.value = directors[0];
            }
            // Populate decades
            const decades = [...new Set(
                allFilters.filter(f =>
                    (!genre || f.genre === genre) &&
                    (!subgenre || f.subgenre === subgenre) &&
                    (!director || f.director === director)
                ).map(f => f.decade).filter(Boolean)
            )].sort((a, b) => a - b);
            decadeSelect.innerHTML = '<option value="">All Decades</option>' +
                decades.map(d => `<option value="${d}"${String(d) === decade ? ' selected' : ''}>${d}s</option>`).join('');
            if (decades.length === 1) {
                decadeSelect.value = decades[0];
            }
        }

        // Attach event listeners for dropdowns to update and submit filters
        genreSelect.addEventListener('focus', updateDropdowns);
        subgenreSelect.addEventListener('focus', updateDropdowns);
        directorSelect.addEventListener('focus', updateDropdowns);
        decadeSelect.addEventListener('focus', updateDropdowns);

        genreSelect.addEventListener('change', function () {
            document.getElementById('filter-form').submit();
        });
        subgenreSelect.addEventListener('change', function () {
            document.getElementById('filter-form').submit();
        });
        directorSelect.addEventListener('change', function () {
            document.getElementById('filter-form').submit();
        });
        decadeSelect.addEventListener('change', function () {
            document.getElementById('filter-form').submit();
        });
        resetBtn.addEventListener('click', function (e) {
            e.preventDefault();
            genreSelect.value = '';
            subgenreSelect.value = '';
            directorSelect.value = '';
            decadeSelect.value = '';
            document.getElementById('filter-form').submit();
        });

        // Initial call to populate dropdowns on page load
        updateDropdowns();
    }

    // Quantity controls for cart items
    function EnableDisableQuantityChange(itemId) {
        let input = document.getElementById(`id_qty_${itemId}`);
        if (!input) return;
        let currentValue = parseInt(input.value);
        let minValue = parseInt(input.getAttribute('min')) || 1;
        let maxValue = parseInt(input.getAttribute('max'));
        let minusDisabled = currentValue <= minValue;
        let plusDisabled = currentValue >= maxValue;
        let decBtn = document.getElementById(`decrement-qty_${itemId}`);
        let incBtn = document.getElementById(`increment-qty_${itemId}`);
        if (decBtn) decBtn.disabled = minusDisabled;
        if (incBtn) incBtn.disabled = plusDisabled;
    }
    // Attach listeners to quantity input fields
    document.querySelectorAll('.qty_input').forEach(function (input) {
        let itemId = input.getAttribute('data-item_id');
        EnableDisableQuantityChange(itemId);
        input.addEventListener('change', function () {
            EnableDisableQuantityChange(itemId);
        });
    });
    // Increment quantity button
    document.querySelectorAll('.increment-qty').forEach(function (btn) {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            let input = this.closest('.input-group').querySelector('.qty_input');
            let currentValue = parseInt(input.value);
            let maxValue = parseInt(input.getAttribute('max'));
            if (currentValue < maxValue) {
                input.value = currentValue + 1;
                input.dispatchEvent(new Event('change'));
            }
        });
    });
    // Decrement quantity button
    document.querySelectorAll('.decrement-qty').forEach(function (btn) {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            let input = this.closest('.input-group').querySelector('.qty_input');
            let currentValue = parseInt(input.value);
            let minValue = parseInt(input.getAttribute('min')) || 1;
            if (currentValue > minValue) {
                input.value = currentValue - 1;
                input.dispatchEvent(new Event('change'));
            }
        });
    });

    // Update cart item quantity on click of update link
    document.querySelectorAll('.update-link').forEach(function (link) {
        link.addEventListener('click', function (e) {
            let form = this.previousElementSibling;
            if (form && form.classList.contains('update-form')) {
                form.submit();
            }
        });
    });

    // Remove item from cart and redirect to homepage if cart is empty
    document.querySelectorAll('.remove-item').forEach(function (link) {
        link.addEventListener('click', function (e) {
            let csrfToken = getCookie('csrftoken');
            let itemId = this.id.split('remove_')[1];
            let url = `/checkout/remove/${itemId}/`;
            let data = `csrfmiddlewaretoken=${encodeURIComponent(csrfToken)}`;
            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: data
            }).then(function (response) {
                if (response.ok) {
                    response.json().then(function (data) {
                        if (data.redirect) {
                            window.location.href = data.redirect;
                        } else {
                            location.reload();
                        }
                    }).catch(function () {
                        location.reload();
                    });
                }
            });
        });
    });

    // Tooltip for quantity input validation
    function showTooltip(input, message) {
        let oldTip = input.parentElement.querySelector('.qty-tooltip');
        if (oldTip) oldTip.remove();
        let tooltip = document.createElement('div');
        tooltip.className = 'qty-tooltip';
        tooltip.textContent = message;
        tooltip.style.top = (input.offsetTop - 30) + 'px';
        tooltip.style.left = input.offsetLeft + 'px';
        input.parentElement.style.position = 'relative';
        input.parentElement.appendChild(tooltip);
        setTimeout(function () {
            tooltip.remove();
        }, 2000);
    }
    // Listen for manual input and show tooltip if out of bounds
    document.querySelectorAll('.qty_input').forEach(function (input) {
        input.addEventListener('input', function () {
            let min = parseInt(this.getAttribute('min')) || 1;
            let max = parseInt(this.getAttribute('max'));
            let val = parseInt(this.value);
            if (val < min) {
                this.value = min;
                showTooltip(this, 'Minimum available is ' + min);
            } else if (max && val > max) {
                this.value = max;
                showTooltip(this, 'Maximum available is ' + max);
            }
        });
    });

    // Show all Bootstrap toasts (notifications)
    document.querySelectorAll('.toast').forEach(function (toastEl) {
        let toast = new bootstrap.Toast(toastEl, {
            delay: 3000
        });
        toast.show();
    });

    // Update delivery option on change
    let deliverySelect = document.getElementById('delivery_option');
    if (deliverySelect) {
        deliverySelect.addEventListener('change', function () {
            this.form.submit();
        });
    }

    // Stripe Payment Logic for checkout
    let stripe_public_key_elem = document.getElementById('id_stripe_public_key');
    let client_secret_elem = document.getElementById('id_client_secret');
    if (stripe_public_key_elem && client_secret_elem) {
        let stripePublicKey = JSON.parse(stripe_public_key_elem.textContent);
        let clientSecret = JSON.parse(client_secret_elem.textContent);
        let stripe = Stripe(stripePublicKey);
        let elements = stripe.elements();
        let style = {
            base: {
                color: '#000',
                fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
                fontSmoothing: 'antialiased',
                fontSize: '16px',
                '::placeholder': {
                    color: '#aab7c4'
                }
            },
            invalid: {
                color: '#dc3545',
                iconColor: '#dc3545'
            }
        };
        let card = elements.create('card', {
            style: style
        });
        card.mount('#card-element');
        card.on('change', function (event) {
            let errorDiv = document.getElementById('card-errors');
            if (event.error) {
                let html = `
                    <span class="icon" role="alert">
                        <i class="fas fa-times"></i>
                    </span>
                    <span>${event.error.message}</span>
                `;
                errorDiv.innerHTML = html;
            } else {
                errorDiv.textContent = '';
            }
        });

        // Helper function to poll for order and redirect to success page
        function pollForOrderAndRedirectByPid(pid, attempts = 0, maxAttempts = 30) {
            fetch(`/checkout/get-order-number-by-pid/${pid}/`)
                .then(response => response.json())
                .then(data => {
                    if (data.order_number) {
                        window.location.href = `/checkout/checkout_success/${data.order_number}/`;
                    } else if (attempts < maxAttempts) {
                        setTimeout(function () {
                            pollForOrderAndRedirectByPid(pid, attempts + 1, maxAttempts);
                        }, 2000); // 2 seconds
                    } else {
                        alert('Order processing is taking longer than expected. Please check your email for confirmation.');
                        window.location.href = '/checkout/';
                    }
                })
                .catch(() => {
                    if (attempts < maxAttempts) {
                        setTimeout(function () {
                            pollForOrderAndRedirectByPid(pid, attempts + 1, maxAttempts);
                        }, 2000);
                    } else {
                        alert('Order processing is taking longer than expected. Please check your email for confirmation.');
                        window.location.href = '/checkout/';
                    }
                });
        }
        // Stripe payment form submission handler
        let form = document.getElementById('payment-form');
        form.addEventListener('submit', function (ev) {
            ev.preventDefault();
            // Collect required fields and their user-friendly names
            const requiredFields = [{
                    field: form.full_name,
                    label: "Full Name"
                },
                {
                    field: form.email,
                    label: "Email Address"
                },
                {
                    field: form.phone_number,
                    label: "Phone Number"
                },
                {
                    field: form.street_address1,
                    label: "Street Address 1"
                },
                {
                    field: form.town_or_city,
                    label: "Town or City"
                },
                {
                    field: form.postcode,
                    label: "Postal Code"
                },
                {
                    field: form.country,
                    label: "Country"
                }
            ];

            // Find the first missing field
            for (let i = 0; i < requiredFields.length; i++) {
                const value = requiredFields[i].field ? requiredFields[i].field.value.trim() : "";
                if (!value) {
                    let errorDiv = document.getElementById('card-errors');
                    errorDiv.innerHTML = `
                <span class="icon" role="alert">
                    <i class="fas fa-times"></i>
                </span>
                <span>Please enter your ${requiredFields[i].label.toLowerCase()} before submitting payment.</span>
            `;
                    return; // Stop submission if any required field is missing
                }
            }
            card.update({
                'disabled': true
            });
            document.getElementById('submit-button').disabled = true;
            document.getElementById('payment-form').style.display = 'none';
            document.getElementById('loading-overlay').style.display = 'block';

            let saveInfo = document.getElementById('id-save-info') && document.getElementById('id-save-info').checked;
            let csrfToken = form.csrfmiddlewaretoken.value;
            let postData = new URLSearchParams({
                'csrfmiddlewaretoken': csrfToken,
                'client_secret': clientSecret,
                'save_info': saveInfo,
            });
            let url = '/checkout/cache_checkout_data/';

            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: postData.toString()
            }).then(function (response) {
                if (response.ok) {
                    stripe.confirmCardPayment(clientSecret, {
                        payment_method: {
                            card: card,
                            billing_details: {
                                name: form.full_name.value.trim(),
                                phone: form.phone_number.value.trim(),
                                email: form.email.value.trim(),
                                address: {
                                    line1: form.street_address1.value.trim(),
                                    line2: form.street_address2.value.trim(),
                                    city: form.town_or_city.value.trim(),
                                    country: form.country.value.trim(),
                                    state: form.county.value.trim(),
                                }
                            }
                        },
                        shipping: {
                            name: form.full_name.value.trim(),
                            phone: form.phone_number.value.trim(),
                            address: {
                                line1: form.street_address1.value.trim(),
                                line2: form.street_address2.value.trim(),
                                city: form.town_or_city.value.trim(),
                                country: form.country.value.trim(),
                                postal_code: form.postcode.value.trim(),
                                state: form.county.value.trim(),
                            }
                        },
                    }).then(function (result) {
                        if (result.error) {
                            let errorDiv = document.getElementById('card-errors');
                            let html = `
                                <span class="icon" role="alert">
                                <i class="fas fa-times"></i>
                                </span>
                                <span>${result.error.message}</span>`;
                            errorDiv.innerHTML = html;
                            document.getElementById('payment-form').style.display = 'block';
                            document.getElementById('loading-overlay').style.display = 'none';
                            card.update({
                                'disabled': false
                            });
                            document.getElementById('submit-button').disabled = false;
                        } else {
                            if (result.paymentIntent.status === 'succeeded') {
                                // Poll for the order and redirect to success page
                                pollForOrderAndRedirectByPid(result.paymentIntent.id);
                            }
                        }
                    });
                } else {
                    location.reload();
                }
            }).catch(function () {
                // Create toast HTML
                let toastHtml = `
                                <div class="toast align-items-center text-bg-danger border-0 show" role="alert" aria-live="assertive" aria-atomic="true">
                                    <div class="d-flex">
                                        <div class="toast-body">
                                            <i class="fas fa-exclamation-circle"></i>
                                            An error occurred. Please try again.
                                        </div>
                                        <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
                                    </div>
                                </div>
                            `;
                let container = document.querySelector('.message-container');
                if (container) {
                    container.insertAdjacentHTML('beforeend', toastHtml);
                    let toastEl = container.lastElementChild;
                    let toast = new bootstrap.Toast(toastEl, {
                        delay: 4000
                    });
                    toast.show();
                } else {
                    alert("An error occurred. Please try again.");
                }
            });
        });
    }
    // Handle lightbox button clicks to prevent carousel interference
    document.querySelectorAll('[data-bs-target="#lightboxModal"]').forEach(function (button) {
        button.addEventListener('click', function (e) {
            e.stopPropagation(); // Prevent carousel from handling the click
        });
    });

    // Lightbox modal for release details
    const lightboxModal = document.getElementById('lightboxModal');
    const lightboxImage = document.getElementById('lightboxImage');

    if (lightboxModal && lightboxImage) {
        lightboxModal.addEventListener('show.bs.modal', function (event) {
            const button = event.relatedTarget;
            const imageUrl = button.getAttribute('data-img-url');

            if (imageUrl) {
                lightboxImage.src = imageUrl;
                lightboxImage.alt = 'Large image preview';
            }
        });

        // Remove aria-hidden when modal is shown
        lightboxModal.addEventListener('shown.bs.modal', function () {
            lightboxModal.removeAttribute('aria-hidden');
        });

        // Clear lightbox image when modal is closed and restore aria-hidden
        lightboxModal.addEventListener('hidden.bs.modal', function () {
            lightboxImage.src = '';
            lightboxModal.setAttribute('aria-hidden', 'true');
        });
    }
});