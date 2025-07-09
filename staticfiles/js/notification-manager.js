class NotificationManager {
    constructor() {
        this.notifications = [];
        this.container = null;
        this.init();
    }

    init() {
        // Create notification container
        this.container = document.createElement('div');
        this.container.id = 'notification-container';
        this.container.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 9999;
            max-width: 400px;
            pointer-events: none;
        `;
        document.body.appendChild(this.container);
    }

    show(message, type = 'info', duration = 4000) {
        const notification = this.createNotification(message, type);
        this.container.appendChild(notification);
        this.notifications.push(notification);

        // Trigger entrance animation
        setTimeout(() => {
            notification.classList.add('show');
        }, 10);

        // Auto remove after duration
        setTimeout(() => {
            this.remove(notification);
        }, duration);

        return notification;
    }

    createNotification(message, type) {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        
        const icons = {
            success: 'fas fa-check-circle',
            error: 'fas fa-exclamation-circle',
            warning: 'fas fa-exclamation-triangle',
            info: 'fas fa-info-circle'
        };

        const colors = {
            success: '#28a745',
            error: '#dc3545',
            warning: '#ffc107',
            info: '#17a2b8'
        };

        notification.style.cssText = `
            background: white;
            border-left: 4px solid ${colors[type]};
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            margin-bottom: 10px;
            padding: 16px 20px;
            transform: translateX(100%);
            transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
            pointer-events: auto;
            max-width: 400px;
            position: relative;
            overflow: hidden;
        `;

        notification.innerHTML = `
            <div style="display: flex; align-items: flex-start; gap: 12px;">
                <div style="flex-shrink: 0;">
                    <i class="${icons[type]}" style="color: ${colors[type]}; font-size: 20px;"></i>
                </div>
                <div style="flex-grow: 1; min-width: 0;">
                    <div style="font-weight: 500; color: #333; margin-bottom: 4px; font-size: 14px;">
                        ${this.getTitle(type)}
                    </div>
                    <div style="color: #666; font-size: 13px; line-height: 1.4;">
                        ${message}
                    </div>
                </div>
                <button class="notification-close" style="
                    background: none;
                    border: none;
                    color: #999;
                    cursor: pointer;
                    font-size: 16px;
                    padding: 0;
                    margin-left: 8px;
                    flex-shrink: 0;
                    transition: color 0.2s;
                " onclick="this.parentElement.parentElement.remove()">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <div class="notification-progress" style="
                position: absolute;
                bottom: 0;
                left: 0;
                height: 3px;
                background: ${colors[type]};
                width: 100%;
                transform: scaleX(1);
                transform-origin: left;
                transition: transform 4s linear;
            "></div>
        `;

        // Add hover effects
        notification.addEventListener('mouseenter', () => {
            const progress = notification.querySelector('.notification-progress');
            if (progress) {
                progress.style.transition = 'none';
            }
        });

        notification.addEventListener('mouseleave', () => {
            const progress = notification.querySelector('.notification-progress');
            if (progress) {
                progress.style.transition = 'transform 4s linear';
            }
        });

        // Add show class for animation
        setTimeout(() => {
            notification.classList.add('show');
            notification.style.transform = 'translateX(0)';
        }, 10);

        return notification;
    }

    getTitle(type) {
        const titles = {
            success: 'Success',
            error: 'Error',
            warning: 'Warning',
            info: 'Information'
        };
        return titles[type] || 'Notification';
    }

    remove(notification) {
        if (notification && notification.parentNode) {
            notification.style.transform = 'translateX(100%)';
            notification.style.opacity = '0';
            
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
                const index = this.notifications.indexOf(notification);
                if (index > -1) {
                    this.notifications.splice(index, 1);
                }
            }, 300);
        }
    }

    clear() {
        this.notifications.forEach(notification => {
            this.remove(notification);
        });
    }

    // Convenience methods
    success(message, duration = 4000) {
        return this.show(message, 'success', duration);
    }

    error(message, duration = 5000) {
        return this.show(message, 'error', duration);
    }

    warning(message, duration = 4000) {
        return this.show(message, 'warning', duration);
    }

    info(message, duration = 4000) {
        return this.show(message, 'info', duration);
    }

    // Custom confirmation dialog
    confirm(message, onConfirm, onCancel) {
        const notification = this.createConfirmationNotification(message, onConfirm, onCancel);
        this.container.appendChild(notification);
        this.notifications.push(notification);

        setTimeout(() => {
            notification.classList.add('show');
        }, 10);

        return notification;
    }

    createConfirmationNotification(message, onConfirm, onCancel) {
        const notification = document.createElement('div');
        notification.className = 'notification notification-confirm';
        
        notification.style.cssText = `
            background: white;
            border-left: 4px solid #17a2b8;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            margin-bottom: 10px;
            padding: 20px;
            transform: translateX(100%);
            transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
            pointer-events: auto;
            max-width: 400px;
            position: relative;
            overflow: hidden;
        `;

        notification.innerHTML = `
            <div style="display: flex; align-items: flex-start; gap: 12px;">
                <div style="flex-shrink: 0;">
                    <span style="color: #17a2b8; font-size: 20px; font-weight: bold;">❓</span>
                </div>
                <div style="flex-grow: 1; min-width: 0;">
                    <div style="font-weight: 500; color: #333; margin-bottom: 8px; font-size: 14px;">
                        Confirmation
                    </div>
                    <div style="color: #666; font-size: 13px; line-height: 1.4; margin-bottom: 16px;">
                        ${message}
                    </div>
                    <div style="display: flex; gap: 8px; justify-content: flex-end;">
                        <button class="btn-cancel" style="
                            background: #6c757d;
                            color: white;
                            border: none;
                            padding: 6px 12px;
                            border-radius: 4px;
                            cursor: pointer;
                            font-size: 12px;
                            transition: background-color 0.2s;
                        ">Cancel</button>
                        <button class="btn-confirm" style="
                            background: #dc3545;
                            color: white;
                            border: none;
                            padding: 6px 12px;
                            border-radius: 4px;
                            cursor: pointer;
                            font-size: 12px;
                            transition: background-color 0.2s;
                        ">Confirm</button>
                    </div>
                </div>
            </div>
        `;

        // Add event listeners
        const confirmBtn = notification.querySelector('.btn-confirm');
        const cancelBtn = notification.querySelector('.btn-cancel');

        confirmBtn.addEventListener('click', () => {
            this.remove(notification);
            if (onConfirm) onConfirm();
        });

        cancelBtn.addEventListener('click', () => {
            this.remove(notification);
            if (onCancel) onCancel();
        });

        // Add hover effects
        confirmBtn.addEventListener('mouseenter', () => {
            confirmBtn.style.backgroundColor = '#c82333';
        });
        confirmBtn.addEventListener('mouseleave', () => {
            confirmBtn.style.backgroundColor = '#dc3545';
        });

        cancelBtn.addEventListener('mouseenter', () => {
            cancelBtn.style.backgroundColor = '#5a6268';
        });
        cancelBtn.addEventListener('mouseleave', () => {
            cancelBtn.style.backgroundColor = '#6c757d';
        });

        setTimeout(() => {
            notification.classList.add('show');
            notification.style.transform = 'translateX(0)';
        }, 10);

        return notification;
    }
}

// Initialize notification manager globally
window.notificationManager = new NotificationManager();

// Add CSS for better animations
const style = document.createElement('style');
style.textContent = `
    .notification {
        opacity: 1;
        transition: all 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
    }
    
    .notification.show {
        opacity: 1;
        transform: translateX(0) !important;
    }
    
    .notification-close:hover {
        color: #333 !important;
    }
    
    .notification-progress {
        animation: progress-shrink 4s linear forwards;
    }
    
    @keyframes progress-shrink {
        from { transform: scaleX(1); }
        to { transform: scaleX(0); }
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        #notification-container {
            top: 10px;
            right: 10px;
            left: 10px;
            max-width: none;
        }
        
        .notification {
            margin-bottom: 8px;
            padding: 12px 16px;
        }
    }
`;
document.head.appendChild(style); 