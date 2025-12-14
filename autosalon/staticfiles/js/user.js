// static/js/user.js
// Управление избранным и историей через LocalStorage

class UserStorage {
    constructor() {
        this.favoritesKey = 'autoelite_favorites';
        this.historyKey = 'autoelite_history';
        this.maxHistoryItems = 20;
    }

    // === ИЗБРАННОЕ ===
    getFavorites() {
        try {
            const favorites = localStorage.getItem(this.favoritesKey);
            return favorites ? JSON.parse(favorites) : [];
        } catch (error) {
            console.error('Ошибка получения избранного:', error);
            return [];
        }
    }

    addToFavorites(car) {
        try {
            const favorites = this.getFavorites();

            // Проверяем, нет ли уже этого автомобиля в избранном
            if (!favorites.some(fav => fav.id === car.id)) {
                favorites.push({
                    id: car.id,
                    brand: car.brand?.name || car.brand,
                    model: car.model,
                    price: car.price,
                    year: car.year,
                    image: car.image_url || 'https://images.unsplash.com/photo-1549399542-7e3f8b79c341',
                    added_at: new Date().toISOString()
                });

                localStorage.setItem(this.favoritesKey, JSON.stringify(favorites));
                this.showNotification('Автомобиль добавлен в избранное');
                return true;
            } else {
                this.showNotification('Автомобиль уже в избранном');
                return false;
            }
        } catch (error) {
            console.error('Ошибка добавления в избранное:', error);
            return false;
        }
    }

    removeFromFavorites(carId) {
        try {
            const favorites = this.getFavorites();
            const newFavorites = favorites.filter(fav => fav.id !== carId);
            localStorage.setItem(this.favoritesKey, JSON.stringify(newFavorites));
            this.showNotification('Автомобиль удален из избранного');
            return true;
        } catch (error) {
            console.error('Ошибка удаления из избранного:', error);
            return false;
        }
    }

    isFavorite(carId) {
        const favorites = this.getFavorites();
        return favorites.some(fav => fav.id === carId);
    }

    // === ИСТОРИЯ ПРОСМОТРОВ ===
    addToHistory(car) {
        try {
            let history = this.getHistory();

            // Удаляем старую запись если есть
            history = history.filter(item => item.id !== car.id);

            // Добавляем новую запись в начало
            history.unshift({
                id: car.id,
                brand: car.brand?.name || car.brand,
                model: car.model,
                price: car.price,
                year: car.year,
                viewed_at: new Date().toISOString()
            });

            // Ограничиваем историю
            if (history.length > this.maxHistoryItems) {
                history = history.slice(0, this.maxHistoryItems);
            }

            localStorage.setItem(this.historyKey, JSON.stringify(history));
            return true;
        } catch (error) {
            console.error('Ошибка добавления в историю:', error);
            return false;
        }
    }

    getHistory() {
        try {
            const history = localStorage.getItem(this.historyKey);
            return history ? JSON.parse(history) : [];
        } catch (error) {
            console.error('Ошибка получения истории:', error);
            return [];
        }
    }

    clearHistory() {
        localStorage.removeItem(this.historyKey);
        this.showNotification('История просмотров очищена');
    }

    clearFavorites() {
        localStorage.removeItem(this.favoritesKey);
        this.showNotification('Избранное очищено');
    }

    // === УТИЛИТЫ ===
    showNotification(message, type = 'success') {
        // Создаем уведомление
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 9999;
            min-width: 300px;
        `;
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        document.body.appendChild(notification);

        // Автоматически удаляем через 3 секунды
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 3000);
    }

    // === СИМУЛЯЦИЯ АВТОРИЗАЦИИ ===
    login(username = 'demo@autoelite.ru', password = 'demo123') {
        const user = {
            id: 1,
            username: username,
            email: username,
            name: 'Демо Пользователь',
            phone: '+7 (999) 123-45-67',
            isDemo: true,
            loginTime: new Date().toISOString()
        };

        localStorage.setItem('autoelite_user', JSON.stringify(user));
        this.showNotification('Вход выполнен успешно!');
        return user;
    }

    logout() {
        localStorage.removeItem('autoelite_user');
        this.showNotification('Выход выполнен');
    }

    getCurrentUser() {
        try {
            const user = localStorage.getItem('autoelite_user');
            return user ? JSON.parse(user) : null;
        } catch (error) {
            return null;
        }
    }

    isLoggedIn() {
        return this.getCurrentUser() !== null;
    }

    // === ФОРМАТИРОВАНИЕ ===
    formatPrice(price) {
        return new Intl.NumberFormat('ru-RU').format(price) + ' ₽';
    }

    formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('ru-RU', {
            day: 'numeric',
            month: 'long',
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    }
}

// Создаем глобальный экземпляр
window.userStorage = new UserStorage();