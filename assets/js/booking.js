// ==================== QUICK BOOKING MODULE (VIETMAP) ====================

class QuickBooking {
    constructor() {
        // VietMap configuration (replace key in production)
        this.VIETMAP_API_KEY = '53ec8c719c14153d869267e0d128744358409b741db32847';
        this.VIETMAP_STYLE_URL = `https://maps.vietmap.vn/maps/styles/tm/style.json?apikey=${this.VIETMAP_API_KEY}`;
        this.VIETMAP_AUTOCOMPLETE_URL = 'https://maps.vietmap.vn/api/autocomplete/v4';
        this.VIETMAP_PLACE_URL = 'https://maps.vietmap.vn/api/place/v4';
        this.VIETMAP_REVERSE_URL = 'https://maps.vietmap.vn/api/reverse/v4';
        this.VIETMAP_ROUTE_URL = 'https://maps.vietmap.vn/api/route/v3';

        this.mapCenter = { lat: 16.0544, lng: 108.2022 }; // Da Nang
        this.pickupCoords = null;
        this.dropoffCoords = null;
        this.distanceKm = 0;
        this.durationMinutes = 0;
        this.activeMapTarget = 'pickup';

        this.routeSourceId = 'booking-route-source';
        this.routeLayerId = 'booking-route-layer';

        // DOM Elements
        this.pickupInput = document.getElementById('pickup-input');
        this.dropoffInput = document.getElementById('dropoff-input');
        this.pickupSuggestions = document.getElementById('pickup-suggestions');
        this.dropoffSuggestions = document.getElementById('dropoff-suggestions');
        this.pickupLocateBtn = document.getElementById('pickup-locate-btn');
        this.pickupMapBtn = document.getElementById('pickup-map-btn');
        this.dropoffMapBtn = document.getElementById('dropoff-map-btn');

        this.distanceDisplay = document.getElementById('distance-display');
        this.durationDisplay = document.getElementById('duration-display');
        this.priceDisplay = document.getElementById('price-display');

        this.form = document.getElementById('quick-booking-form');
        this.submitBtn = document.getElementById('submit-booking-btn');
        this.errorMsg = document.getElementById('booking-error-msg');
        this.successMsg = document.getElementById('booking-success-msg');

        this.markers = {};

        this.initMap();
        this.initAutocomplete();
        this.initMapButtons();
        this.initFormSubmit();
    }

    // Initialize VietMap GL map
    initMap() {
        this.map = new vietmapgl.Map({
            container: 'booking-map',
            style: this.VIETMAP_STYLE_URL,
            center: [this.mapCenter.lng, this.mapCenter.lat],
            zoom: 13,
            minZoom: 10,
            maxZoom: 18,
        });

        this.map.addControl(new vietmapgl.NavigationControl({ showCompass: true }), 'top-right');

        this.map.on('click', async (e) => {
            const lng = e.lngLat.lng;
            const lat = e.lngLat.lat;
            const address = await this.reverseGeocode(lat, lng);

            if (this.activeMapTarget === 'dropoff') {
                this.dropoffInput.value = address;
                this.setLocation('dropoff', lat, lng, address);
            } else {
                this.pickupInput.value = address;
                this.setLocation('pickup', lat, lng, address);
            }
        });

        this.map.on('load', () => {
            this.map.addSource(this.routeSourceId, {
                type: 'geojson',
                data: {
                    type: 'FeatureCollection',
                    features: [],
                },
            });

            this.map.addLayer({
                id: this.routeLayerId,
                type: 'line',
                source: this.routeSourceId,
                layout: {
                    'line-join': 'round',
                    'line-cap': 'round',
                },
                paint: {
                    'line-color': '#006BFD',
                    'line-width': 5,
                    'line-opacity': 0.85,
                },
            });
        });
    }

