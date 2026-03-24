// ==================== QUICK BOOKING MODULE (VIETMAP) ====================

class QuickBooking {
    constructor() {
        // VietMap configuration (replace key in production)
        this.VIETMAP_TILE_KEY = '3f8a731ea623af779ef30acd8097e199a556ab3905abf141';
        this.VIETMAP_SERVICES_KEY = '53ec8c719c14153d869267e0d128744358409b741db32847';
        this.VIETMAP_STYLE_URL = `https://maps.vietmap.vn/maps/styles/tm/style.json?apikey=${this.VIETMAP_TILE_KEY}`;
        this.VIETMAP_AUTOCOMPLETE_URL = 'https://maps.vietmap.vn/api/autocomplete/v4';
        this.VIETMAP_PLACE_URL = 'https://maps.vietmap.vn/api/place/v4';
        this.VIETMAP_REVERSE_URL = 'https://maps.vietmap.vn/api/reverse/v4';
        this.VIETMAP_ROUTE_URL = 'https://maps.vietmap.vn/api/route/v3';

        this.EMAILJS_SERVICE_ID = 'service_1cwk8gu';
        this.EMAILJS_PUBLIC_KEY = 'FelIR87iDLCKdybMB';
        this.EMAILJS_BOOKING_TEMPLATE_ID = 'template_xa0eh55';
        this.EMAILJS_AUTOREPLY_TEMPLATE_ID = 'template_zsif1bu';

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
        this.travelTimeInput = document.getElementById('customer-travel-time');

        this.distanceDisplay = document.getElementById('distance-display');
        this.durationDisplay = document.getElementById('duration-display');
        this.priceDisplay = document.getElementById('price-display');

        this.form = document.getElementById('quick-booking-form');
        this.submitBtn = document.getElementById('submit-booking-btn');
        this.errorMsg = document.getElementById('booking-error-msg');
        this.successMsg = document.getElementById('booking-success-msg');

        this.mapModal = document.getElementById('booking-map-modal');
        this.mapModalTitle = document.getElementById('booking-map-modal-title');
        this.mapModalSearchInput = document.getElementById('modal-map-search');
        this.mapModalSuggestions = document.getElementById('modal-map-suggestions');
        this.mapModalCancelBtn = document.getElementById('modal-map-cancel');
        this.mapModalConfirmBtn = document.getElementById('modal-map-confirm');

        this.markers = {};
        this.modalMap = null;
        this.modalMarker = null;
        this.modalSelectionTarget = 'pickup';
        this.modalPendingLocation = null;
        this.modalSearchDebounce = null;

        this.initMap();
        this.initTravelTimeField();
        this.initAutocomplete();
        this.initMapPickerModal();
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
                this.openMapPickerModal('pickup');
            });
        }

        if (this.dropoffMapBtn) {
            this.dropoffMapBtn.addEventListener('click', () => {
                this.openMapPickerModal('dropoff');
            });
        }

        if (this.pickupLocateBtn) {
            this.pickupLocateBtn.addEventListener('click', () => this.locatePickupByBrowser());
        }

        this.setActiveMapTarget('pickup');
    }

    initTravelTimeField(shouldSetValue = true) {
        if (!this.travelTimeInput) {
            return;
        }

        const minDate = new Date();
        minDate.setMinutes(minDate.getMinutes() + 5, 0, 0);
        const minValue = this.toDateTimeLocalValue(minDate);

        this.travelTimeInput.min = minValue;

        if (shouldSetValue && (!this.travelTimeInput.value || this.travelTimeInput.value < minValue)) {
            this.travelTimeInput.value = minValue;
        }

        if (!this.travelTimeInput.dataset.boundMinUpdater) {
            this.travelTimeInput.addEventListener('focus', () => this.initTravelTimeField(false));
            this.travelTimeInput.dataset.boundMinUpdater = '1';
        }
    }

    toDateTimeLocalValue(date) {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        const hours = String(date.getHours()).padStart(2, '0');
        const minutes = String(date.getMinutes()).padStart(2, '0');
        return `${year}-${month}-${day}T${hours}:${minutes}`;
    }

    formatTravelTime(value) {
        const date = new Date(value);
        if (Number.isNaN(date.getTime())) {
            return value;
        }
        return date.toLocaleString('vi-VN');
    }

    initMapPickerModal() {
        if (!this.mapModal || !this.mapModalSearchInput || !this.mapModalSuggestions) {
            return;
        }

        this.mapModalCancelBtn?.addEventListener('click', () => this.closeMapPickerModal());
        this.mapModalConfirmBtn?.addEventListener('click', () => this.confirmMapPickerSelection());

        this.mapModal.addEventListener('click', (e) => {
            if (e.target?.dataset?.closeModal === 'true') {
                this.closeMapPickerModal();
            }
        });

        this.mapModalSearchInput.addEventListener('input', (e) => {
            clearTimeout(this.modalSearchDebounce);
            const query = e.target.value.trim();

            if (query.length < 2) {
                this.mapModalSuggestions.classList.add('hidden');
                return;
            }

            this.modalSearchDebounce = setTimeout(() => {
                this.fetchModalSuggestions(query);
            }, 280);
        });

        document.addEventListener('click', (e) => {
            if (!e.target.closest('.booking-map-modal-search-wrap')) {
                this.mapModalSuggestions.classList.add('hidden');
            }
        });

        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.mapModal && !this.mapModal.classList.contains('hidden')) {
                this.closeMapPickerModal();
            }
        });
    }

    ensureModalMap() {
        if (this.modalMap) {
            return;
        }

        this.modalMap = new vietmapgl.Map({
            container: 'booking-map-modal-canvas',
            style: this.VIETMAP_STYLE_URL,
            center: [this.mapCenter.lng, this.mapCenter.lat],
            zoom: 13,
            minZoom: 10,
            maxZoom: 18,
        });

        this.modalMap.addControl(new vietmapgl.NavigationControl({ showCompass: true }), 'top-right');

        this.modalMap.on('click', async (e) => {
            const lng = e.lngLat.lng;
            const lat = e.lngLat.lat;
            const address = await this.reverseGeocode(lat, lng);
            this.setModalPendingLocation(lat, lng, address, false);
        });
    }

    openMapPickerModal(target) {
        if (!this.mapModal) {
            return;
        }

        this.modalSelectionTarget = target;
        this.mapModalTitle.textContent = target === 'pickup' ? 'Chọn điểm đón trên bản đồ' : 'Chọn điểm đến trên bản đồ';

        this.mapModal.classList.remove('hidden');
        document.body.style.overflow = 'hidden';

        this.ensureModalMap();

        const currentLocation = target === 'pickup' ? this.pickupCoords : this.dropoffCoords;
        if (currentLocation) {
            this.setModalPendingLocation(currentLocation.lat, currentLocation.lng, currentLocation.address, true);
        } else {
            this.modalPendingLocation = null;
            this.mapModalSearchInput.value = '';
            this.mapModalSuggestions.classList.add('hidden');

            if (this.modalMarker) {
                this.modalMarker.remove();
                this.modalMarker = null;
            }
            this.modalMap.flyTo({ center: [this.mapCenter.lng, this.mapCenter.lat], zoom: 13 });
        }

        requestAnimationFrame(() => {
            this.modalMap.resize();
            if (this.modalPendingLocation) {
                this.modalMap.flyTo({
                    center: [this.modalPendingLocation.lng, this.modalPendingLocation.lat],
                    zoom: 15,
                });
            }
        });
    }

    closeMapPickerModal() {
        if (!this.mapModal) {
            return;
        }
        this.mapModal.classList.add('hidden');
        this.mapModalSuggestions?.classList.add('hidden');
        document.body.style.overflow = '';
    }

    async fetchModalSuggestions(query) {
        try {
            const response = await axios.get(this.VIETMAP_AUTOCOMPLETE_URL, {
                params: {
                    apikey: this.VIETMAP_SERVICES_KEY,
                    text: query,
                    focus: `${this.mapCenter.lat},${this.mapCenter.lng}`,
                    display_type: 5,
                },
            });

            const suggestions = Array.isArray(response.data) ? response.data : [];
            this.renderModalSuggestions(suggestions);
        } catch (error) {
            console.error('Lỗi autocomplete modal VietMap:', error);
            this.showError('Không thể gợi ý địa chỉ trong popup. Vui lòng thử lại.');
        }
    }

    renderModalSuggestions(suggestions) {
        if (!this.mapModalSuggestions) {
            return;
        }

        this.mapModalSuggestions.innerHTML = '';

        if (!suggestions.length) {
            this.mapModalSuggestions.innerHTML = '<div class="suggestion-item text-gray-500">Không tìm thấy kết quả</div>';
            this.mapModalSuggestions.classList.remove('hidden');
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
                this.setModalPendingLocation(place.lat, place.lng, place.address, true);
            });

            this.mapModalSuggestions.appendChild(div);
        });

        this.mapModalSuggestions.classList.remove('hidden');
    }

    setModalPendingLocation(lat, lng, address, flyToMap) {
        this.modalPendingLocation = { lat, lng, address };
        this.mapModalSearchInput.value = address;
        this.mapModalSuggestions.classList.add('hidden');

        if (this.modalMarker) {
            this.modalMarker.remove();
        }

        this.modalMarker = new vietmapgl.Marker({ color: this.modalSelectionTarget === 'pickup' ? '#006BFD' : '#ea47ed' })
            .setLngLat([lng, lat])
            .addTo(this.modalMap);

        if (flyToMap) {
            this.modalMap.flyTo({ center: [lng, lat], zoom: 15 });
        }
    }

    confirmMapPickerSelection() {
        if (!this.modalPendingLocation) {
            this.showError('Vui lòng chọn vị trí trên bản đồ hoặc từ ô tìm kiếm.');
            return;
        }

        const selected = this.modalPendingLocation;
        const target = this.modalSelectionTarget;

        if (target === 'pickup') {
            this.pickupInput.value = selected.address;
        } else {
            this.dropoffInput.value = selected.address;
        }

        this.setLocation(target, selected.lat, selected.lng, selected.address);
        this.closeMapPickerModal();
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
                    apikey: this.VIETMAP_SERVICES_KEY,
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
                    apikey: this.VIETMAP_SERVICES_KEY,
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
                    apikey: this.VIETMAP_SERVICES_KEY,
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
            query.append('apikey', this.VIETMAP_SERVICES_KEY);
            query.append('point', `${this.pickupCoords.lat},${this.pickupCoords.lng}`);
            query.append('point', `${this.dropoffCoords.lat},${this.dropoffCoords.lng}`);
            query.append('vehicle', 'car');
            query.append('points_encoded', 'false');

            const response = await axios.get(`${this.VIETMAP_ROUTE_URL}?${query.toString()}`);
            console.log('VietMap route response JSON:', response.data);

            const route = response.data?.paths?.[0];
            if (!route) {
                this.showError('Không thể tính lộ trình VietMap. Vui lòng kiểm tra lại địa chỉ.');
                return;
            }

            const distanceMeters = this.extractDistanceMeters(route);
            const durationSeconds = this.extractDurationSeconds(route);
            const coordinates = this.extractRouteCoordinates(route);

            if (distanceMeters == null || durationSeconds == null) {
                this.showError('Không đọc được dữ liệu quãng đường/thời gian từ VietMap.');
                return;
            }

            this.distanceKm = (distanceMeters / 1000).toFixed(2);
            this.durationMinutes = Math.ceil(durationSeconds / 60);

            this.drawRoute(coordinates);
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

    extractDistanceMeters(route) {
        if (typeof route?.distance === 'number' && Number.isFinite(route.distance)) {
            return route.distance;
        }
        if (typeof route?.distance_m === 'number' && Number.isFinite(route.distance_m)) {
            return route.distance_m;
        }
        if (typeof route?.distance_km === 'number' && Number.isFinite(route.distance_km)) {
            return route.distance_km * 1000;
        }
        if (typeof route?.summary?.distance === 'number' && Number.isFinite(route.summary.distance)) {
            return route.summary.distance;
        }
        return null;
    }

    extractDurationSeconds(route) {
        const rawTime =
            typeof route?.time === 'number' && Number.isFinite(route.time)
                ? route.time
                : typeof route?.duration === 'number' && Number.isFinite(route.duration)
                    ? route.duration
                    : typeof route?.summary?.time === 'number' && Number.isFinite(route.summary.time)
                        ? route.summary.time
                        : null;

        if (rawTime == null) {
            return null;
        }

        // Most routing APIs return milliseconds or seconds; convert both safely to seconds.
        return rawTime > 100000 ? rawTime / 1000 : rawTime;
    }

    normalizeCoordinatePair(pair) {
        if (!Array.isArray(pair) || pair.length < 2) {
            return null;
        }

        const first = Number(pair[0]);
        const second = Number(pair[1]);
        if (!Number.isFinite(first) || !Number.isFinite(second)) {
            return null;
        }

        // [lat,lng] -> [lng,lat]
        if (Math.abs(first) <= 90 && Math.abs(second) <= 180) {
            return [second, first];
        }

        // [lng,lat]
        if (Math.abs(first) <= 180 && Math.abs(second) <= 90) {
            return [first, second];
        }

        return null;
    }

    decodePolyline(encoded, precision = 5) {
        const coordinates = [];
        let index = 0;
        let lat = 0;
        let lng = 0;
        const factor = Math.pow(10, precision);

        while (index < encoded.length) {
            let result = 0;
            let shift = 0;
            let byte;

            do {
                byte = encoded.charCodeAt(index++) - 63;
                result |= (byte & 0x1f) << shift;
                shift += 5;
            } while (byte >= 0x20);

            const dLat = (result & 1) ? ~(result >> 1) : (result >> 1);
            lat += dLat;

            result = 0;
            shift = 0;

            do {
                byte = encoded.charCodeAt(index++) - 63;
                result |= (byte & 0x1f) << shift;
                shift += 5;
            } while (byte >= 0x20);

            const dLng = (result & 1) ? ~(result >> 1) : (result >> 1);
            lng += dLng;

            coordinates.push([lng / factor, lat / factor]);
        }

        return coordinates;
    }

    extractRouteCoordinates(route) {
        const pointsEncoded = route?.points_encoded === true;

        if (pointsEncoded) {
            const encoded =
                typeof route?.points === 'string'
                    ? route.points
                    : typeof route?.geometry === 'string'
                        ? route.geometry
                        : null;

            if (!encoded) {
                return [];
            }

            try {
                return this.decodePolyline(encoded);
            } catch (error) {
                console.error('Không decode được polyline encoded:', error);
                return [];
            }
        }

        const rawCoordinates =
            Array.isArray(route?.points)
                ? route.points
                : Array.isArray(route?.points?.coordinates)
                    ? route.points.coordinates
                    : Array.isArray(route?.geometry?.coordinates)
                        ? route.geometry.coordinates
                        : Array.isArray(route?.geometry)
                            ? route.geometry
                            : [];

        return rawCoordinates
            .map((pair) => this.normalizeCoordinatePair(pair))
            .filter((pair) => Array.isArray(pair));
    }

    drawRoute(coordinates) {

        if (!coordinates.length) {
            console.warn('Không có coordinates để vẽ route.');
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
            this.priceDisplay.textContent = 'Trên 30km: vui lòng liên hệ hotline 0985 666 044 để được tư vấn và báo giá phù hợp.';
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

        this.initTravelTimeField(false);
        const travelTime = this.travelTimeInput?.value;
        if (!travelTime) {
            this.showError('Vui lòng chọn thời gian đi.');
            return false;
        }

        const travelDate = new Date(travelTime);
        if (Number.isNaN(travelDate.getTime())) {
            this.showError('Thời gian đi không hợp lệ.');
            return false;
        }

        if (travelDate.getTime() < Date.now()) {
            this.showError('Thời gian đi không được ở quá khứ.');
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
                distance: distanceText,
                duration: durationText,
                estimated_price: this.priceDisplay.textContent,
                customer_name: document.getElementById('customer-name').value,
                customer_phone: document.getElementById('customer-phone').value,
                customer_email: document.getElementById('customer-email').value,
                departure_time: this.travelTimeInput?.value || '',
                notes: document.getElementById('customer-notes').value,
                booking_time: new Date().toLocaleString('vi-VN'),
            };

            const travelTimeDisplay = this.formatTravelTime(formData.departure_time);

            await emailjs.send(this.EMAILJS_SERVICE_ID, this.EMAILJS_BOOKING_TEMPLATE_ID, {
                pickup_address: formData.pickup_address,
                dropoff_address: formData.dropoff_address,
                customer_name: formData.customer_name,
                customer_phone: formData.customer_phone,
                customer_email: formData.customer_email,
                departure_time: formData.departure_time,
                notes: formData.notes,
                distance: formData.distance,
                duration: formData.duration,
                estimated_price: formData.estimated_price,

                // Backward-compatible aliases for existing template placeholders
                customer_travel_time: formData.departure_time,
                customer_notes: formData.notes,
                distance_text: formData.distance,
                duration_text: formData.duration,
                travel_time: formData.departure_time,

                name: formData.customer_name,
                phone: formData.customer_phone,
                email: formData.customer_email,
                message:
                    `Điểm đón: ${formData.pickup_address}\n` +
                    `Điểm đến: ${formData.dropoff_address}\n` +
                    `Thời gian đi: ${travelTimeDisplay}\n` +
                    `Quãng đường: ${formData.distance}\n` +
                    `Thời gian: ${formData.duration}\n` +
                    `Giá tạm tính: ${formData.estimated_price}\n` +
                    `Ghi chú: ${formData.notes || 'Không có'}`,
                time: formData.booking_time,
                booking_time: formData.booking_time,
            }, this.EMAILJS_PUBLIC_KEY);

            await emailjs.send(this.EMAILJS_SERVICE_ID, this.EMAILJS_AUTOREPLY_TEMPLATE_ID, {
                name: formData.customer_name,
                email: formData.customer_email,
                departure_time: formData.departure_time,
                message: `Đã nhận yêu cầu đặt tài xế cho thời gian ${travelTimeDisplay}. Điều phối viên sẽ liên hệ bạn trong vòng 5 phút.`,
            }, this.EMAILJS_PUBLIC_KEY);

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
        this.initTravelTimeField();
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
