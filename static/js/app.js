// ChemVista JavaScript Application

class ChemVista {
    constructor() {
        this.searchInput = document.getElementById('searchInput');
        this.suggestionsContainer = document.getElementById('searchSuggestions');
        this.isSearching = false;
        this.searchTimeout = null;
        
        this.init();
    }
    
    init() {
        this.bindEvents();
        this.initializeTooltips();
        this.initializeAnimations();
    }
    
    bindEvents() {
        // Search functionality
        if (this.searchInput) {
            this.searchInput.addEventListener('input', this.handleSearchInput.bind(this));
            this.searchInput.addEventListener('focus', this.handleSearchFocus.bind(this));
            this.searchInput.addEventListener('blur', this.handleSearchBlur.bind(this));
            this.searchInput.addEventListener('keydown', this.handleSearchKeydown.bind(this));
        }
        
        // Element hover effects
        this.initializeElementHovers();
        
        // Example button clicks
        this.initializeExampleButtons();
        
        // Smooth scrolling for navigation
        this.initializeSmoothScrolling();
        
        // Search form submission
        this.initializeSearchForm();
    }
    
    handleSearchInput(event) {
        const query = event.target.value.trim();
        
        // Clear previous timeout
        if (this.searchTimeout) {
            clearTimeout(this.searchTimeout);
        }
        
        // Debounce search requests
        this.searchTimeout = setTimeout(() => {
            if (query.length >= 2) {
                this.fetchSuggestions(query);
            } else {
                this.hideSuggestions();
            }
        }, 300);
    }
    
    async fetchSuggestions(query) {
        if (this.isSearching) return;
        
        this.isSearching = true;
        
        try {
            const response = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
            const suggestions = await response.json();
            this.displaySuggestions(suggestions);
        } catch (error) {
            console.error('Error fetching suggestions:', error);
        } finally {
            this.isSearching = false;
        }
    }
    
    displaySuggestions(suggestions) {
        if (!this.suggestionsContainer) return;
        
        if (suggestions.length === 0) {
            this.hideSuggestions();
            return;
        }
        
        const suggestionsHTML = suggestions.map(suggestion => `
            <div class="suggestion-item" data-name="${suggestion.name}" data-formula="${suggestion.formula}" data-id="${suggestion.id}">
                <div class="d-flex justify-content-between align-items-center">
                    <div>
                        <strong>${this.highlightMatch(suggestion.name, this.searchInput.value)}</strong>
                        <small class="text-muted d-block">${suggestion.formula}</small>
                    </div>
                    <i class="fas fa-arrow-right text-muted"></i>
                </div>
            </div>
        `).join('');
        
        this.suggestionsContainer.innerHTML = suggestionsHTML;
        this.suggestionsContainer.style.display = 'block';
        
        // Bind click events to suggestions
        this.suggestionsContainer.querySelectorAll('.suggestion-item').forEach(item => {
            item.addEventListener('click', this.handleSuggestionClick.bind(this));
        });
    }
    
    hideSuggestions() {
        if (this.suggestionsContainer) {
            this.suggestionsContainer.style.display = 'none';
        }
    }
    
    highlightMatch(text, query) {
        if (!query) return text;
        
        const regex = new RegExp(`(${query})`, 'gi');
        return text.replace(regex, '<mark>$1</mark>');
    }
    
    handleSuggestionClick(event) {
        const item = event.currentTarget;
        const compoundId = item.dataset.id;
        window.location.href = `/compound/${compoundId}`;
    }
    
    handleSearchFocus() {
        // Show suggestions if input has value
        if (this.searchInput.value.trim().length >= 2) {
            this.fetchSuggestions(this.searchInput.value.trim());
        }
    }
    
    handleSearchBlur() {
        // Hide suggestions after a short delay to allow clicks
        setTimeout(() => {
            this.hideSuggestions();
        }, 200);
    }
    
    handleSearchKeydown(event) {
        if (event.key === 'Escape') {
            this.hideSuggestions();
            this.searchInput.blur();
        }
    }
    
    initializeElementHovers() {
        const elements = document.querySelectorAll('.element');
        
        elements.forEach(element => {
            element.addEventListener('mouseenter', this.handleElementHover.bind(this));
            element.addEventListener('mouseleave', this.handleElementLeave.bind(this));
        });
    }
    
    handleElementHover(event) {
        const element = event.currentTarget;
        const atomicNumber = element.dataset.element;
        
        // Add hover class for enhanced styling
        element.classList.add('element-hovered');
        
        // Create tooltip with element info (if not already exists)
        this.showElementTooltip(element, atomicNumber);
    }
    
    handleElementLeave(event) {
        const element = event.currentTarget;
        element.classList.remove('element-hovered');
        this.hideElementTooltip();
    }
    