    initMapButtons() {
        if (this.pickupMapBtn) {
            this.pickupMapBtn.addEventListener('click', () => {
                this.setActiveMapTarget('pickup');
                this.showSuccess('Đã bật chọn Điểm Đón trên bản đồ. Hãy bấm vào vị trí cần đón.');
            });
        }

        if (this.dropoffMapBtn) {
            this.dropoffMapBtn.addEventListener('click', () => {
                this.setActiveMapTarget('dropoff');
                this.showSuccess('Đã bật chọn Điểm Đến trên bản đồ. Hãy bấm vào vị trí cần trả.');
            });
        }

        if (this.pickupLocateBtn) {
            this.pickupLocateBtn.addEventListener('click', () => this.locatePickupByBrowser());
        }

        this.setActiveMapTarget('pickup');
    }

    setActiveMapTarget(target) {
        this.activeMapTarget = target;
        this.pickupMapBtn?.classList.toggle('active', target === 'pickup');
        this.dropoffMapBtn?.classList.toggle('active', target === 'dropoff');
    }

    async locatePickupByBrowser() {
        if (!navigator.geolocation) {
            this.showError('Trình duyệt không hỗ trợ định vị GPS.');
            return;
        }

        this.clearError();

        navigator.geolocation.getCurrentPosition(
            async (position) => {
                const lat = position.coords.latitude;
                const lng = position.coords.longitude;
                const address = await this.reverseGeocode(lat, lng);

                this.pickupInput.value = address;
                this.setLocation('pickup', lat, lng, address);
                this.map.flyTo({ center: [lng, lat], zoom: 15 });
            },
            (error) => {
                console.error('Lỗi định vị:', error);
                this.showError('Không thể lấy vị trí hiện tại. Vui lòng cho phép quyền định vị.');
            },
            {
                enableHighAccuracy: true,
                timeout: 12000,
                maximumAge: 0,
            }
        );
    }

    initAutocomplete() {
        let pickupTimeout;
        let dropoffTimeout;

        this.pickupInput.addEventListener('input', (e) => {
            clearTimeout(pickupTimeout);
            const query = e.target.value.trim();

            if (query.length < 2) {
                this.pickupSuggestions.classList.add('hidden');
                return;
            }

            pickupTimeout = setTimeout(() => {
                this.fetchSuggestions(query, 'pickup');
            }, 300);
        });

        this.dropoffInput.addEventListener('input', (e) => {
            clearTimeout(dropoffTimeout);
            const query = e.target.value.trim();

            if (query.length < 2) {
                this.dropoffSuggestions.classList.add('hidden');
                return;
            }

            dropoffTimeout = setTimeout(() => {
                this.fetchSuggestions(query, 'dropoff');
            }, 300);
        });

        document.addEventListener('click', (e) => {
            if (!e.target.closest('#quick-booking-form')) {
                this.pickupSuggestions.classList.add('hidden');
                this.dropoffSuggestions.classList.add('hidden');
            }
        });
    }

    async fetchSuggestions(query, type) {
        try {
            const response = await axios.get(this.VIETMAP_AUTOCOMPLETE_URL, {
                params: {
                    apikey: this.VIETMAP_API_KEY,
                    text: query,
                    focus: `${this.mapCenter.lat},${this.mapCenter.lng}`,
                    display_type: 5,
                },
            });

            const suggestions = Array.isArray(response.data) ? response.data : [];
            this.showSuggestions(suggestions, type);
        } catch (error) {
            console.error('Lỗi autocomplete VietMap:', error);
            this.showError('Không thể gợi ý địa chỉ. Vui lòng thử lại.');
        }
    }

    showSuggestions(suggestions, type) {
        const container = type === 'pickup' ? this.pickupSuggestions : this.dropoffSuggestions;

        container.innerHTML = '';

        if (!suggestions.length) {
            container.innerHTML = '<div class="suggestion-item text-gray-500">Không tìm thấy kết quả</div>';
            container.classList.remove('hidden');
            return;
        }

        suggestions.slice(0, 10).forEach((item) => {
            const div = document.createElement('div');
            div.className = 'suggestion-item';
            div.textContent = item.display || `${item.name || ''} ${item.address || ''}`.trim() || 'Địa chỉ không xác định';

            div.addEventListener('click', async () => {
                const place = await this.fetchPlaceDetail(item.ref_id);

                if (!place) {
                    this.showError('Không lấy được chi tiết địa điểm. Vui lòng chọn lại.');
                    return;
                }

                if (type === 'pickup') {
                    this.pickupInput.value = place.address;
                } else {
                    this.dropoffInput.value = place.address;
                }

                container.classList.add('hidden');
                this.setLocation(type, place.lat, place.lng, place.address);
            });

            container.appendChild(div);
        });

        container.classList.remove('hidden');
    }

