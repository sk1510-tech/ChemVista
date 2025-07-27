// ChemVista Enhanced JavaScript - Complete Functionality

document.addEventListener('DOMContentLoaded', function() {
    console.log('ChemVista Enhanced - Loading...');
    
    // Initialize the application
    initializeApp();
    initializePeriodicTable();
    initializeSearch();
    initializeModal();
    initializeTooltips();
    
    console.log('ChemVista Enhanced - Loaded successfully!');
});

// Main app initialization
function initializeApp() {
    // Add smooth scrolling to all anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add loading animations
    addLoadingAnimations();
    
    // Initialize theme system
    initializeTheme();
}

// Enhanced Periodic Table Functionality
function initializePeriodicTable() {
    const periodicTable = document.getElementById('periodic-table');
    if (!periodicTable) return;

    // Create complete periodic table if it doesn't exist
    if (periodicTable.children.length === 0) {
        createPeriodicTable();
    }

    // Add click handlers to all elements
    document.querySelectorAll('.element').forEach(element => {
        element.addEventListener('click', function() {
            const atomicNumber = this.dataset.atomicNumber;
            const elementData = this.dataset;
            showElementModal(elementData);
        });

        // Add hover effects
        element.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.05) rotateY(5deg)';
            this.style.zIndex = '10';
            showElementTooltip(this);
        });

        element.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1) rotateY(0deg)';
            this.style.zIndex = '1';
            hideElementTooltip();
        });
    });

    // Add keyboard navigation
    addKeyboardNavigation();
}

// Create complete periodic table dynamically
function createPeriodicTable() {
    const tableContainer = document.getElementById('periodic-table');
    if (!tableContainer) return;

    // Get elements data from the page
    const elementsData = window.elementsData || [];
    
    if (elementsData.length === 0) {
        console.warn('No elements data found');
        return;
    }

    // Clear existing content
    tableContainer.innerHTML = '';

    // Create main periodic table grid
    const mainTable = document.createElement('div');
    mainTable.className = 'periodic-grid';
    
    // Create 18x7 grid for main table
    for (let period = 1; period <= 7; period++) {
        for (let group = 1; group <= 18; group++) {
            const element = elementsData.find(el => el.period === period && el.group === group);
            
            if (element) {
                const elementDiv = createElementDiv(element);
                elementDiv.style.gridRow = period;
                elementDiv.style.gridColumn = group;
                mainTable.appendChild(elementDiv);
            } else if (period === 6 && group === 3) {
                // Lanthanides placeholder
                const placeholder = createPlaceholder('La-Lu*', 57, 71);
                placeholder.style.gridRow = period;
                placeholder.style.gridColumn = group;
                mainTable.appendChild(placeholder);
            } else if (period === 7 && group === 3) {
                // Actinides placeholder
                const placeholder = createPlaceholder('Ac-Lr**', 89, 103);
                placeholder.style.gridRow = period;
                placeholder.style.gridColumn = group;
                mainTable.appendChild(placeholder);
            }
        }
    }

    tableContainer.appendChild(mainTable);

    // Create lanthanides and actinides sections
    createLanthanidesActinides(tableContainer, elementsData);
}

// Create individual element div
function createElementDiv(element) {
    const div = document.createElement('div');
    div.className = `element ${element.category} clickable`;
    div.dataset.atomicNumber = element.atomic_number;
    div.dataset.symbol = element.symbol;
    div.dataset.name = element.name;
    div.dataset.category = element.category;
    div.dataset.atomicMass = element.atomic_mass;
    div.dataset.description = element.description || '';
    
    div.innerHTML = `
        <div class="atomic-number">${element.atomic_number}</div>
        <div class="symbol">${element.symbol}</div>
        <div class="name">${element.name}</div>
        <div class="atomic-mass">${element.atomic_mass}</div>
    `;
    
    return div;
}