    showElementTooltip(element, atomicNumber) {
        // Simple tooltip implementation
        const rect = element.getBoundingClientRect();
        const tooltip = document.createElement('div');
        tooltip.className = 'element-tooltip';
        tooltip.innerHTML = `
            <div class="tooltip-content">
                <strong>Atomic Number: ${atomicNumber}</strong><br>
                <small>Click for details</small>
            </div>
        `;
        
        tooltip.style.position = 'fixed';
        tooltip.style.top = `${rect.bottom + 5}px`;
        tooltip.style.left = `${rect.left + (rect.width / 2)}px`;
        tooltip.style.transform = 'translateX(-50%)';
        tooltip.style.backgroundColor = 'rgba(0, 0, 0, 0.8)';
        tooltip.style.color = 'white';
        tooltip.style.padding = '8px 12px';
        tooltip.style.borderRadius = '6px';
        tooltip.style.fontSize = '0.8rem';
        tooltip.style.zIndex = '1000';
        tooltip.style.pointerEvents = 'none';
        
        document.body.appendChild(tooltip);
        this.currentTooltip = tooltip;
    }
    
    hideElementTooltip() {
        if (this.currentTooltip) {
            this.currentTooltip.remove();
            this.currentTooltip = null;
        }
    }
    
    initializeExampleButtons() {
        const exampleButtons = document.querySelectorAll('.example-btn');
        
        exampleButtons.forEach(button => {
            button.addEventListener('click', (event) => {
                const searchTerm = button.dataset.search;
                if (this.searchInput) {
                    this.searchInput.value = searchTerm;
                }
                window.location.href = `/search?q=${encodeURIComponent(searchTerm)}`;
            });
        });
    }
    
    initializeSmoothScrolling() {
        const scrollLinks = document.querySelectorAll('a[href^="#"]');
        
        scrollLinks.forEach(link => {
            link.addEventListener('click', (event) => {
                event.preventDefault();
                const targetId = link.getAttribute('href').substring(1);
                const targetElement = document.getElementById(targetId);
                
                if (targetElement) {
                    targetElement.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            });
        });
    }
    
    initializeSearchForm() {
        const searchForms = document.querySelectorAll('form[action*="search"]');
        
        searchForms.forEach(form => {
            form.addEventListener('submit', (event) => {
                const input = form.querySelector('input[name="q"]');
                if (input && !input.value.trim()) {
                    event.preventDefault();
                    input.focus();
                    this.showMessage('Please enter a search term', 'warning');
                }
            });
        });
    }
    
    initializeTooltips() {
        // Initialize Bootstrap tooltips if available
        if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
            const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
            tooltipTriggerList.map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
        }
    }
    
    initializeAnimations() {
        // Intersection Observer for scroll animations
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('fade-in');
                }
            });
        }, observerOptions);
        
        // Observe elements that should animate on scroll
        const animatedElements = document.querySelectorAll('.card, .feature-card');
        animatedElements.forEach(el => observer.observe(el));
    }
    
    showMessage(message, type = 'info') {
        // Create and show a toast message
        const toast = document.createElement('div');
        toast.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        toast.style.top = '20px';
        toast.style.right = '20px';
        toast.style.zIndex = '9999';
        toast.style.minWidth = '300px';
        
        toast.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(toast);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (toast.parentNode) {
                toast.remove();
            }
        }, 5000);
    }
    
    // Utility methods
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
    
    throttle(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }
}

// Global utility functions
window.scrollToPeriodicTable = function() {
    const element = document.getElementById('periodic-table-section');
    if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
    }
};

window.scrollToFormula = function() {
    const element = document.getElementById('formula-finder-section');
    if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
    }
};

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.chemVista = new ChemVista();
    
    // Add loading states to forms
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', () => {
            const submitButton = form.querySelector('button[type="submit"]');
            if (submitButton) {
                submitButton.disabled = true;
                const originalHTML = submitButton.innerHTML;
                submitButton.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Searching...';
                
                // Re-enable after 10 seconds as fallback
                setTimeout(() => {
                    submitButton.disabled = false;
                    submitButton.innerHTML = originalHTML;
                }, 10000);
            }
        });
    });
    
    // Add click effects to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        if (card.querySelector('a')) {
            card.style.cursor = 'pointer';
            card.addEventListener('click', (event) => {
                if (event.target.tagName !== 'A' && event.target.tagName !== 'BUTTON') {
                    const link = card.querySelector('a');
                    if (link) {
                        link.click();
                    }
                }
            });
        }
    });
    
    // Handle element clicks
    document.querySelectorAll('.element').forEach(element => {
        element.addEventListener('click', function() {
            const atomicNumber = this.dataset.element;
            if (atomicNumber) {
                window.location.href = `/element/${atomicNumber}`;
            }
        });
    });
});

// Handle page visibility changes
document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
        // Page is hidden, pause any ongoing operations
        if (window.chemVista) {
            window.chemVista.hideSuggestions();
        }
    }
});

// Handle window resize
window.addEventListener('resize', window.chemVista?.throttle(() => {
    // Adjust layout if needed
    if (window.chemVista) {
        window.chemVista.hideSuggestions();
    }
}, 250));

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ChemVista;
}