    async fetchPlaceDetail(refid) {
        if (!refid) {
            return null;
        }

        try {
            const response = await axios.get(this.VIETMAP_PLACE_URL, {
                params: {
                    apikey: this.VIETMAP_API_KEY,
                    refid,
                },
            });

            const result = response.data;
            if (!result || typeof result.lat !== 'number' || typeof result.lng !== 'number') {
                return null;
            }

            const textAddress = result.display || [result.address, result.ward, result.district, result.city].filter(Boolean).join(',');

            return {
                lat: result.lat,
                lng: result.lng,
                address: textAddress || `${result.lat}, ${result.lng}`,
            };
        } catch (error) {
            console.error('Lỗi place detail VietMap:', error);
            return null;
        }
    }

    async reverseGeocode(lat, lng) {
        try {
            const response = await axios.get(this.VIETMAP_REVERSE_URL, {
                params: {
                    apikey: this.VIETMAP_API_KEY,
                    lat,
                    lng,
                    display_type: 5,
                },
            });

            const first = Array.isArray(response.data) ? response.data[0] : null;
            return first?.display || first?.address || `${lat.toFixed(6)}, ${lng.toFixed(6)}`;
        } catch (error) {
            console.error('Lỗi reverse VietMap:', error);
            return `${lat.toFixed(6)}, ${lng.toFixed(6)}`;
        }
    }

    setLocation(type, lat, lng, address) {
        const coords = { lat, lng, address };

        if (type === 'pickup') {
            this.pickupCoords = coords;
            this.addMarker('pickup', coords, 'Điểm Đón', true);
        } else {
            this.dropoffCoords = coords;
            this.addMarker('dropoff', coords, 'Điểm Đến', false);
        }

        if (this.pickupCoords && this.dropoffCoords) {
            this.fitMapBounds();
            this.calculateRoute();
        } else {
            this.map.flyTo({ center: [lng, lat], zoom: 15 });
        }
    }

    addMarker(type, coords, label, isPickup) {
        if (this.markers[type]) {
            this.markers[type].remove();
        }

        const marker = new vietmapgl.Marker({ color: isPickup ? '#006BFD' : '#ea47ed' })
            .setLngLat([coords.lng, coords.lat]);

        const popup = new vietmapgl.Popup({ offset: 20 }).setHTML(
            `<strong>${label}</strong><br/>${coords.address}`
        );

        marker.setPopup(popup).addTo(this.map);
        this.markers[type] = marker;
    }

    fitMapBounds() {
        if (!this.pickupCoords || !this.dropoffCoords) {
            return;
        }

        const bounds = new vietmapgl.LngLatBounds();
        bounds.extend([this.pickupCoords.lng, this.pickupCoords.lat]);
        bounds.extend([this.dropoffCoords.lng, this.dropoffCoords.lat]);

        this.map.fitBounds(bounds, {
            padding: 80,
            duration: 800,
        });
    }

    async calculateRoute() {
        if (!this.pickupCoords || !this.dropoffCoords) {
            return;
        }

        try {
            const query = new URLSearchParams();
            query.append('apikey', this.VIETMAP_API_KEY);
            query.append('point', `${this.pickupCoords.lat},${this.pickupCoords.lng}`);
            query.append('point', `${this.dropoffCoords.lat},${this.dropoffCoords.lng}`);
            query.append('vehicle', 'car');
            query.append('points_encoded', 'false');

            const response = await axios.get(`${this.VIETMAP_ROUTE_URL}?${query.toString()}`);

            const route = response.data?.paths?.[0];
            if (!route) {
                this.showError('Không thể tính lộ trình VietMap. Vui lòng kiểm tra lại địa chỉ.');
                return;
            }

            this.distanceKm = (route.distance / 1000).toFixed(2);
            this.durationMinutes = Math.ceil(route.time / 60000);

            this.drawRoute(route.points, route.points_encoded);
            this.updatePriceDisplay();
            this.clearError();
        } catch (error) {
            console.error('Lỗi route VietMap:', error);
            this.showError('Không tính được quãng đường/thời gian. Vui lòng thử lại.');
            this.distanceDisplay.textContent = '--';
            this.durationDisplay.textContent = '--';
            this.priceDisplay.textContent = '--';
        }
    }