// Create placeholder for lanthanides/actinides
function createPlaceholder(text, startNum, endNum) {
    const div = document.createElement('div');
    div.className = 'element placeholder';
    div.innerHTML = `
        <div class="symbol">${text}</div>
        <div class="range">${startNum}-${endNum}</div>
    `;
    return div;
}

// Create lanthanides and actinides sections
function createLanthanidesActinides(container, elementsData) {
    // Lanthanides (57-71)
    const lanthanidesContainer = document.createElement('div');
    lanthanidesContainer.className = 'lanthanides-actinides';
    lanthanidesContainer.innerHTML = '<h4>* Lanthanides</h4>';
    
    const lanthanidesGrid = document.createElement('div');
    lanthanidesGrid.className = 'lanthanides-grid';
    
    for (let atomicNum = 57; atomicNum <= 71; atomicNum++) {
        const element = elementsData.find(el => el.atomic_number === atomicNum);
        if (element) {
            lanthanidesGrid.appendChild(createElementDiv(element));
        }
    }
    
    lanthanidesContainer.appendChild(lanthanidesGrid);
    container.appendChild(lanthanidesContainer);

    // Actinides (89-103)
    const actinidesContainer = document.createElement('div');
    actinidesContainer.className = 'lanthanides-actinides';
    actinidesContainer.innerHTML = '<h4>** Actinides</h4>';
    
    const actinidesGrid = document.createElement('div');
    actinidesGrid.className = 'actinides-grid';
    
    for (let atomicNum = 89; atomicNum <= 103; atomicNum++) {
        const element = elementsData.find(el => el.atomic_number === atomicNum);
        if (element) {
            actinidesGrid.appendChild(createElementDiv(element));
        }
    }
    
    actinidesContainer.appendChild(actinidesGrid);
    container.appendChild(actinidesContainer);
}

// Enhanced Search Functionality
function initializeSearch() {
    const searchInput = document.getElementById('search-input');
    const searchResults = document.getElementById('search-results');
    const searchBtn = document.getElementById('search-btn');
    
    if (!searchInput) return;

    let searchTimeout;

    // Real-time search with debouncing
    searchInput.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        const query = this.value.trim();
        
        if (query.length >= 2) {
            searchTimeout = setTimeout(() => {
                performSearch(query);
            }, 300);
        } else {
            clearSearchResults();
        }
    });

    // Search button click
    if (searchBtn) {
        searchBtn.addEventListener('click', function() {
            const query = searchInput.value.trim();
            if (query) {
                performSearch(query);
            }
        });
    }

    // Enter key search
    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            const query = this.value.trim();
            if (query) {
                performSearch(query);
            }
        }
    });
}

// Perform search operation
async function performSearch(query) {
    try {
        showLoading('search-results');
        
        const response = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
        const results = await response.json();
        
        displaySearchResults(results, query);
    } catch (error) {
        console.error('Search error:', error);
        showError('search-results', 'Search failed. Please try again.');
    }
}

// Display search results
function displaySearchResults(results, query) {
    const container = document.getElementById('search-results');
    if (!container) return;

    container.innerHTML = '';

    if (results.length === 0) {
        container.innerHTML = `
            <div class="no-results">
                <i class="fas fa-search"></i>
                <p>No compounds found for "${query}"</p>
            </div>
        `;
        return;
    }

    const resultsTitle = document.createElement('h4');
    resultsTitle.textContent = `Found ${results.length} compound(s) for "${query}":`;
    container.appendChild(resultsTitle);

    const resultsList = document.createElement('div');
    resultsList.className = 'results-list';

    results.forEach(compound => {
        const resultItem = document.createElement('div');
        resultItem.className = 'result-item';
        resultItem.innerHTML = `
            <div class="compound-formula">${compound.formula}</div>
            <div class="compound-name">${compound.name}</div>
        `;
        
        resultItem.addEventListener('click', () => {
            showCompoundModal(compound);
        });
        
        resultsList.appendChild(resultItem);
    });

    container.appendChild(resultsList);
}

// Clear search results
function clearSearchResults() {
    const container = document.getElementById('search-results');
    if (container) {
        container.innerHTML = '';
    }
}

