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

document.addEventListener('DOMContentLoaded', function () {
    // --- Filter dropdowns ---
    const allFiltersElem = document.getElementById('all-filters-data');
    if (allFiltersElem) {
        const allFilters = JSON.parse(allFiltersElem.textContent);
        const genreSelect = document.getElementById('genre-select');
        const subgenreSelect = document.getElementById('subgenre-select');
        const directorSelect = document.getElementById('director-select');
        const decadeSelect = document.getElementById('decade-select');
        const resetBtn = document.getElementById('reset-filters-btn');

        genreSelect.addEventListener('focus', updateDropdowns);
        subgenreSelect.addEventListener('focus', updateDropdowns);
        directorSelect.addEventListener('focus', updateDropdowns);
        decadeSelect.addEventListener('focus', updateDropdowns);


        function updateDropdowns() {
            const genre = genreSelect.value;
            const subgenre = subgenreSelect.value;
            const director = directorSelect.value;
            const decade = decadeSelect.value;
            // GENRES
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
            // SUBGENRES
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
            // DIRECTORS
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
            // DECADES
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

        // Initial call to populate dropdowns
        updateDropdowns();
    }

    // --- Quantity controls ---
    function EnableDisableQuantityChange(itemId) {
        var input = document.getElementById(`id_qty_${itemId}`);
        if (!input) return;
        var currentValue = parseInt(input.value);
        var minValue = parseInt(input.getAttribute('min')) || 1;
        var maxValue = parseInt(input.getAttribute('max'));
        var minusDisabled = currentValue <= minValue;
        var plusDisabled = currentValue >= maxValue;
        var decBtn = document.getElementById(`decrement-qty_${itemId}`);
        var incBtn = document.getElementById(`increment-qty_${itemId}`);
        if (decBtn) decBtn.disabled = minusDisabled;
        if (incBtn) incBtn.disabled = plusDisabled;
    }
    document.querySelectorAll('.qty_input').forEach(function (input) {
        var itemId = input.getAttribute('data-item_id');
        EnableDisableQuantityChange(itemId);
        input.addEventListener('change', function () {
            EnableDisableQuantityChange(itemId);
        });
    });
    document.querySelectorAll('.increment-qty').forEach(function (btn) {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            var input = this.closest('.input-group').querySelector('.qty_input');
            var currentValue = parseInt(input.value);
            var maxValue = parseInt(input.getAttribute('max'));
            if (currentValue < maxValue) {
                input.value = currentValue + 1;
                input.dispatchEvent(new Event('change'));
            }
        });
    });
    document.querySelectorAll('.decrement-qty').forEach(function (btn) {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            var input = this.closest('.input-group').querySelector('.qty_input');
            var currentValue = parseInt(input.value);
            var minValue = parseInt(input.getAttribute('min')) || 1;
            if (currentValue > minValue) {
                input.value = currentValue - 1;
                input.dispatchEvent(new Event('change'));
            }
        });
    });

    // --- Update quantity on click ---
    document.querySelectorAll('.update-link').forEach(function (link) {
        link.addEventListener('click', function (e) {
            var form = this.previousElementSibling;
            if (form && form.classList.contains('update-form')) {
                form.submit();
            }
        });
    });

    // --- Remove item from cart and redirect to homepage if cart empty ---
    document.querySelectorAll('.remove-item').forEach(function (link) {
        link.addEventListener('click', function (e) {
            var csrfToken = getCookie('csrftoken');
            var itemId = this.id.split('remove_')[1];
            var url = `/checkout/remove/${itemId}/`;
            var data = `csrfmiddlewaretoken=${encodeURIComponent(csrfToken)}`;
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

    // --- Tooltip for quantity input ---
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
    document.querySelectorAll('.qty_input').forEach(function (input) {
        input.addEventListener('input', function () {
            var min = parseInt(this.getAttribute('min')) || 1;
            var max = parseInt(this.getAttribute('max'));
            var val = parseInt(this.value);
            if (val < min) {
                this.value = min;
                showTooltip(this, 'Minimum available is ' + min);
            } else if (max && val > max) {
                this.value = max;
                showTooltip(this, 'Maximum available is ' + max);
            }
        });
    });

    // --- Show all Bootstrap toasts ---
    document.querySelectorAll('.toast').forEach(function (toastEl) {
        var toast = new bootstrap.Toast(toastEl, {
            delay: 3000
        });
        toast.show();
    });

    // --- Update delivery option on change ---
    var deliverySelect = document.getElementById('delivery_option');
    if (deliverySelect) {
        deliverySelect.addEventListener('change', function () {
            this.form.submit();
        });
    }

    // --- Stripe Payment Logic ---
    var stripe_public_key_elem = document.getElementById('id_stripe_public_key');
    var client_secret_elem = document.getElementById('id_client_secret');
    if (stripe_public_key_elem && client_secret_elem) {
        var stripePublicKey = JSON.parse(stripe_public_key_elem.textContent);
        var clientSecret = JSON.parse(client_secret_elem.textContent);
        var stripe = Stripe(stripePublicKey);
        var elements = stripe.elements();
        var style = {
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
        var card = elements.create('card', {
            style: style
        });
        card.mount('#card-element');
        card.on('change', function (event) {
            var errorDiv = document.getElementById('card-errors');
            if (event.error) {
                var html = `
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

        // Helper for polling order and redirecting
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
        var form = document.getElementById('payment-form');
        form.addEventListener('submit', function (ev) {
            ev.preventDefault();
            card.update({
                'disabled': true
            });
            document.getElementById('submit-button').disabled = true;
            document.getElementById('payment-form').style.display = 'none';
            document.getElementById('loading-overlay').style.display = 'block';

            var saveInfo = document.getElementById('id-save-info') && document.getElementById('id-save-info').checked;
            var csrfToken = form.csrfmiddlewaretoken.value;
            var postData = new URLSearchParams({
                'csrfmiddlewaretoken': csrfToken,
                'client_secret': clientSecret,
                'save_info': saveInfo,
            });
            var url = '/checkout/cache_checkout_data/';

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
                            var errorDiv = document.getElementById('card-errors');
                            var html = `
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
                location.reload();
            });
        });
    }
});

// Lightbox modal for release details
document.addEventListener('DOMContentLoaded', function () {
    var lightboxModal = document.getElementById('lightboxModal');
    var lightboxImage = document.getElementById('lightboxImage');
    var carouselImages = document.querySelectorAll('[data-bs-target="#lightboxModal"]');

    carouselImages.forEach(function (imgLink) {
        imgLink.addEventListener('click', function (e) {
            e.preventDefault();
            var imgUrl = this.getAttribute('data-img-url');
            if (imgUrl && lightboxImage) {
                lightboxImage.src = imgUrl;
            }
        });
    });

    if (lightboxModal) {
        lightboxModal.addEventListener('hidden.bs.modal', function () {
            if (lightboxImage) {
                lightboxImage.src = '';
            }
        });
    }
});