    normalizeRoutePoints(points) {
        if (!Array.isArray(points)) {
            return [];
        }

        return points
            .filter((p) => Array.isArray(p) && p.length >= 2)
            .map((p) => {
                const a = Number(p[0]);
                const b = Number(p[1]);

                // VietMap docs mention [lat,lng] when points_encoded=false.
                // Convert safely to [lng,lat] for map rendering.
                if (Math.abs(a) <= 90 && Math.abs(b) <= 180) {
                    return [b, a];
                }

                return [a, b];
            });
    }

    drawRoute(points, pointsEncoded) {
        let coordinates = [];

        if (pointsEncoded) {
            coordinates = [];
        } else {
            coordinates = this.normalizeRoutePoints(points);
        }

        if (!coordinates.length) {
            return;
        }

        const source = this.map.getSource(this.routeSourceId);
        if (!source) {
            return;
        }

        source.setData({
            type: 'FeatureCollection',
            features: [
                {
                    type: 'Feature',
                    geometry: {
                        type: 'LineString',
                        coordinates,
                    },
                    properties: {},
                },
            ],
        });

        const bounds = new vietmapgl.LngLatBounds();
        coordinates.forEach((point) => bounds.extend(point));
        this.map.fitBounds(bounds, { padding: 90, duration: 900 });
    }

    updatePriceDisplay() {
        this.distanceDisplay.textContent = `${this.distanceKm} km`;
        this.durationDisplay.textContent = `${this.durationMinutes} phút`;

        let price = 0;
        const distance = parseFloat(this.distanceKm);

        if (distance <= 5) {
            price = 150000;
        } else if (distance <= 10) {
            price = 200000;
        } else if (distance <= 30) {
            price = 200000 + (distance - 10) * 15000;
        } else {
            price = null;
        }

        if (price === null) {
            this.priceDisplay.textContent = 'Vui lòng liên hệ 0985 666 044';
            this.priceDisplay.classList.add('price-contact-note');
            this.priceDisplay.classList.add('text-gray-dark');
            this.priceDisplay.classList.remove('text-secondary');
        } else {
            this.priceDisplay.textContent = `${Math.round(price).toLocaleString('vi-VN')}đ`;
            this.priceDisplay.classList.remove('price-contact-note');
            this.priceDisplay.classList.remove('text-gray-dark');
            this.priceDisplay.classList.add('text-secondary');
        }
    }

    initFormSubmit() {
        this.form.addEventListener('submit', (e) => {
            e.preventDefault();

            if (!this.validateForm()) {
                return;
            }

            this.submitBooking();
        });
    }

    validateForm() {
        if (!this.pickupCoords || !this.dropoffCoords) {
            this.showError('Vui lòng chọn điểm đón và điểm đến từ gợi ý hoặc bản đồ.');
            return false;
        }

        if (!this.distanceKm) {
            this.showError('Chưa tính được quãng đường. Vui lòng kiểm tra lại địa chỉ.');
            return false;
        }

        const phone = document.getElementById('customer-phone').value;
        if (!/^\d{10}$/.test(phone)) {
            this.showError('Số điện thoại không hợp lệ. Vui lòng nhập 10 chữ số.');
            return false;
        }

        const email = document.getElementById('customer-email').value.trim();
        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
            this.showError('Email không hợp lệ. Vui lòng kiểm tra lại.');
            return false;
        }