// Modal functionality
function initializeModal() {
    // Element modal
    const elementModal = document.getElementById('element-modal');
    if (elementModal) {
        elementModal.addEventListener('click', function(e) {
            if (e.target === this) {
                hideElementModal();
            }
        });
    }

    // Compound modal
    const compoundModal = document.getElementById('compound-modal');
    if (compoundModal) {
        compoundModal.addEventListener('click', function(e) {
            if (e.target === this) {
                hideCompoundModal();
            }
        });
    }

    // Close buttons
    document.querySelectorAll('.modal-close').forEach(button => {
        button.addEventListener('click', function() {
            hideElementModal();
            hideCompoundModal();
        });
    });

    // Escape key to close modals
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            hideElementModal();
            hideCompoundModal();
        }
    });
}

// Show element modal
function showElementModal(elementData) {
    const modal = document.getElementById('element-modal');
    const modalContent = document.getElementById('element-modal-content');
    
    if (!modal || !modalContent) {
        // Create modal if it doesn't exist
        createElementModal(elementData);
        return;
    }

    modalContent.innerHTML = `
        <div class="modal-header">
            <h2>${elementData.name} (${elementData.symbol})</h2>
            <button class="modal-close">&times;</button>
        </div>
        <div class="modal-body">
            <div class="element-preview ${elementData.category}">
                <div class="atomic-number">${elementData.atomicNumber}</div>
                <div class="symbol">${elementData.symbol}</div>
                <div class="name">${elementData.name}</div>
            </div>
            <div class="element-properties">
                <p><strong>Atomic Number:</strong> ${elementData.atomicNumber}</p>
                <p><strong>Atomic Mass:</strong> ${elementData.atomicMass}</p>
                <p><strong>Category:</strong> ${formatCategory(elementData.category)}</p>
                <p><strong>Description:</strong> ${elementData.description || 'No description available.'}</p>
            </div>
        </div>
    `;

    modal.style.display = 'flex';
    setTimeout(() => modal.classList.add('show'), 10);
}

// Hide element modal
function hideElementModal() {
    const modal = document.getElementById('element-modal');
    if (modal) {
        modal.classList.remove('show');
        setTimeout(() => modal.style.display = 'none', 300);
    }
}

// Show compound modal
function showCompoundModal(compound) {
    const modal = document.getElementById('compound-modal');
    if (!modal) {
        createCompoundModal(compound);
        return;
    }

    const modalContent = modal.querySelector('.modal-content');
    modalContent.innerHTML = `
        <div class="modal-header">
            <h2>${compound.name}</h2>
            <button class="modal-close">&times;</button>
        </div>
        <div class="modal-body">
            <div class="compound-formula-large">${compound.formula}</div>
            <div class="compound-details">
                <p><strong>Molecular Formula:</strong> ${compound.formula}</p>
                <p><strong>Common Name:</strong> ${compound.name}</p>
                <p><strong>Type:</strong> ${compound.type || 'Chemical Compound'}</p>
                <p><strong>Uses:</strong> ${compound.uses || 'Various industrial and research applications'}</p>
            </div>
        </div>
    `;

    modal.style.display = 'flex';
    setTimeout(() => modal.classList.add('show'), 10);
}

// Hide compound modal
function hideCompoundModal() {
    const modal = document.getElementById('compound-modal');
    if (modal) {
        modal.classList.remove('show');
        setTimeout(() => modal.style.display = 'none', 300);
    }
}

// Create element modal dynamically
function createElementModal(elementData) {
    const modal = document.createElement('div');
    modal.id = 'element-modal';
    modal.className = 'modal';
    modal.innerHTML = `
        <div class="modal-content" id="element-modal-content">
            <!-- Content will be populated by showElementModal -->
        </div>
    `;
    document.body.appendChild(modal);
    
    initializeModal();
    showElementModal(elementData);
}

