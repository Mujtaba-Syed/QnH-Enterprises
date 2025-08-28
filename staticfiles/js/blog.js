document.addEventListener('DOMContentLoaded', function() {
    const keywordContainers = document.querySelectorAll('.post-seo-keywords');
    
    keywordContainers.forEach(function(container) {
        const keywords = container.getAttribute('data-keywords');
        if (keywords) {
            // Split keywords by comma and trim whitespace
            const keywordList = keywords.split(',').map(keyword => keyword.trim());
            
            // Create individual badges for each keyword
            keywordList.forEach(function(keyword) {
                if (keyword) {
                    const badge = document.createElement('span');
                    badge.className = 'badge me-1 mb-1';
                    badge.style.backgroundColor = '#198754';
                    badge.textContent = keyword;
                    container.appendChild(badge);
                }
            });
        }
    });
});