        return true;
    }

    async submitBooking() {
        this.clearError();
        this.submitBtn.disabled = true;
        this.submitBtn.classList.add('loading');
        this.submitBtn.textContent = 'Đang gửi...';

        try {
            if (typeof emailjs === 'undefined') {
                throw new Error('EmailJS SDK chưa được nạp');
            }

            const distanceText = `${this.distanceKm} km`;
            const durationText = `${this.durationMinutes} phút`;

            const formData = {
                pickup_address: this.pickupInput.value,
                dropoff_address: this.dropoffInput.value,
                distance_text: distanceText,
                duration_text: durationText,
                estimated_price: this.priceDisplay.textContent,
                customer_name: document.getElementById('customer-name').value,
                customer_phone: document.getElementById('customer-phone').value,
                customer_email: document.getElementById('customer-email').value,
                customer_notes: document.getElementById('customer-notes').value,
                booking_time: new Date().toLocaleString('vi-VN'),
            };

            // Reuse the same EmailJS flow as contact form: admin email + auto-reply.
            await emailjs.send('service_l0mto1g', 'template_v5zt6rp', {
                // Booking fields required by business flow
                pickup_address: formData.pickup_address,
                dropoff_address: formData.dropoff_address,
                customer_name: formData.customer_name,
                customer_phone: formData.customer_phone,
                customer_email: formData.customer_email,
                customer_notes: formData.customer_notes,
                distance_text: formData.distance_text,
                duration_text: formData.duration_text,
                estimated_price: formData.estimated_price,

                // Keep contact-template compatibility
                name: formData.customer_name,
                phone: formData.customer_phone,
                email: formData.customer_email,
                message:
                    `Điểm đón: ${formData.pickup_address}\n` +
                    `Điểm đến: ${formData.dropoff_address}\n` +
                    `Quãng đường: ${formData.distance_text}\n` +
                    `Thời gian: ${formData.duration_text}\n` +
                    `Giá tạm tính: ${formData.estimated_price}\n` +
                    `Ghi chú: ${formData.customer_notes || 'Không có'}`,
                time: formData.booking_time,
                booking_time: formData.booking_time,
            });

            await emailjs.send('service_l0mto1g', 'template_hdn720u', {
                name: formData.customer_name,
                email: formData.customer_email,
                message: 'Đã nhận yêu cầu đặt tài xế. Điều phối viên sẽ liên hệ bạn trong vòng 5 phút.',
            });

            this.showSuccess(
                `Yêu cầu thành công! Điều phối viên sẽ liên hệ bạn trong vòng 5 phút.\n` +
                `Lộ trình: ${this.distanceKm} km | Thời gian: ${this.durationMinutes} phút`
            );

            this.form.reset();
            this.resetBooking();
        } catch (error) {
            console.error('Lỗi gửi booking:', error);
            this.showError('Lỗi gửi yêu cầu. Vui lòng thử lại hoặc gọi 0985 666 044.');
        } finally {
            this.submitBtn.disabled = false;
            this.submitBtn.classList.remove('loading');
            this.submitBtn.textContent = 'Yêu cầu điều phối tài xế';
        }
    }

    resetBooking() {
        this.pickupCoords = null;
        this.dropoffCoords = null;
        this.distanceKm = 0;
        this.durationMinutes = 0;
        this.distanceDisplay.textContent = '--';
        this.durationDisplay.textContent = '--';
        this.priceDisplay.textContent = '--';

        Object.values(this.markers).forEach((marker) => marker.remove());
        this.markers = {};

        const source = this.map.getSource(this.routeSourceId);
        if (source) {
            source.setData({
                type: 'FeatureCollection',
                features: [],
            });
        }

        this.map.flyTo({ center: [this.mapCenter.lng, this.mapCenter.lat], zoom: 13 });
        this.setActiveMapTarget('pickup');
    }

    showError(message) {
        this.errorMsg.textContent = message;
        this.errorMsg.classList.add('show');
        setTimeout(() => this.errorMsg.classList.remove('show'), 5000);
    }

    showSuccess(message) {
        this.successMsg.textContent = message;
        this.successMsg.classList.add('show');
        setTimeout(() => this.successMsg.classList.remove('show'), 5000);
    }

    clearError() {
        this.errorMsg.classList.remove('show');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new QuickBooking();
});