// Create compound modal dynamically
function createCompoundModal(compound) {
    const modal = document.createElement('div');
    modal.id = 'compound-modal';
    modal.className = 'modal';
    modal.innerHTML = `
        <div class="modal-content">
            <!-- Content will be populated by showCompoundModal -->
        </div>
    `;
    document.body.appendChild(modal);
    
    initializeModal();
    showCompoundModal(compound);
}

// Tooltip functionality
function initializeTooltips() {
    let tooltipElement = null;

    window.showElementTooltip = function(element) {
        hideElementTooltip();
        
        tooltipElement = document.createElement('div');
        tooltipElement.className = 'element-tooltip';
        tooltipElement.innerHTML = `
            <strong>${element.dataset.name}</strong><br>
            Symbol: ${element.dataset.symbol}<br>
            Atomic #: ${element.dataset.atomicNumber}<br>
            Mass: ${element.dataset.atomicMass}
        `;
        
        document.body.appendChild(tooltipElement);
        
        const rect = element.getBoundingClientRect();
        tooltipElement.style.left = rect.left + rect.width / 2 - tooltipElement.offsetWidth / 2 + 'px';
        tooltipElement.style.top = rect.top - tooltipElement.offsetHeight - 10 + 'px';
        
        setTimeout(() => tooltipElement.classList.add('show'), 10);
    };

    window.hideElementTooltip = function() {
        if (tooltipElement) {
            tooltipElement.remove();
            tooltipElement = null;
        }
    };
}

// Add loading animations
function addLoadingAnimations() {
    // Animate elements on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
            }
        });
    }, observerOptions);

    // Observe all animatable elements
    document.querySelectorAll('.card, .element, .feature-card').forEach(el => {
        observer.observe(el);
    });
}

// Theme system
function initializeTheme() {
    const themeToggle = document.getElementById('theme-toggle');
    if (!themeToggle) return;

    // Check for saved theme
    const savedTheme = localStorage.getItem('chemvista-theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);

    themeToggle.addEventListener('click', function() {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('chemvista-theme', newTheme);
    });
}

// Keyboard navigation
function addKeyboardNavigation() {
    let currentElement = null;
    const elements = document.querySelectorAll('.element:not(.placeholder)');
    
    document.addEventListener('keydown', function(e) {
        if (!elements.length) return;
        
        if (!currentElement) {
            currentElement = elements[0];
            currentElement.focus();
            return;
        }
        
        const currentIndex = Array.from(elements).indexOf(currentElement);
        let newIndex = currentIndex;
        
        switch(e.key) {
            case 'ArrowLeft':
                newIndex = Math.max(0, currentIndex - 1);
                break;
            case 'ArrowRight':
                newIndex = Math.min(elements.length - 1, currentIndex + 1);
                break;
            case 'ArrowUp':
                newIndex = Math.max(0, currentIndex - 18);
                break;
            case 'ArrowDown':
                newIndex = Math.min(elements.length - 1, currentIndex + 18);
                break;
            case 'Enter':
            case ' ':
                e.preventDefault();
                currentElement.click();
                return;
            default:
                return;
        }
        
        e.preventDefault();
        currentElement = elements[newIndex];
        currentElement.focus();
        currentElement.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    });
}

// Utility functions
function formatCategory(category) {
    return category.replace(/-/g, ' ')
                  .replace(/\b\w/g, l => l.toUpperCase());
}

function showLoading(containerId) {
    const container = document.getElementById(containerId);
    if (container) {
        container.innerHTML = `
            <div class="loading">
                <div class="spinner"></div>
                <p>Searching...</p>
            </div>
        `;
    }
}

function showError(containerId, message) {
    const container = document.getElementById(containerId);
    if (container) {
        container.innerHTML = `
            <div class="error">
                <i class="fas fa-exclamation-triangle"></i>
                <p>${message}</p>
            </div>
        `;
    }
}

// Export functions for global access
window.ChemVista = {
    showElementModal,
    hideElementModal,
    showCompoundModal,
    hideCompoundModal,
    showElementTooltip,
    hideElementTooltip,
    performSearch
};
