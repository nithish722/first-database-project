const API_BASE = 'http://localhost:5000/api';

const App = {
    state: {
        user: JSON.parse(localStorage.getItem('tastehub_user')) || null,
        role: localStorage.getItem('tastehub_role') || null, // 'customer' or 'admin'
        cart: JSON.parse(localStorage.getItem('tastehub_cart')) || [],
        currentKitchenId: localStorage.getItem('tastehub_kitchen_id') || null,
    },

    // --- UTILITIES ---
    saveState() {
        localStorage.setItem('tastehub_user', JSON.stringify(this.state.user));
        localStorage.setItem('tastehub_role', this.state.role);
        localStorage.setItem('tastehub_cart', JSON.stringify(this.state.cart));
        localStorage.setItem('tastehub_kitchen_id', this.state.currentKitchenId);
    },

    logout() {
        this.state.user = null;
        this.state.role = null;
        this.state.cart = [];
        this.state.currentKitchenId = null;
        this.saveState();
        window.location.href = '/index.html';
    },

    // --- AUTH API ---
    async registerUser(data) {
        const res = await fetch(`${API_BASE}/auth/register`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        });
        return res.json();
    },

    async login(email, password, isAdmin = false) {
        const endpoint = isAdmin ? '/auth/admin_login' : '/auth/login';
        const res = await fetch(`${API_BASE}${endpoint}`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({email, password})
        });
        const data = await res.json();
        if (data.success) {
            this.state.user = isAdmin ? data.admin : data.user;
            this.state.role = data.role;
            this.saveState();
        }
        return data;
    },

    // --- KITCHEN API ---
    async getKitchens() {
        const res = await fetch(`${API_BASE}/kitchens`);
        return res.json();
    },

    async getKitchenMenu(kitchenId) {
        const res = await fetch(`${API_BASE}/kitchens/${kitchenId}/menu`);
        return res.json();
    },

    async getKitchenReviews(kitchenId) {
        const res = await fetch(`${API_BASE}/kitchens/${kitchenId}/reviews`);
        return res.json();
    },

    // --- CART ---
    addToCart(item, kitchenId) {
        if (this.state.currentKitchenId && this.state.currentKitchenId !== String(kitchenId) && this.state.cart.length > 0) {
            alert('You can only order from one kitchen at a time. Clear your cart to switch kitchens.');
            return false;
        }
        
        this.state.currentKitchenId = String(kitchenId);
        
        const existing = this.state.cart.find(i => i.item_id === item.item_id);
        if (existing) {
            existing.quantity += 1;
        } else {
            this.state.cart.push({...item, quantity: 1});
        }
        this.saveState();
        return true;
    },
    
    removeFromCart(itemId) {
        this.state.cart = this.state.cart.filter(i => i.item_id !== itemId);
        if (this.state.cart.length === 0) {
            this.state.currentKitchenId = null;
        }
        this.saveState();
    },
    
    getCartTotal() {
        return this.state.cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    },

    // --- ORDERS API ---
    async placeOrder(paymentMethod) {
        const res = await fetch(`${API_BASE}/orders`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                user_id: this.state.user.user_id,
                kitchen_id: this.state.currentKitchenId,
                items: this.state.cart,
                payment_method: paymentMethod
            })
        });
        const data = await res.json();
        if(data.success) {
            this.state.cart = [];
            this.state.currentKitchenId = null;
            this.saveState();
        }
        return data;
    },
    
    async getUserOrders() {
        const res = await fetch(`${API_BASE}/orders/user/${this.state.user.user_id}`);
        return res.json();
    },
    
    async cancelOrder(orderId) {
        const res = await fetch(`${API_BASE}/orders/${orderId}/cancel`, {
            method: 'POST'
        });
        return res.json();
    },
    
    // --- ADMIN API ---
    async getAdminOrders() {
        const res = await fetch(`${API_BASE}/admin/orders`);
        return res.json();
    },
    
    async getAdminStats() {
        const res = await fetch(`${API_BASE}/admin/stats`);
        return res.json();
    },
    
    updateCartQuantity(itemId, delta) {
        const item = this.state.cart.find(i => i.item_id === itemId);
        if (item) {
            item.quantity += delta;
            if (item.quantity <= 0) {
                this.removeFromCart(itemId);
            } else {
                this.saveState();
            }
        }
    },
    
    async updateOrderStatus(orderId, status) {
        const res = await fetch(`${API_BASE}/admin/orders/${orderId}/status`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                status,
                admin_id: this.state.user.admin_id
            })
        });
        return res.json();
    },
    
    // --- REVIEWS API ---
    async submitReview(userId, kitchenId, rating, comment) {
        const res = await fetch(`${API_BASE}/reviews`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                user_id: userId,
                kitchen_id: kitchenId,
                rating: rating,
                comment: comment
            })
        });
        return res.json();
    }
};

window.App = App;
